import os
import sys
import traceback

# Delete scratch files to resolve user's lint error
files_to_delete = ["run_tests_script.py", "robust_test_runner.py", "capture_tests.py", "start_server.py"]
for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)

# Try to import FastAPI app to catch startup errors
with open("startup_debug_log.txt", "w") as out:
    try:
        from app.main import app
        out.write("Successfully imported app.main. No syntax or import errors.\n")
    except Exception as e:
        out.write("FAILED TO IMPORT APP.MAIN:\n")
        traceback.print_exc(file=out)
