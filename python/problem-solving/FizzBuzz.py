n=15
res = ""
for i in range(1,n+1):
    if i%3==0 and i%5==0:
        res+="fizzbuzz"
    elif i%3==0:
        res+='fizz'
    elif i%5==0:
        res+='buzz'
    else:
        res+=str(i)
print(res)