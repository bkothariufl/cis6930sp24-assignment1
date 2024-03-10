import argparse
import glob
import os
import re
import sys
import spacy
import pyap
from spacy_download import load_spacy

# Will download the model if it isn't installed yet
nlp = load_spacy("en_core_web_sm")  

total_name_count = 0
total_date_count = 0
total_address_count = 0
total_phone_count = 0
def censor_file(file_path, censor_names, censor_dates, censor_phones, censor_address):
    # print(f"Censoring file: {file_path} with flags - names: {censor_names}, dates: {censor_dates}, phones: {censor_phones}, address: {censor_address}")

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        
        replacements = {
            'PERSON': '[NAME]',
            'DATE': '[DATE]',
            'GPE': '[ADDRESS]'
        }

        # Local variables to track counts for each file
        file_name_count = 0
        file_date_count = 0
        file_address_count = 0
        file_phone_count = 0

        if censor_address:
            addresses = pyap.parse(content, country='US')
            for address in addresses:
                # print(address)
                count=0
                content, count = content.replace(address.full_address, '███', 1), count + 1
                file_address_count += count
        doc = nlp(content)

        if censor_names or censor_dates or censor_address:
            for ent in doc.ents:
                # print(ent.text, ent.start_char, ent.end_char, ent.label_)
                if ent.label_ == 'PERSON' and censor_names:
                    # print("Censoring Person: "+ent.text)
                    content = content.replace(ent.text, '███')
                    file_name_count += 1
                elif (ent.label_ == 'DATE' or ent.label_=='TIME') and censor_dates:
                    # print("Censoring Date: "+ent.text)
                    content = content.replace(ent.text, '███')
                    file_date_count += 1
                elif (ent.label_ == 'GPE' or ent.label_ =='FAC') and censor_address:
                    # print("Censoring Address: "+ent.text)
                    content = content.replace(ent.text, '███')
                    file_address_count += 1
                # print("----------------------------------------------------------------")
        # if censor_address:
        #     addresses = pyap.parse(content, country='US')
        #     for address in addresses:
        #         # print(address)
        #         count=0
        #         content, count = content.replace(address.full_address, '███', 1), count + 1
        #         file_address_count += count

        if censor_phones:
            phone_regex = r'(\+\d{1,3}\s?)?(?:\(\d{1,}\)[\s.-]?)?\d{3,}[\s.-]?\d{3,}[\s.-]?\d{3,}'
            content, file_phone_count = re.subn(phone_regex, '███', content)
        
        if censor_names:
            pattern = r'(?<![@\w])\b[a-zA-Z]+(?:\.[a-zA-Z]+)+\b(?![a-zA-Z@])'
            name_count_temp=0
            content,name_count_temp = re.subn(pattern, '███', content, flags=re.IGNORECASE)
            file_name_count+=name_count_temp
            
            name_count_temp=0
            email_name_name_pattern = r'(\b[a-zA-Z]+(?:\.[a-zA-Z]+)+\b)@'
            # Directly replace the 'name.name' part with '███' followed by '@'
            content,name_count_temp = re.subn(email_name_name_pattern, '███@', content, flags=re.IGNORECASE)
            file_name_count+=name_count_temp

        
        process_file_stats(file_path,censor_names,file_name_count,censor_address,file_address_count,censor_dates,file_date_count,censor_phones,file_phone_count)
      

    except Exception as e:
        print(f"Error censoring file {file_path}: {e}")
        return None
    

    # return content

    return content

def process_file_stats(file_path,censor_names,file_name_count,censor_address,file_address_count,censor_dates,file_date_count,censor_phones,file_phone_count):
        global total_name_count, total_date_count, total_address_count, total_phone_count
        total_address_count+=file_address_count
        total_phone_count+=file_phone_count
        total_date_count+=file_date_count
        total_name_count+=file_name_count
        try:
            stats_file = "tmp/tempStats.txt"
            # Check if the file exists, create it if not
            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            if not os.path.exists(stats_file):
                with open(stats_file, 'w') as new_stats_file:
                    new_stats_file.write("Censorship Statistics\n")

            with open(stats_file, 'a') as stats_output:
                stats_output.write(f"\nStats for File: {file_path}\n")
                if censor_names:
                    stats_output.write(f"Names Redacted: {file_name_count}\n")
                if censor_dates:
                    stats_output.write(f"Dates Redacted: {file_date_count}\n")
                if censor_address:
                    stats_output.write(f"Addresses Redacted: {file_address_count}\n")
                if censor_phones:
                    stats_output.write(f"Phones Numbers Redacted: {file_phone_count}\n")

        except Exception as e:
            print(f"Error processing stats for file {file_path}: {e}")

def process_total_stats(censor_names, censor_dates, censor_phones, censor_address):
        try:
            stats_file = "tmp/tempStats.txt"
            # Check if the file exists, create it if not
            if not os.path.exists(stats_file):
                with open(stats_file, 'w') as new_stats_file:
                    new_stats_file.write("Censorship Statistics\n")

            with open(stats_file, 'a') as stats_output:
                stats_output.write(f"\nCompiled Statistics\n")
                if censor_names:
                    stats_output.write(f"Total Names Redacted: {total_name_count}\n")
                if censor_dates:
                    stats_output.write(f"Total Dates Redacted: {total_date_count}\n")
                if censor_address:
                    stats_output.write(f"Total Addresses Redacted: {total_address_count}\n")
                if censor_phones:
                    stats_output.write(f"Total Phones Numbers Redacted: {total_phone_count}\n")

        except Exception as e:
            print(f"Error processing Compiled Statistics: {e}")

def print_stats(output_type):
    stats_file = "tmp/tempStats.txt"
    try:
        with open(stats_file, 'r') as stats_output:
            if output_type == "stdout":
                print(stats_output.read())
            elif output_type == "stderr":
                print(stats_output.read(), file=sys.stderr)
            else:
                with open(output_type, 'w') as custom_output_file:
                    custom_output_file.write(stats_output.read())
        os.remove(stats_file)


    except Exception as e:
        print(f"Error printing statistics: {e}")


def process_files(input_pattern, censor_names, censor_dates, censor_phones, censor_address, output_directory,output_type):
    
    input_files = glob.glob(input_pattern)
    if not input_files:
        print(f"No files found matching pattern: {input_pattern}")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_path in input_files:
        output_path = os.path.join(output_directory, os.path.basename(file_path) + '.censored')
        censored_content = censor_file(file_path, censor_names, censor_dates, censor_phones, censor_address)

        with open(output_path, 'w') as output_file:
            output_file.write(censored_content)
    
    process_total_stats(censor_names, censor_dates, censor_phones, censor_address)
    print_stats(output_type)



def main():

    parser = argparse.ArgumentParser(description="Censor sensitive information from plain text documents.")

    parser.add_argument("--input", required=True, help="Input file pattern (e.g., '*.txt')")
    parser.add_argument("--names", action="store_true", help="Censor names")
    parser.add_argument("--dates", action="store_true", help="Censor dates")
    parser.add_argument("--phones", action="store_true", help="Censor phone numbers")
    parser.add_argument("--address", action="store_true", help="Censor addresses")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--stats", choices=["stdout", "stderr"], default="stdout", help="Output statistics to stdout or stderr")

    args = parser.parse_args()

    process_files(args.input, args.names, args.dates, args.phones, args.address, args.output, args.stats)

if __name__ == "__main__":
    main()
