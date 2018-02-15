#!/usr/bin/perl -w
# @(#)$Id$;

$|++;
use strict;
use Time::Local;
use Data::Dumper;
use Getopt::Std;
use Term::ANSIColor;

my %opts = ();
getopts('xl:h:t:', \%opts);

my $debug = $opts{x} || 0;
my $min = $opts{l} || 100;
my $max = $opts{h} || 100;
my $timespan = $opts{t} || 5;

my @logs = </tmp/currencies_log_*>;
my $backlog = "/tmp/backlog.txt";


my $delay = ( ($timespan + 120) * 60);
my $t0 = time - $delay;       # now - delay 
my $SECS_PER_DAY = 24 * 3600;

my @markets = ();

my %change = ();

for my $log (@logs) {
  do {
    print STDERR "$log ignored - too old\n" if $debug;
    next;
  } if ((-M $log) * $SECS_PER_DAY) > $delay;

  open LOG, '<', $log or do {
    warn "$log: $!";
    next;
  };

  open BACKLOG, '+<', $backlog or do {
    warn "$backlog: $!";
    next;
  };

  # Go trough the log and parse the values
  while (<LOG>) {
    next unless /btc-/i;
    # 2017-08-23T15:29:59.04
    my ( $datetime , $market, $volume, $high, $low, $last ) = split /;/, $_;
    next unless $datetime =~ /(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2}).*/;
    
    my $t = timelocal($6, $5, $4, $3, $2-1, $1);
    #print $4,":",$5,":",$6," ",$3,"/",$2,"/",$1,"\n";
    print $datetime."\t"."T->",$t," T0->",$t0,"\n" if $debug;
    
    next if($t < $t0); 
  
    $change{$market}{lo} = $last if not defined $change{$market}{lo};
    $change{$market}{la} = $last;
    $change{$market}{datetime} = $datetime;
  }
}
  
my %changepm = ();

print STDERR Dumper \%change if $debug;
foreach my $market (sort keys %change) {
  my $init = $change{$market}{lo} + 0;
  my $now = $change{$market}{la} + 0;
  #print $market."-".$low."-".$last."\n";
  my $result = 0;
  $result = (( $now - $init ) * 100)/$init;
  #printf $market."-> %.2f \n",$result;
  $changepm{$market}=$result;
}

my %backlog = ();
while (<BACKLOG>) {
  my ( $datetime, $market, $change, $last ) = split /;/, $_;
  $backlog{$market}{$datetime}{change}=$change; 
  $backlog{$market}{$datetime}{value}=$last; 
}
print STDERR Dumper \%backlog if $debug;

#close BACKLOG;
#
open BACKLOG, '>', $backlog or do {
  warn "$backlog: $!";
  next;
};

foreach my $market (sort { $changepm{$a} <=> $changepm{$b} } keys %changepm) {
  
  my $previousval = 0;
  if ($changepm{$market} >= $max and $max!=100) {
    my $totaldiff = 0;
    foreach my $hst ( sort keys %{$backlog{$market}} ) {
      $hst =~ /(\d{4})\-(\d{2})\-(\d{2})T(\d{2}):(\d{2}):(\d{2}).*/; 
      my $t = timelocal($6, $5, $4, $3, $2-1, $1);    
      my $t0 = time - $delay*2;
      next if $t < $t0;
      my $diff = ($backlog{$market}{$hst}{value} - $previousval)*10e7;
      $totaldiff = $totaldiff + $diff if $previousval != 0;
      printf $market.";".$hst.";%.12f\n",$backlog{$market}{$hst}{value} if $previousval == 0;
      printf $market.";".$hst.";%.12f - diff: %.12f - change: %.2f\n",$backlog{$market}{$hst}{value},$diff,$backlog{$market}{$hst}{change} if $previousval != 0;
      $previousval = $backlog{$market}{$hst}{value};
    }
    print "Total diff: $totaldiff\n";
  }

  printf $market.";%.2f\n\n",$changepm{$market} if $changepm{$market} >= $max and $max!=100;
  printf $market.";%.2f\n",$changepm{$market} if $changepm{$market} <= $min and $min!=100;
  printf $market.";%.2f\n",$changepm{$market} if $min==100 and $max==100;
  printf BACKLOG $change{$market}{datetime}.";".$market.";%.2f;%.12f\n",$changepm{$market},$change{$market}{la} if $changepm{$market} >= $max; 
}
