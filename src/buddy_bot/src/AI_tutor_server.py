#!/usr/bin/env python3

# Whisper: DX77AIKB63K7HKFT8CGVKPN52WIM1EMX
# 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

import rospy
import actionlib
import requests
import json
from buddy_bot.msg import AITutorAction, AITutorResult

class AITutorActionServer(object):
    def __init__(self):
        self.server = actionlib.SimpleActionServer('aitutor', AITutorAction, self.execute, False)
        self.server.start()

    def generate_answer(self, question):
        gpt_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
        data = {"prompt": question, "max_tokens": 60}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer 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"}
        response = requests.post(gpt_url, headers=headers, data=json.dumps(data))
        return response.json()['choices'][0]['text']  # Replace this with actual answer extraction logic

    def execute(self, goal):
        answer = self.generate_answer(goal.question)
        result = buddy_bot.msg.AITutorResult()
        result.answer = answer
        self.server.set_succeeded(result)

if __name__ == "__main__":
    rospy.init_node('AI_tutor_server')
    server = AITutorActionServer()
    rospy.spin()


