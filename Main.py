import math
import operator
from Node import *
def readExel(exelname):
    import xlrd

    ExcelFileName= exelname
    workbook = xlrd.open_workbook(ExcelFileName)
    worksheet = workbook.sheet_by_name("Data")

    num_rows = worksheet.nrows  #Number of Rows
    num_cols = worksheet.ncols  #Number of Columns

    result_data =[]
    for curr_row in range(2,num_rows): # read except header
        row_data = []

        for curr_col in range(1, num_cols): # read except ID
            data = worksheet.cell_value(curr_row, curr_col) # Read the data in the current cell
            # print(data)
            row_data.append(data)

        result_data.append(row_data)
    print("read done")
    # print(result_data[0].__len__())
    return result_data
def I(n):
    n=list(n)
    info=0
    for i in n :
        if(i==0):
            info=0
            break
        pi=i/sum(n)
        info-=pi*math.log(pi,2)

    return info
def createAnode(data,layer,header,node,parent):
    print(header.__len__(),header)
    if not data :
        return
    print(data[0].__len__())

    minn = list(map(min, zip(*data)))
    maxx = list(map(max, zip(*data)))

    # print(maxx)
    # print(minn)

    ans = []
    for i in data:
        ans.append(int(i[(i.__len__() - 1)]))

    infoE = I([ans.count(0),ans.count(1)])

    sd=[]
    for i in range(maxx.__len__()):
        tmp= (maxx[i] - minn[i]) / 3
        sd.append(tmp)
    # print(sd)

    infoN=[]
    # sum(i > 0 for i in tmp)
    pnall=[]


    for i in header:
        tmp = []
        for j in range(data.__len__()):
            tmp.append(data[j][i])

        pn=[[0,0],[0,0],[0,0]]
        for j in range(tmp.__len__()):
            for k in range(pn.__len__()):
                if((minn[i] + (k * sd[i]))<=tmp[j]<(minn[i] + (k + 1) * sd[i])):
                    if(ans[j]==1):
                        pn[k][0]+=1
                    elif(ans[j]==0):
                        pn[k][1]+=1
            if(tmp[j]==maxx[i]):
                if(ans[j]==1):
                    pn[k][0]+=1
                elif(ans[j]==0):
                    pn[k][1]+=1
        # print(pn)
        pnall.append(pn)
        # print(i,sum(pn[0])+sum(pn[1])+sum(pn[2]))
        #
        # break
        attr=0
        for j in range(pn.__len__()):

            if(pn[j][0]+pn[j][1]>0):
                attr+= ((pn[j][0]+pn[j][1])/data.__len__())*I(pn[j])
        infoN.append(attr)

    # print("Info Expected",infoE)
    # print("Info each",infoN)

    gain=[]
    for i in infoN:
        gain.append(infoE-i)

    index, value = max(enumerate(gain), key=operator.itemgetter(1))
    print("index",index)
    print("HEAD",header[index])
    print(pnall[index])

    tree.append([])
    tree[layer].append(Node(header.pop(index),minn[index],sd[index],pnall[index]))
    if(parent!=None):
        parent.add_child(tree[layer][tree[layer].__len__()-1])
    # if(layer>0):
    #     for node in range(tree[layer].__len__()):
    #         tree[layer-1][0].add_child(tree[layer][node])

    datac=[]
    for i in range(3):
        datac.append([])
        if(i<2):
            datac[i] = [v for v in data if tree[layer][node].minn+(i)*tree[layer][node].sd<=v[index] < tree[layer][node].minn+(i+1)*tree[layer][node].sd ]
        else:
            datac[i] = [v for v in data if tree[layer][node].minn+(i)*tree[layer][node].sd<=v[index] <=tree[layer][node].minn+(i+1)*tree[layer][node].sd]

    for i in range(pnall[index].__len__()):
        if(pnall[index][i][0] and pnall[index][i][1] !=0):
            if(layer<3):
                tree[layer][tree[layer].__len__()-1].choice.append(i)
            else:
                tree[layer][tree[layer].__len__()-1].choice.append(bool(pnall[index][i][0]>pnall[index][i][1]))
        else:
            tree[layer][tree[layer].__len__()-1].choice.append(bool(pnall[index][i][0]>pnall[index][i][1]))

    layer+=1

    if(layer<5):
        for i in range(pnall[index].__len__()):
            if(type(tree[layer-1][tree[layer-1].__len__()-1].choice[i]) is int):
                createAnode(datac[i],layer,header,i,tree[layer-1][tree[layer-1].__len__()-1])

            # for j in range(datac.__len__()):
            #     if(j==i):
            #         break
            #     for k in range(datac[j].__len__()):
            #         datac[j][k].pop(index)



    # for i in range(pnall.__len__()):
    #     if pnall[i][0] and pnall[i][1] != 0 :
    #         createAnode(datac[i],layer,header,i)
    #         if(i<datac.__len__()-1):
    #             for j in range(datac[i+1].__len__()):
    #                 datac[i+1][j].pop(index)
    return index

data = readExel('data.xls')
tree = []
header=[]
for i in range(data[0].__len__()-1):
    header.append(i)
print(data[0].__len__()-1)

createAnode(data,0,header,0,None)

print(tree)
for i in tree:
    for j in i:
        print(j.attr,end=" ")
    if i:
        print()

for i in tree:
    for j in i:
        if(j.choice==None):
            print(j.attr,end=" ")
        else:
            print(j.choice,end=" ")
    if i:
        print()

tree[0][0]
str(tree[0][0])
print(tree[0][0])

for layer in tree:
    for node in layer:
        node.filloutput()


tree[0][0]
str(tree[0][0])
print(tree[0][0])