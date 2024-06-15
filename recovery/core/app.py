from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button

from recovery.widgets.welcome import WelcomeWidget


class Recovery(App):
    BINDINGS = [
        ("q", "quit", "Quit recovery"),
    ]

    CSS_PATH = "app.tcss"

    TITLE = "StrawberryOS Recovery"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        yield Footer()
        yield WelcomeWidget()
