#!/Users/santhoshk/opt/anaconda3/bin/python -tt

import sys
import os

def mimic_dict(filename):
    mimic = {}
    with open(filename, "r") as f:
        lines=f.read().lower().split('\n')

    slines = " ".join(lines)
    all_words=[ w for w in slines.split(' ') if w.isalpha()]

    for i in all_words:
        for j,v in enumerate(all_words):
                if i == v:
                    try:
                        if not i in mimic:
                            mimic[i] = [all_words[j+1]]
                        else:
                            mimic[i].append(all_words[j+1])
                    except:
                        break

    return mimic

def main():
    if len(sys.argv) != 2:
        print ('usage: ./mimic.py file-to-read')
        sys.exit(1)

    dict = mimic_dict(sys.argv[1])
    print (dict)

if __name__ == '__main__':
  main()