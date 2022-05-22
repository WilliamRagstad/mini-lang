from io import StringIO
from src.atoms import Atom, ValueAtom
from src.interpreter import execute, globalEnvironment

all_asserts_passed = True
crash_on_error = False

def eval(input: str) -> Atom:
    res, _ = execute(StringIO(input), globalEnvironment())
    return res

def assert_eval(input: str, expected: Atom) -> None:
    global all_asserts_passed
    try:
        actual = eval(input)
        if actual != expected:
            all_asserts_passed = False
            print(f"  - FAILED AT: {input}")
            print(f"    Expected: {expected}, got: {actual}")
    except Exception as e:
        all_asserts_passed = False
        print(f"  - FAILED AT: {input}")
        print(f"    Exception: {e}")
        if crash_on_error:
            raise e

def get_all_asserts_passed() -> bool:
    return all_asserts_passed

def new_test_suite(forTests: str) -> None:
    global all_asserts_passed
    all_asserts_passed = True
    print(f"\nRunning {forTests} tests:")

def set_crash_on_error(crash: bool) -> None:
    global crash_on_error
    crash_on_error = crash
