#!/usr/bin/env python3

# Author: Dylan Boland (Student)
#
#
# 1542 Bytes for 802.11a/g frames. Therefore the no. of bits is: 1542*8 = 12336.
# In OFDM, each frame has a tail of 6 bits. Therefore we get: 12336 + 6 = 12342 bits.
#
# Example calculation 1 (802.11a at maximum data rate):
#
# (802.11a): max rate of 54 Mbps.
# Data bits per OFDM symbol: (No. bits per data symbol)(Encoding Rate)(No. channels) = (6)(3/4)(48) = 216 bits
# Therefore the no. of OFDM symbols needed is: (12342/216) = 57.138, which rounds up to 58.
# For 802.11a, the symbol duration (T) is 4 us. Therefore the transmit time needed for 58 symbols is:
# (58)(4 us) = 232 us
#
# Example calculation 2 (802.11a at minimum data rate):
#
# (802.11a): min rate of 6 Mbps.
# Data bits per OFDM symbol: (No. bits per data symbol)(Encoding Rate)(No. channels) = (1)(1/2)(48) = 24 bits
# So the no. of OFDM symbols needed is: (12342/24) = 514.25, which rounds up to 515 symbols.
# The symbol duration (T) for 802.11a is 4 us. This gives us a transmit time of:
# (515)(4 us) = 2060 us
#
# Example calculation 3 (802.11a at maximum data rate, transmitting RTS)
#
# (802.11a): max rate of 54 Mbps.
# RTS frame is 20 Bytes. This equals 20*8 = 160 bits. Again, there is a tail of 6 bits.
# So the total size in bits is 166 bits. No. of OFDM symbols needed is (166/216) -> 1 symbol.
# And each symbol has a duration 4 us. The same is true for the ACK.
#
# Example calculation 4 (802.11a at maximum data rate, transmitting TCP ACK)
#
# (802.11a): max rate of 54 Mbps.
# TCP ACK: 40 + 42 Bytes = 82 Bytes in total. Total size in bits is 82*8 + 6 = 664 (we add the 6-bit tail)
# No. of OFDM symbols needed: (664/216) = 3.07 -> 4 symbols. This will take:
# (4)(4 us) = 16 us
#
# Example calculation 5 (802.11a at minimum data rate, TCP ACK):
#
# (802.11a): min rate of 6 Mbps.
# TCP ACK: 40 + 42 Bytes = 82 Bytes in total. Total size in bits is 82*8 + 6 = 664 (we add the 6-bit tail)
# No. bits per OFDM symbols: (No. bits per data symbol)(Encoding Rate)(No. channels) = (1)(1/2)(48) = 24 bits
# No. of OFDM symbols needed: (664/24) = 27.6 -> 28 symbols. This will take:
# (28)(4 us) = 112 us
#
# Example calculation 6 (802.11n at maximum data rate, TCP ACK):
# 
# (802.11n): max rate of 96.3 Mbps.
# TCP ACK: 40 + 48 Bytes = 88 Bytes. Total size in bits is 88*8 + 6 = 710 (we add the 6-bit tail)
# No. bits per OFDM symbols: (No. bits per data symbol)(Encoding Rate)(No. channels) = (8)(5/6)(52) = 346.6 -> 346 bits.
# Therefore the no. of OFDM symbols needed is: (710/346) = 2.05 -> 3 symbols. Symbol duration for 802.11n is 3.6 us.
# This TCP ACK transmission will take: (3)(3.6) = 10.8 us
#
# Example calculation 7 (802.11n at mininum data rate, TCP ACK):
#
# (802.11n): min rate of 7.2 Mbps.
# TCP ACK: 40 + 48 Bytes = 88 Bytes. Total size in bits is 88*8 + 6 = 710 (we add the 6-bit tail)
# No. bits per OFDM symbols: (No. bits per data symbol)(Encoding Rate)(No. channels) = (1)(1/2)(52) = 26 bits.
# Therefore the no. of OFDM symbols needed is: (710/26) = 27.3 -> 28 symbols. Symbol duration for 802.11n is 3.6 us.
# Therefore the time taken for the transmission is: (28)(3.6 us) = 100.8 us
#
# Example calculation 8 (802.11n at mininum data rate):
#
# (802.11n): min rate of 7.2 Mbps.
# 1548 Bytes for 802.11n frames. This is equal to 1548*8 + 6 = 12390 bits.
# No. of bits per OFDM symbol: (No. bits per data symbol)(Encoding Rate)(No. channels) = (1)(1/2)(52) = 26 bits
# Therefore the no. of OFDM symbols needed is: (12390/26) = 476.5 -> 477 symbols. Symbol duration for 802.11n is 3.6 us.
# Therefore the time taken for transmission is: (477)(3.6 us) = 1717.2 us
#
# Example calculation 9 (802.11n at maximum data rate, 4 spatial streams):
#
# (802.11n): max rate of 600 Mbps.
# 1548 Bytes for 802.11n frames. This is equal to 1548*8 + 6 = 12390 bits.
# Maximum of 4 spatial streams. Maximum of 40 MHz channels
# No. of bits in OFDM symbol: (No. bits per data symbol)(Encoding Rate)(No. channels)(No. spatial streams) = (6)(5/6)(108)(4) = 2160 bits.
# Therefore the no. of OFDM symbols needed is: (12390/2160) = 5.73 -> 6 symbols. Symbol duration for 802.11n is 3.6 us.
# Therefore the time taken for this transaction is: (6)(3.6 us) = 21.6 us
#
# Example calculation 10 (802.11ax at minimum data rate, 8 spatial streams, data):
#
# (802.11ax): 8 spatial streams.
# No. of bits in OFDM symbol: (No. bits per data symbol)(Encoding Rate)(No. channels)(No. spatial streams) = (1)(1/2)(1960)(8) = 7840 bits.
# 1548 Bytes for 802.11ax frames. This is equal to 1548*8 + 6 = 12390 bits.
# Therefore the no. of OFDM symbols needed is: (12390/7840) = 1.58 -> 2 symbols. Symbol duration for 802.11ax is 13.6 us.
# Therefore the time for this transmission is: (2)(13.6 us) = 27.2 us



