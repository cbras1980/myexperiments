my @letters = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F');
for (my $i=0;$i<16;$i++) {
  for (my $j=0;$j<16;$j++) {
    for (my $k=0;$k<16;$k++) {
        for (my $l=0;$l<16;$l++) {
           for (my $m=0;$m<16;$m++) {
              for (my $n=0;$n<16;$n++) {
            print "00%3A1A%3A79%3A".$letters[$i].$letters[$j]."%3A".$letters[$k].$letters[$l]."%3A".$letters[$m].$letters[$n]."\n";
              }
           }
        }
    }
  }
}
