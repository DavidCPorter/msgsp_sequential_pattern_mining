import sys

# borrowed from the pydocs since python3 deprecated the sorted() cmp parameter
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

mis = dict()
S = []
sup = dict()
setI = []
x = []
tcount = 0

def initializeFreqDict(canList):
    for i in canList:
        sup[i] = 0

def countFreq(canList):
    return


def main():
    global tcount

    #arg1 = data; arg2 = params;
    datafile = sys.argv[1]
    paramsfile = sys.argv[2]

    def mis_compare(x,y):
        return mis[x]-mis[y]

    with open(paramsfile, 'r') as paramsfile:
        for param in paramsfile:
            s = param.strip('MIS(')
            s = s.replace(')', '')
            s = s.strip('\n')
            list = s.split('=')
            mis[list[0]] = float(list[1])

    temp = mis.keys()
    initializeFreqDict(temp)

    with open(datafile, 'r') as data:
        allitems = []

        for datum in data:

            tcount = tcount+1

            s = datum.replace('{', '')
            s = s.strip('<')
            s = s.strip('>\n')
            list = s.split('}')
            list.pop()
            list = [i.split(',') for i in list]

            # need to sort
            # think this is the wrong sorting method... need to sort simply the set of all sequences.
            #but now i'm thinking this is needed
            temp2 = []
            for i in list:
                temp2.append(sorted(i, key=cmp_to_key(mis_compare)))

            S.append(temp2)

            seqlist = []
            #create setI
            for i in list:
                seqlist+=i
                allitems+=i


            setSeqList = set(seqlist)

            for i in setSeqList:
                sup[i]+=1

        setI = set(allitems)

    print(mis)
    print(sup)
    sortedSetI = sorted(setI, key=cmp_to_key(mis_compare))
    print("This is sortedSetI ->", sortedSetI)
    #takes (sortedSetI, S) and returns i and j items that have supp(j)>mis(i)
    L = init_pass(sortedSetI)
    print("THIS is L ->", L)
    F1 = generateF1(L)
    print("This is F1->", F1)



def generateF1(L):
    F1 = []
    for i in L:
        if ((sup[i]/tcount)>=mis[i]):
            F1.append(i)
    return F1


#takes (setI, S) and returns i and j items that have supp(j)>mis(i)
def init_pass(sortedSetI):
    L = []
    count = -1
    count2 = -1

    #find first element with supp
    for i in sortedSetI:
        count+=1
        if (sup[i]/tcount>mis[i]):
            L.append(i)
            break

    #now append all elements with sup>mis(i)
    for j in sortedSetI:
        count2+=1
        if (count2 <= count):
            continue
        elif((sup[j]/tcount)>=mis[i]):
            L.append(j)

    return L


if __name__ == "__main__":
    main()
