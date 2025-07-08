from pathlib import Path

# Define project root
project_root = Path("auto_you")

# Define all folders to create
folders = [
    project_root / "config",
    project_root / "auth",
    project_root / "tools",
    project_root / "llm",
    project_root / "app",
]

# Define all files to create (empty for now)
files = {
    project_root / ".env": "",
    project_root / "credentials.json": "",
    project_root / "token.json": "",
    project_root / "README.md": "# Auto-You Project\n",
    project_root / "config" / "secrets.py": "# Secrets config\n",
    project_root / "config" / "paths.py": "# Paths setup using pathlib\n",
    project_root / "auth" / "gmail_auth.py": "# Gmail OAuth logic\n",
    project_root / "tools" / "gmail_tool.py": "# GmailTool class\n",
    project_root / "llm" / "summarizer.py": "# LLM Summarizer API\n",
    project_root / "app" / "main.py": "# Entry point for CLI or FastAPI\n",
}

# Create folders
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

# Create files with basic content
for file_path, content in files.items():
    if not file_path.exists():
        file_path.write_text(content)

print(f"Project structure created at: {project_root.resolve()}")
