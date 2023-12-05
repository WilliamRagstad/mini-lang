from tests.util import done, set_crash_on_error
from tests.map import run_all as run_all_map_tests
from tests.lists import run_all as run_all_list_tests
from tests.std import run_all as run_all_std_tests
from tests.examples import run_all as run_all_examples

def main():
    # run all tests
    set_crash_on_error(False)
    passed = True
    print("\nRunning all tests:")
    print("==================")
    passed &= run_all_map_tests()
    passed &= run_all_list_tests()
    passed &= run_all_std_tests()
    passed &= run_all_examples()
    done(passed)

if __name__ == "__main__":
    main()
