from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button

from recovery.screens.reinstall import ReinstallScreen
from recovery.screens.network import NetworkScreen


class WelcomeWidget(Container):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "open_console":
                exit(0)
            case "open_disk_util":
                pass
            case "reinstall_sbos":
                self.app.push_screen(ReinstallScreen())
            case "configure_network":
                self.app.push_screen(NetworkScreen())
            case "restore_base_from_disk":
                pass

    def compose(self) -> ComposeResult:
        yield Button(label="Open a console", id="open_console")
        yield Button(label="Open disk utility", id="open_disk_util")
        yield Button(label="Configure network", id="configure_network")
        yield Button(label="Reinstall StrawberryOS", id="reinstall_sbos")
        yield Button(label="Restore base system from another disk", id="restore_base_from_disk")
