#!/usr/bin/env python3

import os
import re
from datetime import datetime
import argparse  # Import the argparse module

def load_triggers(filepath):
    triggers = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split('=')
            if len(parts) == 2:
                trigger_regex = r'\b' + re.escape(parts[0]) + r'\b'
                triggers[trigger_regex] = parts[1]
    return triggers

def log_and_print(log_file, message):
    print(message)
    log_file.write(message + '\n')

def replace_phrases_in_file(filepath, triggers, log_file):
    with open(filepath, 'r', encoding='utf-8') as file:
        contents = file.read()
    
    total_replacements = 0
    for trigger_regex, replacement in triggers.items():
        contents, replacements_count = re.subn(trigger_regex, replacement, contents)
        total_replacements += replacements_count
        if replacements_count > 0:
            trigger_word = trigger_regex.strip(r'\b')
            log_and_print(log_file, f'Replaced in {filepath} {replacements_count} instances of "{trigger_word}" with "{replacement}"')
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(contents)
    
    return total_replacements

def process_files(directory, triggers, triggers_filename, log_file_path, log_file):
    total_replacements = 0
    if os.path.isfile(directory):  # If a specific file is provided
        filepath = directory
        if filepath != log_file_path and filepath != triggers_filename:
            replacements = replace_phrases_in_file(filepath, triggers, log_file)
            total_replacements += replacements
    else:  # Recursive directory processing
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename == triggers_filename or filename.startswith('replacement_log_'):
                    continue
                if filename.endswith(('.srt', '.txt')):
                    filepath = os.path.join(root, filename)
                    if filepath == log_file_path:
                        continue
                    replacements = replace_phrases_in_file(filepath, triggers, log_file)
                    total_replacements += replacements
    return total_replacements

def main():
    parser = argparse.ArgumentParser(description='Replace phrases in text files.')
    parser.add_argument('-f', '--file', help='Specify a single file for processing.', required=False)
    args = parser.parse_args()

    # Prompt for confirmation if no file is specified for recursive operation
    if not args.file:
        response = input("This will recursively replace phrases in all .srt and .txt files in the current directory and subdirectories. Are you sure? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return

    triggers_filename = '/home/mp/summarizer/triggers.db'
    triggers_file = triggers_filename
    triggers = load_triggers(triggers_file)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    log_filename = f'replacement_log_{timestamp}.log'
    log_file_path = os.path.join(os.getcwd(), log_filename)  
    
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        if args.file:
            directory_or_file = args.file
        else:
            directory_or_file = '.'
        total_replacements = process_files(directory_or_file, triggers, triggers_filename, log_file_path, log_file)
        summary = f'\nTotal replacements made: {total_replacements}\nTimestamp: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
        log_and_print(log_file, summary)

if __name__ == '__main__':
    main()
