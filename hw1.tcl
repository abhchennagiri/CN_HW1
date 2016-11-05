#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Yellow

#Open the NAM trace file
set nf [open outhw1_1.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open out1_1.tr w]
$ns trace-all $tf

#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Close the Trace file
        close $tf
        #Execute NAM on the trace file
        exec nam outhw1_1.nam 
        exit 0
}


#Create six nodes
# A small hack to improve readability. Added another node
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail

#Set Queue Size of link (n2-n3) to 10
$ns queue-limit $n2 $n3 10

#Give node position (for NAM)

$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n4 $n3 orient left-down
$ns duplex-link-op $n6 $n3 orient left-up

#Make all the nodes TCP agents and n3 as sink
set tcp1 [new Agent/TCP/Newreno]
$tcp1 set class_ 1
$ns attach-agent $n1 $tcp1

set tcp5 [new Agent/TCP/Vegas]
$tcp5 set class_ 2
$ns attach-agent $n5 $tcp5


set sink4 [new Agent/TCPSink]
$sink4 set class_ 1
$ns attach-agent $n4 $sink4

set sink6 [new Agent/TCPSink]
$sink6 set class_ 2
$ns attach-agent $n6 $sink6

#Setup a CBR over UDP connection
set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp2 $null
set cbr2 [new Application/Traffic/CBR]
$cbr2 attach-agent $udp2

#Setup an FTP over TCP connection

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ns connect $tcp1 $sink4
$tcp1 set fid_ 1

set ftp5 [new Application/FTP]
$ftp5 attach-agent $tcp5
$ns connect $tcp5 $sink6
$tcp5 set fid_ 2

$cbr2 set type_ CBR
$cbr2 set packet_size_ 1000
$cbr2 set random_ false


#Schedule events for the CBR events
$ns at 0.0 "$n1 label N1"
$ns at 0.0 "$n2 label N2"
$ns at 0.0 "$n3 label N3"
$ns at 0.0 "$n4 label N4"
$ns at 0.0 "$n5 label N5"
$ns at 0.0 "$n6 label N6"

set time_interval 4
set gap 1
set cbr_rate 2
set start_time 0
set inc_count 1
set data Mb
set end_time [ expr { $start_time + $time_interval } ]
set num_readings 10
set i 0
    
while {$i < $num_readings} { 

  set cbr_rate_string $cbr_rate$data
  puts "$cbr_rate_string $start_time $end_time"
  $ns at $start_time "$cbr2 set rate_  $cbr_rate_string"
  $ns at $start_time "$cbr2 start"
  $ns at $start_time "$ftp1 start"
  $ns at $start_time "$ftp5 start"
  $ns at $end_time "$ftp1 stop"
  $ns at $end_time "$ftp5 stop"
  $ns at $end_time "$cbr2 stop"

  set start_time [ expr { $start_time + $time_interval + $gap } ]
  set end_time [ expr { $start_time + $time_interval } ]

  set cbr_rate [ expr { $cbr_rate + $inc_count } ]
  incr i

}

puts "$end_time"


#Detach tcp and sink agents (not really necessary)
$ns at $end_time "$ns detach-agent $n1 $tcp1; $ns detach-agent $n3 $null; $ns detach-agent $n2 $udp2; $ns detach-agent $n4 $sink4; $ns detach-agent $n6 $sink6; $ns detach-agent $n5 $tcp5"

#Call the finish procedure after $start_time seconds of simulation time 
$ns at $start_time "finish"

#Run the simulation
$ns run




