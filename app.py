from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
from yt_dlp import YoutubeDL
import requests

# 🛡️ Giả lập User-Agent để tránh bị chặn bởi Google
requests.utils.default_headers = lambda: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ YouTube Transcript API with Metadata is running!'

@app.route('/transcript')
def get_transcript():
    video_id = request.args.get('v')
    lang = request.args.get('lang', 'en')

    if not video_id:
        return jsonify({'error': 'Missing video ID. Use ?v=VIDEO_ID'}), 400

    try:
        # Gọi transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

        # Gọi metadata bằng yt_dlp
        ydl_opts = {'quiet': True, 'skip_download': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)

        # Kiểm tra ngôn ngữ mô tả (title, v.v.) nếu cần lọc tiếng Anh
        if info.get("language") and info["language"] != "en":
            return jsonify({'error': 'Video is not in English (lang=' + info["language"] + ')'}), 400

        metadata = {
            'id': info.get('id'),
            'title': info.get('title'),
            'description': info.get('description'),
            'upload_date': info.get('upload_date'),
            'uploader': info.get('uploader'),
            'uploader_id': info.get('uploader_id'),
            'channel_id': info.get('channel_id'),
            'channel_url': info.get('channel_url'),
            'webpage_url': info.get('webpage_url'),
            'duration': info.get('duration'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'categories': info.get('categories'),
            'tags': info.get('tags'),
            'thumbnail': info.get('thumbnail'),
            'average_rating': info.get('average_rating'),
            'is_live': info.get('is_live'),
            'language': info.get('language')
        }

        return jsonify({
            'transcript': transcript,
            'metadata': metadata
        })

    except YouTubeRequestFailed as e:
        return jsonify({'error': '❌ YouTube blocked the transcript request.', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
