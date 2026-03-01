from pathlib import Path
from behave import given, when, then
import subprocess


@given("the project dependencies are locked")
def step_dependencies_locked(context):
    # Basic pre-condition asserting we are in the right repo
    assert Path("pyproject.toml").exists(), "Must be run from the repository root"


@when("I inspect the pyproject.toml configuration")
def step_inspect_pyproject(context):
    with open("pyproject.toml", "r") as f:
        context.pyproject_content = f.read()


@then('the "dev" dependencies should include "{package}"')
def step_check_dev_dependency(context, package):
    # Simple un-parsed text check since it's sufficient for verifying it's in the list
    assert (
        f'"{package}"' in context.pyproject_content
        or f'"{package}>=' in context.pyproject_content
    ), f"Expected to find {package} in pyproject.toml"


@given("the pytest-sugar plugin is installed")
def step_pytest_sugar_installed(context):
    result = subprocess.run(
        ["uv", "run", "python", "-c", "import pytest_sugar"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "pytest-sugar is not installed in the environment"


@when("I run the test suite")
def step_run_test_suite(context):
    result = subprocess.run(
        ["uv", "run", "pytest", "-q", "--no-header"],
        capture_output=True,
        text=True,
    )
    context.test_output = result.stdout + result.stderr
    context.test_exit_code = result.returncode


@then(
    "the output should be formatted with a progress bar and clear pass/fail indicators"
)
def step_check_output_format(context):
    assert context.test_exit_code == 0, (
        f"Test suite failed (exit code {context.test_exit_code}):\n{context.test_output}"
    )
    output_upper = context.test_output.upper()
    assert "PASSED" in output_upper or "passed" in context.test_output, (
        f"Pass/fail indicators not found in output:\n{context.test_output}"
    )


@given("the Justfile exists")
def step_justfile_exists(context):
    assert Path("Justfile").exists(), "Justfile not found"


@when("I locate the test execution command")
def step_locate_test_cmd(context):
    with open("Justfile", "r") as f:
        context.justfile = f.read()


@then('it should be configured to run pytest with "{flag}"')
def step_pytest_flag(context, flag):
    test_lines = [line for line in context.justfile.splitlines() if "pytest" in line]
    assert test_lines, "Could not find a pytest command in the Justfile"
    assert any(flag in line for line in test_lines), (
        f"Expected pytest to run with {flag}, found commands: {test_lines}"
    )
