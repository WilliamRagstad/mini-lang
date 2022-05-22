from .util import assert_eval, get_all_asserts_passed, new_test_suite, ValueAtom

def test_create_list():
    print("- Testing create list...")
    assert_eval("[]", ValueAtom("list", []))
    assert_eval("[1]", ValueAtom("list", [ValueAtom("number", 1)]))
    assert_eval("[1, 2]", ValueAtom("list", [ValueAtom("number", 1), ValueAtom("number", 2)]))

def test_index_access():
    print("- Testing index access...")
    assert_eval("[1, 2, 3][0]", ValueAtom("number", 1))
    assert_eval("[1, 2, 3][1]", ValueAtom("number", 2))
    assert_eval("[1, 2, 3][2]", ValueAtom("number", 3))
    assert_eval("[1, 2, 3][-1]", ValueAtom("number", 3))
    assert_eval("[1, 2, 3][-2]", ValueAtom("number", 2))
    assert_eval("[1, 2, 3][-3]", ValueAtom("number", 1))

def test_index_assignment():
    print("- Testing index assignment...")
    assert_eval("m = [1, 2, 3] m[1] = 6 m[1]", ValueAtom("number", 6))

def test_range_index():
    print("- Testing range index...")
    assert_eval("[1, 2, 3][1:2]", ValueAtom("list", [ValueAtom("number", 2)]))
    assert_eval("[1, 2, 3][1:3]", ValueAtom("list", [ValueAtom("number", 2), ValueAtom("number", 3)]))
    assert_eval("[1, 2, 3][1:4]", ValueAtom("list", [ValueAtom("number", 2), ValueAtom("number", 3), ValueAtom("number", 4)]))

def run_all() -> bool:
    new_test_suite("list")
    test_create_list()
    test_index_access()
    test_index_assignment()
    test_range_index()
    return get_all_asserts_passed()

if __name__ == "__main__":
    run_all()
