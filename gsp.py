import sys

#*--------------------------------------------------------------------
#           Plugins
#*--------------------------------------------------------------------

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


#*--------------------------------------------------------------------
#           Globals
#*--------------------------------------------------------------------

mis = dict()
S = []
sup = dict()
setI = []
x = []
tcount = 0
allitems = []
chars = []
for i in range(55):
    i=i+33
    chars.append(chr(i))

charMap = dict()
newmis = dict()
revCharMap = dict()

#*--------------------------------------------------------------------
#           Data Preprocessing Functions
#*--------------------------------------------------------------------


def initializeSupDict(canList):
    for i in range(len(canList)):
        char = chars[i]
        sup[char] = 0

def initializeCharMap(nums):
    count = 0
    for i in nums:
        charMap[i] = chars[count]
        count = count+1


def initializeReverseCharMap():

    for i in charMap:
        qval=charMap[i]
        revCharMap[qval] = i

    # revCharMap


#creates a set of seq
def countSup(seq):
    global allitems
    toHashable = []
    for i in seq:
        toHashable+=i
        allitems+=i

    setSeqList = set(toHashable)
    # counting support for all items in a sequence
    for i in setSeqList:
        sup[i]+=1

    return setSeqList

#*--------------------------------------------------------------------
#           Main
#*--------------------------------------------------------------------

def main():
    global tcount, newmis, charMap

    datafile = sys.argv[1]
    paramsfile = sys.argv[2]



    def mis_compare(x,y):
        return newmis[x]-newmis[y]

    #takes (setI, S) and returns i and j items that have supp(j)>mis(i)
    def init_pass(sortedSetI):
        L = []
        count = -1
        count2 = -1

        #find first element with supp
        for i in sortedSetI:
            count+=1
            if (sup[i]/tcount>newmis[i]):
                L.append(i)
                break

        #now append all elements with sup>mis(i)
        for j in sortedSetI:
            count2+=1
            if (count2 <= count):
                continue
            elif((sup[j]/tcount)>=newmis[i]):
                L.append(j)

        return L


#*--------------------------------------------------------------------
#                 Load Data and Params
#*--------------------------------------------------------------------


    with open(paramsfile, 'r') as paramsfile:
        for param in paramsfile:
            s = param.strip('MIS(')
            s = s.replace(' ', '')
            s = s.replace(')', '')
            s = s.strip('\n')
            paramslist = s.split('=')

            ### Initializing MIS
            mis[paramslist[0]] = float(paramslist[1])

    temp = mis.keys()
    #initialize sup[] dict w/ 0s
    initializeCharMap(temp)
    initializeSupDict(temp)
    initializeReverseCharMap()
    for i in mis:
        char=charMap[i]
        newmis[char] = mis[i]

    with open(datafile, 'r') as data:

        for datum in data:

            tcount = tcount+1

            s = datum.replace('{', '')
            s = s.strip('<')
            s = s.strip('>\n')
            s = s.replace(' ','')
            sequence = s.split('}')
            sequence.pop()
            sequence = [i.split(',') for i in sequence]
            for i in range(len(sequence)):
                for j in range(len(sequence[i])):
                    num2replace = sequence[i][j]
                    sequence[i][j] = charMap[num2replace]


            # need to sort
            # think this is the wrong sorting method... need to sort simply the set of all sequences.
            #but now i'm thinking this is needed
            temp2 = []
            for i in sequence:
                temp2.append(sorted(i, key=cmp_to_key(mis_compare)))

            S.append(temp2)

            countSup(sequence)

        fullset = set(allitems)

#*--------------------------------------------------------------------
#           MAIN FUNCTION Cont..
#*--------------------------------------------------------------------

    #at this point we have



    sortedSetI = sorted(fullset, key=cmp_to_key(mis_compare))
    #takes (sortedSetI, S) and returns i and j items that have supp(j)>mis(i)

    Fks = []
    L = init_pass(sortedSetI)
    #print("THIS is L ->", L)
    F1 = generateF1(L)
    # add step to split then pop each element in the string into a hashtable lookup

    #convert int to char

    Fks.append(F1)
    print("This is F1->", F1)
    C2 = level2_candidate_gen(L)
    print("This is C2 ->", C2)
    F2 = generateF2(C2)
    print("This is F2->", F2)
    Fks.append(F2)
    k = 2
    Fk=F2

    while(True):
        k = k +1
        Ck = generateCandidates(k, Fk)
        print("CK", Ck)
        if Ck == []:
            break
        Fk = pruneCk(Ck, k, Fk)
        Fks.append(Fk)




#*--------------------------------------------------------------------
#           OUTPUT TEXTFILE
#*--------------------------------------------------------------------


    with open("output.txt", 'w') as out:
        k = 0
        print("FK-", Fks)

        for i in range(len(Fks)):
            k = k+1
            num = str(k)
            out.write("The number of length "+num+" sequential patterns is "+str(len(Fks[i]))+"\n")
            for j in Fks[i]:
                pattern = j.split(' ')
                pat = ''
                for l in pattern:
                    setNums = ''
                    if len(l) >1:
                        counter = 0
                        for m in l:
                            counter= counter+1
                            setNums = setNums+str(revCharMap[m])
                            if counter == len(l):
                                break
                            setNums=setNums+','

                        pat = pat+'{'+setNums+'}'

                    elif len(l) ==1:
                        pat = pat+'{'+revCharMap[l]+'}'

                out.write("Pattern: <"+pat+"> count:"+str(sup[l])+"\n")

