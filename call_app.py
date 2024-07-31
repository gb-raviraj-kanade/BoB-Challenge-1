import io
import subprocess
import uuid
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_silence, detect_leading_silence

from app.agent_call import Agent
from app.azure_utils.speech import speech_to_text, text_to_speech
from app.config import Config, AzureLanguages


app = Flask(__name__)
agent = None
audio_outputs = {}
audio_inputs = bytes()
read_start = 0
language = AzureLanguages.English

@app.route('/call')
def index():
    return render_template('index.html')

@app.route('/call/start_call', methods=['POST'])
def start_call():
    customer_id = request.json.get('customer_id')
    print(f"Starting call with customer {customer_id}")
    global agent, language
    agent = Agent(user_name=f"Customer{customer_id}")
    language = request.json.get('language')
    return jsonify({"message": f"Call started with customer {customer_id}"})

@app.route('/call/end_call', methods=['POST'])
def end_call():
    customer_id = request.json.get('customer_id')
    print(f"Ending call with customer {customer_id}")
    global agent
    agent.summarize()
    agent = None
    return jsonify({"message": f"Call ended with customer {customer_id}"})

@app.route('/call/saverecordedaudio', methods=['POST'])
def saverecordedaudio():
    audio_file = request.files['audio']
    pipe = subprocess.run(['ffmpeg', '-hide_banner', '-i', 'pipe:0', '-ar', '16000', '-ac', '1', '-f', 's16le', '-'], 
                          input=audio_file.stream.read(), 
                          stdout=subprocess.PIPE)
    translated_text = speech_to_text(pipe.stdout, AzureLanguages[language].value)
    if translated_text:
        return jsonify({'status': 'success', 'message': 'Audio received and processed successfully', 'user': translated_text})
    else:
        return jsonify({'status': 'error', 'message': 'Please Try Again'})
    
# @app.route('/call/saverecordedaudio', methods=['POST'])
# def saverecordedaudio():
#     global audio_inputs, read_start
#     audio_file = request.files['audio']
#     # Read the audio file as bytes
#     audio_bytes = audio_file.stream.read()
#     # Append the new chunk to the accumulated audio
#     audio_inputs += audio_bytes
#     try:
#         audio_seg = AudioSegment.from_file(io.BytesIO(audio_inputs), codec="opus")
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#     og_duration = audio_seg.duration_seconds
#     audio_seg = audio_seg[read_start*1000:]
#     # Detect silence in the accumulated audio
#     silence_chunks = detect_silence(audio_seg, Config.MinSilenceLength, Config.SilenceThreshold)
#     leading_silence = detect_leading_silence(audio_seg, Config.SilenceThreshold)
#     print(f"Leading Silence: {leading_silence}, Silence Chunks: {silence_chunks}")
#     # Remove leading silence from silence chunks
#     if leading_silence > 0 and silence_chunks:
#         silence_chunks.pop(0)
#     # If silence is detected, process the accumulated audio
#     if silence_chunks:
#         audio_seg.export("temp.wav", format="wav", parameters=["-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1"])
#         # audio_inputs = bytes()
#         read_start = og_duration
#         return jsonify({'status': 'success', 'message': 'Audio ready to be processed'})
#     # If no silence is detected, return a response indicating accumulation is ongoing
#     return jsonify({'status': 'pending', 'message': 'Accumulating audio chunks'})

@app.post('/call/get_response')
async def generate_response():
    model_reply = agent.chat(request.json.get("text"))
    print(model_reply)
    audio_uid = convert_text_to_voice(model_reply)
    return {'status': 'success', 'message': '', 'assistant': model_reply, 'audio_uid': audio_uid}

# @app.post('/call/get_response')
# async def generate_response():
#     audio_data = AudioSegment.from_wav("temp.wav")
#     audio_data = audio_data.set_frame_rate(16000)
#     audio_data = audio_data.set_channels(1)
#     audio_data = audio_data.raw_data
#     print("Running Speech to Text!!!")
#     translated_text = speech_to_text(audio_data)
#     if not translated_text:
#         return {'status': 'error', 'message': 'Please Try Again'}
#     print(translated_text)
#     try:
#         model_reply = agent.chat(translated_text)
#         print(model_reply)
#         audio_uid = convert_text_to_voice(model_reply)
#         return {'status': 'success', 'message': '', 'assistant': model_reply, 'audio_uid': audio_uid}
#     except Exception as err:
#         return {'status': 'error', 'message': str(err)}

@app.get('/call/fetch_audio/<uid>')
async def fetch_audio(uid):
    if uid not in audio_outputs:
        return f"Error: No audio found for uid '{uid}'", 404
    buffer = io.BytesIO(audio_outputs.pop(uid))
    return send_file(buffer, mimetype='audio/wav')

def convert_text_to_voice(text: str) -> str:
    audio_data = text_to_speech(text, AzureLanguages[language].value)
    UID = uuid.uuid4().hex
    audio_outputs[UID] = audio_data
    return UID

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=False)
