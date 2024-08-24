import requests
import pandas as pd

def get_spotify_token(client_id, client_secret):
    """
    Function to get Spotify access token using client credentials flow.
    """
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data.get('access_token')

def search_track(track_name, artist_name, token):
    """
    Function to search for a track and get its ID.
    """
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    json_data = response.json()
    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except (KeyError, IndexError):
        return None

def get_track_details(track_id, token):
    """
    Function to get track details, specifically the image URL.
    """
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    json_data = response.json()
    try:
        image_url = json_data['album']['images'][0]['url']
        return image_url
    except (KeyError, IndexError):
        return None

# Your Spotify API Credentials
client_id = '71d8ee89da2f4d379c8f5654dec790e4'
client_secret = '7e052faeff1f446d9cc1cef951067886'

# Get Access Token
access_token = get_spotify_token(client_id, client_secret)

# Read your DataFrame (replace 'your_file.csv' with the path to your CSV file)
df_spotify = pd.read_csv(r'C:\Users\bmish\Spotify Project\spotify-2023.csv', encoding='ISO-8859-1')

# Loop through each row to get track details and add to DataFrame
for i, row in df_spotify.iterrows():
    track_id = search_track(row['track_name'], row['artist(s)_name'], access_token)
    if track_id:
        image_url = get_track_details(track_id, access_token)
        if image_url:
            df_spotify.at[i, 'image_url'] = image_url

# Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
df_spotify.to_csv('finalupdated_file.csv', index=False)
