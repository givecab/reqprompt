import webview
from pathlib import Path
from api import API, DATA_DIR
from reqprompt.constants import APP_NAME


def main():
    assets_dir = Path(__file__).parent / "assets"
    api = API(DATA_DIR)
    window = webview.create_window(
        title=APP_NAME,
        url=str(assets_dir / "index.html"),
        js_api=api,
        width=1200,
        height=800,
        min_size=(900, 600),
        resizable=True,
    )
    api.window = window
    webview.start(debug=False, icon=str(assets_dir / "icono.png"))

if __name__ == "__main__":
    main()
