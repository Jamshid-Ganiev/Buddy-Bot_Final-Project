#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
import speech_recognition as sr
import sys
import math

def draw_shape(shape, pub):
    sides = 0
    angle = 0

    # Speed for drawing shapes
    shape_speed = 4.0

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
    elif shape == "heart":
        sides = 20
        angle = 36

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
    command_types = ['forward', 'backward', 'left', 'right', 'finish', 'clean',
                     'rectangle', 'triangle', 'pentagon', 'star', 'octagon', 'heart']

    transcription_list = transcription.split()
    for word in transcription_list:
        if word.lower() in command_types:
            return "command", word.lower()

    return "unknown", transcription

def handle_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    rospy.wait_for_service('/reset')  
    reset_turtle = rospy.ServiceProxy('/reset', Empty)  
    reset_turtle()  

    while True:
        movement_started = False
        with microphone as source:
            while True:
                rospy.loginfo("Listening...")
                audio = recognizer.listen(source, timeout=4)
                try:
                    transcription = recognizer.recognize_google(audio).lower()
                    rospy.loginfo(f"Heard: {transcription}")

                    command_type, command_text = parse_transcription(transcription)

                    if command_type == "command":
                        velocity = Twist()
                        if command_text in ['forward', 'backward', 'left', 'right']:
                            if command_text == "forward":
                                velocity.linear.x = 2.0
                            elif command_text == "backward":
                                velocity.linear.x = -2.0
                            elif command_text == "left":
                                velocity.angular.z = 1.0
                            elif command_text == "right":
                                velocity.angular.z = -1.0

                            if not movement_started:
                                rospy.loginfo("Movement started.")
                                movement_started = True

                            command_publisher.publish(velocity)
                            rospy.sleep(3)

                        elif command_text in ['rectangle', 'triangle', 'pentagon', 'star', 'octagon', 'heart']:
                            draw_shape(command_text, command_publisher)

                        elif command_text == "clean":
                            rospy.loginfo("Cleaning...")
                            rospy.wait_for_service('/clear')
                            clear = rospy.ServiceProxy('/clear', Empty)
                            clear()

                        elif command_text == "finish":
                            rospy.loginfo("Finishing...")
                            sys.exit()

                except sr.UnknownValueError:
                    rospy.loginfo("Couldn't understand. Try again.")

if __name__ == '__main__':
    rospy.init_node('voice_control')
    command_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    handle_audio()
    rospy.spin()