# All the values in the dictionary below are in units of microseconds (us).
# CTS: time in us to send clear-to-send CTS frame
# RTS: time in us to send ready-to-send RTS frame
# SIFS: short inter-frame spacing duration in us
# DIFS: distributed inter-frame spacing duration in us
# ACK: acknowledgement transmission time in us
# Preamble: time to transmit preamble in us
# tcpACK: time to transmit TCP ACK in us
# 3 SS: 3 spatial streams
# 4 SS: 4 spatial streams
# 8 SS: 8 spatial streams
# Data: time in us to send either 1542 Bytes (802.11a/g frames) or 1548 Bytes (802.11n/ac/ax frames)

wlanOptions = {
    "802.11a": {"Maximum rate": {
        "CTS": 4,
        "RTS": 4,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 4,
        "Data": 232,
        "Preamble": 20,
        "tcpACK": 16
    },
    "Minimum rate": {
        "CTS": 20,
        "RTS": 28,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 20,
        "Data": 2060,
        "Preamble": 20,
        "tcpACK": 112
        }
    },
    "802.11g": {"Maximum rate": {
        "CTS": 10,
        "RTS": 10,
        "SIFS": 10,
        "DIFS": 28,
        "ACK": 10,
        "Data": 238,
        "Preamble": 20,
        "tcpACK": 22
    },
    "Minimum rate": {
        "CTS": 26,
        "RTS": 34,
        "SIFS": 10,
        "DIFS": 28,
        "ACK": 26,
        "Data": 2063,
        "Preamble": 20,
        "tcpACK": 118       
        }
    },
    "802.11n": {"Maximum rate": {
        "CTS": 3.6,
        "RTS": 3.6,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 3.6,
        "Data": 172.8,
        "Preamble": 20,
        "tcpACK": 10.8
    },
    "Minimum rate": {
        "CTS": 18,
        "RTS": 25.2,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 18,
        "Data": 1717.2,
        "Preamble": 20,
        "tcpACK": 100.8       
    },
    "Spatial stream Info.": {
        "4 SS": {"Preamble": 46, "tcpACK": 3.6, "Data at max rate": 21.6, "Data at min rate": 208.8, "CTS at min rate": 3.6, "RTS at min rate": 3.6, "ACK at min rate": 3.6,  "tcpACK at min rate": 14.4}
        }
    },
    "802.11ac": {"Maximum rate": {
        "CTS": 3.6,
        "RTS": 3.6,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 3.6,
        "Data": 129.6,
        "Preamble": 20,
        "tcpACK": 10.8
    },
    "Minimum rate": {
        "CTS": 18,
        "RTS": 25.2,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 18,
        "Data": 1717.2,
        "Preamble": 20,
        "tcpACK": 100.8 
    },
    "Spatial stream Info.": {
        "3 SS": {"Preamble": 56.8, "tcpACK": 3.6, "Data at max rate": 10.8, "Data at min rate": 129.6, "CTS at min rate": 3.6, "RTS at min rate": 3.6, "ACK at min rate": 3.6, "tcpACK at min rate": 10.8},
        "8 SS": {"Preamble": 92.8, "tcpACK": 3.6, "Data at max rate": 3.6, "Data at min rate": 25.2, "CTS at min rate": 3.6, "RTS at min rate": 3.6, "ACK at min rate": 3.6}
        }
    },
    "802.11ax": {"Maximum rate": {
        "CTS": 13.6,
        "RTS": 13.6,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 13.6,
        "Data": 95.2,
        "Preamble": 20,
        "tcpACK": 13.6
    },
    "Minimum rate": {
        "CTS": 27.2,
        "RTS": 27.2,
        "SIFS": 16,
        "DIFS": 34,
        "ACK": 27.2,
        "Data": 1441.6,
        "Preamble": 20,
        "tcpACK": 95.2
    },
    "Spatial stream Info.": {
        "8 SS": {"Preamble": 92.8, "tcpACK": 13.6, "Data at max rate": 13.6, "Data at min rate": 27.2, "CTS at min rate": 13.6, "RTS at min rate": 13.6, "ACK at min rate": 13.6}
        }
    }
}

