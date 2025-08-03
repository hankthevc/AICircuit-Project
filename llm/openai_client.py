from openai import OpenAI
import yaml
import os

with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Get API key from environment variable if config contains a variable reference
api_key = config['openai_api_key']
if api_key.startswith('${') and api_key.endswith('}'):
    env_var = api_key[2:-1]  # Remove ${ and }
    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(f"Environment variable {env_var} not set. Please set it with your OpenAI API key.")

client = OpenAI(api_key=api_key)

def generate_blog_post(topic, keywords):
    prompt = f"""
You are a professional content writer. Write a 1000-word SEO-optimized blog post on the topic: '{topic}'.

Target keywords: {keywords}

Tone: friendly, authoritative. Include an intro, 3-5 subheadings, and a conclusion. Use Markdown.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content 