#!/bin/sh
#
# Shell script to call scripts!
#
############ Print out normal fasta files and key sheets, id's -> locations
clear

#Declare kingdoms
king=("rodents" "fungi" "human" "mammals" "plants")

#Declare locations, used for iterating
locations=("Nucleus" "Cytoplasm" "Endoplasmicreticulum" "Secreted" "Mitochodria" "Lysosome" "Cellmembrane" "Peroxisome" "Golgiapparatus" "Melanosome" "Chloroplast" "Plastid" "Vacuole" "Membrane(other)")

#Declare Properties
prop=("mass" "hydrophobic" "acceptor" "pka" "pi")

##############################################
# Initalization Complete
# Proceed to parsing starting data files (raw files from ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/)
##############################################
one () {
echo "Stage One, beginning..."
for x in "${king[@]}"
do
	echo "Processing $x"
	perl SwissParser.pl ../StartingFiles/uniprot_sprot_${x}.dat | tee 'parsed/'${x}parsed.txt
done
}

# Use stage 1's file to create fasta files,
# Count locations procured and write to file
two () {
echo "Stage Two, beginning..."
Make sure counts are empty
rm counts/*.txt
rm fasta/*.fasta
for y in "${king[@]}"
do
   echo "Processing $y"

   php locs_mammal.php 'parsed/'${y}parsed.txt ${y}
	for z in "${locations[@]}"
	do

		count=$(grep -o "$z" 'fasta/'${y}.fasta | wc -l)
		# Adjust minimum count for proteins needed for a location here
		if [ $count -le 300 ]
			then
			python stringReplace.py -i 'fasta/'${y}.fasta -o fasta/temp.fasta -l ${z}; mv fasta/temp.fasta 'fasta/'${y}.fasta
		else
			spacer=","
			text=$z$spacer$count
			echo $text >> .'/counts/'${y}_counts.txt
		fi
	done

done
}


##############################################
# Stage Completed
# Calculate Chaos game values for each sequence and then get haar wavelet numbers
##############################################
three () {
echo "Stage Three, beginning..."
for x in "${king[@]}"
do
	echo "Processing $x"

	for y in "${prop[@]}"
	do
		python cgr.py -i 'fasta/'${x}.fasta -t ${y} > 'haar/'${x}'/'${y}_HAAR.csv
	done
done
}



##############################################
# Stage Completed
# Pulls features,scores, and confusion matrix after running classifiers
# Using sklearns library of classifiers
##############################################
four () {
echo "Stage Four, beginning...!"
rm -rf 'sklearnFormat/'
rm -rf 'scores/'
for x in "${king[@]}"
do
	mkdir -p sklearnFormat'/'${x}
	echo "Processing $x"
	for y in "${prop[@]}"
	do
		cat haar'/'${x}'/'${y}_HAAR.csv | cut -d \, -f 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 >> ./sklearnFormat'/'${x}'/'${y}_data.csv
		cat haar'/'${x}'/'${y}_HAAR.csv | cut -d \, -f 25 >> sklearnFormat'/'${x}'/'${y}_target.csv
		python stringReplace.py -i sklearnFormat'/'${x}'/'${y}_target.csv -o sklearnFormat'/'${x}'/'${y}_numeric.csv

		python classification.py -d sklearnFormat'/'${x}'/'${y}_data.csv -t sklearnFormat'/'${x}'/'${y}_numeric.csv

	done
done
}


####################################################
#Run other predictor(s) with my data to compare with
#Calculate run times ###Not implemented
####################################################
five () {
	for x in "${king[@]}"
	do
			echo "Processing "${x}
		python wolfpsortAccuracy.py -w wolfpsort'/'${x}WPsort.txt  -i idmaps'/'${x}.txt -k ${x}
	done
#multiloc2

}

#Function calling is done here #comment out to not run that function
one
two
three
four
five
