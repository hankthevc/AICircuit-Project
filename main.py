import os
from datetime import date
import yaml
import jinja2
from llm.openai_client import generate_blog_post

def generate_and_save_post(topic, keywords):
    """Generate and save a blog post"""
    # Load config
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Generate content
    content = generate_blog_post(topic, keywords)

    # Prepare Jekyll frontmatter
    frontmatter = {
        'layout': 'default',
        'title': topic,
        'date': date.today().strftime('%Y-%m-%d'),
        'author': config['blog']['author'],
        'keywords': keywords.split(',')
    }

    # Format post with frontmatter
    post_content = "---\n"
    post_content += yaml.dump(frontmatter, default_flow_style=False)
    post_content += "---\n\n"
    post_content += content

    # Save to file
    os.makedirs(config['blog']['output_dir'], exist_ok=True)
    output_path = os.path.join(
        config['blog']['output_dir'],
        f"{date.today()}-{topic.replace(' ', '-').lower()}.md"
    )
    with open(output_path, "w") as f:
        f.write(post_content)

    print(f"✅ Blog post saved to {output_path}")
    return output_path

if __name__ == "__main__":
    # Default topic and keywords for direct script execution
    topic = "Best Indoor Plants for Small Apartments"
    keywords = "indoor plants, small space, apartment gardening"
    generate_and_save_post(topic, keywords) 