import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), 
                                       region=os.getenv("AZURE_REGION"))

def speech_to_text(audio_data: bytes, language: str) -> str | None:
    audio_stream = speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat())
    audio_stream.write(audio_data)
    audio_stream.close()
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
    speech_config.speech_recognition_language = language
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech Recognition canceled: {}".format(result.cancellation_details.reason))
        return None

def text_to_speech(text: str, language: str) -> bytes | None:
    output_stream = speechsdk.audio.PullAudioOutputStream()
    audio_config = speechsdk.audio.AudioOutputConfig(stream=output_stream)
    speech_config.speech_synthesis_language = language
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech synthesis canceled: {}".format(result.cancellation_details.reason))
        return None