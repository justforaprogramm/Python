import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
from urllib.parse import parse_qs, urlparse
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Global variable to hold the captured authorization code
_captured_auth_code: Optional[str] = None


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler to catch the Spotify redirect callback."""

    def do_get(self) -> None:
        """Handles the GET request sent by Spotify's redirect."""
        global _captured_auth_code
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Parse the URL to extract the 'code' parameter
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if "code" in query_params:
            _captured_auth_code = query_params["code"][0]
            html_response = """
            <html>
                <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                    <h2 style="color: #1DB954;">Authentication Successful!</h2>
                    <p>You can close this window and return to your terminal.</p>
                </body>
            </html>
            """
            self.wfile.write(html_response.encode("utf-8"))
        else:
            self.wfile.write(b"Authentication failed. No code found.")

    def log_message(self, format: str, *args: any) -> None:
        """Suppresses standard server logs in the terminal."""
        return


class SpotifyController:
    """A controller to manage Spotify playback with automatic authentication.

    This class handles automatic local redirect trapping for environments like
    Dev Containers where standard browser redirect flows might fail.
    """

    def __init__(self) -> None:
        """Initializes the SpotifyController and loads environment variables."""
        load_dotenv()
        self._scope: str = "user-modify-playback-state user-read-playback-state"
        self._client_id: str = os.getenv("SPOTIPY_CLIENT_ID", "")
        self._client_secret: str = os.getenv("SPOTIPY_CLIENT_SECRET", "")
        self._redirect_uri: str = os.getenv(
            "SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback"
        )

        self._oauth = SpotifyOAuth(
            client_id=self._client_id,
            client_secret=self._client_secret,
            redirect_uri=self._redirect_uri,
            scope=self._scope,
            open_browser=False,  # Headless mode for container compatibility
        )
        self.sp: spotipy.Spotify = self._authenticate()

    def _start_local_server(self) -> None:
        """Starts a temporary HTTP server to intercept the redirect code."""
        # Parse port from redirect URI (default to 8888)
        parsed_uri = urlparse(self._redirect_uri)
        port = parsed_uri.port if parsed_uri.port else 8888

        server = HTTPServer(("0.0.0.0", port), CallbackHandler)
        print(f"\n[Waiting] Listening for Spotify response on port {port}...")
        # Serve exactly one request (the callback redirection) then stop
        server.handle_request()

    def _authenticate(self) -> spotipy.Spotify:
        """Handles manual token entry to bypass broken port forwarding."""
        token_info = self._oauth.validate_token(
            self._oauth.cache_handler.get_cached_token()
        )

        if not token_info:
            auth_url = self._oauth.get_authorize_url()
            print("\n" + "=" * 60)
            print("MANUAL AUTHENTICATION")
            print("=" * 60)
            print(f"1. Open this link in your host browser:\n\n{auth_url}\n")
            print("2. Log in, click 'Agree'.")
            print(
                "3. You will land on a broken localhost page. Copy that "
                "WHOLE URL from the address bar."
            )
            print("=" * 60)

            # Ask you directly to paste the URL into the terminal
            redirected_url = input("\nPaste the full redirect URL here: ")

            # Extract the code from the URL manually
            parsed_url = urlparse(redirected_url)
            query_params = parse_qs(parsed_url.query)

            if "code" in query_params:
                auth_code = query_params["code"][0]
                token_info = self._oauth.get_access_token(
                    auth_code, as_dict=False
                )
            else:
                print("[Error] No code found in the URL you pasted.")
                sys.exit(1)

        return spotipy.Spotify(auth_manager=self._oauth)

    def toggle_playback(self) -> None:
        """Toggles the current playback state between Play and Pause."""
        try:
            playback_status: Optional[dict] = self.sp.current_playback()

            if playback_status is None:
                print(
                    "\nNo active device found. Please open Spotify on your "
                    "physical machine (PC/Mobile) and play a track first!"
                )
                return

            if playback_status["is_playing"]:
                print("Music is playing -> Pausing...")
                self.sp.pause_playback()
                print("Successfully paused!")
            else:
                print("Music is paused -> Resuming...")
                self.sp.start_playback()
                print("Playback resumed!")

        except Exception as e:
            print(f"Error controlling playback: {e}")


if __name__ == "__main__":
    controller = SpotifyController()
    controller.toggle_playback()