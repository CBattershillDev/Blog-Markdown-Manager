import reflex as rx
from typing import TypedDict, Optional
import datetime
import re
import os

POSTS_DIR = rx.get_upload_dir() / "posts"


class Post(TypedDict):
    """
    Represents a single blog post.
    """

    id: str
    title: str
    author: str
    date: str
    tags: list[str]
    excerpt: str
    image_url: str
    content: str


class BlogState(rx.State):
    """
    Manages the state for the blog, including posts.
    """

    posts: list[Post] = []

    @rx.event(background=True)
    async def load_posts(self):
        """
        Loads all posts from the markdown files.
        """
        async with self:
            self.posts = []
            POSTS_DIR.mkdir(parents=True, exist_ok=True)
            for filename in os.listdir(POSTS_DIR):
                if filename.endswith(".md"):
                    filepath = POSTS_DIR / filename
                    with filepath.open("r") as f:
                        content_with_frontmatter = f.read()
                    frontmatter_match = re.match(
                        "^---\\n(.*?)\\n---\\n(.*)", content_with_frontmatter, re.DOTALL
                    )
                    if frontmatter_match:
                        frontmatter_str, content = frontmatter_match.groups()
                        post_data = {
                            "id": filename.replace(".md", ""),
                            "content": content.strip(),
                        }
                        for line in frontmatter_str.strip().split("""
"""):
                            if ":" in line:
                                key, value = line.split(":", 1)
                                key = key.strip()
                                value = value.strip()
                                if key == "tags":
                                    post_data[key] = [
                                        tag.strip() for tag in value.split(",")
                                    ]
                                else:
                                    post_data[key] = value
                        if "excerpt" not in post_data:
                            post_data["excerpt"] = (
                                content.strip().split("""
""")[0][:150]
                                + "..."
                            )
                        if "image_url" not in post_data:
                            post_data["image_url"] = "/placeholder.svg"
                        self.posts.append(Post(**post_data))
            self.posts.sort(key=lambda p: p["date"], reverse=True)

    @rx.var
    def get_post_by_id(self) -> Optional[Post]:
        """
        Returns a post by its ID from the router params.
        """
        post_id = self.router.page.params.get("post_id", "")
        for post in self.posts:
            if post["id"] == post_id:
                return post
        return None