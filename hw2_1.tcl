#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Yellow

#Open the NAM trace file
set nf [open outhw2_1.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open out2_1.tr w]
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
        exec nam outhw2_1.nam 
        exit 0
}


#Create six nodes
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
$ns duplex-link $n2 $n3 1.5Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


#Give node position (for NAM)

$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n4 $n3 orient left-down
$ns duplex-link-op $n6 $n3 orient left-up

#Make all the nodes TCP agents and n3 as sink
set tcp1 [new Agent/TCP/Sack1]
$tcp1 set class_ 1
$ns attach-agent $n1 $tcp1
$tcp1 set packetSize_ 960


set sink4 [new Agent/TCPSink/Sack1]
$sink4 set class_ 1
$ns attach-agent $n4 $sink4


#Setup a CBR over UDP connection
set udp5 [new Agent/UDP]
$ns attach-agent $n5 $udp5
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp5 $null
set cbr5 [new Application/Traffic/CBR]
$cbr5 attach-agent $udp5
$udp5 set class_ 2
#$ns connect $udp2 $sink3

#Setup an FTP over TCP connection

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ns connect $tcp1 $sink4
$tcp1 set fid_ 1

$cbr5 set type_ CBR
$cbr5 set packet_size_ 500
$cbr5 set rate_ 1Mb
$cbr5 set random_ false


#Schedule events for the CBR events
$ns at 0.0 "$n1 label N1"
$ns at 0.0 "$n2 label N2"
$ns at 0.0 "$n3 label N3"
$ns at 0.0 "$n4 label N4"
$ns at 0.0 "$n5 label N5"
$ns at 0.0 "$n6 label N6"


$ns at 0.0 "$ftp1 start"
$ns at 5.0 "$cbr5 start"
#$ns at 0.0 "$ftp5 start"
$ns at 20.0 "$ftp1 stop"
$ns at 20.0 "$cbr5 stop"
#$ns at 6.0 "$cbr2 stop"

#Call the finish procedure after $start_time seconds of simulation time 
$ns at 21.0 "finish"

#Run the simulation
$ns run


