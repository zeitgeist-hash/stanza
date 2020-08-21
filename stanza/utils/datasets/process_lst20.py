"""Processes the tokenization section of the LST20 Thai dataset

The dataset is available here:

https://aiforthai.in.th/corpus.php


python3 -m stanza.utils.datasets.process_lst20 extern_data/thai/LST20_Corpus data/tokenize

Unlike Orchid and BEST, LST20 has train/eval/test splits, which we relabel train/dev/test.

./scripts/run_tokenize.sh UD_Thai-lst20 --dropout 0.05 --unit_dropout 0.05
"""


import glob
import os
import sys

from pythainlp import sent_tokenize

from stanza.utils.datasets.process_thai_tokenization import write_section, convert_processed_lines, reprocess_lines

def read_data(input_dir, section):
    input_dir = os.path.join(input_dir, section)
    filenames = glob.glob(os.path.join(input_dir, "*.txt"))
    documents = []
    for filename in filenames:
        lines = open(filename).readlines()
        processed_lines = []
        sentence = []
        for line in lines:
            line = line.strip()
            if not line:
                if sentence:
                    processed_lines.append(sentence)
                    sentence = []
            else:
                pieces = line.split("\t")
                if pieces[0] == '_':
                    sentence.append(' ')
                else:
                    sentence.append(pieces[0])
        if sentence:
            processed_lines.append(sentence)

        processed_lines = reprocess_lines(processed_lines)
        paragraphs = convert_processed_lines(processed_lines)

        documents.extend(paragraphs)
    return documents

def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    for (in_section, out_section) in (("train", "train"),
                                      ("eval", "dev"),
                                      ("test", "test")):
        documents = read_data(input_dir, in_section)
        write_section(output_dir, "lst20", out_section, documents)


if __name__ == '__main__':
    main()
