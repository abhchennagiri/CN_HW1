# A Python script to parse and calculate the throughput and end-to-end latency 


def calTPT(start_time,end_time):
    udp1_count = 0
    udp2_count = 0
    udp3_count = 0
    t = end_time - start_time
    with open('out2_2.tr') as trace_file:
        for line in trace_file:
            event,time,from_node,to_node,pkt_type,pkt_size,flags,flow_id,src_addr,dst_addr,seq_num,pkt_id = line.split()
            #print time
            if(float(time) >= start_time and float(time) <= end_time):
                if(event == 'r' and to_node == '3' and flow_id == '1'):
                    udp1_count +=  1
                if(event == 'r' and to_node == '3' and flow_id == '2'):
                    udp2_count +=  1
                if(event == 'r' and to_node == '3' and flow_id == '3'):
                    udp3_count +=  1     
            
    numBytes_udp1 = (udp1_count) * 1000 
    numBytes_udp2 = (udp2_count) * 1000
    numBytes_udp3 = (udp3_count) * 500

    tpt_udp1 = (numBytes_udp1 * 8/float(t))
    tpt_udp2 = (numBytes_udp2 * 8/float(t))
    tpt_udp3 = (numBytes_udp3 * 8/float(t))

    print tpt_udp1/float(1000000)
    print tpt_udp2/float(1000000)
    print tpt_udp3/float(1000000)

def calLatency(start_time, end_time, gap):

    with open('out2_2.tr', "rb") as f:
        first = f.readline()      # Read the first line.
        f.seek(-2, 2)             # Jump to the second last byte.
        while f.read(1) != b"\n": # Until EOL is found...
                f.seek(-2, 1)         # ...jump back the read byte plus one more.
        last = f.readline() 
    event,time,from_node,to_node,pkt_type,pkt_size,flags,flow_id,src_addr,dst_addr,seq_num,pkt_id = last.split()


    startTime_udp1 = [0] * (int(pkt_id) + 100)
    endTime_udp1 = [0] * (int(pkt_id) + 100)

    startTime_udp2 = [0] * (int(pkt_id) + 100)
    endTime_udp2 = [0] * (int(pkt_id) + 100)

    startTime_udp3 = [0] * (int(pkt_id) + 100)
    endTime_udp3 = [0] * (int(pkt_id) + 100)

    num_udp1 = 0
    num_udp2 = 0
    num_udp3 = 0        
    
    

    t = end_time - start_time
    with open('out2_2.tr') as trace_file:
        for line in trace_file:
            event,time,from_node,to_node,pkt_type,pkt_size,flags,flow_id,src_addr,dst_addr,seq_num,pkt_id = line.split()
            pkt_id = int(pkt_id)
            if(float(time) >= start_time and float(time) <= (end_time + gap)):
                if(event == '+' and from_node == '1' ):
                    if(startTime_udp1[pkt_id] == 0):
                        startTime_udp1[pkt_id] = float(time)
                #if(event == '-' and from_node == '5' ):   
                #    totalPktXmit_tcp2 += 1
                if(event == '+' and from_node == '7' ):
                    if(startTime_udp2[pkt_id] == 0):
                        startTime_udp2[pkt_id] = float(time)
 
                if(event == '+' and from_node == '5' ):
                        if(startTime_udp3[pkt_id] == 0):
                                startTime_udp3[pkt_id] = float(time)
                 
                if(event == 'r' and to_node == '4' ):
                    if(endTime_udp1[pkt_id] == 0):
                        endTime_udp1[pkt_id] = float(time)
                if(event == 'r' and to_node == '8' ):
                        if(endTime_udp2[pkt_id] == 0):
                                endTime_udp2[pkt_id] = float(time)
 
                if(event == 'r' and to_node == '6' ):
                        if(endTime_udp3[pkt_id] == 0):
                                endTime_udp3[pkt_id] = float(time)
    
    #print 'End Times: 1\n'
    #for i in xrange(len(startTime_udp2)):
    #    print endTime_udp1[i],startTime_udp1[i]

    sum = 0    
    for i in xrange(len(startTime_udp1)):
        if(endTime_udp1[i] != 0.0 and startTime_udp1[i] != 0.0):
            sum += endTime_udp1[i]  - startTime_udp1[i]
            num_udp1 += 1
    #print num_udp1
    print sum/float(num_udp1)

    sum = 0    
    for i in xrange(len(startTime_udp2)):
        if(endTime_udp2[i] != 0.0 and startTime_udp2[i] != 0.0 ):
            sum += endTime_udp2[i]  - startTime_udp2[i]
            num_udp2 += 1
            #num_udp2 = 1
    print sum/float(num_udp2)

    sum = 0    
    for i in  xrange(len(startTime_udp3)):
        if(endTime_udp3[i] != 0  and startTime_udp3[i] != 0):
            sum += endTime_udp3[i]  - startTime_udp3[i]
            num_udp3 += 1
    print sum/float(num_udp3)


def main():
    choice = int(raw_input("Choose 1 - Throughput , 2 - End-End Delay\n"))
    if(choice == 1):
        calTPT(0,15)
    if(choice == 2):    
        calLatency(0,15,1)

if __name__ == "__main__":
    main()