displayOptions = {
    1: "802.11a",
    2: "802.11g",
    3: "802.11n",
    4: "802.11ac",
    5: "802.11ax"
}

protocols = { #  other protocols could easily be added here in the future
    1: "UDP",
    2: "TCP"
}

# Function to work out the time to send a packet in the case of UDP being used:
def udp(difs, preamble, rts, cts, sifs, data, ack):
    timeToSend = difs + preamble + rts + sifs + preamble + cts + sifs + preamble + data + sifs + preamble + ack
    return timeToSend

# Function to work out the time to send a packet in the case of TCP being used:
def tcp(difs, preamble, rts, cts, sifs, data, ack, tcpack):
    timeToSend = tcpack + data + 2*ack + 2*cts + 2*rts + 2*difs + 6*sifs + 8*preamble
    return timeToSend

# Some print-out messages that our program will use:
welcomeMsg = """Welcome. This program allows a user to see the MAC throughput in both
normal and best-case scenarios for various 802.11 IEEE WLAN standards.\n\n"""
endQuestion = """\nWould you like to investigate another 802.11 standard? [y/n]"""
goodbyeMsg = """\n\nThanks and goodbye!"""
invalidOptionMsg = "Please enter a valid option."

# Some variables that will be used in the computation stage:
packetSize = 1500 # packet size in Bytes
transferSize = 15000000000 # the amount of Bytes for transfer
numPackets = transferSize/packetSize # the number of packets for transfer

