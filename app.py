from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
import requests
from yt_dlp import YoutubeDL

# 🛡️ Giả lập User-Agent để tránh bị chặn bởi Google
requests.utils.default_headers = lambda: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ YouTube Transcript API is running!'

def get_metadata(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'forcejson': True,
        'extract_flat': 'in_playlist',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Tùy trường hợp info['language'] có thể không có
        language = info.get('language', 'unknown')
        if language != 'en':
            return None

        return {
            'title': info.get('title'),
            'channel': info.get('channel'),
            'duration': info.get('duration'),  # giây
            'view_count': info.get('view_count'),
            'publish_date': info.get('upload_date'),  # yyyyMMdd
            'language': language
        }

@app.route('/transcript')
def get_transcript():
    video_id = request.args.get('v')
    lang = request.args.get('lang', 'en')

    if not video_id:
        return jsonify({'error': 'Missing video ID. Use ?v=VIDEO_ID'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        metadata = get_metadata(video_id)

        if metadata is None:
            return jsonify({'error': '❌ Only English videos are supported.'}), 400

        return jsonify({
            'transcript': transcript,
            'metadata': metadata
        })

    except YouTubeRequestFailed as e:
        return jsonify({'error': '❌ YouTube blocked the request.', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Railway truyền PORT động vào biến môi trường
    app.run(host='0.0.0.0', port=port)
