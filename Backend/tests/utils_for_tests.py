
import inspect


def pytest_start_test_display():
    """Called when a test starts and prints the calling function name."""
    caller_function = inspect.stack()[1].function  # Gets the caller's function name
    print()
    print(f"\t🟢 RUNNING '{caller_function}()'")

def pytest_assertion_success(msg="SUCCESS"):
    """Called when an assertion passes."""
    print(f"\t\t✅ Assertion Passed: {msg}")

def pytest_test_success(msg=""):
    """Called when a test passes and prints the calling function name."""
    caller_function = inspect.stack()[1].function  # Gets the caller's function name
    print(f"\t✅ PASSED '{caller_function}()': {msg}")

def pytest_assertion_failure(msg="FAILURE"):
    """Called when an assertion fails."""
    print(f"\\tt❌ Assertion Failed: {msg}")
    print("\t❌ Test Failed")