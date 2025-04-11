import urllib3
import json
import argparse

class WLEDCALL:
    def __init__(self):
        self.url = f"http://192.168.2.115/json/state"
        self.http = urllib3.PoolManager()

    def get_state(self):
        response = self.http.request('GET', self.url)
        return json.loads(response.data.decode('utf-8'))

    def toggle(self, debug=False):
        state = self.get_state()
        new_state = not state.get("on", False)

        payload = {"on": new_state}
        response = self.http.request(
            'POST',
            self.url,
            body = json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        if debug:
            print("Response status:", response.status)
            print("New state:", "ON" if new_state else "OFF")

        return new_state

def main():
    parser = argparse.ArgumentParser(description="Toggle WLED on/off")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    wled = WLEDCALL()
    wled.toggle(debug=args.debug)

if __name__ == "__main__":
    main()
