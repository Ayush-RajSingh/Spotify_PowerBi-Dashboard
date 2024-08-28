import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

# Set up Spotify API credentials
os.environ['SPOTIPY_CLIENT_ID'] = '8b8b4a4f96b14aa49ada749c5dcc255f'
os.environ['SPOTIPY_CLIENT_SECRET'] = '1777e4a68e284956afc19ea7960f19a7'

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Read the CSV file
df = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

# Function to search for a track and get its URL and album cover
def get_track_info(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_url = track['external_urls']['spotify']
        album_cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None
        return track_url, album_cover_url
    return None, None

# Add new columns for track URL and album cover URL
df['track_url'] = ''
df['album_cover_url'] = ''

# Update the DataFrame with track and album cover URLs
for index, row in tqdm(df.iterrows(), total=len(df), desc="Fetching URLs"):
    track_url, album_cover_url = get_track_info(row['track_name'], row['artist(s)_name'])
    df.at[index, 'track_url'] = track_url
    df.at[index, 'album_cover_url'] = album_cover_url

# Display the first few rows of the updated DataFrame
print(df[['track_name', 'artist(s)_name', 'track_url', 'album_cover_url']].head())

# Save the updated DataFrame to a new CSV file
df.to_csv('spotify-2023-with-urls.csv', index=False)
print("\
Updated CSV file saved as 'spotify-2023-with-urls.csv'")