from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
from youtube_transcript_api._utils import _get_transcript_json

# Patch headers để fake trình duyệt
import requests
requests.utils.default_headers = lambda: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Transcript API is live!'

@app.route('/transcript')
def transcript():
    video_id = request.args.get('v')
    lang = request.args.get('lang', 'en')
    try:
        result = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return jsonify(result)
    except YouTubeRequestFailed as e:
        return jsonify({'error': 'YouTube blocked the request. Try again later or from a different IP.', 'details': str(e)}), 429
    except Exception as e:
        return jsonify({'error': str(e)}), 400
