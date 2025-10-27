import reflex as rx
from typing import Literal

Theme = Literal["light", "dark"]


class ThemeState(rx.State):
    """
    Manages the theme of the application, including light/dark mode.
    """

    theme: Theme = rx.LocalStorage("light", name="theme")

    @rx.event
    def toggle_theme(self):
        """
        Toggles the application theme between light and dark mode.
        """
        self.theme = "dark" if self.theme == "light" else "light"