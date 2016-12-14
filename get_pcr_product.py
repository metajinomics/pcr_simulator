#!/usr/bin/python

#this scrip gives pcr product from given primers 
#usage: python get_pcr_product.py primers geneseq.fa
#example: python get_pcr_product.py 16s.full.primers.txt eskape.16s.fa > pcr_product.fa

import sys
import reverse_complement
import re
import gzip

def get_product(fpri,rpri,se,name):
    product = ''
    psize = 0
    pfpri = ''
    prpri = ''
    for x in fpri.items():
        ma = [m.start() for m in re.finditer(x[0], se)]
        if len(ma) > 0:
            for st in ma:
                tempseq = se[st:st+400]
                for y in rpri.items():
                    rma = [m.start() for m in re.finditer(y[0],tempseq)]
                    if len(rma) > 0 :
                        for rst in rma:
                            product = tempseq[:rst+len(y[0])]
                            psize = len(product)
                            pfpri = x[0]
                            prpri = y[0]
                            print ">%s %s(%s) %s %s(%s) %s %s\n%s" %(name, pfpri,fpri[pfpri],st, reverse_complement.get_rc(prpri),rpri[prpri],st+rst+len(y[0]),len(product), product)
    return 0

def find_product(fpri,rpri,file):
    if file[-2:] == 'gz':
        seqs = gzip.open(file,'r')
    else:
        seqs = open(file,'r')
    name = ''
    flag = 0
    seq =[]
    for line in seqs:
        if(line[:1] == ">" and flag == 0):
            name = line.strip()[1:]
            flag = 1
        elif(line[:1] == ">" and flag == 1):
            se = ''.join(seq)
            get_product(fpri,rpri,se,name)
            name = line.strip()[1:]
            seq = []
        else:
            seq.append(line.strip())
    se = ''.join(seq)
    get_product(fpri,rpri,se,name)
        
def read_primer(file):
    prim = open(file,'r')
    swi = 0
    fpri = {}
    rpri = {}
    name = ""
    for line in prim:
        if(line[:1] == ">"):
            name = line.strip()[1:]
        else:
            seq = line.strip()
            rseq = reverse_complement.get_rc(seq)
            if fpri.has_key(seq):
                temp = fpri[seq] + ','+name
                fpri[seq] = temp
                temp = rpri[rseq] + ',' +name
                rpri[rseq] = temp
            else:
                fpri[seq] = name
                rpri[rseq] = name
    prim.close()
    return fpri,rpri
            
def main():
    #read primer
    prim = sys.argv[1])
    fpri,rpri = read_primer(prim)

    #find product
    seqs = sys.argv[2]
    find_product(fpri,rpri,seqs)

if __name__ == '__main__':
    main()
