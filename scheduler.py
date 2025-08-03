import schedule
import time
import yaml
import random
from datetime import datetime
import os
from main import generate_and_save_post
from publisher.github_pages import GitHubPagesPublisher

class BlogScheduler:
    def __init__(self):
        self.topics = [
            "Best Indoor Plants for Small Apartments",
            "How to Start a Home Garden",
            "Essential Tools for Urban Gardening",
            "Low-Maintenance Houseplants for Beginners",
            "Vertical Gardening Solutions",
            "Herb Garden Tips for Kitchen Windows",
            "Succulent Care Guide",
            "Air-Purifying Plants for Your Home",
            "Container Gardening Basics",
            "Pet-Safe Indoor Plants"
        ]
        
        self.keywords = {
            "Best Indoor Plants for Small Apartments": "indoor plants, small space, apartment gardening",
            "How to Start a Home Garden": "home garden, gardening basics, beginner gardening",
            "Essential Tools for Urban Gardening": "urban gardening, gardening tools, city garden",
            "Low-Maintenance Houseplants for Beginners": "low maintenance plants, easy care plants, beginner plants",
            "Vertical Gardening Solutions": "vertical garden, wall garden, space saving garden",
            "Herb Garden Tips for Kitchen Windows": "herb garden, kitchen herbs, windowsill garden",
            "Succulent Care Guide": "succulents, succulent care, indoor succulents",
            "Air-Purifying Plants for Your Home": "air purifying plants, clean air, indoor air quality",
            "Container Gardening Basics": "container garden, pot plants, container plants",
            "Pet-Safe Indoor Plants": "pet friendly plants, safe plants, cat safe plants"
        }

    def generate_post(self):
        """Generate a new blog post"""
        # Pick a random topic
        topic = random.choice(self.topics)
        keywords = self.keywords[topic]
        
        print(f"🌱 Generating post: {topic}")
        
        # Generate and save the post
        generate_and_save_post(topic, keywords)
        
        # Publish to GitHub Pages
        publisher = GitHubPagesPublisher()
        publisher.publish()
        
        print(f"✨ Post generated and published at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    scheduler = BlogScheduler()
    
    # Schedule post generation
    # Default: Every day at 9:00 AM
    schedule.every().day.at("09:00").do(scheduler.generate_post)
    
    print("🚀 Blog post scheduler started!")
    print("📅 Next post will be generated at 09:00 AM tomorrow")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 