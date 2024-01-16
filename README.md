# Study Spaces App for The University of Virginia

__Developers:__ Tyler Donovan, Henry Evans, Charlotte Zhang, Sebastian Fugle, Paula Delgado

# Website Link
http://studyspot.live/

# Herokuapp Link: 
https://b02-site-ed63d9be471c.herokuapp.com

# Motivation

The Study Spaces App was designed for UVA students to be able to interact with new places on grounds specifically when it comes to studying. As student's we know it can become very difficult to find study spots that match our preferences, so we created to app to hopefully alleviate that difficulty. Our App connects with google maps to allow students to find study spaces based on locations around grounds and interact with them by reviewing them based on their experience with the space. If a building/more general location isn't currently on the map they can create a new pin and submit it for approval before adding the location to the map.

Technologies Used:
- Heroku
- Django
- Javascript

# Challenges

During development we faced some challenges getting heroku postgres to connect properly with our django application which slowed down development and may still need to be fixed. We also had some issues with database versions control and migrating models properly, but we were able to fix most of those problems.

# How to Use

To use the study spots app, you must sign in through google which you can find in the navbar or scroll down menu:

![image](https://github.com/ty-donovan/studyspots/assets/121574913/b50acd65-6b67-4301-9780-ab18369bc8ab)

![image](https://github.com/ty-donovan/studyspots/assets/121574913/9a48f92d-87f0-446b-841f-1bb282555863)

After logging in you can either add a new spot by clicking the button in the navbar/scroll down menu and fill out the form, or you can interact with existing spots through the links on the study spots list or by clicking directly on the pins on the map.

If you want to leave a review you can click on an existing study spot and then click "Review this spot" in the top right of the screen.

![image](https://github.com/ty-donovan/studyspots/assets/121574913/222f057a-0fa1-4e65-8d20-08c7980cf719)

After that you can just fill out the existing information fields and submit your review!

# For Developers

## Installation
___
1. pip install -r requirements.txt
