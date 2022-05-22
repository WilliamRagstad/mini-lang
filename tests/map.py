from .util import assert_eval, get_all_asserts_passed, new_test_suite, ValueAtom

def test_create_map():
    print("- Testing create map...")
    assert_eval("#{}", ValueAtom("map", {}))
    assert_eval("#{a: 5}", ValueAtom("map", {"a": ValueAtom("number", 5)}))
    assert_eval("#{a: 5, b: 6}", ValueAtom("map", {"a": ValueAtom("number", 5), "b": ValueAtom("number", 6)}))

def test_member_access():
    print("- Testing member access...")
    assert_eval("#{a: 5}.a", ValueAtom("number", 5))
    assert_eval("m = #{a: 5} m.a", ValueAtom("number", 5))
    assert_eval("#{a: #{ b: 5}}.a.b", ValueAtom("number", 5))
    assert_eval("#{a: #{ b: #{c: 6}}}.a.b.c", ValueAtom("number", 6))
    assert_eval("#{a: 5}['a']", ValueAtom("number", 5))
    assert_eval("#{a: #{ b: 5}}['a']['b']", ValueAtom("number", 5))

def test_member_assignment():
    print("- Testing member assignment...")
    assert_eval("m = #{a: 5} m.a = 6 m.a", ValueAtom("number", 6))

def run_all() -> bool:
    new_test_suite("map")
    test_create_map()
    test_member_access()
    test_member_assignment()
    return get_all_asserts_passed()

if __name__ == "__main__":
    run_all()
