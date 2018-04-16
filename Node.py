class Node:


    def __init__(self,attr,min,sd,pn=[]):


        self.attr=attr
        self.child=[]
        self.sd=sd
        self.minn=min
        self.choice=[]
        self.pn=pn
        self.value=[]
        for i in range(self.pn.__len__()):
            self.value.append(min+((i+1)*sd))

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.attr)+":"+repr(self.choice)+"\n"
        for child in self.child:
            if child != None:
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

    def add_child(self ,obj):

        self.child.append(obj)

        return

    def filloutput(self):
        while(self.child.__len__()<3):
            self.child.append(None)
        for i in range(self.choice.__len__()) :
            if type(self.choice[i]) != bool and self.child[i]== None :
                self.choice[i]= bool(self.pn[0]>self.pn[1])

