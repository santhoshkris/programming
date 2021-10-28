#Bank transcation log calculation
mydict={'D':[], 'W':[]}
while True:
    s=input('Enter a log : ')
    if s=='':
        break
    if s.split(' ')[0] == 'D':
        mydict['D'].append(int(s.split(' ')[1]))
    elif s.split(' ')[0] == 'W':
        mydict['W'].append(int(s.split(' ')[1]))
    else:
        pass
print ("Net Amount is {}".format(sum(mydict['D'])-sum(mydict['W'])))
