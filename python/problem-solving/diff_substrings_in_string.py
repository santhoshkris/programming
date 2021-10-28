# Python 3 program to find number of 
# different sub stings 

# function to return number of different 
# sub-strings 
def numberOfDifferentSubstrings(s, a, b): 

	# initially our answer is zero. 
	ans = 0

	# find the length of given strings 
	ls = len(s) 
	la = len(a) 
	lb = len(b) 

	# currently make array and initially 
	# put zero. 
	x = [0] * ls 
	y = [0] * ls 

	# find occurrence of "a" and "b" in string "s" 
	for i in range(ls): 
		
		if (s[i: la + i] == a): 
			x[i] = 1
		if (s[i: lb + i] == b): 
			y[i] = 1

	# We use a hash to make sure that same 
	# substring is not counted twice. 
	hash = [] 

	# go through all the positions to find 
	# occurrence of "a" first. 
	curr_substr = "" 
	for i in range(ls): 
	
		# if we found occurrence of "a". 
		if (x[i]): 
		
			# then go through all the positions 
			# to find occurrence of "b". 
			for j in range( i, ls): 
			
				# if we do found "b" at index 
				# j then add it to already 
				# existed substring. 
				if (not y[j]): 
					curr_substr += s[j] 

				# if we found occurrence of "b". 
				if (y[j]): 
				
					# now add string "b" to 
					# already existed substing. 
				
					curr_substr += s[j: lb + j] 
					
					# If current substring is not 
					# included already. 
					if curr_substr not in hash: 
						ans += 1

					# put any non negative integer 
					# to make this string as already 
					# existed. 
					hash.append(curr_substr)

			# make substring null. 
			curr_substr = "" 
	# return answer. 
	return hash,ans 

# Driver Code 
if __name__ == "__main__": 
	
	s = "malayalam"
	begin = "a"
	end = "a"
	print(numberOfDifferentSubstrings(s, begin, end)) 

# This code is contributed by ita_c 
