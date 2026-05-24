import os
import yt_dlp
from pyrogram import Client


def progress_callback(current, total):
    percent = (current / total) * 100
    print(f"Upload progress: {percent:.2f}%")


def main():
    video_filename = None

    try:
        tg_string_session = os.environ['TG_STRING_SESSION']
        tg_api_id = int(os.environ['TG_API_ID'])
        tg_api_hash = os.environ['TG_API_HASH']
        video_url = os.environ['VIDEO_URL']
        target_chat_id = int(os.environ['TARGET_CHAT_ID'])

        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_filename = ydl.prepare_filename(info)

        app = Client(
            name="upload_bot",
            api_id=tg_api_id,
            api_hash=tg_api_hash,
            session_string=tg_string_session
        )

        with app:
            app.send_video(
                chat_id=target_chat_id,
                video=video_filename,
                progress=progress_callback,
                progress_args=()
            )
            print("Video uploaded successfully")

    except Exception as e:
        print(f"Error: {e}")
        raise

    finally:
        if video_filename and os.path.exists(video_filename):
            os.remove(video_filename)
            print(f"Deleted local file: {video_filename}")


if __name__ == "__main__":
    main()