# Craft an ICMP (ping) packet
packet = IP(dst="www.google.com")/ICMP()

# Send and receive a response (one packet)
send_recv = sr1(packet) 

# Print a summary of the packet
print(packet.show()) 

# Print the response (if any)
print(send_recv.show()) 
