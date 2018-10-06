import sys

# borrowed from the pydocs since python3 deprecated the cmp parameter
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





def main():
    #arg1 = data; arg2 = params;
    datafile = sys.argv[1]
    paramsfile = sys.argv[2]

    def mis_compare(x,y):
        return mis[x]-mis[y]

    with open(paramsfile, 'r') as paramsfile:

        mis = dict()

        for param in paramsfile:
            s = param.strip('MIS(')
            s = s.replace(')', '')
            s = s.strip('\n')
            list = s.split('=')
            mis[list[0]] = float(list[1])

    with open(datafile, 'r') as data:
        #organize data in array("S") of arrays('s')
        S = []
        s = []

        for datum in data:
            s = datum.replace('{', '')
            s = s.strip('<')
            s = s.strip('>\n')
            list = s.split('}')
            list.pop()
            list = [i.split(',') for i in list]
            #need to sort
            temp = []
            for i in list:
                temp.append(sorted(i, key=cmp_to_key(mis_compare)))

            S.append(temp)


    print(mis, S)





if __name__ == "__main__":
    main()
