from .util import eval, ValueAtom

def test_create_object():
    print("- Testing create object...")
    assert eval("#{}") == ValueAtom("map", {})
    assert eval("#{a: 5}") == ValueAtom("map", {"a": ValueAtom("number", 5)})
    assert eval("#{a: 5, b: 6}") == ValueAtom("map", {"a": ValueAtom("number", 5), "b": ValueAtom("number", 6)})

def test_member_access():
    print("- Testing member access...")
    assert eval("#{a: 5}.a") == ValueAtom("number", 5)
    assert eval("m = #{a: 5} m.a") == ValueAtom("number", 5)
    assert eval("#{a: #{ b: 5}}.a.b") == ValueAtom("number", 5)
    assert eval("#{a: #{ b: #{c: 6}}}.a.b.c") == ValueAtom("number", 6)

def test_member_assignment():
    print("- Testing member assignment...")
    assert eval("m = #{a: 5} m.a = 6 m.a") == ValueAtom("number", 6)

def run_all():
    print("Running all object tests:")
    test_create_object()
    test_member_access()
    test_member_assignment()

if __name__ == "__main__":
    run_all()
