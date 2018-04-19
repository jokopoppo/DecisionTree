import math
import operator
import random
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
    # find the information gain
    n=list(n)
    info=0
    for i in n :
        if(i==0):
            info=0
            break
        pi=i/sum(n)
        info-=pi*math.log(pi,2)

    return info
def createAnode(n,data,layer,header,node,parent):

    print(header.__len__(),header)
    if not data :
        return

    minn = list(map(min, zip(*data)))
    maxx = list(map(max, zip(*data)))


    ans = []
    for i in data:
        ans.append(int(i[(i.__len__() - 1)]))
    # find entropy

    infoE = I([ans.count(0),ans.count(1)])

    # divided the attribute to n class
    sd=[]
    for i in range(maxx.__len__()):
        tmp= (maxx[i] - minn[i]) / n
        sd.append(tmp)


    infoN=[]

    pnall=[]

    # find information gain of each attribute
    for i in header:
        tmp = []
        for j in range(data.__len__()):
            tmp.append(data[j][i])

        pn=[]
        for j in range(n):
            pn.append([0,0])
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

        pnall.append(pn)

        attr=0
        for j in range(pn.__len__()):

            if(pn[j][0]+pn[j][1]>0):
                attr+= ((pn[j][0]+pn[j][1])/data.__len__())*I(pn[j])
        infoN.append(attr)


    # find information gain of all attribute that left
    gain=[]
    for i in infoN:
        gain.append(infoE-i)


    index, value = max(enumerate(gain), key=operator.itemgetter(1))

    #  the winner will be a node this round
    tree.append([])
    tree[layer].append(Node(header.pop(index),minn[index],sd[index],pnall[index]))

    if(parent!=None):
        parent.add_child(tree[layer][tree[layer].__len__()-1])

    datac=[]
    # copy the others data for find next node
    for i in range(n):
        datac.append([])

        if(i<n-1):
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

    # if still has attributes go find next node
    if(header):
        for i in range(pnall[index].__len__()):
            if(type(tree[layer-1][tree[layer-1].__len__()-1].choice[i]) is int):
                createAnode(n,datac[i],layer,header,i,tree[layer-1][tree[layer-1].__len__()-1])

    return index

# read data from excel
data = readExel('data.xls')

# divided data in to 10 box
percent=int(data.__len__()*10/100)
random.shuffle(data)
# shuffle data
dat=[]

for i in range(10):
    dat.append(data[i*percent:(i+1)*percent])

forest=[]
acc=[]
# loop for train each box of data
for box in range(dat.__len__()):
    tree = []
    header=[]

    # index of Attribute in data
    for i in range(data[0].__len__()-1):
        header.append(i)

    # set data train from 9 boxs and data test from 1 box

    datatrain=[]
    datatest=dat[box]

    for i in range(dat.__len__()):
        if(i!=box):
            datatrain+=dat[i]
    # shuffle data in data train
    random.shuffle(datatrain)

    # recursive to create a tree node by node
    createAnode(2,datatrain,0,header,0,None)


    # fill the output of leaf node in tree
    for layer in tree:
        for node in layer:
            node.filloutput()


    for layer in range(tree.__len__()-1,-1,-1):
        if(not tree[layer]):
            tree.pop(layer)
        else:
            for i in range(tree[layer].__len__()-1,-1,-1):
                if(tree[layer][i]==None):
                    tree[layer].pop(i)

    tree[0][0]
    str(tree[0][0])
    print(tree[0][0])

    root = tree[0][0]
    c=0
    n=0

    # start to test the tree by data test
    # let the tuple run pass the path in tree
    for i in datatest:

        root=tree[0][0]
        n+=1
        for layer in range(tree.__len__()):
            # print("layer",layer)
            for j in range(root.value.__len__()):
                if(j<root.value.__len__()-1):
                    if root.value[j]-root.sd<=i[root.attr]<root.value[j]:
                        if(root.child[j] != None):
                            root=root.child[j]
                        else:
                            # print(i[i.__len__()-1],root.choice[j])
                            if(i[i.__len__()-1] == 0 and root.choice[j] == False):
                                c+=1
                            elif(i[i.__len__()-1] == 1 and root.choice[j] == True):
                                c+=1
                        layer=tree.__len__()
                        break
                else:
                    if root.value[j]-root.sd<=i[root.attr]<=root.value[j]:
                        if(root.child[j] != None):
                            root=root.child[j]
                        else:
                            # print(i[i.__len__()-1],root.choice[j])
                            if(i[i.__len__()-1] == 0 and root.choice[j] == False):
                                c+=1
                            elif(i[i.__len__()-1] == 1 and root.choice[j] == True):
                                c+=1
                        layer=tree.__len__()
                        break
    print(n,c)
    print(header)
    acc.append(c)

    # keep a tree in forest to find the best tree
    forest.append(tree)

# find mean of accuracy of all 10 tree
print(acc)
accurancy=((sum(acc)/acc.__len__())/datatest.__len__())*100
index, value = max(enumerate(acc), key=operator.itemgetter(1))
print("Tree",index,", Acc :",(value/datatest.__len__())*100,"%")
print("Accuracy = ",accurancy,"%")
print(forest[index][0][0])