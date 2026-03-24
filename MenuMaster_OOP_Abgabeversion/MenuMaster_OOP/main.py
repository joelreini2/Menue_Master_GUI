"""Startpunkt der Browser-App MenuMaster."""

from app.ui.pages import create_app


if __name__ in {"__main__", "__mp_main__"}:
    app = create_app()
    app.run(title="MenuMaster", reload=False)
