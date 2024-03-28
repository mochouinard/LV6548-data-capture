I own an MPP LV6548, and it does have some remote control capability.  But there is no way to connect to the unit and store these informations.

So I decided to look at how the LV6548 communicate, and I notice it was a simple socket with zero encryption at all with just a simple packet system in both direction.

It probably used a standard communication method that these type of unit use, but I decided to just try to decode the packets myself.

Since you cannot tell the unit where to communicate with, so it was either modifying the firmware uploaded to the device, or capturing it at the router level.

I didn't want to modify the firmware at all, so I went with the router route.

I use Mikrotik router, which are really configurable, and here the firewall rules I've added :



/ip firewall nat
add action=dst-nat chain=dstnat dst-address=47.242.188.205 src-address=192.168.88.200 to-addresses=192.168.88.10
add action=masquerade chain=srcnat dst-address=192.168.88.10 src-address=192.168.88.200

47.242.188.205 Is the remote server that manage the LV6548 remote application.
192.168.88.200 Is the address of my LV6548 
192.168.88.10 The machine that run the code found in this repository

Once this is done, all communication from your LV6548 will be went to your own machine.

This machine need to relay this information to the original IP so you can still use the mobile application.

There is a lot of stuff that can be done here... But in my case, I just wanted to log the data sent so I can create graph afterward.  But if the remote server ever stop working, I could write my own.


This is not a pretty well made project !  Just raw stuff that I needed to get to the point I got the data I wanted

So to run the program, you need to do this

python3 ./relay_socket.py -p 502 -d 47.242.188.205 -P 502 -l lv6548-home.log -D -v

This will start the local server listening to 502 and sending it back to the destination server

It will log to the lv6548-home.log file, and using the parse_log.py, you will be able to extract information from that log output.
