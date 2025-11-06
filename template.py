import os

structure = [
    "app",
    ".github/workflows",
    ".tekton"
]

for folder in structure:
    os.makedirs(folder, exist_ok=True)

files = {
    "app/main.py": """from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from OpenShift CI/CD Pipeline!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
""",
    "app/test_main.py": """def test_hello_route():
    from app.main import app
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello from OpenShift" in response.data
""",
    "requirements.txt": "Flask==3.0.2\npytest==8.0.0\nflake8==7.0.0\n",
    ".github/workflows/workflow.yml": """name: CI-CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run linting
        run: |
          flake8 app/

      - name: Run tests
        run: |
          pytest app/
""",
    ".tekton/tasks.yml": """apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: cleanup-task
spec:
  steps:
    - name: cleanup
      image: alpine:3.19
      script: |
        #!/bin/sh
        echo "Cleaning up temporary files..."
        rm -rf /workspace/source/tmp || true
        echo "Cleanup complete!"
---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: nose-test-task
spec:
  steps:
    - name: run-nose-tests
      image: python:3.10
      script: |
        #!/bin/bash
        pip install -r requirements.txt
        pytest app/
        echo "Tests completed!"
"""
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ All project files created successfully!")
