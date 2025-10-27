import reflex as rx
import datetime
from app.states.theme_state import ThemeState


def nav_link(text: str, href: str) -> rx.Component:
    """
    A navigation link component.
    """
    return rx.el.a(
        text,
        href=href,
        class_name="""
        text-sm font-medium
        text-gray-500 hover:text-gray-900
        dark:text-gray-400 dark:hover:text-white
        transition-colors
        """,
    )


def theme_toggle() -> rx.Component:
    """
    A component to toggle between light and dark themes.
    """
    return rx.el.button(
        rx.icon(
            tag=rx.cond(ThemeState.theme == "light", "moon", "sun"),
            class_name="h-5 w-5 text-gray-500 dark:text-gray-400",
        ),
        on_click=ThemeState.toggle_theme,
        class_name="""
        p-2 rounded-full
        hover:bg-gray-100 dark:hover:bg-gray-800
        transition-colors
        """,
    )


def navbar() -> rx.Component:
    """
    The main navigation bar for the application.
    """
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.icon("book-open-text", class_name="h-6 w-6 text-emerald-600"),
                rx.el.span(
                    "ReflexPress",
                    class_name="ml-2 text-lg font-bold text-gray-900 dark:text-white",
                ),
                href="/",
                class_name="flex items-center",
            ),
            rx.el.nav(
                nav_link("Home", "/"),
                nav_link("Create Post", "/editor"),
                nav_link("Settings", "#"),
                class_name="hidden md:flex items-center gap-6",
            ),
            rx.el.div(theme_toggle(), class_name="flex items-center gap-4"),
            class_name="""
            container mx-auto px-4 md:px-6 h-16
            flex items-center justify-between
            """,
        ),
        class_name="""
        sticky top-0 z-50 w-full
        border-b border-gray-200 dark:border-gray-800
        bg-white/80 dark:bg-gray-950/80
        backdrop-blur-sm
        """,
    )


def main_layout(child: rx.Component) -> rx.Component:
    """
    The main layout wrapping every page.
    """
    return rx.el.div(
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    child, class_name="container mx-auto px-4 md:px-6 py-8 md:py-12"
                )
            ),
            rx.el.footer(
                rx.el.div(
                    rx.el.p(
                        f"© {datetime.date.today().year} ReflexPress. Built with Reflex & Love.",
                        class_name="text-sm text-gray-500 dark:text-gray-400",
                    ),
                    class_name="container mx-auto px-4 md:px-6 py-6 text-center",
                ),
                class_name="border-t border-gray-200 dark:border-gray-800",
            ),
            class_name="font-['Raleway'] min-h-screen flex flex-col bg-white dark:bg-gray-950",
        ),
        class_name=ThemeState.theme,
    )