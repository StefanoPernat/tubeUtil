from pytube import YouTube, Playlist
from threading import Thread
import os
import argparse


def create_youtube_link(video_id):
    return "https://www.youtube.com/watch?v=" + video_id


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = round((bytes_downloaded / total_size) * 100, 2)
    print("Downloaded: " + str(percentage) + "%")


def perform_download(video_url, output_path):
    yt = YouTube(video_url)

    # register on_progress_callback so we can get the progress percentage
    yt.register_on_progress_callback(on_progress)

    try:
        print("Downloading: " + yt.title)
        yt.streams.get_highest_resolution().download(output_path=output_path)
    except Exception:
        print("Error downloading video: " + video_url)
    print("Downloaded video " + video_url)


def get_playlist_details(playlist_id):
    playlist = Playlist(
        "https://www.youtube.com/playlist?list=" + playlist_id)

    return playlist.title, playlist.video_urls


def create_output_path(type):
    output_path = os.path.join(os.getcwd(), type)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


if __name__ == "__main__":
    thread_list = []

    # add command line flags to switch between playlist and single video
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        type=str,
        required=False,
        help="Enter a YouTube playlist ID to download all videos in the playlist")
    parser.add_argument(
        "-v",
        type=str,
        required=False,
        help="Enter a YouTube video ID to download")
    args = parser.parse_args()

    # if playlist flag is set, create directory and download all videos in the playlist
    if args.p is not None:
        output_path = create_output_path("playlists")
        playlist_id = args.p
        title, video_urls = get_playlist_details(playlist_id)
        print("Playlist title: " + title)
        playlist_dir = os.path.join(output_path, title)
        if not os.path.exists(playlist_dir):
            print("Creating directory: " + title)
            os.mkdir(playlist_dir)
            for video_url in video_urls:
                thread = Thread(target=perform_download,
                                args=(video_url, playlist_dir))
                thread_list.append(thread)
            for thread in thread_list:
                thread.start()
    elif args.v is not None:
        output_path = create_output_path("videos")
        video_id = args.v
        video_url = create_youtube_link(video_id)
        perform_download(video_url, output_path)
