#!/usr/bin/python
import os,subprocess,time,re,datetime
import socket
#CREATE STATISTICS FILE EVERY MINUTE
#SIP    resolver    curl-timers     rtt     timestamp   variance
TARGET="facebook.com"
command="ping -c 1 {}".format(TARGET)
ping_l=[]
error=0
print socket.gethostbyname(socket.getfqdn())
while(True):
    try:
        data_s=subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
    # print data_s
    except subprocess.CalledProcessError as e:
        #ping took too long, command is failing
        print e
        error=error+1
        continue
    #NON ERROR STAGES
    rtt=re.findall(r"round-trip.*(\d\.\d+)/",data_s)
    ping_l.append(float(rtt[0]))
    print ping_l
    if len(ping_l)==10:
        #COMPUTE VALUES
        avg=sum(ping_l)/len(ping_l)
        minimum=min(ping_l)
        maximum=max(ping_l)
        timestamp=datetime.datetime.utcnow()
        data= "|||{}|||{}|||{}|||{}|||{}".format(timestamp,avg,minimum,maximum,error)
        #WRITE DATA TO FILE
        with open("/Users/garmanav/Documents/python/project/data.out","a+") as f:
            f.write(data)
            f.write("\n")
        print "Average RTT of last 60 working samples is {}".format(sum(ping_l)/len(ping_l))
        print "Least value of last 60 working samples is {}".format(min(ping_l))
        print "Max value of last 60 working samples is {}".format(max(ping_l))
        print "Number of error in last 60 working samples are {}".format(str(error))

        #CLEAN UU PING LIST
        ping_l=[]
        error=0
    time.sleep(1)
