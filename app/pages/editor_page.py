import reflex as rx
from reflex_monaco import monaco
from app.components.layout import main_layout
from app.states.editor_state import EditorState
from app.states.theme_state import ThemeState


def editor_page() -> rx.Component:
    """
    The page for creating and editing blog posts.
    """
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Post Title",
                    on_change=EditorState.set_title,
                    class_name="text-2xl font-bold w-full p-2 border-b-2 border-gray-200 dark:border-gray-700 focus:outline-none focus:border-emerald-500 bg-transparent",
                    default_value=EditorState.title,
                ),
                rx.el.input(
                    placeholder="Tags, comma-separated",
                    on_change=EditorState.set_tags_str,
                    class_name="w-full p-2 mt-2 border-b border-gray-200 dark:border-gray-700 focus:outline-none focus:border-emerald-500 bg-transparent",
                    default_value=EditorState.tags_str,
                ),
                rx.el.button(
                    rx.icon(tag="save", class_name="mr-2 h-4 w-4"),
                    "Save Post",
                    on_click=EditorState.save_post,
                    class_name="mt-4 flex items-center bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700 transition-colors",
                ),
                class_name="p-4 border-b border-gray-200 dark:border-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    monaco(
                        default_value=EditorState.content,
                        language="markdown",
                        theme=rx.cond(
                            ThemeState.theme == "light", "vs-light", "vs-dark"
                        ),
                        on_change=EditorState.on_editor_change.debounce(300),
                        height="calc(100vh - 250px)",
                    ),
                    class_name="w-1/2 h-full border-r border-gray-200 dark:border-gray-800",
                ),
                rx.el.div(
                    rx.markdown(
                        EditorState.content,
                        class_name="prose dark:prose-invert max-w-none p-8",
                    ),
                    class_name="w-1/2 h-full overflow-y-auto bg-gray-50 dark:bg-gray-900",
                ),
                class_name="flex flex-grow",
            ),
            class_name="flex flex-col h-full bg-white dark:bg-gray-950 rounded-lg shadow-md overflow-hidden",
            on_mount=EditorState.on_load,
        )
    )