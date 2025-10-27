import reflex as rx
from app.pages.index_page import index
from app.pages.editor_page import editor_page
from app.states.theme_state import ThemeState

app = rx.App(
    theme=rx.theme(
        appearance="light", accent_color="green", gray_color="gray", radius="medium"
    ),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;700;800&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(src="https://cdn.tailwindcss.com/3.4.1"),
        rx.el.script(
            "tailwind.config = { darkMode: 'class', theme: { extend: { typography: (theme) => ({}) } } }"
        ),
    ],
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/nprogress/0.2.0/nprogress.min.css"
    ],
)
app.add_page(index, route="/")
app.add_page(editor_page, route="/editor")
app.add_page(editor_page, route="/editor/[post_id]")