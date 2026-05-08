from scapy.all import sniff

def process_packet(packet):
    print(packet.summary())

def start_sniffing():
    sniff(prn=process_packet, store=False)

start_sniffing()