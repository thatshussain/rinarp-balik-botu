import uuid

def get_mac_address():
    mac = uuid.getnode()
    return ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))

if __name__ == "__main__":
    mac_address = get_mac_address()
    print("Bilgisayarın MAC Adresi:", mac_address)
    
    input("Devam etmek için bir tuşa basın...")
