# README

## NAME: Abhishek Kothari
## UFID: 35641285


## Assignment Description:
Design a system which accepts plain text documents then detects and censors “sensitive” items. The data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. Documents such as police reports, court transcripts, and hospital records all contain sensitive information. The program should look to censor all names and dates, and phone numbers. Each censored file should be transformed into new files of the same name with the .censored extension, and written to the folder described by --output flag. The final parameter, --stats, describes the file or location to write the statistics of the censored files. 

Censor flags to be used: --names, --dates, --phones, --address 




## How to install
On an ubuntu server: 
curl https://pyenv.run | bash
pyenv install 3.11
pyenv global 3.11
pipenv install --dev pytest
pipenv install spacy


## How to run
pipenv run python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stderr

https://github.com/bkothariufl/cis6930sp24-assignment1/assets/151199302/383d5cde-246e-43cb-b75c-47b7dbb20e44



## censor.py Function Descriptions

### `censor_file(file_path: str, censor_names: bool, censor_dates: bool, censor_phones: bool, censor_address: bool) -> str`

Censors sensitive information in the specified file based on the provided flags. Supports redaction of names, dates, phone numbers, and addresses. Returns the censored content. Utilizes the spaCy library for named entity recognition and regular expressions for additional patterns.

### `process_file_stats(file_path: str, censor_names: bool, file_name_count: int, censor_address: bool, file_address_count: int, censor_dates: bool, file_date_count: int, censor_phones: bool, file_phone_count: int)`

Processes and updates the statistics for a specific file, including the count of redacted names, addresses, dates, and phone numbers. These statistics are stored in a temporary file for later compilation.

### `process_total_stats(censor_names: bool, censor_dates: bool, censor_phones: bool, censor_address: bool)`

Processes and updates the compiled statistics, including the total count of redacted names, addresses, dates, and phone numbers. These compiled statistics are stored in a temporary file.

### `print_stats(output_type: str)`

Prints the censorship statistics based on the specified output type ('stdout', 'stderr', or a custom file path). Reads the statistics from the temporary file and removes it afterward.

### `process_files(input_pattern: str, censor_names: bool, censor_dates: bool, censor_phones: bool, censor_address: bool, output_directory: str, output_type: str)`

Processes a set of files based on the provided input pattern and censorship flags. Generates censored files in the specified output directory and prints statistics. Utilizes spaCy for entity recognition and regular expressions for additional patterns.

### `main()`

The main function responsible for parsing command-line arguments, invoking the file processing, and handling user input errors. It orchestrates the entire censorship process for a given set of input files.

## test_main.py functions

### `test_censoring_cmd()`
This test case runs the censorship command using subprocess and asserts that the exit code is 0, indicating successful execution. It also cleans up the generated censored files directory.

### `test_censoring_names()`
This test case processes a sample file with name-related information and checks if the total count of redacted names matches the expected count. It cleans up the generated statistics file and censored files directory.

### `test_censoring_dates()`
Similar to the names test, this test case processes a file with date-related information and checks if the total count of redacted dates matches the expected count. It cleans up the generated statistics file and censored files directory.

### `test_censoring_phones()`
Processes a file with phone number-related information and checks if the total count of redacted phone numbers matches the expected count. Cleans up the generated statistics file and censored files directory.

### `test_censoring_address()`
Processes a file with address-related information and checks if the total count of redacted addresses matches the expected count. Cleans up the generated statistics file and censored files directory.


## Assumptions and Challenges: 

For the censoring logic, i decided to use the spacy library. It made it easy to identify the names,  dates and addresses. There was an issue with the python import because of the model being used, to over come that, I used another package downloader called spacy_download.


I observed that the spacy library was not highly efficient in identifying addresses, due to which i decided the pyap library as a first level check to censor the address, It is currently configured for the addresses in United States. 

For censoring names, the first level censoring was done using spacy and then using regular expressions especially in the instances where the name was formatted like firstName.lastName or fN.ln@EMAIL.COM. 

The phone numbers are censored using a regular expression.
