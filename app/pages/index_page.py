import reflex as rx
from app.states.blog_state import BlogState, Post
from app.components.layout import main_layout


def post_card(post: Post) -> rx.Component:
    """
    A card component to display a blog post preview.
    """
    return rx.el.div(
        rx.el.a(
            rx.el.div(
                rx.el.div(
                    rx.icon("book-text", class_name="w-12 h-12 text-emerald-200"),
                    class_name="""
                    w-full h-48
                    flex items-center justify-center
                    bg-gradient-to-br from-emerald-400 to-green-600
                    rounded-t-lg
                    """,
                ),
                rx.el.div(
                    rx.el.h2(
                        post["title"],
                        class_name="text-xl font-bold text-gray-900 dark:text-white mb-2",
                    ),
                    rx.el.p(
                        f"By {post['author']} on {post['date']}",
                        class_name="text-sm text-gray-500 dark:text-gray-400 mb-4",
                    ),
                    rx.el.p(
                        post["excerpt"],
                        class_name="text-base font-medium text-gray-700 dark:text-gray-300 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            post["tags"],
                            lambda tag: rx.el.span(
                                tag,
                                class_name="""
                                inline-block bg-emerald-100 text-emerald-800
                                dark:bg-emerald-900 dark:text-emerald-200
                                text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full
                                """,
                            ),
                        ),
                        class_name="flex flex-wrap",
                    ),
                    class_name="p-6",
                ),
                class_name="""
                h-full flex flex-col
                """,
            ),
            href=f"/editor/{post['id']}",
        ),
        class_name="""
        bg-white dark:bg-gray-800
        rounded-lg border border-gray-200 dark:border-gray-700
        shadow-sm hover:shadow-lg
        transition-shadow duration-300
        overflow-hidden
        """,
    )


def index() -> rx.Component:
    """
    The main index page, listing all blog posts.
    """
    return main_layout(
        rx.el.div(
            rx.el.h1(
                "From the Blog",
                class_name="""
                text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white
                tracking-tight mb-8
                """,
            ),
            rx.el.div(
                rx.foreach(BlogState.posts, post_card),
                class_name="""
                grid gap-8
                md:grid-cols-2 lg:grid-cols-3
                """,
            ),
            on_mount=BlogState.load_posts,
        )
    )