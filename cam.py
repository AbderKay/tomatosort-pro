# Python
__pycache__/
*.py[cod]
.venv/
venv/
env/
.ipynb_checkpoints/

# Data — full dataset lives on Roboflow, not in git (samples/ is kept on purpose)
dataset/train/
dataset/valid/
dataset/test/
*.zip

# We DO ship the trained model (small YOLOv8n). Ignore other large weights.
runs/
*.onnx
*.engine

# Env / OS / IDE
.env
.vscode/
.idea/
.DS_Store
Thumbs.db
*.log
