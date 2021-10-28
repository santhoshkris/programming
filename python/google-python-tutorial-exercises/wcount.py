#!/Users/santhoshk/opt/anaconda3/bin/python -tt

from collections import Counter
import sys
import os


def print_words(filename):
	word_count={}
	lines=[]

	with open(filename, "r") as f:
		lines=f.read().lower().split('\n')

	slines = " ".join(lines)
	all_words=[ w for w in slines.split(' ') if w.isalpha()]
	# print ('All words now are: ',all_words)
	#uniq_words = set(all_words)
	c = Counter(all_words)
	# print (f'Counter values: {c}')
	print (f"\nWord count in file: '{filename}'\n")
	for i,num in c.items():
 		print (f'Word : {i}, Count: {num}')
	# for i in uniq_words:
	# 	if i.isalpha():
	# 		word_count[i] = all_words.count(i)
	# 		#print ("Word: {} Count: {}".format(i,slines.count(i)))
	# 	else:
	# 		pass
	# #print (word_count, len(word_count.keys()))

	# for i,v in sorted(word_count.items()):
	# 	print (f"Word '{i}' : Count '{v}'")

def print_top(filename):
	word_count={}
	lines=[]

	with open(filename, "r") as f:
		lines=f.read().lower().split('\n')

	slines = " ".join(lines)
	all_words=[ w for w in slines.split(' ') if w.isalpha()]
	# print ('All words now are: ',all_words)
	#uniq_words = set(all_words)
	c = Counter(all_words)
	# print (f'Counter values: {c}')
	print (f"\n10 Top Word count in file: '{filename}'\n")
	# print (c.most_common(10))
	for w, n in c.most_common(10):
		print (f"Word '{w}', Count {n}")
	# for i in uniq_words:
	# 	if i.isalpha():
	# 		word_count[i] = all_words.count(i)
	# 		#print ("Word: {} Count: {}".format(i,slines.count(i)))
	# 	else:
	# 		pass
	# #print (word_count, len(word_count.keys()))

	# for i,v in sorted(word_count.items()):
	# 	print (f"Word '{i}' : Count '{v}'")


def main():

	if len(sys.argv) != 3:
   		print ('usage: ./wcount.py {--count | --topcount} file')
   		sys.exit(1)

	option = sys.argv[1]
	filename = sys.argv[2]

	if option == '--count':
		os.system('clear')
		print_words(filename)
	elif option == '--topcount':
		print_top(filename)
	else:
		print ('unknown option: ' + option )
		print ('usage: ./wcount.py {--count | --topcount} file')
		sys.exit(1)
	print ('\nEnd of it...\n')

if __name__ == '__main__':
  main()


