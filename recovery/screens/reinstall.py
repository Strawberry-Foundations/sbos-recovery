from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Header, Footer, Button


class ReinstallScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Go back")]
    TITLE = "Reinstall StrawberryOS"

    class ReinstallScreenContainer(Container):
        def compose(self) -> ComposeResult:
            yield Button(label="Reinstall base system (Keep data)", id="reinstall_sbos")
            yield Button(label="Wipe disk and reinstall StrawberryOS", id="restore_base_from_disk")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield ReinstallScreen.ReinstallScreenContainer()
