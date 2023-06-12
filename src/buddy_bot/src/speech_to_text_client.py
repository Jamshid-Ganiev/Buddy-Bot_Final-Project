#!/usr/bin/env python3

import sys
import rospy
from buddy_bot.srv import SpeechToText

def speech_to_text_client():
    rospy.wait_for_service('speech_to_text')
    try:
        speech_to_text = rospy.ServiceProxy('speech_to_text', SpeechToText)
        response = speech_to_text()
        return response.result
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")

def usage():
    return "%s" % sys.argv[0]

if __name__ == "__main__":
    print("Requesting transcription...")
    print(speech_to_text_client())
