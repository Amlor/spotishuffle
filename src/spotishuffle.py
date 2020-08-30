import argparse, logging, random

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('spotishuffle')
logging.basicConfig(level='WARN')

scope = 'user-library-read playlist-modify-private'
limit = 50


def get_args():
    parser = argparse.ArgumentParser(description='Creates a playlist using shuffled tracks from another playlist or '
                                                 'liked songs')
    parser.add_argument('-o', '--output', required=True, help='Target playlist name (required)')
    parser.add_argument('-i', '--input', help='Source playlist name')
    parser.add_argument('-l', '--liked', action='store_true', help='Liked songs (default)')
    return parser.parse_args()


def main():
    args = get_args()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path='~/.cache/spotishuffle_cache'))
    user_id = sp.current_user()['id']

    if args.liked or args.input is None:
        track_uris = get_liked(sp)
    else:
        track_uris = get_playlist(sp, args)

    playlist = sp.user_playlist_create(user_id, args.output, public=False)
    playlist_id = playlist['id']
    random.shuffle(track_uris)
    for chunk in chunks(track_uris, 100):
        sp.playlist_add_items(playlist_id, chunk)


def get_liked(sp):
    offset = 0
    all_track_uris = []

    while True:
        tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
        track_uris = [track['track']['uri'] for track in tracks]
        if len(track_uris) > 0:
            all_track_uris.extend(track_uris)
            offset += limit
        else:
            break

    return all_track_uris


def get_playlist(sp, args):
    """TODO"""
    return []


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    main()
