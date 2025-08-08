import os
import yaml
import shutil
from datetime import datetime
from git import Repo, GitCommandError

def _load_config():
    """Load config from _config.yml or config.yaml if present."""
    for name in ("_config.yml", "config.yaml"):
        if os.path.exists(name):
            with open(name, "r") as f:
                return yaml.safe_load(f) or {}
    return {}

class GitHubPagesPublisher:
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.config = _load_config()

        try:
            self.repo = Repo(self.repo_path)
        except Exception as e:
            raise RuntimeError(f"Directory {self.repo_path} is not a git repository: {e}")

        self.deploy_branch = self.config.get('blog', {}).get('deploy_branch', 'gh-pages')
        self.output_dir = self.config.get('blog', {}).get('output_dir', 'posts')

    def _branch_exists(self, name: str) -> bool:
        return name in [b.name for b in self.repo.branches]

    def _ensure_deploy_branch(self):
        """Ensure the deployment branch exists; if not, create an orphan branch with an initial commit."""
        if self._branch_exists(self.deploy_branch):
            return

        # Create orphan branch
        try:
            # Create orphan branch and make an empty initial commit
            self.repo.git.checkout('--orphan', self.deploy_branch)
            # Remove all files from index and working directory
            for item in os.listdir(self.repo_path):
                if item == '.git':
                    continue
                path = os.path.join(self.repo_path, item)
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except Exception:
                    pass

            # Create an empty commit
            self.repo.git.add(all=True)
            self.repo.index.commit("Initialize deployment branch")
        finally:
            # Checkout back to main (if exists) or to the first available branch
            default_branch = 'main' if 'main' in [b.name for b in self.repo.branches] else self.repo.branches[0].name
            try:
                self.repo.git.checkout(default_branch)
            except Exception:
                pass

    def publish(self):
        """Publish blog posts to GitHub Pages by copying the site files to the deployment branch and pushing."""
        # Record current branch so we can switch back
        try:
            current_branch = self.repo.active_branch.name
        except TypeError:
            current_branch = None

        # Ensure deploy branch exists
        self._ensure_deploy_branch()

        try:
            # Checkout deploy branch
            self.repo.git.checkout(self.deploy_branch)

            # Wipe working directory except .git
            for item in os.listdir(self.repo_path):
                if item == '.git':
                    continue
                path = os.path.join(self.repo_path, item)
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except Exception:
                    pass

            # Items to copy
            files_to_copy = [
                '_config.yml',
                'index.md',
                '_layouts',
                self.output_dir,
            ]

            for item in files_to_copy:
                src = os.path.join(self.repo_path, item)
                if not os.path.exists(src):
                    continue
                dest = os.path.join(self.repo_path, os.path.basename(item))
                try:
                    if os.path.isfile(src):
                        shutil.copy2(src, dest)
                    elif os.path.isdir(src):
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                except Exception:
                    pass

            # Commit and push
            self.repo.git.add('--all')
            commit_message = f"Update blog posts - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            try:
                # Use index commit to avoid accidental empty commits
                if self.repo.index.diff('HEAD') or self.repo.untracked_files:
                    self.repo.index.commit(commit_message)
            except Exception:
                # In case HEAD doesn't exist (fresh orphan), allow commit
                try:
                    self.repo.index.commit(commit_message)
                except Exception:
                    pass

            # Force push to remote
            try:
                self.repo.git.push('origin', self.deploy_branch, '--force')
                print("✅ Successfully published to GitHub Pages")
            except GitCommandError as e:
                print(f"Failed to push to remote: {e}")

        finally:
            # Switch back to original branch if available
            if current_branch:
                try:
                    self.repo.git.checkout(current_branch)
                except Exception:
                    pass


if __name__ == "__main__":
    publisher = GitHubPagesPublisher()
    publisher.publish()