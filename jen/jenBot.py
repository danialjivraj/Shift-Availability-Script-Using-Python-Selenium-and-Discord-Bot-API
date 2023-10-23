import discord
import asyncio
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from chromeDriverMode import create_chrome_driver
from days import loop_specific_days_and_shifts, loop_available_days_and_booked_days
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN") # Token retrieved from .env
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID")) # Target channel id number retrieved from .env
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID") # Discord User ID retrieved from .env
USERNAME = os.getenv("LOGIN_USERNAME") # Login username information retrieved from .env
PASSWORD = os.getenv("LOGIN_PASSWORD") # Login password information retrieved from .env

intents = discord.Intents.default() # Define the intents to enable
intents.message_content = True
client = discord.Client(intents=intents) # Create a client instance with intents

@client.event
async def on_ready():
    print(f'{client.user.name} is on')

#################### the following parameters are a set of booleans which create different variations for different commands
async def run_script(filter_specific_days=True, include_booked_days=True, include_available_days=True, include_specific_days_and_shifts=True, break_out_of_loop=False, auto_check=None):
 tracked_specific_shift_days = []  # List to track the specific shifts and days. This list is used to compare with current list, if both match, the bot won't send a repeated message
 tracked_filtered_available_days = [] # List to track the filtered available days. This list is used to compare with current list, if both match, the bot won't send a repeated message

 while True:
    driver = create_chrome_driver(headless=True)

    LOGIN_URL = os.getenv("LOGIN_URL") # Goes to Login page.
    driver.get(LOGIN_URL)

    # Wait for the username element to be visible on the login page
    wait = WebDriverWait(driver, 3)  # Maximum wait time in seconds

    username_elem = wait.until(EC.presence_of_element_located((By.ID, "mitarbeiternummer"))) # The element containing the Login username field
    password_elem = driver.find_element(By.ID, "passwort") # The element containing the Login password field

    username_elem.send_keys(USERNAME) # Populates the username field with my username details
    password_elem.send_keys(PASSWORD) # Populates the username field with my password details

    #n Find and click the login button with text "Log In"
    login_button_elem = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]/span[text()='Log In']")
    login_button_elem.click()

    # Wait for the page to load
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@onclick=\"gotoTarget('schichtplan');\"]")))
    # Click on the "Shift Schedule" link/button
    shift_schedule_elem = driver.find_element(By.XPATH, "//a[@onclick=\"gotoTarget('schichtplan');\"]")
    shift_schedule_elem.click()
    # Wait for the booking calendar page to load
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='tagsNr']")))
 
    available_days = [] # List to store available days
    booked_days = [] # List to store booked days
    current_specific_shift_days = [] # The current_specific_shift_days will store the current list of the shifts and days
    automation_checked_list=[]

    # Find all relevant div elements on the first page
    div_elements_first_page = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-14 tag')]")

    # Check availability for each shift on the first page
    loop_available_days_and_booked_days(div_elements_first_page, available_days, booked_days)

    if include_specific_days_and_shifts: # It runs the following if this is True in the commands
       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Saturday", "10:00 - 18:00", automation_checked_list, auto_check)
       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Sunday", "11:00 - 18:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Monday", "17:00 - 21:00", automation_checked_list, auto_check)     
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Wednesday", "17:00 - 21:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Thursday", "17:00 - 21:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Friday", "17:00 - 21:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Tuesday", "17:00 - 21:00", automation_checked_list, auto_check)

    # Navigate to the second page to retrieve more days information
    SECOND_URL = os.getenv("SECOND_URL")
    driver.get(SECOND_URL)

    # Wait for the booking calendar page on the second URL to load
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='tagsNr']")))

    # Find all relevant div elements on the second page
    div_elements_second_page = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-14 tag')]")

    loop_available_days_and_booked_days(div_elements_second_page, available_days, booked_days)

    if include_specific_days_and_shifts: # It runs the following if this is True in the commands
        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Saturday", "10:00 - 18:00", automation_checked_list, auto_check)
        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Sunday", "11:00 - 18:00", automation_checked_list, auto_check)
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Monday", "17:00 - 21:00")        
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Wednesday", "17:00 - 21:00")
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Thursday", "17:00 - 21:00")
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Friday", "15:00 - 21:00")
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Tuesday", "15:00 - 21:00")

    driver.quit() # Close the browser window
    
    # If a day was added from automation, it will update it in booked days
    for days in automation_checked_list:
        booked_days.append(f'\nDays added:\n__{days}__')
    print(booked_days)

    current_filtered_available_days = available_days # Changed name to make it easier to understand the code from here

    if filter_specific_days: # If in the command it is set to True, it filters the days to the prefered days of the week, in this case, I chose weekends
        specific_days = ["Saturday", "Sunday"]
        current_filtered_available_days = [day for day in current_filtered_available_days if any(day.startswith(day_name) for day_name in specific_days)]

    print("current_filtered_available_days =", current_filtered_available_days)
    print("tracked_filtered_available_days =", tracked_filtered_available_days)
    # Check if the current available days list is different from the tracked available days, if so, send message, if not don't send
    if current_filtered_available_days != tracked_filtered_available_days:
        # Check if filtered_available_days is not empty
        if current_filtered_available_days:
            if include_available_days: # This will include the ping message if it is set to true in the commands
                ping_user = f"SHIFTS AVAILABLE! {DISCORD_USER_ID}\nGrab 'em quick!" # Pings user
                await client.get_channel(TARGET_CHANNEL_ID).send(ping_user)
            if include_booked_days: # This will include the booked days if it is included in the commands
                booked_days_list = "\n".join(booked_days)
                await send_embed_message(TARGET_CHANNEL_ID, "Booked Days", booked_days_list, discord.Color.blue()) # Send the booked days as a Discord embed
            if include_available_days: # This will include the available days if it is set to true in the commands
                # Sorts the filtered available days before sending it to Jen
                sorted_available_days = "\n".join(current_filtered_available_days)
                await send_embed_message(TARGET_CHANNEL_ID, "Available Days", sorted_available_days, discord.Color.green(), LOGIN_URL, link_text="Book now!") # Send the sorted available days as a Discord embed
        # Update sent_available_days with the new available days
        tracked_filtered_available_days = current_filtered_available_days

    print("automation_checked_list =", automation_checked_list)
    print("current_specific_shift_days =", current_specific_shift_days)
    print("tracked_specific_shift_days =", tracked_specific_shift_days)
    # Check if the current specific shift days list is different from the tracked specific shift days, if so, send message, if not don't send
    if current_specific_shift_days != tracked_specific_shift_days:
        # Update the tracked_specific_shift_days set
        tracked_specific_shift_days = current_specific_shift_days
    
        if automation_checked_list: # If automation was used, remove the matching day from the current_specific_shift_days list
            for day in automation_checked_list:
                current_specific_shift_days.remove(day)

        # Filter shift messages for the current day and sort them chronologically
        current_specific_shift_days = sorted(current_specific_shift_days, key=lambda x: (datetime.strptime(x.split(" - ")[0], "%A, %d of %B").month, datetime.strptime(x.split(" - ")[0], "%A, %d of %B").day))
        # Combine all sorted shift messages into one string
        current_specific_shift_days = "\n".join(current_specific_shift_days)
        automation_checked_list = "\n".join(automation_checked_list)
        # Check if there are any messages to send
        if current_specific_shift_days: # If it isn't empty send the following message:
            await client.get_channel(TARGET_CHANNEL_ID).send(DISCORD_USER_ID)
            # Send the combined shift messages as a Discord embed
            await send_embed_message(TARGET_CHANNEL_ID, "Specific Shift Days", current_specific_shift_days, discord.Color.purple(), LOGIN_URL, link_text="Book now!")
        if automation_checked_list: # If it isn't empty send the following message:
            await client.get_channel(TARGET_CHANNEL_ID).send(DISCORD_USER_ID)
            # Send the combined shift messages as a Discord embed
            await send_embed_message(TARGET_CHANNEL_ID, "Automatically Added Shift", automation_checked_list, discord.Color.red(), LOGIN_URL, link_text="Check your bookings!") 
    if break_out_of_loop: # If a command needs to be used for one iteration once, this boolean will be set to True to break out of the loop after 1 iteration
        break
    await asyncio.sleep(10)  # Sleep for x seconds before running the script again