#*--------------------------------------------------------------------

#*-------------------------------------------------


#*--------------------------------------------------------------------
#          CANDIDATE FUNCTIONS
#*--------------------------------------------------------------------

def weirdStuff(joinedC):
    return


def generateCandidates(k, Fk):
    # four scenarios for k = 3:
    # 1) < j k l >
    # 2) < jk l >
    # 3) < j kl >
    # 4) < jkl >

    #do join

    if k == 3:

        joined = joinFkminus1s(F2)
        weirdStuff(joined)
        return joined
    if k > 3:
        joined = joinFkminus1s(Fk)
        return joined

def joinFkminus1s(F):
    joined = []
    print("F=", F)
    for i in F:
        for j in F:
            # #print(i, j)
            cmp1 = i[1:].replace(' ','')
            cmp2 = j[:-1].replace(' ','')
            #print(cmp1, cmp2)
            if cmp1 == cmp2:
                #print("i-",i)
                #print("j-",j)
                if j[-2] == ' ':
                    temp = i+j[-2:]

                #if not separate add as group
                else:
                    temp = i+j[-1]

                #print("temp", temp)
                joined.append(temp)
    return joined

#*--------------------------------------------------------------------
#          PRUNE FUNCTIONS
#*--------------------------------------------------------------------

def pruneCk(Ck, k, F):
    #if all k-1 subsequences are frequent, then it's frequent OR if sequence doesn't have lowest MIS value

    Fk = []
    for i in Ck:
        lowMis = lowestMis(i.replace(' ',''))
        count = 0
        # i = 'a b c'
        for j in range(len(i)):
            if i[j] != ' ':
                temp = i[:j]+i[(j+1):]
                subseq = temp.replace("  ", ' ')
                if(subseq[0]==' '):
                    subseq = subseq[1:]

            #check all subsequence
            print(subseq)
            count = count+checkSub(subseq, F, lowMis)

        #if all subsequences return 0 aka pass their F test then they are Fk
        if count == 0:
            Fk.append(i)
    return(Fk)


def checkSub(sub, F, low):

    #return 0 if subs in Fk-1
    if sub in F:
        return 0

    #return 0 if subs does not contain lowestMis
    count = 0
    for i in sub.replace(' ', ''):
        print("III",i)
        if newmis[i]>low:
            count= count +1
        if count == len(sub):
            print('asdasdf')
            return 0

    return 1

def lowestMis(s):
    lowest = 1
    for i in s:
        lowest = min(lowest, newmis[i])

    return lowest



#is subseqence contained?
def countContained3(c, scount):
    scount = scount +1
    if scount == tcount-1:
        return 0
    for i in range(len(S[scount])):
        # #print("---")
        # #print(S[scount][i])
        if c[0] in S[scount][i]:
            # #print(range(len(S[scount])-i-1))
            for j in range(len(S[scount])-i-1):
                # #print(S[scount][j+i])
                if c[2] in S[scount][j+i+1]:
                    return 1 + countContained3(c, scount)

    return 0 + countContained3(c, scount)

def countContained2(c, scount):
    scount = scount +1
    if scount == tcount-1:
        return 0
    for i in range(len(S[scount])):
        if c[0] in S[scount][i]:
            if c[1] in S[scount][i]:
                if S[scount][i].index(c[0]) < S[scount][i].index(c[1]):
                    return 1 + countContained2(c, scount)
    return 0 + countContained2(c, scount)

C2 = []


#if c.count/n >= MIS(c.minMISitem) -> F
def generateF2(C2):
    for c in C2:
        if len(c) == 3:
            ccount3 = countContained3(c, -1)
            sup[c] = ccount3

            # #print(c, ccount)
        elif len(c) == 2:
            ccount2 = countContained2(c, -1)
            sup[c] = ccount2

    return checkFrequency()

F2 = []
#is c.count/n >= min(mis(c))
def checkFrequency():
    for i in C2:
        for j in i:
            if j != ' ':
                if sup[i]/tcount >= newmis[j]:
                    F2.append(i)
                    break
    return F2

        # if ccount/tcount >= mis(c):
        # elif (ccount/tcount >= mis(c)):


#generate nXn
def level2_candidate_gen(L):


    for i in range(len(L)):
        #sup >= mis
        if (sup[L[i]]/tcount >= newmis[L[i]]):
            for j in range(len(L)):
                #generate <{x} {y}> candidate
                if (sup[L[i]]/tcount >= newmis[L[i]]):
                    C2.append(L[i]+' '+L[j])

                #generate <{x,y}> candidate
                #sup diff <= SDC
                if((sup[L[i]]/tcount-sup[L[j]]/tcount)<=mis["DC"]):
                    C2.append(L[i]+L[j])

    return C2


def generateF1(L):
    F1 = []
    for i in L:
        if ((sup[i]/tcount)>=newmis[i]):
            F1.append(i)
    return F1




if __name__ == "__main__":
    main()
