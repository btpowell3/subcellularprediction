<?php
/****
Sequence requirements:
Must be at least 3 aa in length
Considering requiring M as start codon
****/

$file = fopen($argv[1],'r');

$fasta = 'fasta//'.$argv[2].'.fasta';
$fastaWithoutLocs = 'fasta//WO'.$argv[2].'.fasta';
$idmaps = 'idmaps//'.$argv[2].'.txt';

while(!feof($file))
{
$str = fgets($file);
$idseq = preg_split('/\t/', $str);

if(strlen($idseq[1])>30)
{
$parts = preg_split('/[,:;!?.-]/u', $idseq[2], -1, PREG_SPLIT_NO_EMPTY);
array_pop($parts);
$locCounter = 0;
foreach ($parts as $part)
{
	//Limit to location predictions, currently set at 1
	if($locCounter==1)  break;
	$locations[$locCounter] = subs(trim($part));
	$locCounter++;
}

//if(strcmp($locations[0],$locations[1])==false) unset($locations[1]);
if($locations[0] != NULL)
{


    file_put_contents($fasta,">".$idseq[0]."|".$locations[0]."|\n".$idseq[1]."\n", FILE_APPEND);

	//Fasta file without loc
    file_put_contents($fastaWithoutLocs,">".$idseq[0]."\n".$idseq[1]."\n", FILE_APPEND);

	//IDmap file
    file_put_contents($idmaps,$idseq[0].",".$locations[0]."\n", FILE_APPEND);
}

unset($locations);
}
}

function subs($string)
{
	$loc = "";
switch ($string)
	{
		case (preg_match('/Nucleus*/', $string) ? true : false):
		$loc = "Nucleus";
		break;

		#cell membrane and plasma membrane are similiar
		case (preg_match('/Cell membrane*/', $string) ? true : false):
		$loc = "Cellmembrane";
		break;

		#cytoplasm = cytosol + organelles, maybe count as cytoskeleton too
		case (preg_match('/Cytoplasm*/', $string) ? true : false):
		$loc = "Cytoplasm";
		break;

		case (preg_match('/Endoplasmic reticulum*/', $string) ? true : false):
		$loc = "Endoplasmicreticulum";
		break;

		case (preg_match('/Secreted*/', $string) ? true : false):
		$loc = "Secreted";
		break;

		case (preg_match('/Mito*/', $string) ? true : false):
		$loc = "Mitochodria";
		break;

		case (preg_match('/Lysosome*/', $string) ? true : false):
		$loc = "Lysosome";
		break;

		case (preg_match('/Peroxisome*/', $string) ? true : false):
		$loc = "Peroxisome";
		break;

		case (preg_match('/Golgi apparatus*/', $string) ? true : false):
		$loc = "Golgiapparatus";
		break;

		//ambiguous with secreted
		case (preg_match('/Extracellular space*/', $string) ? true : false):
		$loc = "Secreted";
		break;

		case (preg_match('/Melanosome*/', $string) ? true : false):
		$loc = "Melanosome";
		break;

		case (preg_match('/Chloroplast*/', $string) ? true : false):
		$loc = "Chloroplast";
		break;

		#Appear in same line everytime
		case (preg_match('/Plastid*/', $string) ? true : false):
		$loc = "Chloroplast";
		break;

		case (preg_match('/Vacuole*/', $string) ? true : false):
		$loc = "cret";
		break;

		# Ranges from organelle membranes to single/multi pass
		case (preg_match('/Membrane*/', $string) ? true : false):
		$loc = "Membrane";
		break;

		default:
		$loc = NULL;
		break;

	}

return $loc;
}

?>
