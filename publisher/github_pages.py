import os
from git import Repo
import yaml
import shutil
from datetime import datetime

class GitHubPagesPublisher:
    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)
        
        self.repo = Repo(os.getcwd())
        self.deploy_branch = self.config['blog']['deploy_branch']

    def _ensure_deploy_branch(self):
        """Ensure the deployment branch exists"""
        try:
            # Try to check out the existing branch
            self.repo.git.checkout(self.deploy_branch)
            # Switch back to main
            self.repo.git.checkout('main')
        except:
            # Branch doesn't exist, create it as an orphan branch
            current = self.repo.active_branch
            self.repo.git.checkout('--orphan', self.deploy_branch)
            # Remove all files from the index
            self.repo.git.rm('-rf', '.')
            # Create initial commit
            self.repo.git.commit('--allow-empty', '-m', "Initialize gh-pages branch")
            # Switch back to original branch
            current.checkout()

    def publish(self):
        """Publish blog posts to GitHub Pages"""
        current_branch = self.repo.active_branch
        
        try:
            # Ensure deploy branch exists
            self._ensure_deploy_branch()
            
            # Switch to deploy branch
            self.repo.git.checkout(self.deploy_branch)
            
            # Clean existing files except .git
            for item in os.listdir():
                if item != '.git':
                    if os.path.isfile(item):
                        os.remove(item)
                    elif os.path.isdir(item):
                        shutil.rmtree(item)
            
            # Copy Jekyll files
            files_to_copy = [
                '_config.yml',
                'index.md',
                '_layouts',
                self.config['blog']['output_dir']
            ]
            
            for item in files_to_copy:
                if os.path.exists(item):
                    if os.path.isfile(item):
                        shutil.copy2(item, '.')
                    else:
                        shutil.copytree(item, f"./{os.path.basename(item)}", dirs_exist_ok=True)
            
            # Add and commit changes
            self.repo.git.add(all=True)
            commit_message = f"Update blog posts - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.repo.index.commit(commit_message)
            
            # Force push to remote
            self.repo.git.push('origin', self.deploy_branch, '--force')
            
            print(f"✅ Successfully published to GitHub Pages")
            
        finally:
            # Switch back to original branch
            current_branch.checkout()

if __name__ == "__main__":
    publisher = GitHubPagesPublisher()
    publisher.publish() 