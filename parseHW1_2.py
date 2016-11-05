# A Python script to parse the average bandwidth and the average packet loss rate

#Define Global Variables here
mb  = 1000000
file_trace = "out1_1.tr"
time_interval = 4
gap = 1
initial_cbr_rate = 2
num_simulations  = 10
bw_increase = 1
bw_initial = 2


def calBW(start_time,end_time,bw_specified):
    tcpflow1_count = 0
    #tcpflow2_count = 0
    cbrflow_count = 0

    tcpack1_count = 0
    #tcpack2_count = 0
    t = end_time - start_time

    with open(file_trace) as trace_file:
        for line in trace_file:
            event,time,from_node,to_node,pkt_type,pkt_size,flags,fid,src_addr,dst_addr,seq_num,pkt_id = line.split()
            if(float(time) >= start_time and float(time) <= end_time):
                #Calculate TCP Flow 1 Packets    
                if(event == 'r' and to_node == '3' and src_addr == '1.0' and dst_addr == '4.0'):
                    tcpflow1_count = tcpflow1_count + 1
                #if (event == 'r' and to_node == '2' and src_addr == '4.0' and dst_addr == '1.0'):
                #    tcpack1_count += 40
                #Calculate TCP Flow 2 Packets     
                #if(event == 'r' and to_node == '3' and src_addr == '5.0' and dst_addr == '6.0'):
                #    tcpflow2_count = tcpflow2_count + 1
                #if((event == 'r' and to_node == '2' and src_addr == '6.0' and dst_addr == '5.0')):
                #    tcpack2_count += 40
                #Calculate CBR Flow Packets
                if(event == 'r' and to_node == '3' and src_addr == '2.0' and dst_addr == '3.0'):
                    cbrflow_count = cbrflow_count + 1
            
    numBytes_tcp1 = (tcpflow1_count) * 1040 
    #numBytes_tcp2 = (tcpflow2_count) * 1040
    numBytes_cbr = (cbrflow_count) * 1000

 #   print numBytes_tcp1,numBytes_tcp2, numBytes_cbr

    bw_tcp1 = float(numBytes_tcp1*8/(t))/(mb)
    #bw_tcp2 = float(numBytes_tcp2*8/(t))/mb
    bw_cbr = float(numBytes_cbr*8/(t))/mb

    print bw_specified,bw_tcp1,bw_cbr

def calAvgPktLoss(start_time, end_time, gap,bw_specified):

    totalPktXmit_tcp1 = 0
    totalPktXmit_tcp2 = 0
    totalPktXmit_cbr = 0

    totalPktDrop_tcp1 = 0
    totalPktDrop_tcp2 = 0
    totalPktDrop_cbr = 0

    t = end_time - start_time

    with open(file_trace) as trace_file:
        for line in trace_file:
            event,time,from_node,to_node,pkt_type,pkt_size,flags,flow_id,src_addr,dst_addr,seq_num,pkt_id = line.split()
            if(float(time) >= start_time and float(time) <= (end_time + gap)):
                if(event == '-' and from_node == '1' ):
                    totalPktXmit_tcp1 += 1
                #if(event == '-' and from_node == '5' ):   
                #    totalPktXmit_tcp2 += 1
                if(event == '-' and from_node == '2' ):
                    totalPktXmit_cbr += 1
                    
                if(event == 'd' and flow_id == '1'):
                    totalPktDrop_tcp1 += 1
                #if(event == 'd' and flow_id == '2'):
                #    totalPktDrop_tcp2 += 1
                if(event == 'd' and flow_id == '0'):
                    totalPktDrop_cbr += 1
        
        
    
    pktLossRate_tcp1 = ((totalPktDrop_tcp1)/float(totalPktXmit_tcp1))
    #pktLossRate_tcp2 = ((totalPktDrop_tcp2)/float(totalPktXmit_tcp2))
    pktLossRate_cbr = (( totalPktDrop_cbr)/float(totalPktXmit_cbr))
    
    #print totalPktXmit_tcp1,totalPktXmit_tcp2,totalPktXmit_cbr
    #print totalPktDrop_tcp1,totalPktDrop_tcp2,totalPktDrop_cbr
    print  bw_specified, pktLossRate_tcp1, pktLossRate_cbr     


def main():
    start_time = 0
    end_time = start_time + time_interval
    choice = int(raw_input("Enter 1 for bandwidth, 2 for avg packet loss, 3 for both\n"))    
    bw = bw_initial
    bw_interval = 1

    if(choice == 1 or choice == 3):
        for i in xrange(num_simulations):
            #print "Start Time: ", start_time, "End Time: ", end_time
            calBW(start_time,end_time,bw)
            start_time = end_time + gap
            end_time = start_time + time_interval
            bw += bw_interval 


    start_time = 0
    end_time = start_time + time_interval
    bw = bw_initial
    
    if(choice == 2 or choice == 3):
        for i in xrange(num_simulations):
            #print "Start Time: ", start_time, "End Time: ", end_time
            calAvgPktLoss(start_time,end_time,gap,bw)
            start_time = end_time + gap 
            end_time = start_time + time_interval
            bw += bw_interval

if __name__ == "__main__":
    main()
