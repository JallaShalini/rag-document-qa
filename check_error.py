import subprocess

result = subprocess.run(
    ["venv\\Scripts\\python.exe", "-c", "import app.main"],
    capture_output=True,
    text=True
)
with open("python_error.log", "w") as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\nSTDERR:\n")
    f.write(result.stderr)
