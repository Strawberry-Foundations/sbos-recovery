from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Button, Label

from recovery.utils.colors import *

import subprocess
import os
import socket


def get_network_interfaces():
    """Get a list of all network interfaces, excluding virtual interfaces."""
    virtual_interfaces_prefixes = ('docker', 'veth', 'br-', 'lo', 'virbr', 'vmnet', 'vboxnet')
    interfaces = []
    for interface in os.listdir('/sys/class/net/'):
        if not interface.startswith(virtual_interfaces_prefixes):  # Exclude virtual interfaces
            interfaces.append(interface)
    return interfaces


def get_connected_interface():
    result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "default" in line:
            return line.split()[4]
    return None


def check_internet_connection():
    """Check if the machine is connected to the internet."""
    try:
        socket.create_connection(("strawberryfoundations.xyz", 80), timeout=5)
        return True
    except OSError:
        return False


def scan_wifi_networks():
    """List available Wi-Fi networks."""
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID,FREQ', 'dev', 'wifi'], capture_output=True, text=True)
    networks = result.stdout.splitlines()
    ssids = []
    freqs = []
    for network in networks:
        ssid, freq = network.split(':')
        ssids.append(ssid)
        freq = int(str(freq).replace(" MHz", "").strip())
        if freq < 3000:
            freqs.append(f"[2.4 GHz]")
        else:
            freqs.append(f"[5 GHz]")

    ssids.extend(["+ Add Wi-Fi"])
    return ssids, freqs

def connect_to_wifi(ssid, password):
    try:
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)

        print(f"Successfully {GREEN}connected{CRESET} with {CYAN}{ssid}{CRESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}{BOLD}Error connecting to {ssid}: {e}{CRESET}")

def establish_wifi():
    print(f"Connected via {CYAN}Wi-Fi{CRESET}. Search for available Wi-Fi networks ...")
    wifi_networks, wifi_freqs = scan_wifi_networks()

    if wifi_networks:
        ssid = ""
        if ssid == "+ Add Wi-Fi":
            _input = True
            while _input:
                ssid = input("\nSSID: ")
                if ssid.strip() == "":
                    print(f"{YELLOW}{BOLD}SSID cannot be empty{CRESET}")
                else:
                    _input = False
        if show_password:
            password = input(f"\nPassword for {ssid}: ")
        else:
            password = input(f"\nPassword for {ssid}: ")

        print(f"Connection to {CYAN}{ssid}{CRESET} is being established ...")
        connect_to_wifi(ssid, password)

    else:
        print("No Wi-Fi networks found.")


class NetworkScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Go back")]
    TITLE = "Configure network"

    class NetworkScreenContainer(Container):
        def __init__(self):
            super().__init__()
            self.app.force_wifi_connect = False

        class ConfirmScreen(Screen):
            def compose(self) -> ComposeResult:
                yield Grid(
                    Label("Your Wi-Fi connection already seems to be working. Would you still like to set up a connection?", id="confirmscreen"),
                    Button("Yes", variant="primary", id="confirm"),
                    Button("No", variant="error", id="cancel"),
                    id="dialog",
                )

            def on_button_pressed(self, event: Button.Pressed):
                if event.button.id == "confirm":
                    self.app.pop_screen()
                    self.app.force_wifi_connect = True
                else:
                    self.app.pop_screen()
                    self.app.force_wifi_connect = False

        def compose(self) -> ComposeResult:
            interfaces = get_network_interfaces()
            connected_interface = get_connected_interface()

            if len(interfaces) > 1:
                self.app.pop_screen()
            else:
                if not connected_interface:
                    connected_interface = interfaces[0]

            if connected_interface:
                yield Label(f"You are connected to {CYAN}{connected_interface}{CRESET}")

                connection_available = check_internet_connection()

                if connection_available:
                    yield Label(f"Internet connection is {GREEN}{BOLD}available{CRESET}")
                else:
                    yield Label(f"{YELLOW}{BOLD}Internet connection is {RED}not {YELLOW}available{CRESET}")
                    if "en" in connected_interface:
                        yield Label(f"{YELLOW}{BOLD}No active internet connection is available. Please check your connection.{CRESET}")

                if "wl" in connected_interface:
                    if connection_available:
                        self.app.push_screen(NetworkScreen.NetworkScreenContainer.ConfirmScreen())

                        yield Label(f"Connected via {CYAN}LAN{CRESET}")

                        if self.app.force_wifi_connect:
                            print("")
                            establish_wifi()
                    else:
                        establish_wifi()

                elif "en" in connected_interface:
                    yield Label(f"Connected via {CYAN}LAN{CRESET}")
                else:
                    yield Label("Unknown network interface.")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield NetworkScreen.NetworkScreenContainer()
