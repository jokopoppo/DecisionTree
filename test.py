a=[1,1,1,1,1,1,1,1]
print(a.__len__())

for i in range(a.__len__()):
    print(i)
    a.pop(i)
