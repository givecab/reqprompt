from .constants import CATEGORY_ORDER


def build_prompt(project, rows):
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    for row in rows:
        cat = row["category"]
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(row)

    qa_text = ""
    for cat in CATEGORY_ORDER:
        qs = grouped.get(cat, [])
        if not qs:
            continue
        qa_text += f"\n### {cat.upper()}\n"
        for q in qs:
            ans = (q["value"] or "").strip()
            qa_text += f"P: {q['text']}\nR: {ans if ans else '(Sin respuesta)'}\n\n"

    notes_line = f"NOTAS: {project['notes']}\n" if project["notes"] else ""

    return f"""Sos un ingeniero de requerimientos senior. A partir de las siguientes respuestas de una entrevista de elicitación con el cliente, generá documentación completa y estructurada para que el equipo de desarrollo pueda pasar directamente a los casos de uso.

PROYECTO: {project['name']}
CLIENTE: {project['client']}
TIPO: {project['type']}
{notes_line}
PREGUNTAS Y RESPUESTAS DE LA ENTREVISTA:
{qa_text}
Generá el siguiente documento completo en markdown:

---

# Documentación de Requerimientos — {project['name']}

## 1. Descripción general del sistema
(Párrafo de contexto del problema y la solución propuesta)

## 2. Objetivos del negocio y reglas de negocio
Lista numerada RN-001, RN-002... de reglas y objetivos clave extraídos de las respuestas.

## 3. Stakeholders y usuarios
Tabla con: Rol | Descripción | Nivel de interacción

## 4. Requerimientos funcionales
Lista RF-001, RF-002... Cada uno:
- **ID**: RF-XXX
- **Descripción**: qué debe hacer el sistema
- **Prioridad**: Alta / Media / Baja

## 5. Requerimientos no funcionales
Lista RNF-001, RNF-002... Cada uno:
- **ID**: RNF-XXX
- **Descripción**
- **Categoría**: Rendimiento / Seguridad / Disponibilidad / Usabilidad / etc.

## 6. Restricciones del proyecto
Lista de restricciones técnicas, de tiempo, presupuesto y normativas.

## 7. Interfaces e integraciones
Detalle de sistemas externos, APIs e interfaces de usuario requeridas.

## 8. Glosario de términos del dominio
Tabla: Término | Definición

## 9. Casos de uso sugeridos
Lista CU-001, CU-002... Cada uno:
- **ID**: CU-XXX
- **Nombre**
- **Actores**
- **Descripción breve** (1 línea)
- **Requerimientos relacionados** (RF-XXX)

---

Usá solo la información de las respuestas. Si algo no fue cubierto, indicalo como \"Por definir\"."""
