from .util import assert_eval, get_all_asserts_passed, new_test_suite, ValueAtom

def test_print():
    print("- Testing print function")
    assert_eval("print(\"Hello World\")", ValueAtom("unit", None))

def test_input():
    print("- Testing input function")
    assert_eval("input(\"What is your name?\")", ValueAtom("string", "John"))

def run_all() -> bool:
    new_test_suite("standard library")
    test_print()
    test_input()
    return get_all_asserts_passed()

if __name__ == "__main__":
    run_all()
