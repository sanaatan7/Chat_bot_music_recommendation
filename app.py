from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Spotify API 
SPOTIFY_CLIENT_ID = '1adb4eaf57f34a5397a3c69c29773ad9'  
SPOTIFY_CLIENT_SECRET = '67a02c67e6e14d91974dcf3624cdd185'  

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/', methods=['GET', 'POST'])
def home():
    bot_response = None
    song_data = []  # Initialize song_data as an empty list
    if request.method == 'POST':
        user_message = request.form['user_message']
        
        # Search for tracks based on user's mood
        try:
            results = sp.search(q=f'mood:{user_message}', type='track', limit=3)
            print("API Response:", results)  # Debug: Print the API response
            tracks = results['tracks']['items']
            
            if tracks:
                print("Tracks Found:", tracks)  # Debug: Print the tracks
                # Get the top 3 tracks with their links and album art
                for track in tracks:
                    song_name = track['name']
                    song_url = track['external_urls']['spotify']  # Spotify song link
                    album_art = track['album']['images'][0]['url'] if track['album']['images'] else 'https://via.placeholder.com/100'  # Fallback for missing album art
                    song_data.append((song_name, song_url, album_art))  # Store name, link, and art
                
                bot_response = f"Bot: Here are some {user_message} songs for you:"
            else:
                bot_response = f"Bot: Sorry, I couldn't find any {user_message} songs."
        except Exception as e:
            print("Error:", e)  # Debug: Print any errors
            bot_response = f"Bot: Oops! Something went wrong: {str(e)}"

    return render_template('chat.html', bot_response=bot_response, song_data=song_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)