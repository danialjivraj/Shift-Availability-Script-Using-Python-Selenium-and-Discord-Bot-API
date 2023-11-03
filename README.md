# Booking Shift Website Webscraper Using Selenium and Sending Notifications Of Available Shifts Through The Discord Bot API
## The Problem
This is a booking shift website, which works on a first come first serve.
Now for example, the shift "10:00 - 18:00" on the Saturdays could be available for only 50 people, and the first 50 people to book them get it. Now suppose, let's say Bob, was the 50th person to book this shift, the day would turn into the colour grey (if there was no more shifts available from that day). <br>
But Bob could for example take his shift off 1-3 days before his Saturday shift, so for example if he took his shift off on Friday, that would mean that the "10:00 - 18:00" would be available again, but the problem is that no one gets notified about this available shift, so unless you were in the website at that exact moment when Bob unbooked himself from the shift, there would be no way of knowing about this now-available shift.

This is what the booking webpage looks like:
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/79e0fe66-0ddc-461c-a9f1-08362bdc4052)<br>
Clicking on a day will display the different shifts available as seen here:<br>
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/84464807-b133-420f-96ff-da4d8b1a042e)<br>
Clicking on a day which has been booked:<br>
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/92ec7304-1b68-4c01-8572-b6789b76384e)<br>

## Objective
The objective of this project was to create an infinite while loop script using Selenium, checking for shifts on the booking webpage every x seconds. If available shifts are found, the Discord Bot notifies the user about the available shift/s through a message on the server channel.

## Dependencies
- **discord.py:** `pip install discord.py`
- **selenium:** `pip install selenium`
- **python-dotenv:** `pip install python-dotenv`

## Chrome Driver
Chrome Driver is necessary for the program to work when using Selenium, once installed you will need to define the path for it to run properly.
To see the versions of Chrome Driver available, click <a href="https://googlechromelabs.github.io/chrome-for-testing/">here!</a>
I put my Chrome Driver logic in my `chromeDriverMode.py` file. And when calling it on `jenBot.py`, I can set it to `True`, meaning it will be in headless mode, making it invisible, or to `False`, making it visible, so that I can see the brower opening and executing the steps. I would only set it to `False`, to check for bugs or to see if it was running problem in real time, when everything was running perfectly, I could set it to `True` and let it run in the background for as long as I wanted it to.

## Jen Description
**Jen** is a Discord bot designed to automate and notify the process of checking and booking shifts on a scheduling website. It utilizes Selenium to interact with the scheduling website and retrieve information about available and booked shifts. **Jen** then sends a notification on a designated discord channel regarding the available/booked days. <br>
**Jen** operates based on various different commands entered in the designated Discord channel.

## Features
- **Shift Availability Notification:** Notifies users in real-time about available and booked shifts on specified days, as well as having the ability to look for specific shifts, for example **"10:00 - 18:00"** on Saturday.
- **Automatic Booking:** Can automatically book desired shifts based on predefined criteria.
- **Shift Filtering:** Filters shifts based on specific days and shifts, allowing users to focus on preferred time slots.
- **User Interaction:** Listens to commands entered by the user in a Discord channel and responds accordingly.
- **Discord Embed Messages:** Sends formatted Discord embed messages containing shift details and clickable links for quick action.

## How It Works
1. **User Commands:** When the trigger command is typed in the Discord channel it executes the script.
2. **Login:** The script logs into the scheduling website and redirects itself onto the booking webpage.
3. **Day Availability:** Checks for available and booked shifts on specified days, the logic can be found in `days.py` in `loop_available_days_and_booked_days`.
4. **Specific Shift Availability:** Checks for specific shifts for specific days, the logic can be found in `days.py` in `loop_specific_days_and_shifts`
5. **Notification:** Notifies users about available shifts through Discord messages when it meets the conditions.
6. **Automation:** Optionally automates the booking process automatically for desired shifts without manual interaction.

## Commands
These are the various different commands I decided to create, they are abbreviated so that I can easily type a command. Each of these commands has a different combination of boolean conditions in the function's parameters, which creates flexibility, giving over 10 different type of options of how the script can be run without breaking the code.
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/ba8740d1-7116-4d23-9fc7-6c4291da1ffe)

![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/8ec5480c-2954-413b-8445-94ac1d14a443)

