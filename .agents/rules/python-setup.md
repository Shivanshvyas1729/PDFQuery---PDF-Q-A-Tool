# Python Project Setup

When setting up a new Python project in this workspace:

1. **Always configure `pyproject.toml` with build-system and package discovery:**
   ```toml
   [build-system]
   requires = ["setuptools>=61.0"]
   build-backend = "setuptools.build_meta"
   
   [tool.setuptools.packages.find]
   include = ["<package_name>*"]
   
   [tool.pyright]
   extraPaths = ["."]
   ```

2. **Always create a `pyrightconfig.json` at the project root:**
   ```json
   {
     "venvPath": ".",
     "venv": ".venv",
     "extraPaths": ["."],
     "pythonVersion": "3.12"
   }
   ```

3. **Always install the project in editable mode** after setting up pyproject.toml:
   ```bash
   uv pip install -e .
   ```
   This registers the package in `.venv/Lib/site-packages/` so all tools and the IDE can find it.

4. **Never rely on `.vscode/settings.json` for Python import resolution.** Use `pyrightconfig.json` (standard Python tooling file) instead.

5. The user's Antigravity IDE is configured globally to use Pylance with Pyrefly language services disabled. Do not change these global settings.
