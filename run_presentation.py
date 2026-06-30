#!/usr/bin/env python3
import subprocess
import sys

# Try to install python-pptx
result = subprocess.run([sys.executable, "-m", "pip", "install", "python-pptx"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Installation error:", result.stderr)
else:
    print("✓ python-pptx installed")

# Now run the presentation script
print("\nGenerating presentation...")
exec(open("create_professional_presentation.py").read())