- **f:** Filter available and booked shifts and send both booked and available days.
- **fa:** Filter available shifts only and send available days only (no booked days).
- **af:** Automatically book desired shifts, filter available and booked shifts.
- **afa:** Automatically book desired shifts, filter available shifts only (no booked days).
- **afb:** Automatically book desired shifts, filter booked days only (no available days).
- **a:** All available and booked shifts and send both booked and available days.
- **aa:** All available days and send only available days (no booked days).
- **a a:** Automatically book desired shifts, all available and booked shifts.
- **a aa:** Automatically book desired shifts, all available shifts only (no booked days).
- **a ab:** Automatically book desired shifts, all booked days only (no available days).
- **b:** Retrieve booked days only (loops once).
- **s:** Stop the bot and halt all executions.

## .env
I stored `Discord ID`, `Channel ID` and the `Discord Token` information inside of `.env`. <br>
The log in details are also inside here.<br>
The `SECOND_URL` is an identical page, which extra days, of which is why the code is repeated twice, scanning for the same elements again.

## The loop_available_days_and_booked_days Function
This loop will only check for available and booked days. It does not need to click on any day for it to know if it is available or not, as it can retrieve all the information necessary from the get-go. It does not matter what type of shift is available, if there is any shift availble, it will let me know by sending a message through **Jen**.<br>
When the message is sent, it will send both available and booked days.<br>
The code contains the current day, which is used to compare the present day with the days from the website. If there is an available day but that day was from a previous day compared to present day (which did happen because although it was Grey in the website, meaning it was unavailable, the source code would indicate it was not for some reason), it should not send me a message, because it is impossible to book days which are in the past. This logic ensures the that it will only show me days starting from tomorrow onwards.
An example of what it would show if I used my `f` command, which in my case only looks for Saturday and Sunday days
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/3b7600fa-7ec8-4d79-b790-79d04ee4890a)

For Booked Days, I don't really need to worry about previous days, if there was a shift I had done in the past, I don't mind seeing it, and therefore, any past days which were booked were shown crossed out. <br>
In this example, I used my `a` command, which will check for every day instead of filtering, as you can see below, many days are available, although it does not show which shift it's available (and notice how it does not show Saturday nor Sunday days in here because I had already booked all of them):
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/39cf3b72-8032-4a99-ae2f-4aafea06862a)

For further explanation, the "f" simply means filtering days. The logic can be found in here:
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/ab0653d8-cfb3-44e0-bd2b-a626b3bbbcc7)

![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/773de279-df62-40e1-815e-c27fd5c4bba6)


## The loop_specific_days_and_shifts Function
This loop will click on specific days, and check for specific shifts I had set up. When the script is running, it will click on each day that was defined in the parameter, and then it will start looking to see if any of the shifts available match the shift time defined in the parameter.
If it does match, it will send this message:
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/e60b0913-0273-4aa5-b5aa-afe58bf0d6b9)
In this case it also sent available and booked days because I hadn't booked anything for that specific day, but if for example I had booked the shift "10:00 - 14:00" for Sunday but I want to have the "11:00 - 18:00" shift, **Jen** would only send me the purple message if it found the shift to be available, which would look like this:
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/b76de76d-ee53-488e-ab2c-280689a3abf3)

## Automatically add specific shifts
I also included the option of having an automated booking system, which was defined using `auto_check`, which is a boolean of which when it is `True`, it will click on the checkbox that matches the condition.<br>
When a checkbox is clicked, the page refreshes itself. This was a problem for my script because it would crash, I would have to catch the exception, so that even if it closes the script, it had clicked on the checkbox, which meant the day was now booked, and with the day being booked I could let **Jen** send me this following message (notice how I used the command `af`, which means it is going to automate my booking only for the **filtered** days, and send me both available and booked days):
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/1890493b-247c-4b48-b149-a8001fc2fb7c)

Not only will it tell me it has been automatically added, but it also updates the Booked Days message with the "Days added" followed by the day that was added. This required 0 human interaction as the script booked it automatically according to my preferences.

## Discord Logic
After the script runs, it will store the information in lists, and then those lists are used and sent to **Jen**. <br>
I formatted the discord text and made it embed to make it look nicer and cleaner. Booked days display a blue line, while Available days display green. Specific Available days as purple and Automatic Checking as red.

## Conclusion
This project was overall a really good way to experiment with Selenium and the Discord API using only Python.<br>
I had little knowledge on Selenium and Chrome Driver before working on this project. I had also never used a Discord Bot and it's API in order to send messages, so combining both of these technologies together allowed me to create something extremely affective, and allowed me to improve my Python skills overall and managing information through lists.<br>
