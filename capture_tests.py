import subprocess
with open("pytest_results.txt", "w") as f:
    subprocess.run(["venv\\Scripts\\python.exe", "-m", "pytest", "tests/"], stdout=f, stderr=f)
