#!/usr/bin/env python3


import rospy
import actionlib
import os
import requests
from buddy_bot.msg import AITutorAction, AITutorGoal

class AITutorActionClient(object):
    def __init__(self):
        self.client = actionlib.SimpleActionClient('aitutor', AITutorAction)
        self.client.wait_for_server()

    def transcribe_audio(self, audio_file_path):
        whisper_url = "https://transcribe.whisperapi.com"
        headers = {'Authorization': 'Bearer DX77AIKB63K7HKFT8CGVKPN52WIM1EMX'}
        with open(audio_file_path, 'rb') as audio_file:
            file = {'file': audio_file}
            data = {
                "fileType": "wav",  # Replace with actual file type
                "language": "en",
                "task": "transcribe"
            }
            response = requests.post(whisper_url, headers=headers, files=file, data=data)
        return response.text  # Replace this with actual transcribed text extraction logic

    def get_answer(self, question):
        goal = buddy_bot.msg.AITutorGoal()
        goal.question = question
        self.client.send_goal(goal)
        self.client.wait_for_result(rospy.Duration.from_sec(60.0))  # Increase timeout if necessary
        return self.client.get_result()

if __name__ == "__main__":
    rospy.init_node('AI_tutor_client')

    # Get the directory of the script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create a filepath for the audio file in the audio_data directory
    audio_file_path = os.path.join(dir_path, 'audio_data', 'USER_AUDIO_FILE')

    client = AITutorActionClient()
    transcribed_text = client.transcribe_audio(audio_file_path)
    answer = client.get_answer(transcribed_text)
    print(answer)
