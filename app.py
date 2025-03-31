from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

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
    except Exception as e:
        return jsonify({'error': str(e)}), 400
