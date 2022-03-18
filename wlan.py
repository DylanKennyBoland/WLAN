#!/usr/bin/env python3

# Tsymbol: the OFDM symbol duration
# SIFS: Short Inter-frame Spacing
# maxRate: the maximum data rate in Mbps
# minRate: the minimum data rate in Mbps
# Nbits maxRate: the number of bits/symbol at maximum data rate
# Nbits minRate: the number of bits/symbol at minimum data rate
wlanOptions = {
    "802.11a": {"maxRate": 54, "minRate": 6, "Tsymbol": 4, "SIFS": 10, "Nbits maxRate": 6, "Nbits minRate": 1},
    "802.11g": {"maxRate": 54, "minRate": 6, "Tsymnol": 4, "SIFS": 10, "Nbits maxRate": 6, "Nbits minRate": 1},
    "802.11n": {"maxRate": 72.2, "minRate": 7.2, "Tsymbol": 3.6, "SIFS": 16, "Nbits maxRate": 8, "Nbits minRate": 1},
    "802.11ac": {"maxRate": 96.3, "minRate": 7.2, "Tsymbol": 3.6, "SIFS": 16, "Nbits maxRate": 8, "Nbits minRate": 1},
    "802.11ax": {"maxRate": 143.4, "minRate": 8.6, "Tsymbol": 13.6, "SIFS": 16, "Nbits maxRate": 10, "Nbits minRate": 1}
}

displayOptions = {
    1: "802.11a",
    2: "802.11g",
    3: "802.11n",
    4: "802.11ac",
    5: "802.11ax"
}

welcomeMsg = """Welcome. This program allows a user to see the MAC throughput in both
normal and best-case scenarios for various 802.11 IEEE WLAN standards.\n\n"""

numOptions = len(displayOptions) # number of options (number of keys in displayOptions dictionary)
userDone = False # a boolean variable to flag if the user is done or not

print(welcomeMsg) # print the welcome message once at the start

while (userDone == False):
    print("The following options are available:\n")
    for option in range(1, numOptions+1):
        print(f"{option}: {displayOptions[option]}\n")
    print("Please enter the option number you want to investigate:\n")
    validOption = False # only set to True when user has chosen a valid option
    while (validOption == False):
        optionNum = int(input()) # take the user's input, and cast it to an int
        if optionNum not in range(1, numOptions+1):
            print("Please enter a valid option.")
        else:
            validOption = True
    chosenStandard = displayOptions[optionNum] # the IEEE 802.11 selected by the user
    print(f"\nWould you like to choose the maximum or minimum data rate for the {chosenStandard} standard?")
    print("\n1: Maximum data rate\n2: Minimum data rate\n")
    validOption = False
    while (validOption == False):
        optionNum = int(input()) # take the user's input, and cast it to an int
        if optionNum not in range(1, 3):
            print("Please enter a valid option.")
        else:
            validOption = True
    userDone = True

