from io import StringIO
from src.atoms import Atom, ValueAtom
from src.interpreter import execute, globalEnvironment


# Helper functions
def colored(c: tuple[int, int, int], text: str) -> str:
    (r, g, b) = c
    return "\033[38;2;{};{};{}m{} \033[0m".format(r, g, b, text)

yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Test Utilitiy functions
all_asserts_passed = True
crash_on_error = False

def eval(input: str) -> Atom:
    res, _ = execute(StringIO(input), globalEnvironment())
    return res

def assert_eval(input: str, expected: Atom) -> None:
    global all_asserts_passed
    try:
        actual = eval(input)
        if not actual.structural_eq(expected):
            all_asserts_passed = False
            print(colored(red, f"  - FAILED AT: {input}"))
            print(colored(yellow, f"    Expected: {expected}, got: {actual}"))
    except Exception as e:
        all_asserts_passed = False
        print(colored(red, f"  - FAILED AT: {input}"))
        print(colored(yellow, f"    Exception: {e}"))
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

def done(passed: bool) -> None:
    if passed:
        print(colored(green, "\nOK: All tests passed!"))
    else:
        print(colored(red, "\nERROR: Some tests failed!"))
