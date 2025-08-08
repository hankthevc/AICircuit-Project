import os
import sys
from datetime import datetime
import yaml
from llm.openai_client import generate_blog_post
from publisher.github_pages import GitHubPagesPublisher

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "blog_post_template.md")
POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "_config.yml")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def render_template(template_path, context):
    with open(template_path, "r") as f:
        template = f.read()
    for k, v in context.items():
        template = template.replace(f"{{{{ {k} }}}}", str(v))
    return template

def main():
    config = load_config()
    blog_cfg = config.get("blog", {})
    topic = os.environ.get("BLOG_TOPIC", "The Future of AI Blogging")
    keywords = os.environ.get("BLOG_KEYWORDS", "AI, blogging, automation")
    author = blog_cfg.get("author", "AI Ghostwriter")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_url = "https://source.unsplash.com/800x400/?ai,blog"  # Placeholder

    print(f"Generating blog post on: {topic}")
    content = generate_blog_post(topic, keywords)

    context = {
        "title": topic,
        "date": date,
        "author": author,
        "image_url": image_url,
        "content": content,
    }

    os.makedirs(POSTS_DIR, exist_ok=True)
    filename = os.path.join(POSTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}-{topic.lower().replace(' ', '-')}.md")
    with open(filename, "w") as f:
        f.write(render_template(TEMPLATE_PATH, context))
    print(f"✅ Blog post saved to {filename}")

    if "--publish" in sys.argv:
        print("Publishing to GitHub Pages...")
        publisher = GitHubPagesPublisher()
        publisher.publish()
        print("✅ Published!")
    else:
        print("(Dry run: not published. Run with --publish to deploy)")

if __name__ == "__main__":
    main()
