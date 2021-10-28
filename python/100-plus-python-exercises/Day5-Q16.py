# nums=(input("Enter ',' separated numbers: ").split(','))
out_list=[str(int(n)**2) for n in input("Enter ',' separated numbers: ").split(',') if int(n)%2!=0]
print(','.join(out_list))