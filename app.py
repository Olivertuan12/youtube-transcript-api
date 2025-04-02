from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
import requests

# 🛡️ Giả lập User-Agent để tránh bị chặn bởi Google
requests.utils.default_headers = lambda: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ YouTube Transcript API is running!'

@app.route('/transcript')
def get_transcript():
    video_id = request.args.get('v')
    lang = request.args.get('lang', 'en')

    if not video_id:
        return jsonify({'error': 'Missing video ID. Use ?v=VIDEO_ID'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return jsonify(transcript)
    except YouTubeRequestFailed as e:
        return jsonify({'error': '❌ YouTube blocked the request.', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Railway truyền PORT động vào biến môi trường
    app.run(host='0.0.0.0', port=port)
