#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import speech_recognition as sr
import sys
import math
import time

def draw_shape(shape, pub):
    sides = 0
    angle = 0

    # Speed for drawing shapes
    shape_speed = 0.2

    if shape == "rectangle":
        sides = 4
        angle = 90
    elif shape == "triangle":
        sides = 3
        angle = 120
    elif shape == "pentagon":
        sides = 5
        angle = 72
    elif shape == "star":
        sides = 5
        angle = 144
    elif shape == "octagon":
        sides = 8
        angle = 45

    # Draw the shape
    for _ in range(sides):
        move(pub, shape_speed, 2)
        turn(pub, angle, 2)

def move(pub, speed, duration):
    twist = Twist()
    twist.linear.x = speed
    pub.publish(twist)
    rospy.sleep(duration)
    twist = Twist()
    pub.publish(twist)

def turn(pub, angle, duration):
    twist = Twist()
    twist.angular.z = angle * math.pi / 180  # Convert angle to radians
    pub.publish(twist)
    rospy.sleep(duration)
    twist = Twist()
    pub.publish(twist)

def parse_transcription(transcription):
    command_types = ['forward', 'backward', 'left', 'right', 'finish', 
                     'rectangle', 'triangle', 'pentagon', 'star', 'octagon']

    transcription_list = transcription.split()
    for word in transcription_list:
        if word.lower() in command_types:
            return "command", word.lower()

    return "unknown", transcription

def handle_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        movement_started = False
        with microphone as source:
            while True:
                rospy.loginfo("Listening...")
                audio = recognizer.listen(source, timeout=30)
                try:
                    transcription = recognizer.recognize_google(audio).lower()
                    rospy.loginfo(f"Heard: {transcription}")

                    command_type, command_text = parse_transcription(transcription)

                    if command_type == "command":
                        velocity = Twist()
                        if command_text in ['forward', 'backward', 'left', 'right']:
                            if command_text == "forward":
                                velocity.linear.x = 0.2
                            elif command_text == "backward":
                                velocity.linear.x = -0.2
                            elif command_text == "left":
                                velocity.angular.z = 0.5
                            elif command_text == "right":
                                velocity.angular.z = -0.5

                            if not movement_started:
                                rospy.loginfo("Movement started.")
                                movement_started = True

                            command_publisher.publish(velocity)
                            rospy.sleep(3)

                        elif command_text in ['rectangle', 'triangle', 'pentagon', 'star', 'octagon']:
                            draw_shape(command_text, command_publisher)

                        elif command_text == "finish":
                            rospy.loginfo("Finishing...")
                            sys.exit()

                except sr.UnknownValueError:
                    rospy.loginfo("Couldn't understand. Try again.")

if __name__ == '__main__':
    rospy.init_node('voice_control')
    command_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    handle_audio()
    time.sleep(2)
    rospy.spin()
