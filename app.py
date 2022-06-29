from kanban_solo import create_app
import config
import webview

app = create_app(config)

if __name__ == "__main__":
    webview.create_window(
        "Kanban Solo",
        app,
        frameless=True,
        fullscreen=True,
        easy_drag=False,
        text_select=True,
    )
    webview.start(debug=True)
