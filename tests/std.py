from .util import assert_eval, get_all_asserts_passed, new_test_suite, ValueAtom


def run_all() -> bool:
    new_test_suite("standard library")
    print("- Testing print function")
    assert_eval("print(\"Hello World\")", ValueAtom("unit", None))
    print("- Testing input function")
    # assert_eval("input(\"What is your name?\")", ValueAtom("string", "John"))
    print("(skipped)")
    print("- Testing exit function")
    # assert_eval("exit(11)", ValueAtom("unit", None))
    print("(skipped)")
    print("- Testing system run function")
    assert_eval("system_run(\"echo Hello World\", true)", ValueAtom("unit", None))
    print("- Testing system output function")
    assert_eval("str_trim(system_output(\"echo Hello World\", true))", ValueAtom("string", "Hello World"))
    print("- Testing file read function")

    return get_all_asserts_passed()

if __name__ == "__main__":
    run_all()
