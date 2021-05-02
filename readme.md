# Django Chat

Django chat is a simple chat application built using django channels. It allows users to create an account and chat with other users on the site or chat in group.

## Features

- Single user to user chat
- Group chat
- Messages saved to db, so the messages do not disappear after you close the channel

## To run project
-  install the required dependecies      ``` pip install -r requirements.txt```
-  install reddis on your local computer for the channel layers and start the reddis server
-  run ```python manage.py migrate ``` to setup the database
-  run ``` python manage.py runserver ``` to start the development and test out the application