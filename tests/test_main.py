import subprocess
import pytest

def test_censoring_cmd():
    input_directory = "tests/testFiles/"
    command = [
        "python", "censoror.py",
        "--input", f"{input_directory}/*.txt",
        "--names", "--dates", "--phones", "--address",
        "--output", "censored_test_files/",
        "--stats", "stdout"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    assert result.returncode == 0, f"Command failed with exit code {result.returncode}"

def test_censoring_names():
    input_directory = "tests/testFiles/"
    command = [
        "python", "censoror.py",
        "--input", f"{input_directory}/enron_test.txt",
        "--names",
        "--output", "censored_test_files/",
        "--stats", "stdout"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    assert result.returncode == 0, f"Command failed with exit code {result.returncode}"


def main():
    # test_censoring_cmd()
    test_censoring_names()

if __name__ == "__main__":
    main()
