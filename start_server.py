import subprocess
with open("uvicorn_log.txt", "w") as f:
    subprocess.run(["venv\\Scripts\\python.exe", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"], stdout=f, stderr=f)
