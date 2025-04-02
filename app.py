from flask import Flask, request, send_file
from pytube import YouTube
import tempfile
import os
import subprocess

app = Flask(__name__)

@app.route('/audio', methods=['GET'])
def audio():
    vid = request.args.get('video_id')

    if not vid:
        return "Missing ?video_id", 400

    yt = YouTube(f"https://www.youtube.com/watch?v={vid}")

    with tempfile.TemporaryDirectory() as tmp:
        # Download audio only
        audio_path = yt.streams.filter(only_audio=True).first().download(tmp, "audio")

        # Convert to MP3 with ffmpeg
        mp3_path = os.path.join(tmp, "audio.mp3")
        subprocess.run(["ffmpeg", "-i", audio_path, "-vn", "-ab", "128k", "-y", mp3_path], check=True)

        # Return MP3 as response
        return send_file(mp3_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True)
