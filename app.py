import os
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from main import generate_and_save_post
from publisher.github_pages import GitHubPagesPublisher
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()

def generate_and_publish_post():
    """Generate and publish a new blog post"""
    from scheduler import BlogScheduler
    blog_scheduler = BlogScheduler()
    blog_scheduler.generate_post()

# Schedule the job to run daily at 9:00 AM UTC
scheduler.add_job(generate_and_publish_post, 'cron', hour=9)
scheduler.start()

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/generate', methods=['POST'])
def generate_post():
    """Manually trigger post generation"""
    try:
        generate_and_publish_post()
        return jsonify({"status": "success", "message": "Blog post generated and published"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 