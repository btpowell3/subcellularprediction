import sys, getopt
from itertools import izip
from string import punctuation
import numpy
import re
def transformLocation(location, ID):
    if re.match('Nucleus',location):
        print ID + ',Nucleus'
    elif re.match('Cell',location):
        print ID + ',Cellmembrane'
    elif re.match('Cytoplasm',location):
        print ID + ',Cytoplasm'
    elif re.match('Mito',location):
        print ID + ',Mitochodria'
    elif re.match('Endoplasmic',location):
        print ID + ',Endoplasmicreticulum'
    elif re.match('Secreted',location):
        print ID + ',Secreted'
    elif re.match('Extracellular',location):
        print ID + ',Secreted'
    elif re.match('Chloroplast',location):
        print ID + ',Chloroplast'
    elif re.match('Plastid',location):
        print ID + ',Chloroplast'
    elif re.match('Golgi',location):
        print ID + ',Golgiapparatus'
    elif re.match('Peroxisome',location):
        print ID + ',Peroxisome'
    elif re.match('Lysosome',location):
        print ID + ',Lysosome'
    elif re.match('Vacuole',location):
        print ID + ',Vacuole'
    elif re.match('Membrane',location):
        print ID + ',Membrane'
    elif re.match('Melanosome',location):
        print ID + ',Melanosome'
        #if isoform: should have handled this
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:",["File="])
    except getopt.GetoptError:
        print 'parser.py -f <file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'parser.py '
            sys.exit()
        elif opt in ("-f", "--File"):
            myfile = arg
    something = 0
    with open(myfile,'r') as f:
        for line in f:
            lineParts = re.split(r'\t+',line)
            #print lineParts[0],
            #print ',',
            location = re.split('\W+',lineParts[2])
            transformLocation(location[0],lineParts[0])

main(sys.argv[1:])
