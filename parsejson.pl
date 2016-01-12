#!/usr/bin/perl
use strict;

use warnings;
 
binmode STDOUT, ":utf8";
use utf8;
 
use JSON;

my $targethost = "host";

my $json;
{
  local $/; #Enable 'slurp' mode
  open my $fh, "<", "lista2.json";
  $json = <$fh>;
  close $fh;
}
my $data = decode_json($json);
# Output to screen one of the values read
my $alldata = $data->{'js'}->{'data'};
my @array=keys($alldata);
my $size=$#array;

while ( my( $key, $value ) = each $alldata ) {
#o  print "Boss' hobbies: " . $alldata->[0]->{'id'} . "n";
 print "#EXTINF:-1," . $value->{'name'} . "\n";
 print "".$value->{'cmd'};
 print "http://$targethost:8000/live/user/pwd/". $value->{'id'} .".ts\n";
}
# Modify the value, and write the output file as json
#open my $fh, ">", "data_out.json";
#print $fh encode_json($data);
#close $fh;
