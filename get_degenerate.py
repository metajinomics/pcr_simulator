#!/usr/bin/python
#usage: python get_degenerate.py input > output
#input file need to be in fasta format looks like below
#>name
#ATAGATGT
import sys
def add_normal(dict,bp):
    if (len(dict)==0):
        dict[0]=[]
    for x in dict.items():
        temp = x[1][:]
        temp.append(bp)
        dict[x[0]] = temp[:]
    return dict

def add_two(dict,bp1,bp2):
    if (len(dict)==0):
        dict[0]=[]
    for x in dict.items():
        temp1 = x[1][:]
        temp2 = x[1][:]
        temp1.append(bp1)
        temp2.append(bp2)
        dict[x[0]] = temp1[:]
        dict[len(dict)] = temp2[:]
    return dict

def add_three(dict,bp1,bp2,bp3):
    if (len(dict)==0):
        dict[0]=[]
    for x in dict.items():
        temp1 = x[1][:]
        temp2 = x[1][:]
        temp3 = x[1][:]
        temp1.append(bp1)
        temp2.append(bp2)
        temp3.append(bp3)
        dict[x[0]] = temp1[:]
        dict[len(dict)] = temp2[:]
        dict[len(dict)+1] = temp3[:]
    return dict

def add_N(dict):
    if (len(dict)==0):
        dict[0]=[]
    for x in dict.items():
        tempA = x[1][:]
        tempC = x[1][:]
        tempG = x[1][:]
        tempT = x[1][:]
        tempA.append("A")
        tempC.append("C")
        tempG.append("G")
        tempT.append("T")
        dict[x[0]] = tempA[:]
        dict[len(dict)] = tempC[:]
        dict[len(dict)+1] = tempG[:]
        dict[len(dict)+2] = tempT[:]
    return dict

def main():
    fread = open(sys.argv[1],'r')
    for line in fread:
        if (line[:1] == ">"):
            ids = line.strip()
            line = fread.next()
            dict = {}
            for x in line.strip().upper():
                if(x =="A" or x=="G" or x=="C" or x=="T"):
                    dict = add_normal(dict,x)
                #this is IUPAC
                elif(x == "R"):
                    dict = add_two(dict,"A","G")
                elif(x == "Y"):
                    dict = add_two(dict,"C","T")
                elif(x == "M"):
                    dict = add_two(dict,"A","C")
                elif(x == "K"):
                    dict = add_two(dict,"G","T")
                elif(x == "S"):
                    dict = add_two(dict,"C","G")
                elif(x == "W"):
                    dict = add_two(dict,"A","T")
                elif(x == "H"):
                    dict = add_three(dict,"A","C","T")
                elif(x == "B"):
                    dict = add_three(dict,"C","G","T")
                elif(x == "V"):
                    dict = add_three(dict,"A","C","G")
                elif(x == "D"):
                    dict = add_three(dict,"A","G","T")
                elif(x == "N"):
                    dict = add_N(dict)
                #this is for RNA
                elif(x == "I"):
                    dict = add_three(dict,"A","C","T")
                else:
                    print "unkwon chractor",x
            for x in dict.items():
                name = [ids,"_",str(x[0])]
                print "".join(name)
                print "".join(x[1])
                
if __name__ == '__main__':
    main()
