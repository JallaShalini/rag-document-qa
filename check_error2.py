import subprocess
import sys
import os

with open("python_error.log", "w") as f:
    try:
        from app.main import app
        f.write("IMPORT SUCCESSFUL!\n")
    except Exception as e:
        import traceback
        f.write("IMPORT ERROR:\n")
        f.write(traceback.format_exc())
