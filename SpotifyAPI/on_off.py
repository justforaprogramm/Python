import os
from typing import Optional
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class SpotifyController:
    """A controller to manage Spotify playback states using the Spotipy library.

    This class automatically loads authentication credentials from environment
    variables and provides methods to toggle, play, and pause music.
    """

    def __init__(self) -> None:
        """Initializes the SpotifyController and authenticates with the API."""
        load_dotenv()
        self._scope: str = "user-modify-playback-state user-read-playback-state"
        self.sp: spotipy.Spotify = self._authenticate()

    def _authenticate(self) -> spotipy.Spotify:
        """Authenticates the user via Spotify OAuth.

        Returns:
            spotipy.Spotify: An authenticated Spotify client instance.
        """
        return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self._scope))

    def toggle_playback(self) -> None:
        """Toggles the current playback state.

        If music is currently playing, it will be paused. If it is paused,
        the playback will be resumed.

        Raises:
            Exception: If communication with the Spotify API fails.
        """
        try:
            playback_status: Optional[dict] = self.sp.current_playback()

            if playback_status is None:
                print(
                    "No active device found. Please open Spotify on "
                    "your PC or smartphone!"
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
    # Create an instance of the controller and run the toggle command
    controller = SpotifyController()
    controller.toggle_playback()