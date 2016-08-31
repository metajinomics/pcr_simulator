#this scrip gives pcr product from given primers 
#usage: python get_pcr_product.py primers geneseq.fa

import sys
import reverse_complement
import re
def get_product(pri,se,name):
    product = ''
    psize = 0
    fpri = ''
    rpri = ''
    for x in pri.items():
        if(x[0] in se):
            temseq = se[se.find(x[0]):se.find(x[0])+400]
            #print se.find(x[0])
            for y in pri.items():
                if(y[0] in temseq and y[0] != x[0]):
                    psize = temseq.find(y[0])+len(y[0])
                    product = temseq[:temseq.find(y[0])+len(y[0])]
                    fpri = x[0]
                    rpri = reverse_complement.get_rc(y[0])
                    print fpri, rpri, psize, product, name
    return fpri, rpri, psize, product

def find_product(pri,seqs):
    name = ''
    flag = 0
    seq =[]
    for line in seqs:
        if(line[:1] == ">" and flag == 0):
            name = line.strip()
            flag = 1
        elif(line[:1] == ">" and flag == 1):
            se = ''.join(seq)
            get_product(pri,se,name)
            name = line.strip()
            seq = []
        else:
            seq.append(line.strip())
    se = ''.join(seq)
    get_product(pri,se,name)
        
def read_primer(prim):
    swi = 0
    pri = {} 
    name = ""
    for line in prim:
        if(line[:2] == ">F"):
            swi = 0
            name = line.strip()[1:]
        elif(line[:2] == ">R"):
            swi = 1
            name = line.strip()[1:]
        else:
            if(swi == 0):
                if not(pri.has_key(line.strip())):
                    pri[line.strip()] = name
                else:
                    temp = pri[line.strip()] +','+name
                    pri[line.strip()] = temp
            else:
                seq = reverse_complement.get_rc(line.strip())
                if not(pri.has_key(seq)):
                    pri[seq] = name
                else:
                    temp = pri[seq] +','+name
                    pri[seq] =temp
    return pri
            
def main():
    #read primer
    prim = open(sys.argv[1],'r')
    seqs = open(sys.argv[2],'r')
    pri = read_primer(prim)
    
    #find product
    find_product(pri,seqs)

if __name__ == '__main__':
    main()
