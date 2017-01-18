#Calculates accuracy based on
#input files that are the output of the Wolfpsort Tool

import sys, getopt
from itertools import izip
from string import punctuation
import numpy
import re
import matplotlib.pyplot as plt

def printtable(w):
	print confusion
	#for x in range(0,9):
	#	print ""
	#	for y in range(0,9):
	#		print confusion[x][y],
	plt.matshow(confusion)
def matrixizer(loc):
	if loc == 'Secreted':
		number = 0
		return number
	elif loc == 'Cytoplasm':
		number = 1
		return number
	elif loc == 'Cellmembrane':
		number = 2
		return number
	elif loc == 'Peroxisome':
		number = 3
		return number
	elif loc == 'Mitochodria':
		number = 4
		return number
	elif loc == 'Nucleus':
		number = 5
		return number
	elif loc == 'Golgiapparatus':
		number = 6
		return number
	elif loc == 'Endoplasmicreticulum':
		number = 7
		return number
	elif loc == 'Chloroplast':
		number = 9
		return number
	elif loc == 'Plastid':
		number = 9
		return number
	elif loc == 'Vacuole':
		number = 8
		return number



def formattedLocation(pLoc):
	if pLoc == 'extr':
		return 'Secreted'
	if pLoc == 'cysk':
		return 'Cytoplasm'
	if pLoc == 'cyto':
		return 'Cytoplasm'
	if pLoc == 'plas':
		return 'Cellmembrane'
	if pLoc == 'pero':
		return 'Peroxisome'
	if pLoc == 'mito':
		return 'Mitochodria'
	if pLoc == 'nucl':
		return 'Nucleus'
	if pLoc == 'golg':
		return 'Golgiapparatus'
	if pLoc == 'E.R.':
		return 'Endoplasmicreticulum'
	if pLoc == 'chlo':
		return 'Plastid'
	if pLoc == 'vacu':
		return 'Vacuole'

#['extr', 'cysk', 'cyto', 'plas', 'pero', 'mito', 'nucl', 'golg', 'er'],[chlo]
#count cysk and cyto as same, plas as cell membrane
#if aLoc = plastid, Transmembrane, Lysosome, Melanosome, Vacuole; then skip
def accuracy(pLoc, aLoc, correct, total,wpID):
	aLoc = aLoc.strip('\n')
	if wpID == 'Q39649':
		print aLoc
	if aLoc == 'Lysosome':
		return correct, total
	elif aLoc == 'Membrane(other)':
		return correct, total
	elif aLoc == 'Membrane':
		return correct, total
	elif aLoc == 'Melanosome':
		return correct, total
	#only one occurence
	elif pLoc == 'lyso':
		return correct, total
	ppLoc = formattedLocation(pLoc)
	ppLoc = ppLoc.replace("'", "")
	#Need titles
	if ppLoc == aLoc:
		diag = matrixizer(ppLoc)
		confusion[diag][diag]+=1
		correct+=1
		total+=1
	else:
		x = matrixizer(ppLoc)
		y = matrixizer(aLoc)
		#if x == 8:
		#	print "fsd"
		confusion[x][y]+=1
		total+=1
	return correct,total


def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hw:i:k:",["PsortFile=","IDmapFile=","Kingdom"])
	except getopt.GetoptError:
		print 'wolfpsortAccuracy.py -w <WPsortFile> -i <Idmaps> -k <kingdom>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'wolfpsortAccuracy.py -w <WPsortFile> -i <Idmaps>'
			sys.exit()
		elif opt in ("-w", "--PsortFile"):
			wp = arg
		elif opt in ("-i", "--IDmapFile"):
			maps = arg
		elif opt in ("-k", "--kingdom"):
			kingdom = arg

	total = 0
	correct = 0
	sentence = ""
	#Account for Chloroplast
	if kingdom == 'plant':
		w, h = 10, 10
	elif kingdom == 'fungi':
		w, h = 9, 9
	else:
		w, h = 8, 8
	global confusion
	confusion = [[0 for x in range(w)] for y in range(h)]
	#this doesn't work, we need to be able to skip lines
	with open(wp,'r') as pre, open(maps,'r') as act:
		p = pre.read().split('\n')[1:-1]
		a = act.read().split('\n')[1:-1]
		for pp in p:
			pID = pp.split(" ")
			for aa in a:
				aID = aa.split(',')
				if (pID==aID):
					print pp

				#pz = p[1].split("_",1)
				#a = a.split(",",1)
				#sentence += a[1] + " "
				#if re.match(a[0].strip(),p[0].strip()):
				#	print p[0] + ' ' + a[0]
			#correct, total = accuracy(pz[0],a[1],correct, total,p[0])
		print str(correct) + ' ' + str(total)
		#print out matrix function
		printtable(w)
		#print set(sentence.translate(None, punctuation).lower().split())
main(sys.argv[1:])
