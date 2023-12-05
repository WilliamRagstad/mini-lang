from os import listdir
from os.path import isfile, join
import subprocess
import sys

from tests.util import done

def run_file(file: str) -> bool:
    """
    run a file in the /examples directory
    using the command line interface:
    `python3 mini.py examples/<file>`
    """
    python = sys.orig_argv[0]
    try:
        out = subprocess.check_output([python, "mini.py", f"examples/{file}"])
        txt = out.decode("utf-8")
        if "error" in txt.lower():
            print(txt)
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"))
        return False

def run_all() -> bool:
    print("\nRunning examples tests:")
    # run all files in the /examples directory
    passed = True
    files = [f for f in listdir("examples") if isfile(join("examples", f))]
    for file in files:
        if file.endswith(".m"):
            print(f"- examples/{file}")
            match file:
                case "input.m" | "unicode.m":
                    print("(skipped)")
                    continue
                case _:
                    passed &= run_file(file)
    return passed

if __name__ == "__main__":
    done(run_all())
