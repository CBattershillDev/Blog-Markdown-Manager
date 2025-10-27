import reflex as rx
from typing import Optional
from app.states.blog_state import BlogState, Post, POSTS_DIR
import datetime
import re


def title_to_slug(title: str) -> str:
    """Converts a post title to a URL-friendly slug."""
    slug = title.lower().strip()
    slug = re.sub("[\\s-]+", "-", slug)
    slug = re.sub("[^a-z0-9-]", "", slug)
    return slug


class EditorState(rx.State):
    """
    Manages the state for the markdown editor page.
    """

    post: Optional[Post] = None
    content: str = ""
    title: str = ""
    tags_str: str = ""

    @rx.event
    async def on_load(self):
        """
        Handles loading the post data when the editor page is visited.
        """
        post_id = self.router.page.params.get("post_id")
        if not post_id:
            self.title = ""
            self.content = "# Start writing your new blog post here..."
            self.tags_str = ""
            self.post = None
            return
        blog_state = await self.get_state(BlogState)
        if not blog_state.posts:
            yield BlogState.load_posts
        blog_state = await self.get_state(BlogState)
        post_to_edit = next((p for p in blog_state.posts if p["id"] == post_id), None)
        if post_to_edit:
            self.post = post_to_edit
            self.content = self.post["content"]
            self.title = self.post["title"]
            self.tags_str = ", ".join(self.post["tags"])
        else:
            yield rx.redirect("/editor")
            return

    @rx.event
    def on_editor_change(self, value: str):
        """
        Updates the content state as the editor value changes.
        """
        self.content = value

    @rx.event
    def save_post(self):
        """
        Saves the new or updated post to a markdown file.
        """
        if not self.title.strip():
            return rx.toast.error("Title cannot be empty.")
        tags = [tag.strip() for tag in self.tags_str.split(",") if tag.strip()]
        date = datetime.date.today().strftime("%B %d, %Y")
        if self.post:
            post_id = self.post["id"]
            author = self.post.get("author", "ReflexPress User")
        else:
            post_id = title_to_slug(self.title)
            author = "ReflexPress User"
        frontmatter = f"---\ntitle: {self.title}\nauthor: {author}\ndate: {date}\ntags: {', '.join(tags)}\n---\n\n"
        file_content = frontmatter + self.content
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        file_path = POSTS_DIR / f"{post_id}.md"
        with file_path.open("w") as f:
            f.write(file_content)
        yield rx.toast.success("Post saved successfully!")
        yield BlogState.load_posts
        return rx.redirect(f"/editor/{post_id}")