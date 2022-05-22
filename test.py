from tests.objects import run_all as run_all_object_tests
from tests.lists import run_all as run_all_list_tests

def main():
    # run all tests
    passed = True
    print("\nRunning all tests:")
    print("==================")
    passed &= run_all_object_tests()
    passed &= run_all_list_tests()
    print("\n==================")
    if passed:
        print("\nOK! All tests passed.")
    else:
        print("\nERROR! Some tests failed.")

if __name__ == "__main__":
    main()
