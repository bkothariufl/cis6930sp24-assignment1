import shutil
import subprocess
import pytest
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from censoror import process_files

def test_censoring_cmd():
    input_directory = "tests/testFiles/"
    output_directory = "censoredFiles/"
    command = [
        "python", "censoror.py",
        "--input", f"{input_directory}/*.txt",
        "--names", "--dates", "--phones", "--address",
        "--output", output_directory,
        "--stats", "stdout"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    shutil.rmtree(output_directory)
    assert result.returncode == 0, f"Command failed with exit code {result.returncode}"

def test_censoring_names():
    input_directory = "tests/testFiles/enron_test.txt"
    stats_file = "stats.txt"
    output_directory = "censoredFiles/"
    process_files(input_directory,True, False, False, False,output_directory,stats_file)
    with open(stats_file, 'r') as stats_output:
        stats_text = stats_output.read()
    total_names_redacted = int(re.search(r"Total Names Redacted: (\d+)", stats_text).group(1))
    print(total_names_redacted)
    os.remove(stats_file)
    shutil.rmtree(output_directory)
    assert total_names_redacted==5
    
def test_censoring_dates():
    input_directory = "tests/testFiles/enron_test.txt"
    stats_file = "stats.txt"
    output_directory = "censoredFiles/"
    process_files(input_directory,False, True, False, False,output_directory,stats_file)
    with open(stats_file, 'r') as stats_output:
        stats_text = stats_output.read()
    total_dates_redacted = int(re.search(r"Total Dates Redacted: (\d+)", stats_text).group(1))
     # Clean up - remove the statistics file
    os.remove(stats_file)
    # Remove the censored files directory
    shutil.rmtree(output_directory)

    assert total_dates_redacted == 4

def test_censoring_phones():
    input_directory = "tests/testFiles/enron_test.txt"
    stats_file = "stats.txt"
    output_directory = "censoredFiles/"
    process_files(input_directory,False, False, True, False,"censoredFiles/",stats_file)
    with open(stats_file, 'r') as stats_output:
        stats_text = stats_output.read()
    total_phones_redacted = int(re.search(r"Total Phones Numbers Redacted: (\d+)", stats_text).group(1))
    os.remove(stats_file)
    shutil.rmtree(output_directory)
    assert total_phones_redacted == 1

def test_censoring_address():
    input_directory = "tests/testFiles/enron_test.txt"
    stats_file = "stats.txt"
    output_directory = "censoredFiles/"
    process_files(input_directory,False, False, False, True,"censoredFiles/",stats_file)
    with open(stats_file, 'r') as stats_output:
        stats_text = stats_output.read()
    
    total_addresses_redacted = int(re.search(r"Total Addresses Redacted: (\d+)", stats_text).group(1))
    os.remove(stats_file)
    shutil.rmtree(output_directory)
    assert total_addresses_redacted==4


# def main():
#     test_censoring_cmd()
#     test_censoring_names()
#     test_censoring_dates()
#     test_censoring_phones()
#     test_censoring_address()

# if __name__ == "__main__":
#     main()
