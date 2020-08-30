# spotishuffle
Download spotify playlist, shuffle and save it to copy

# Before usage:
Set variables SPOTIPY_CLIENT_ID, SPOTIFYL_CLIENT_SECRET and SPOTIPY_REDIRECT_URI (you need to create an app in spotify developer dashboard https://developer.spotify.com/dashboard/)

This process might be improved in the future

# Usage:
spotishuffle.py [-h] -o OUTPUT [-i INPUT] [-l]

Creates a playlist using shuffled tracks from another playlist or liked songs

arguments:

  -h, --help    show this help message and exit

  -o OUTPUT, --output OUTPUT    Target playlist name (required)
  
  -i INPUT, --input INPUT    Source playlist name (not implemented yet)
  
  -l, --liked    Shuffle liked songs (default)
