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


## censor.py Function Descriptions