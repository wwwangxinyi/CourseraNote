import re
str_test="15678324.234638"
str_int_rev=result=""
lst=[]
i=0
str_int_rev=str_test.split(".")[0][::-1]
while i < len(str_int_rev):
    lst.append(str_int_rev[i:i+3])
    i+=3
result=",".join(lst)[::-1]+"."+str_test.split(".")[-1]
print(result)