# Inside the send_embed_message function
async def send_embed_message(channel_id, title, description, color, url=None, link_text=None):
    embed = discord.Embed(title=title, color=color)
    embed.description = description
    if url:  # Check if a URL is provided and add it as a clickable link below the days
        embed.description += f"\n\n[{link_text}]({url})"
    await client.get_channel(channel_id).send(embed=embed)

@client.event
async def on_message(message):
    if message.channel.id == TARGET_CHANNEL_ID and not message.author.bot:
        content = message.content.lower()
        if content == 'f': # filter available and booked
            client.loop.create_task(run_script(True, True, True, True, False, False))  # Loop filtered days and send both booked and available days
        elif content == 'fa': # filter available only
            client.loop.create_task(run_script(True, False, True, True, False, False))  # Loop filtered days and send available days only (no booked days)

        elif content == 'af': # automatically book desired shifts, filter available and booked
            client.loop.create_task(run_script(True, True, True, True, False, True))  # Loops through filtered days, sends both booked and available days and automatically books shift
        elif content == 'afa': # automatically book desired shifts, filter available days only (no booked days)
            client.loop.create_task(run_script(True, False, True, True, False, True))  # Loops through filtered days, sends available days only (no booked days) and automatically books shift
        elif content == 'afb': # automatically book desired shifts, filter booked days only (no available days)
            client.loop.create_task(run_script(True, True, False, True, False, True))  # Loops through filtered days, sends booked days only (no available days) and automatically books shift

        elif content == 'a': # all available and booked
            client.loop.create_task(run_script(False, True, True, True , False, False))  # Loops through all days and send both available and booked days
        elif content == 'aa': # all available only
            client.loop.create_task(run_script(False, False, True, True, False, False))  # Loops through all days and send available days only (no booked days)

        elif content == 'a a': # automatically book desired shifts, loops all available and booked
            client.loop.create_task(run_script(False, True, True, True , False, True))  # Loops through all days and send both available and booked days
        elif content == 'a aa': # automatically book desired shifts, sends all available days only (no booked days)
            client.loop.create_task(run_script(False, False, True, True , False, True))  # Loops through all days and send available days only (no booked days)
        elif content == 'a ab': # automatically book desired shifts, sends booked days only (no available days)
            client.loop.create_task(run_script(True, False, True, True, False, True))  # Loops through all days, sends booked days only (no available days)

        elif content == 'b': # booked
            client.loop.create_task(run_script(False, True, False, False, True, False)) # Retrieve booked days only (loops once)
        elif content == 's': # stop
            await message.channel.send("All executions have halted.")
            await client.close() # Puts the bot offline

# Run the bot
if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
