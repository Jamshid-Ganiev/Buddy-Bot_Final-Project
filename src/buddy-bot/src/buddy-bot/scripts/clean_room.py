#!/usr/bin/env python3

import rospy
from math import radians
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

def display_dots(room_number):
    # Write the code to display dots in the specified room
    pass

def move_turtle_linear(distance, speed):
    # Write the code to move the turtle linearly
    pass

def rotate_turtle(angle, speed):
    # Write the code to rotate the turtle
    pass

def clean_room(room_number):
    rospy.init_node('clean_room', anonymous=True)
    rospy.sleep(1)

    display_dots(room_number)

    # Move the turtle bot to the room and clean
    if room_number == 1:
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
    elif room_number == 2:
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 2)
        rotate_turtle(45, radians(90))
    elif room_number == 3:
        move_turtle_linear(2, 4)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 4)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 4)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 4)
        rotate_turtle(45, radians(90))
    elif room_number == 4:
        move_turtle_linear(2, 6)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 6)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 6)
        rotate_turtle(45, radians(90))
        move_turtle_linear(2, 6)
        rotate_turtle(45, radians(90))
    else:
        rospy.loginfo(f"Room {room_number} is not valid!")

    # Clean the dots in the room
    if room_number >= 1 and room_number <= 4:
        rospy.loginfo("Cleaning the room...")
        rospy.sleep(1)
        # Remove the dots
        rospy.loginfo("The room has been cleaned!")

    # Add more room conditions as needed
