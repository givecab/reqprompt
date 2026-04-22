from pathlib import Path

APP_NAME = "ReqPrompt"
APP_VERSION = "3.0"
BRAND_COLOR = "#204983"

DATA_DIR = Path.home() / ".req_elicit"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "data.db"

CATEGORY_ORDER = ["Negocio", "Funcional", "No funcional", "Restricción", "Interfaz"]
VALID_CATS = {"Funcional", "No funcional", "Negocio", "Restricción", "Interfaz"}
VALID_TYPES = {"Abierta", "Cerrada", "Selección múltiple"}
