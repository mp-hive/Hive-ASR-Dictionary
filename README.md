# Hive ASR Dictionary
 The Hive ASR Dictionary is a growing library of common ASR-mistakes and corrections of common Hive-specific terms + a Python script to scrub txt- and srt files.
 
 Its purpose is to enhance the data quality of automatically transcribed Hive-related videos.

# Usage
- If you run replaceTriggers.py without arguments, you will be prompted to confirm that you want to replace all keywords in triggers.db recursively (meaning all files in the current folder and its subfolders) for any .txt and .srt file present.
- You can also run it on a specific file by using the argument -f (example: replaceTrigger.py -f filename)

# Functionality and the structure of 'triggers.db'
The script will only match and replace the words listed before the "=" sign if they're matched exactly as standalone words. 

Examples from 'triggers.db':
```
block trades=Blocktrades
decentralized high-fund=Decentralized Hive Fund
Splinterland=Splinterlands
```

If we use the last line as an example, the script would replace any occurence of the word 'Splinterland' with 'Splinterlands', but it would NOT replace it if that phrase was part of a word (i.e. it wouldn't identify the phrase "Splinterland" within the word  "Splinterlands", producing the erroneous result "Splinterlandss".