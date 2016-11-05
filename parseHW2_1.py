# A Python script to parse the average bandwidth and the average packet loss rate
mb = 1000000

def calBW(start_time,end_time):
    tcpflow1_count = 0
    #tcpflow2_count = 0
    cbrflow_count = 0

    #tcpack1_count = 0
    #tcpack2_count = 0
    t = end_time - start_time
    with open('out2_1.tr') as trace_file:
        for line in trace_file:
            event,time,from_node,to_node,pkt_type,pkt_size,flags,fid,src_addr,dst_addr,seq_num,pkt_id = line.split()
            #print time
            if(float(time) >= start_time and float(time) <= end_time):
                if(event == 'r' and to_node == '3' and src_addr == '1.0' and dst_addr == '4.0'):
                    tcpflow1_count = tcpflow1_count + 1
                #if (event == 'r' and to_node == '2' and src_addr == '4.0' and dst_addr == '1.0'):
                #    tcpack1_count += 40
                #if(event == 'r' and to_node == '3' and src_addr == '5.0' and dst_addr == '6.0'):
                #    tcpflow2_count = tcpflow2_count + 1
                #if((event == 'r' and to_node == '2' and src_addr == '6.0' and dst_addr == '5.0')):
                #    tcpack2_count += 40
                if(event == 'r' and to_node == '3' and src_addr == '5.0' and dst_addr == '6.0'):
                    cbrflow_count = cbrflow_count + 1
            
    numBytes_tcp1 = (tcpflow1_count) * 1000 
    #numBytes_tcp2 = (tcpflow2_count) * 1040 + tcpack2_count
    numBytes_cbr = (cbrflow_count) * 500

 #   print numBytes_tcp1,numBytes_tcp2, numBytes_cbr

    bw_tcp1 = (numBytes_tcp1 * 8/float(t))/mb
    #bw_tcp2 = (numBytes_tcp2 * 8/float(t))
    bw_cbr = (numBytes_cbr * 8/float(t))/mb

    print bw_tcp1,bw_cbr

def calAvgPktLoss(start_time, end_time, gap):

    totalPktXmit_tcp1 = 0
    #totalPktXmit_tcp2 = 0
    totalPktXmit_cbr = 0

    totalPktDrop_tcp1 = 0
    #totalPktDrop_tcp2 = 0
    totalPktDrop_cbr = 0

    t = end_time - start_time
    with open('out2_1.tr') as trace_file:
        for line in trace_file:
            event,time,from_node,to_node,pkt_type,pkt_size,flags,flow_id,src_addr,dst_addr,seq_num,pkt_id = line.split()
            #print time
            if(float(time) >= start_time and float(time) <= (end_time + gap)):
                if(event == '-' and from_node == '1' ):
                    totalPktXmit_tcp1 += 1
                #if(event == '-' and from_node == '5' ):   
                #    totalPktXmit_tcp2 += 1
                if(event == '-' and from_node == '5' ):
                    totalPktXmit_cbr += 1
                    
                if(event == 'd' and flow_id == '1'):
                    totalPktDrop_tcp1 += 1
                #if(event == 'd' and flow_id == '2'):
                #    totalPktDrop_tcp2 += 1
                if(event == 'd' and flow_id == '2'):
                    totalPktDrop_cbr += 1
        
        
    
    pktLossRate_tcp1 = ((totalPktDrop_tcp1)/float(totalPktXmit_tcp1))
    #pktLossRate_tcp2 = ((totalPktDrop_tcp2)/float(totalPktXmit_tcp2))
    pktLossRate_cbr = (( totalPktDrop_cbr)/float(totalPktXmit_cbr))
    
    #print totalPktXmit_tcp1,totalPktXmit_cbr
    #print totalPktDrop_tcp1,totalPktDrop_cbr
    print  pktLossRate_tcp1, pktLossRate_cbr     


def main():
    calBW(5,20)
    #calBW(5,9)
    #calAvgPktLoss(0,4,1)
    #calAvgPktLoss(5,9,1)
    #calAvgPktLoss(30,34,1)
    calAvgPktLoss(5,20,1)

if __name__ == "__main__":
    main()
