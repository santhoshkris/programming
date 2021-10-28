bin_nums=[str(int(s,2)) for s in (input("enter ',' separated bin values: ").split(',')) if int(s,2)%5==0]
# div_five=[str(x) for x in bin_nums if x%5==0]
print(','.join(bin_nums))
