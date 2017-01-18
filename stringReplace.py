import sys, getopt
##Replace Strings with numerical ID's for sklean format
def replace(inputfile,outputfile):

	with open(inputfile,'r+') as f:
		contents = f.read()
		contents = contents.replace('Nucleus', '0')
		contents = contents.replace('Cytoplasm', '1')
		contents = contents.replace('Endoplasmicreticulum', '2')
		contents = contents.replace('Secreted', '3')
		contents = contents.replace('Mitochodria', '4')
		contents = contents.replace('Lysosome', '5')
		contents = contents.replace('Cellmembrane', '6')
		contents = contents.replace('Peroxisome', '7')
		contents = contents.replace('Golgiapparatus', '8')
		contents = contents.replace('Melanosome', '9')
		contents = contents.replace('Chloroplast', '10')
		contents = contents.replace('Plastid', '10')
		contents = contents.replace('Membrane(other)', '11')
		contents = contents.replace('Vacuole', '12')
		f.write(contents)
		output = open(outputfile,'w')
		output.write(contents)
		output.close()
		f.close()

def remove(inputfile,outputfile,location):
	with open(inputfile) as oldfile, open(outputfile, 'w') as newfile:
		for line in oldfile:
			if location not in line:
				newfile.write(line)


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:l:",["ifile=","ofile=","location="])
   except getopt.GetoptError:
      print 'stringReplace.py -i <inputfile> -o <outputfile> -l <location>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'cgr.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-l", "--location"):
         location = arg

   try:
   	location
   except NameError:

   	replace(inputfile,outputfile)
   else:
   	remove(inputfile,outputfile,location)

main(sys.argv[1:])
