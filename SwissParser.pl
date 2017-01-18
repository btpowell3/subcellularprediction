#!/usr/bin/env perl

use SWISS::Entry;
use SWISS::CCsubcell_location;
use SWISS::CCs;
# Read an entire record at a time
$/ = "\/\/\n";
while (<>){
 @new_locations =  ('form','component','topology','orientation');
  #my $object  = new SWISS::CCsubcell_location;
  $entry = SWISS::Entry->fromText($_);
    my @CCs = $entry -> CCs -> elements();
 
  for my $CC (@CCs) {
     
   #Only print out entries with subcellular comments
   if ($CC -> topic eq 'SUBCELLULAR LOCATION') {
 
      print $entry->AC, "\t";
      print $entry->SQ, "\t";
      print $CC->comment, "\n";
    } 
}

}