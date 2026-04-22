import json
import os
from datetime import datetime
from pathlib import Path

from reqprompt.constants import DATA_DIR, VALID_CATS, VALID_TYPES
from reqprompt.db import get_conn, init_db
from reqprompt.prompt_builder import build_prompt


class API:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.window = None
        init_db()

    def _row(self, row):
        return dict(row) if row else None

    def _rows(self, rows):
        return [dict(r) for r in rows]

    # ── projects ──────────────────────────────────────────────────────────────────
    def get_projects(self):
        with get_conn() as conn:
            projects = self._rows(conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall())
            for p in projects:
                p["extraQids"] = [
                    r["question_id"]
                    for r in conn.execute(
                        "SELECT question_id FROM project_extra_questions WHERE project_id=?", (p["id"],)
                    ).fetchall()
                ]
                p["answers"] = {
                    str(r["question_id"]): r["value"]
                    for r in conn.execute(
                        "SELECT question_id, value FROM answers WHERE project_id=?", (p["id"],)
                    ).fetchall()
                }
        return json.dumps(projects)

    def create_project(self, name: str, client: str, proj_type: str, notes: str):
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO projects (name, client, type, notes, created_at) VALUES (?,?,?,?,?)",
                (name.strip(), client.strip(), proj_type, notes.strip(), datetime.now().strftime("%d/%m/%Y")),
            )
            pid = cur.lastrowid
        return json.dumps({"id": pid, "name": name, "client": client, "type": proj_type,
                           "notes": notes, "generated_doc": "", "doc_date": "",
                           "created_at": datetime.now().strftime("%d/%m/%Y"),
                           "extraQids": [], "answers": {}})

    def delete_project(self, project_id: int):
        with get_conn() as conn:
            conn.execute("DELETE FROM projects WHERE id=?", (project_id,))
        return True

    def set_extra_questions(self, project_id: int, question_ids_json: str):
        qids = json.loads(question_ids_json)
        with get_conn() as conn:
            if not conn.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone():
                return json.dumps({"error": "Proyecto no encontrado."})

            if qids:
                placeholders = ",".join("?" * len(qids))
                valid_qids = [
                    q[0]
                    for q in conn.execute(
                        f"SELECT id FROM questions WHERE id IN ({placeholders})",
                        qids,
                    ).fetchall()
                ]
            else:
                valid_qids = []

            conn.execute("DELETE FROM project_extra_questions WHERE project_id=?", (project_id,))
            if valid_qids:
                conn.executemany(
                    "INSERT INTO project_extra_questions (project_id, question_id) VALUES (?,?)",
                    [(project_id, qid) for qid in valid_qids],
                )
        return True

    # ── questions ─────────────────────────────────────────────────────────────────
    def get_questions(self):
        with get_conn() as conn:
            rows = self._rows(conn.execute("SELECT * FROM questions ORDER BY is_base DESC, id ASC").fetchall())
        for r in rows:
            r["cat"] = r.pop("category")
            r["type"] = r.pop("q_type")
            r["base"] = bool(r.pop("is_base"))
        return json.dumps(rows)

    def create_question(self, category: str, text: str, q_type: str):
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO questions (category, text, q_type, is_base) VALUES (?,?,?,0)",
                (category, text.strip(), q_type),
            )
            qid = cur.lastrowid
        return json.dumps({"id": qid, "cat": category, "text": text, "type": q_type, "base": False})

    def delete_question(self, question_id: int):
        with get_conn() as conn:
            conn.execute("DELETE FROM questions WHERE id=? AND is_base=0", (question_id,))
        return True

    def import_questions(self, questions_json: str):
        """Importa preguntas variables desde un array JSON."""
        try:
            qs = json.loads(questions_json)
            if not isinstance(qs, list):
                return json.dumps({"error": "El archivo debe contener un array JSON de preguntas."})
            inserted = []

            with get_conn() as conn:
                for q in qs:
                    cat = (q.get("category") or q.get("cat", "")).strip()
                    text = q.get("text", "").strip()
                    q_type = (q.get("type") or q.get("q_type", "Abierta")).strip()
                    if cat not in VALID_CATS or not text:
                        continue
                    if q_type not in VALID_TYPES:
                        q_type = "Abierta"
                    cur = conn.execute(
                        "INSERT INTO questions (category, text, q_type, is_base) VALUES (?,?,?,0)",
                        (cat, text, q_type),
                    )
                    inserted.append({"id": cur.lastrowid, "cat": cat, "text": text, "type": q_type, "base": False})

            return json.dumps({"count": len(inserted), "questions": inserted})
        except Exception as e:
            return json.dumps({"error": str(e)})

    # ── answers ───────────────────────────────────────────────────────────────────
    def save_answer(self, project_id: int, question_id: int, value: str):
        with get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO answers (project_id, question_id, value) VALUES (?,?,?)",
                (project_id, question_id, value),
            )
        return True

    # ── prompt ────────────────────────────────────────────────────────────────────
    def generate_prompt(self, project_id: int):
        try:
            with get_conn() as conn:
                p = self._row(conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone())
                if not p:
                    return json.dumps({"error": "Proyecto no encontrado."})
                rows = conn.execute("""
                    SELECT q.category, q.text, q.q_type, COALESCE(a.value,'') AS value
                    FROM questions q
                    LEFT JOIN answers a ON a.question_id = q.id AND a.project_id = ?
                    WHERE q.is_base = 1 OR q.id IN (
                        SELECT question_id FROM project_extra_questions WHERE project_id = ?
                    )
                    ORDER BY q.is_base DESC, q.id ASC
                """, (project_id, project_id)).fetchall()

            prompt = build_prompt(p, rows)

            doc_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            with get_conn() as conn:
                conn.execute(
                    "UPDATE projects SET generated_doc=?, doc_date=? WHERE id=?",
                    (prompt, doc_date, project_id),
                )

            return json.dumps({"prompt": prompt, "date": doc_date})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_generated_doc(self, project_id: int):
        with get_conn() as conn:
            row = conn.execute("SELECT generated_doc, doc_date FROM projects WHERE id=?", (project_id,)).fetchone()
        if row:
            return json.dumps({"doc": row["generated_doc"], "date": row["doc_date"]})
        return json.dumps({"doc": "", "date": ""})

    def export_file(self, project_id: int, content: str, ext: str):
        try:
            with get_conn() as conn:
                p = self._row(conn.execute("SELECT name FROM projects WHERE id=?", (project_id,)).fetchone())
            name = (p["name"] if p else "requerimientos").replace(" ", "_")
            path = self.data_dir / f"{name}_prompt.{ext}"
            path.write_text(content, encoding="utf-8")
            return str(path)
        except Exception as e:
            return f"ERROR: {e}"

    def open_data_folder(self):
        import subprocess
        import sys

        try:
            if sys.platform == "win32":
                os.startfile(str(self.data_dir))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(self.data_dir)])
            else:
                subprocess.Popen(["xdg-open", str(self.data_dir)])
            return True
        except Exception as e:
            return str(e)
