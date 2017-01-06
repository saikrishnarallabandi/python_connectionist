#! /usr/bin/perl

use strict;
use warnings;

my @cols = split(',', $_);
my $n = @cols;
print "row $. =  $n columns\n";
