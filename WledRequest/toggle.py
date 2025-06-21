from argparse import ArgumentParser
from urllib3 import PoolManager
from json import dumps, loads
from ipaddress import IPv4Address, AddressValueError

class WLEDCALL:
    def __init__(self, IP="192.168.2.100"):
        try:
            IPv4Address(IP)
        except AddressValueError:
            print("Fehler: Ungültige IPv4-Adresse angegeben bei -i.")
            exit()

        self.url:str = f"http://{IP}/json/state"
        self.request = PoolManager().request

    def get_state(self) -> dict:
        response = self.request('GET', self.url)
        return loads(response.data.decode('utf-8'))

    def toggle(self, debug=False) -> None:
        new_state = not self.get_state().get("on", False)

        payload = {"on": new_state}
        response = self.request(
            'POST',
            self.url,
            body=dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        if debug:
            print("{Response status:", response.status , ", New state:", "ON" if new_state else "OFF", "}", sep="")

def main():
    parser = ArgumentParser(description="Toggle WLED on/off")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-i", "--ipv4", help="Enter IP address of WLED device")
    args = parser.parse_args()

    WLEDCALL(IP=args.ipv4).toggle(debug=args.debug) if args.ipv4 else WLEDCALL().toggle(debug=args.debug)

if __name__ == "__main__":
    main()