# Begin:
print(welcomeMsg) # print the welcome message once at the start
userDone = False # a boolean variable to flag if the user is done or not
while (userDone == False):
    numOptions = len(displayOptions) # number of options (number of keys in displayOptions dictionary)
    print("The following options are available:\n")
    for option in range(1, numOptions+1):
        print(f"{option}: {displayOptions[option]}\n")
    print("Please enter the option number you want to investigate:\n")
    validOption = False # only set to True when user has chosen a valid option
    while (validOption == False):
        optionNum = int(input()) # take the user's input, and cast it to an int
        if optionNum not in range(1, numOptions+1):
            print(invalidOptionMsg)
        else:
            validOption = True
    chosenStandard = displayOptions[optionNum] # the IEEE 802.11 standard selected by the user
    print(f"\nWould you like to choose the maximum or minimum data rate for the {chosenStandard} standard?")
    print("\n1: Maximum data rate\n2: Minimum data rate\n")
    validOption = False
    while (validOption == False):
        optionNum = int(input()) # take the user's input, and cast it to an int
        if optionNum not in range(1, 3): # user should only enter 1 or 2; range(1, 3) gives [1 2]
            print(invalidOptionMsg)
        else:
            validOption = True
    if (optionNum == 1):
        chosenDataRate = "max"
    else:
        chosenDataRate = "min"
    print("\nWhich of the protocols listed below would you like to use?\n")
    numOptions = len(protocols) # just defining this to hopefully improve readability
    for option in range(1, numOptions+1):
        print(f"{option}: {protocols[option]}\n")
    validOption = False
    while (validOption == False):
        optionNum = int(input()) # take the user's input, and cast it to an int
        if optionNum not in range(1, numOptions+1):
            print(invalidOptionMsg)
        else:
            validOption = True
    chosenProtocol = protocols[optionNum] # assign the chosen protocol to this variable for use later on
    # Computation stage:
    if (chosenDataRate == "max"):
        schemeDetails = wlanOptions[chosenStandard]["Maximum rate"]
    else:
        schemeDetails = wlanOptions[chosenStandard]["Minimum rate"]
    # Let's read in the various values needed for the calculations:
    CTS = schemeDetails["CTS"]
    RTS = schemeDetails["RTS"]
    SIFS = schemeDetails["SIFS"]
    DIFS = schemeDetails["DIFS"]
    ACK = schemeDetails["ACK"]
    data = schemeDetails["Data"]
    preamble = schemeDetails["Preamble"]
    tcpACK = schemeDetails["tcpACK"]
    if (chosenProtocol == "UDP"):
        timeToSend = udp(DIFS, preamble, RTS, CTS, SIFS, data, ACK)
    elif (chosenProtocol == "TCP"):
        timeToSend = tcp(DIFS, preamble, RTS, CTS, SIFS, data, ACK, tcpACK)
    throughput = (12000)/(timeToSend) # 12000 bits divided by the time to send
    print(f"\n\tThe time to send a packet is {timeToSend} microseconds")
    print(f"\n\tTo send {transferSize} Bytes or {numPackets} packets takes: {numPackets*timeToSend/1e6} seconds")
    print(f"\n\tAnd the throughput is {throughput} Mbps")
    if (chosenStandard == "802.11n"):
        spatialStreamDetails = wlanOptions[chosenStandard]["Spatial stream Info."]
        preamble4SS = spatialStreamDetails["4 SS"]["Preamble"]
        tcpACK4SS = spatialStreamDetails["4 SS"]["tcpACK"]
        if (chosenDataRate == "max"):
            data4SS = spatialStreamDetails["4 SS"]["Data at max rate"]
        else: # some small differences when operating at the min rate
            data4SS = spatialStreamDetails["4 SS"]["Data at min rate"]
            CTS4SS = spatialStreamDetails["4 SS"]["CTS at min rate"]
            RTS4SS = spatialStreamDetails["4 SS"]["RTS at min rate"]
            ACK4SS = spatialStreamDetails["4 SS"]["ACK at min rate"]
            tcpACK4SS = spatialStreamDetails["4 SS"]["tcpACK at min rate"]
        if (chosenProtocol == "UDP"):
            timeToSend = udp(DIFS, preamble4SS, RTS4SS, CTS4SS, SIFS, data4SS, ACK4SS)
        elif (chosenProtocol == "TCP"):
            timeToSend = tcp(DIFS, preamble4SS, RTS4SS, CTS4SS, SIFS, data4SS, ACK4SS, tcpACK4SS)
        print("\n\nAnd using a 40 MHz channel with 4 spatial streams and a bitrate of 600 Mbps:\n")
        throughput = (12000)/(timeToSend) # 12000 bits divided by the time to send
        print(f"\n\tThe time to send a packet is {timeToSend} microseconds")
        print(f"\n\tTo send {transferSize} Bytes or {numPackets} packets takes: {numPackets*timeToSend/1e6} seconds")
        print(f"\n\tAnd the throughput is {throughput} Mbps")
    elif (chosenStandard == "802.11ac"):
        spatialStreamDetails = wlanOptions[chosenStandard]["Spatial stream Info."]
        preamble3SS = spatialStreamDetails["3 SS"]["Preamble"]
        preamble8SS = spatialStreamDetails["8 SS"]["Preamble"]
        tcpACK3SS = spatialStreamDetails["3 SS"]["tcpACK"]
        tcpACK8SS = spatialStreamDetails["8 SS"]["tcpACK"]
        if (chosenDataRate == "max"):
            data3SS = spatialStreamDetails["3 SS"]["Data at max rate"]
            data8SS = spatialStreamDetails["8 SS"]["Data at max rate"]
        else:
            data3SS = spatialStreamDetails["3 SS"]["Data at min rate"]
            CTS3SS = spatialStreamDetails["3 SS"]["CTS at min rate"]
            RTS3SS = spatialStreamDetails["3 SS"]["RTS at min rate"]
            ACK3SS = spatialStreamDetails["3 SS"]["ACK at min rate"]
            data8SS = spatialStreamDetails["8 SS"]["Data at min rate"]
            CTS8SS = spatialStreamDetails["8 SS"]["CTS at min rate"]
            RTS8SS = spatialStreamDetails["8 SS"]["RTS at min rate"]
            ACK8SS = spatialStreamDetails["8 SS"]["ACK at min rate"]
            tcpACK3SS = spatialStreamDetails["3 SS"]["tcpACK at min rate"]
        if (chosenProtocol == "UDP"):
            timeToSend3SS = udp(DIFS, preamble3SS, RTS3SS, CTS3SS, SIFS, data3SS, ACK3SS)
            timeToSend8SS = udp(DIFS, preamble8SS, RTS8SS, CTS8SS, SIFS, data8SS, ACK8SS)
        elif (chosenProtocol == "TCP"):
            timeToSend3SS = tcp(DIFS, preamble3SS, RTS3SS, CTS3SS, SIFS, data3SS, ACK3SS, tcpACK3SS)
            timeToSend8SS = tcp(DIFS, preamble8SS, RTS8SS, CTS8SS, SIFS, data8SS, ACK8SS, tcpACK8SS)
        throughput3SS = (12000)/(timeToSend3SS) # throughput when using 3 spatial streams
        throughput8SS = (12000)/(timeToSend8SS)
        print("\n\nAnd using an 80 MHz channel with 3 spatial streams and a bitrate of 1300 Mbps:\n")
        print(f"\n\tThe time to send a packet is {timeToSend3SS} microseconds")
        print(f"\n\tTo send {transferSize} Bytes or {numPackets} packets takes: {numPackets*timeToSend3SS/1e6} seconds")
        print(f"\n\tAnd the throughput is {throughput3SS} Mbps")
        print("\n\nWith a 160 MHz channel and 8 spatial streams and a bitrate of 6933.3 Mbps:\n")
        print(f"\n\tThe time to send a packet is {timeToSend8SS} microseconds")
        print(f"\n\tTo send {transferSize} Bytes or {numPackets} packets takes: {numPackets*timeToSend8SS/1e6} seconds")
        print(f"\n\tAnd the throughput is {throughput8SS} Mbps")
    elif (chosenStandard == "802.11ax"):
        spatialStreamDetails = wlanOptions[chosenStandard]["Spatial stream Info."]
        preamble8SS = spatialStreamDetails["8 SS"]["Preamble"]
        tcpACK8SS = spatialStreamDetails["8 SS"]["tcpACK"]
        if (chosenDataRate ==  "max"):
            data8SS = spatialStreamDetails["8 SS"]["Data at max rate"]
        else: # slightly different values for these quantities when using the min data rate of 8.6 Mbps
            data8SS = spatialStreamDetails["8 SS"]["Data at min rate"]
            CTS8SS = spatialStreamDetails["8 SS"]["CTS at min rate"]
            RTS8SS = spatialStreamDetails["8 SS"]["RTS at min rate"]
            ACK8SS = spatialStreamDetails["8 SS"]["ACK at min rate"]
        if (chosenProtocol == "UDP"):
            timeToSend8SS = udp(DIFS, preamble8SS, RTS8SS, CTS8SS, SIFS, data8SS, ACK8SS)
        elif (chosenProtocol == "TCP"):
            timeToSend8SS = tcp(DIFS, preamble8SS, RTS8SS, CTS8SS, SIFS, data8SS, ACK8SS, tcpACK8SS)
        throughput8SS = (12000)/(timeToSend8SS)
        print("\n\nWith a 160 MHz channel and 8 spatial streams and a bitrate of 9607.8 Mbps:\n")
        print(f"\n\tThe time to send a packet is {timeToSend8SS} microseconds")
        print(f"\n\tTo send {transferSize} Bytes or {numPackets} packets takes: {numPackets*timeToSend8SS/1e6} seconds")
        print(f"\n\tAnd the throughput is {throughput8SS} Mbps")
    print(endQuestion)
    answer = input()
    if (answer == "y"):
        print("") # skip to next line as want the next printout to be apart from the user's response in the console
        continue
    else:
        print(goodbyeMsg)
        userDone = True
