#!/bin/bash

# Step 1: Set variables
ORIG_REPO="https://github.com/hankthevc/Blog-Tool.git"
NEW_DIR="$HOME/MYBLOG"
TMP_DIR="$(mktemp -d)"

# Step 2: Clone the latest version of the original project
git clone "$ORIG_REPO" "$TMP_DIR/Blog-Tool"

# Step 3: Create your new project directory and copy over essential files/folders
mkdir -p "$NEW_DIR"
cd "$TMP_DIR/Blog-Tool"
cp -r llm publisher templates _layouts app.py main.py scheduler.py config.yaml requirements.txt "$NEW_DIR"
cp _config.yml index.md "$NEW_DIR"

# Step 4: Clean up the temporary directory
rm -rf "$TMP_DIR"

# Step 5: Initialize a new Git repository in your MYBLOG directory
cd "$NEW_DIR"
git init
git add .
git commit -m "Initial commit of MYBLOG from Blog-Tool"

# Step 6: Connect to your new GitHub repository
# Replace the URL below with the HTTPS URL of the repository you just created on GitHub
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/MYBLOG.git
git branch -M main
git push -u origin main

# Optional: Remove any old copy of the project if you're sure you no longer need it
# rm -rf /path/to/old/Blog-Tool
