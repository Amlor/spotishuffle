import argparse, logging, random
from pathlib import Path
from typing import List, Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger("spotishuffle")
logging.basicConfig(level="WARN")

SCOPE = "user-library-read playlist-read-private playlist-modify-private"
LIMIT = 50
DEFAULT_CACHE_PATH = ".cache/spotishuffle_cache"


def shuffle(
    out_playlist_name: str, in_playlist_name: Optional[str], liked: bool = False
) -> None:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=SCOPE, cache_path=get_cache_path())
    )
    user_id = sp.current_user()["id"]

    if liked:
        track_uris = get_liked(sp)
    elif in_playlist_name is not None:
        track_uris = get_playlist(sp, in_playlist_name)
    else:
        raise Exception("Please choose either a playlist, or liked tracks")

    if len(track_uris) > 0:
        playlist = sp.user_playlist_create(user_id, out_playlist_name, public=False)
        playlist_id = playlist["id"]
        random.shuffle(track_uris)
        for chunk in chunks(track_uris, 100):
            sp.playlist_add_items(playlist_id, chunk)


def get_cache_path(custom_path: Optional[str] = None) -> str:
    path = DEFAULT_CACHE_PATH
    if custom_path is not None:
        path = custom_path
    return str(Path.home().joinpath(path))


def get_liked(sp) -> List[str]:
    all_track_uris = []

    offset = 0
    while True:
        tracks = sp.current_user_saved_tracks(limit=LIMIT, offset=offset)["items"]
        track_uris = [track["track"]["uri"] for track in tracks]
        if len(track_uris) > 0:
            all_track_uris.extend(track_uris)
            offset += LIMIT
        else:
            break

    return all_track_uris


def get_playlist(sp: spotipy.Spotify, in_playlist_name: str) -> List[str]:
    all_track_uris = []

    user_playlists = sp.current_user_playlists()
    input_playlist = None
    for playlist in user_playlists["items"]:
        if playlist["name"] == in_playlist_name:
            input_playlist = playlist
            break

    if input_playlist is not None:
        playlist_id = input_playlist["id"]
        offset = 0
        while True:
            tracks = sp.playlist_items(playlist_id, limit=LIMIT, offset=offset)["items"]
            track_uris = [track["track"]["uri"] for track in tracks]
            if len(track_uris) > 0:
                all_track_uris.extend(track_uris)
                offset += LIMIT
            else:
                break

    return all_track_uris


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def get_args():
    parser = argparse.ArgumentParser(
        description="Creates a playlist using shuffled tracks from another playlist or "
        "liked songs"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Target playlist name (required)"
    )

    playlist_conflict_group = parser.add_mutually_exclusive_group()
    playlist_conflict_group.add_argument(
        "-i",
        "--input",
        help="Source playlist name (the top playlist with this name \
        will be used)",
    )
    playlist_conflict_group.add_argument(
        "-l", "--liked", action="store_true", help="Liked songs (default)"
    )

    return parser.parse_args()


def as_script():
    args = get_args()
    shuffle(args.output, args.input, args.liked)


if __name__ == "__main__":
    as_script()
