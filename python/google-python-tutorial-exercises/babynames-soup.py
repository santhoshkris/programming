#!/Users/santhoshk/opt/anaconda3/bin/python -tt

import sys
import os
import re
import lxml
import bs4
from bs4 import BeautifulSoup

def cust_sort(data):
	s=data.split(' ')
	return s[1]

def summary_babynames(filename):
	file_contents = []
	final_list = []
	sorted_final_list = []

	with open(filename,'r') as f:
		file_contents = f.read()
	soup = BeautifulSoup(file_contents, 'lxml')
	year = soup.h3.text.split(' ')[2]
	# final_list.append(year)
	# print (final_list)
	rs = soup.find_all('table')[2]
	rs_list = [s for s in rs.stripped_strings]
	rs_list.pop(0)
	rs_list.pop(0)
	rs_list.pop(0)
	rs_list.pop()
	rank_list = rs_list[::3]
	male_name_list = rs_list[1::3]
	female_name_list = rs_list[2::3]
	for r, m, f in zip(rank_list, male_name_list, female_name_list):
		# print ( r, m, f)
		final_list.append(r + ' ' + m)
		final_list.append(r + ' ' + f)
	# final_list.pop(0)
	# print (final_list)
	sorted_final_list=sorted(final_list, key=cust_sort)
	sorted_final_list.insert(0, year)
	return (sorted_final_list)


def main():
	args = sys.argv[1:]

	if not args:
		print ('usage: [--summaryfile] file')
		sys.exit(1)
	if args[0] == '--summaryfile':
		del args[0]
	filename = args[0]
	os.system('clear')
	mylist = summary_babynames(filename)
	print ("Final list of 'Ranking' and 'Names' : ")
	print (mylist)

if __name__ == '__main__':
	main()

