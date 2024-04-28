# booking-shift-webscraper

## Jen
Jen is a Discord bot that collects web-scraped data from a booking shift webpage using Selenium. <br>
This data is then transmitted as notifications detailing available shifts/booked days to a designated text channel on Discord. <br>
The script offers flexibility through a set of boolean flags that allow the user to specifically choose their preferred settings. <br>

## Webscraped Website
This website operates on a first-come, first-served basis for booking shifts. <br>
Reserved shifts can be canceled up to two days before the shift. <br>
However, if a particular day and shift are fully booked and someone cancels, the newly available shift isn't automatically made known to everyone. <br>

## Website Preview

![Available Shifts Preview](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/79e0fe66-0ddc-461c-a9f1-08362bdc4052)

### Clicking on a day with available shifts
![Booked Shifts Preview](https://github.com/danialjivraj/booking-shift-webscraper/assets/61945058/ad17de85-360c-431a-8704-d7d009e9c737)

### Clicking on a day which has been booked
![Shift Booking Process](https://github.com/danialjivraj/booking-shift-webscraper/assets/61945058/d6f433af-b116-4fe7-8226-23ee0894e401)


## Script Features
- Shift Availability Notification
    - Notifies users in real-time about available and booked shifts on specified days, as well as having the ability to look for specific shifts, for example "10:00 - 18:00" on a Saturday.
- Automatic Booking
    - Can automatically book desired shifts based on predefined script selection.
- Shift Filtering
    - Filters shifts based on specific days and shifts, allowing users to focus on preferred time slots.
- User Interaction
    - Listens to the script commands entered by the user in a Discord channel and runs the program accordingly.
- Discord Embed Messages
    - Sends formatted Discord embed messages containing shift details and clickable links for quick action.

## Dependencies

- discord.py
```
pip install discord.py
```
- selenium
```
pip install selenium
```
- python-dotenv
```
pip install python-dotenv
```

### Chrome Driver
The latest version of [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/) is needed. <br>
The path needs to be set up properly in `chromeDriverMode.py`. <br>

## Commands
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

## Preview
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/3b7600fa-7ec8-4d79-b790-79d04ee4890a)
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/39cf3b72-8032-4a99-ae2f-4aafea06862a)
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/e60b0913-0273-4aa5-b5aa-afe58bf0d6b9)
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/b76de76d-ee53-488e-ab2c-280689a3abf3)
![image](https://github.com/danialjivraj/Shift-Availability-Script-Using-Python-Selenium-and-Discord-Bot-API/assets/61945058/1890493b-247c-4b48-b149-a8001fc2fb7c)
  
