# debug.py
import subprocess
import sys

print("Python path:", sys.path)
print("\nInstalled packages:")
subprocess.run([sys.executable, "-m", "pip", "list"])
