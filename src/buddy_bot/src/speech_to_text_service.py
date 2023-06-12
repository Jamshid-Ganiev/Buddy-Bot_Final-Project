#!/usr/bin/env python3

import rospy
import requests
import smtplib, ssl
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import json
from buddy_bot.srv import SpeechToText, SpeechToTextResponse

# Email Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'jamesganiev227@gmail.com'
EMAIL_PASSWORD = 'PASSWORD'
EMAIL_RECEIVER = '12200335@inha.edu'

# Whisper API Configuration
WHISPER_API_KEY = 'WHISPER_API_KEY'
WHISPER_API_URL = 'https://transcribe.whisperapi.com'

AUDIO_DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'audioData')
AUDIO_TRANSCRIPTION_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'audioTranscription')


def record_audio(filename, duration, fs=44100):
    print("Recording started...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    # Save the recorded audio in the 'audioData' directory
    filepath = os.path.join(AUDIO_DATA_DIR, filename)
    wav.write(filepath, fs, np.int16(recording))
    print("Recording finished.")
    return filepath  # Return the filepath for later use


def transcribe_audio(filepath):
    headers = {
        'Authorization': f'Bearer {WHISPER_API_KEY}',
        'Accept': 'application/vnd.whisper.transcript+json'
    }
    file = {'file': open(filepath, 'rb')}
    data = {
        "fileType": "wav",
        "diarization": "false",
        "numSpeakers": "1",
        "language": "en",
        "task": "transcribe"
    }
    response = requests.post(WHISPER_API_URL, headers=headers, files=file, data=data)
    transcription = response.text
    # Save the transcription in the 'audioTranscription' directory
    transcription_filename = os.path.splitext(os.path.basename(filepath))[0] + '.txt'
    transcription_filepath = os.path.join(AUDIO_TRANSCRIPTION_DIR, transcription_filename)
    with open(transcription_filepath, 'w') as f:
        f.write(json.dumps(transcription))
    return transcription

def send_email(transcription):
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    subject = 'Your Voice Transcription'
    body = f'The transcription of your recorded voice is:\n\n{transcription}\n\n\n Jamshid Ganiev'
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, message)
    server.quit()


def handle_speech_to_text(req):
    # Record voice
    filename = 'voice.wav'
    filepath = record_audio(filename, 30)

    # Transcribe voice
    transcription = transcribe_audio(filepath)

    # Send transcription via email
    send_email(transcription)

    return SpeechToTextResponse("Your voice transcription is sent to your email")


def speech_to_text_server():
    rospy.init_node('speech_to_text_server')
    rospy.Service('speech_to_text', SpeechToText, handle_speech_to_text)
    rospy.spin()

if __name__ == "__main__":
    speech_to_text_server()
