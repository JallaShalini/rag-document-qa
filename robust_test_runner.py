import subprocess
import os

try:
    result = subprocess.run([r"venv\Scripts\python.exe", "-m", "pytest", "tests/"], capture_output=True, text=True)
    with open("pytest_results.txt", "w") as f:
        f.write("RETURNCODE: " + str(result.returncode) + "\n")
        f.write("STDOUT:\n" + result.stdout + "\n")
        f.write("STDERR:\n" + result.stderr + "\n")
except Exception as e:
    with open("pytest_results.txt", "w") as f:
        f.write(f"Exception happened: {e}\n")
