# Buddy-Bot_Final-Project
Human Companion Robot with Voice Control and Speech Evalution 
# Buddy_Bot: Your Personal Speech-to-Command Assistant


Welcome to the repository for Buddy_Bot, a cutting-edge project designed to showcase the functionalities of the Robotics Operating System (ROS) in combination with Speech-to-Text services. Buddy_Bot responds to vocal commands and executes various tasks, including movement directives and even drawing geometric shapes.

This project embodies the Publisher-Subscriber and Service paradigms of ROS, and provides a user-friendly interface for you to control your own TurtleBot through simple voice commands!

## Getting Started

To get started with Buddy_Bot, you'll first need to clone this repository. You can do this by running:

```bash
git clone https://github.com/yourusername/Buddy_Bot.git
```
### Once the repository is cloned, navigate into the project directory:

```
cd Buddy_Bot
```
## How to Run Buddy_Bot

Ensure that you have ROS and all the necessary dependencies installed. Once you've done that, you can run the Buddy_Bot scripts.

First, run the talkToMe.py script:

```
python3 talkToMe.py
```

Next, in a separate terminal, run the speech_to_text_service.py script:

```
python3 speech_to_text_service.py
```

Finally, in a third terminal, run the speech_to_text_client.py script:

```
python3 speech_to_text_client.py
```

## Your Buddy_Bot is now ready to receive your voice commands!
</hr>

# Publisher-Subscriber and Service Paradigms

#### Buddy_Bot demonstrates both the Publisher-Subscriber and Service paradigms of ROS.

In the Publisher-Subscriber paradigm, talkToMe.py acts as the publisher, broadcasting commands received from your voice input. It publishes to the /turtle1/cmd_vel topic, which the TurtleBot subscribes to, allowing the bot to execute the published commands.

In the Service paradigm, speech_to_text_service.py and speech_to_text_client.py work together to transcribe your voice commands. When a request is made to the speech_to_text service (defined in speech_to_text_client.py), the speech_to_text_service.py script processes the request and returns the transcribed text.

MIT © Jamshid Ganiev

