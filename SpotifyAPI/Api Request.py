import requests
import base64
import json

# Spotify API credentials
client_id = 'DEINE_CLIENT_ID'
client_secret = 'DEIN_CLIENT_SECRET'

# Spotify API URLs
auth_url = 'https://accounts.spotify.com/api/token'
track_url = 'https://api.spotify.com/v1/tracks/'

def get_access_token(client_id, client_secret):
    # Encode client_id and client_secret in base64
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    # Prepare request headers and body
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'grant_type': 'client_credentials'
    }

    # Send request to Spotify API
    response = requests.post(auth_url, headers=headers, data=body)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print(f"Failed to get access token: {response.status_code}")
        return Nones

def get_track_info(track_id, access_token):
    # Prepare request headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # Send GET request to Spotify API for track information
    response = requests.get(f"{track_url}{track_id}", headers=headers)
    
    if response.status_code == 200:
        track_info = response.json()
        return track_info
    else:
        print(f"Failed to get track info: {response.status_code}")
        return None

# Main execution
if __name__ == '__main__':
    # Get the access token
    access_token = get_access_token(client_id, client_secret)
    
    if access_token:
        # Example track ID (replace with actual track ID)
        track_id = '3n3Ppam7vgaVa1iaRUc9Lp'
        
        # Get track info
        track_info = get_track_info(track_id, access_token)
        
        if track_info:
            # Print track details
            print("Track Title:", track_info['name'])
            print("Artist:", track_info['artists'][0]['name'])
            print("Album:", track_info['album']['name'])
    else:
        print("Failed to retrieve access token.")
