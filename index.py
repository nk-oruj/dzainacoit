import re
import csv
from collections import defaultdict

pattern_vowels = r'(?:((?<![աէոօեիը])ւ)|(?:[աէոօեիը]+վ(?![աէոօեիը]|$)|[աէոօեիը]+[ւյ]?))' # vowels
pattern_consonants = r'[^\n\sաէոօեիըւ0-9]+' # consonants
pattern_digraphs = r'([^\n\s]{2})' #digraph

allow_overlap = False

def count_unique_matches(text, pattern):
    counts = defaultdict(int)

    for match in re.finditer(pattern, text):
        s = match.group(0)
        counts[s] += 1

    return counts

def run_calculator(file, pattern, output):
    # read the input file
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    # count matches
    results = count_unique_matches(text, pattern)

    # sort by frequency descending
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # write csv file
    with open(output, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["string", "count"])  # header row
        for substring, count in sorted_results:
            writer.writerow([substring, count])

    print(f"dataset of {file} written to: {output}")

def collect_unique_words(input_files, output_file):
    unique_words = set()
    pattern_junk = re.compile(r"[-՝՛*\",0-9]")

    for file in input_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                words = line.split()
                for word in words:
                    if pattern_junk.search(word):
                        continue
                    unique_words.add(word)

    sorted_words = sorted(unique_words)

    with open(output_file, "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")

def replace_substring_in_wordlist(input_file, output_file, old, new):
    with open(input_file, "r", encoding="utf-8") as f:
        words = f.readlines()

    with open(output_file, "w", encoding="utf-8") as f:
        for word in words:
            word = word.strip()
            updated = word.replace(old, new)
            f.write(updated + "\n")

if __name__ == "__main__":
    run_calculator("./wordlists/bible.txt", pattern_vowels, "./statistics/vowels/bible.csv")
    run_calculator("./wordlists/bible.txt", pattern_consonants, "./statistics/consonants/bible.csv")
    run_calculator("./wordlists/bible.txt", pattern_digraphs, "./statistics/digraphs/bible.csv")

    run_calculator("./wordlists/dictionary.txt", pattern_vowels, "./statistics/vowels/dictionary.csv")
    run_calculator("./wordlists/dictionary.txt", pattern_consonants, "./statistics/consonants/dictionary.csv")
    run_calculator("./wordlists/dictionary.txt", pattern_digraphs, "./statistics/digraphs/dictionary.csv")

    run_calculator("./wordlists/gold_age.txt", pattern_vowels, "./statistics/vowels/gold_age.csv")
    run_calculator("./wordlists/gold_age.txt", pattern_consonants, "./statistics/consonants/gold_age.csv")
    run_calculator("./wordlists/gold_age.txt", pattern_digraphs, "./statistics/digraphs/gold_age.csv")

    collect_unique_words(["./wordlists/bible.txt", "./wordlists/dictionary.txt", "./wordlists/gold_age.txt"], "./wordlists/total_list.txt")
   
    run_calculator("./wordlists/total_list.txt", pattern_vowels, "./statistics/vowels/total_list.csv")
    run_calculator("./wordlists/total_list.txt", pattern_consonants, "./statistics/consonants/total_list.csv")
    run_calculator("./wordlists/total_list.txt", pattern_digraphs, "./statistics/digraphs/total_list.csv")

    replace_substring_in_wordlist("./wordlists/total_list.txt", "./wordlists/total_list_no_o.txt", "օ", "աւ")

    run_calculator("./wordlists/total_list_no_o.txt", pattern_vowels, "./statistics/vowels/total_list_no_o.csv")
    run_calculator("./wordlists/total_list_no_o.txt", pattern_consonants, "./statistics/consonants/total_list_no_o.csv")
    run_calculator("./wordlists/total_list_no_o.txt", pattern_digraphs, "./statistics/digraphs/total_list_no_o.csv")