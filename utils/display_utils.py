import os
import subprocess


def clear():
    subprocess.call("cls" if os.name == "nt" else "clear")
