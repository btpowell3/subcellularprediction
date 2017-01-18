#Chaos game theory script
from Bio import SeqIO
import numpy as np
import matplotlib.pyplot as plt
import re
import pywt
import sys, getopt


#B = D or N ; Z = E or Q ; J or X not handled.
def switcher(cgrtype):
    switcher = {
        "hydrophobic":  ["[FIWLVM]", "[YCNA]", "[THGSQBZ]", "[RKDEPD]"],
        "acceptor":  ["[ACGILMFPV]", "[DEBZ]", "[RKW]", "[NQHSTY]"],
        "mass": ["[GA]","[SPVTC]","[ILNDBQKEZMH]","[FRYW]"],
        "pka": ["[DBCNFPH]","[EZTQYSKR]","[MVGLAI]","[W]"],
        "pi": ["[DEBZ]","[CNFTQYSM]","[WVGLAIP]","[HKR]"]
    }
    return switcher.get(cgrtype, "DEFAULT")
    print 'nothing'

def cgr(inputfile,outputfile,cgrtype):

   #Header throws off KNN
   #print ("Cd3min,Cd3max,Cd3mean,Cd3sdev,Cd2min,Cd2max,Cd2mean,Cd2sdev,Cd1min,Cd1max,Cd1mean,Cd1sdev")
   fasta_sequences = SeqIO.parse(inputfile,'fasta')
   for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        sequence = list(sequence)
        counter = -1
        x = []
        y = []
        x.append(0.5)
        y.append(0.5)
        a = switcher(cgrtype)
        for amino in sequence:
            counter = counter + 1
          #(0,0)
            if re.match(a[0],amino):
                x.append(x[counter]+.5*(0-x[counter]))
                y.append(y[counter]+.5*(0-y[counter]))
          #(1,0)
            if re.match(a[1],amino):
                x.append(x[counter]+.5*(1-x[counter]))
                y.append(y[counter]+.5*(0-y[counter]))
          #(0,1)
            if re.match(a[2],amino):
                x.append(x[counter]+.5*(0-x[counter]))
                y.append(y[counter]+.5*(1-y[counter]))
          #(1,1)
            if re.match(a[3],amino):
                x.append(x[counter]+.5*(1-x[counter]))
                y.append(y[counter]+.5*(1-y[counter]))
            else:
                x.append(x[counter])
                y.append(y[counter])
        xA3, xD3, xD2, xD1 = pywt.wavedec(x,'haar',level=3)
        yA3, yD3, yD2, yD1 = pywt.wavedec(y,'haar',level=3)
        names = re.split('\|+',name) #remove | for after subcell
        #modify this next line to print to a file
        print xD3.min(),",",xD3.max(),",", xD3.mean(),",",xD3.std(),",",xD2.min(),",",xD2.max(),",", xD2.mean(),",",xD2.std(),",",xD1.min(),",",xD1.max(),",", xD1.mean(),",",xD1.std(),",",yD3.min(),",",yD3.max(),",", yD3.mean(),",",yD3.std(),",",yD2.min(),",",yD2.max(),",", yD2.mean(),",",yD2.std(),",",yD1.min(),",",yD1.max(),",", yD1.mean(),",",yD1.std(),",",names[1]
        del x[:]
        del y[:]

def main(argv):
   inputfile = ''
   outputfile = ''
   cgrtype = ''
   try:
      opts, args = getopt.getopt(argv,"hi:ot:",["ifile=","ofile=","type="])
   except getopt.GetoptError:
      print 'cgr.py -i <inputfile> -o <outputfile> -t <type>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'cgr.py -i <inputfile> -o <outputfile> -t <type>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-t", "--type"):
         cgrtype = arg
   cgr(inputfile,outputfile,cgrtype)



if __name__ == "__main__":
   main(sys.argv[1:])


#("Sequences represented by CGR based on hydrophobicity values and transformed by Haar Wavelet to 3 levels")
        #If you want graph pictures
#        plt.scatter(x,y)
        #plt.savefig(name,format='png')
#        plt.clf()
