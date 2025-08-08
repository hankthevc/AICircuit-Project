import os
import yaml
from openai import OpenAI

def _load_config():
    """Try to load configuration from either config.yaml or _config.yml. Returns a dict."""
    for name in ("config.yaml", "_config.yml"):
        if os.path.exists(name):
            with open(name, "r") as f:
                return yaml.safe_load(f) or {}
    return {}

config = _load_config()

# Prefer explicit environment variable, fall back to config value
api_key = os.getenv("OPENAI_API_KEY") or config.get("openai_api_key")

# Support config values that reference env vars like ${OPENAI_API_KEY}
if isinstance(api_key, str) and api_key.startswith("${") and api_key.endswith("}"):
    env_var = api_key[2:-1]
    api_key = os.getenv(env_var)

if not api_key:
    raise ValueError(
        "OpenAI API key not found. Set OPENAI_API_KEY or add openai_api_key to config.yaml or _config.yml"
    )

client = OpenAI(api_key=api_key)


def generate_blog_post(topic, keywords, word_count=1000):
    """Generate an SEO-optimized blog post on the given topic targeting the provided keywords.

    Returns the generated markdown text.
    """
    prompt = f"""
You are a professional content writer. Write a {word_count}-word SEO-optimized blog post on the topic: "{topic}".

Target keywords: {keywords}

Tone: friendly, authoritative. Include an intro, 3-5 subheadings, and a conclusion. Use Markdown for formatting. Include frontmatter YAML when appropriate.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        # Newer SDKs return response.choices[0].message.content
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenAI request failed: {e}")