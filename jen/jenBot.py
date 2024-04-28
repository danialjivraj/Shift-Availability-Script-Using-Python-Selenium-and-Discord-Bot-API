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

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")
USERNAME = os.getenv("LOGIN_USERNAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} is on')

async def run_script(filter_specific_days=True, include_booked_days=True, include_available_days=True, include_specific_days_and_shifts=True, break_out_of_loop=False, auto_check=None):
 tracked_specific_shift_days = []  # list to track the specific shifts and days, it compares with current list, if both match, the bot won't send a repeated message
 tracked_filtered_available_days = [] # list to track the filtered available days, it compares with current list, if both match, the bot won't send a repeated message

 while True:
    driver = create_chrome_driver(headless=True)

    LOGIN_URL = os.getenv("LOGIN_URL")
    driver.get(LOGIN_URL)

    wait = WebDriverWait(driver, 3)

    username_elem = wait.until(EC.presence_of_element_located((By.ID, "mitarbeiternummer")))
    password_elem = driver.find_element(By.ID, "passwort")

    username_elem.send_keys(USERNAME)
    password_elem.send_keys(PASSWORD)

    login_button_elem = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]/span[text()='Log In']")
    login_button_elem.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@onclick=\"gotoTarget('schichtplan');\"]")))
    shift_schedule_elem = driver.find_element(By.XPATH, "//a[@onclick=\"gotoTarget('schichtplan');\"]")
    shift_schedule_elem.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='tagsNr']")))
 
    available_days = []
    booked_days = []
    current_specific_shift_days = []
    automation_checked_list=[]

    div_elements_first_page = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-14 tag')]")

    loop_available_days_and_booked_days(div_elements_first_page, available_days, booked_days)

    if include_specific_days_and_shifts:
       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Saturday", "10:00 - 18:00", automation_checked_list, auto_check)
       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Sunday", "11:00 - 18:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Monday", "17:00 - 21:00", automation_checked_list, auto_check)     
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Wednesday", "17:00 - 21:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Thursday", "17:00 - 21:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Friday", "17:00 - 21:00", automation_checked_list, auto_check)
#       loop_specific_days_and_shifts(driver, div_elements_first_page, current_specific_shift_days, "Tuesday", "17:00 - 21:00", automation_checked_list, auto_check)

    # navigates to the second page to retrieve more days
    SECOND_URL = os.getenv("SECOND_URL")
    driver.get(SECOND_URL)

    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='tagsNr']")))

    div_elements_second_page = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-14 tag')]")

    loop_available_days_and_booked_days(div_elements_second_page, available_days, booked_days)

    if include_specific_days_and_shifts:
        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Saturday", "10:00 - 18:00", automation_checked_list, auto_check)
        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Sunday", "11:00 - 18:00", automation_checked_list, auto_check)
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Monday", "17:00 - 21:00")        
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Wednesday", "17:00 - 21:00")
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Thursday", "17:00 - 21:00")
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Friday", "15:00 - 21:00")
#        loop_specific_days_and_shifts(driver, div_elements_second_page, current_specific_shift_days, "Tuesday", "15:00 - 21:00")

    driver.quit()
    
    for days in automation_checked_list:
        booked_days.append(f'\nDays added:\n__{days}__')
    print(booked_days)

    current_filtered_available_days = available_days

    if filter_specific_days:
        specific_days = ["Saturday", "Sunday"]
        current_filtered_available_days = [day for day in current_filtered_available_days if any(day.startswith(day_name) for day_name in specific_days)]

    print("current_filtered_available_days = ", current_filtered_available_days)
    print("tracked_filtered_available_days = ", tracked_filtered_available_days)
    if current_filtered_available_days != tracked_filtered_available_days:
        if current_filtered_available_days:
            if include_available_days:
                ping_user = f"SHIFTS AVAILABLE! {DISCORD_USER_ID}\nGrab 'em quick!"
                await client.get_channel(TARGET_CHANNEL_ID).send(ping_user)
            if include_booked_days:
                booked_days_list = "\n".join(booked_days)
                await send_embed_message(TARGET_CHANNEL_ID, "Booked Days", booked_days_list, discord.Color.blue())
            if include_available_days:
                sorted_available_days = "\n".join(current_filtered_available_days)
                await send_embed_message(TARGET_CHANNEL_ID, "Available Days", sorted_available_days, discord.Color.green(), LOGIN_URL, link_text="Book now!")
        tracked_filtered_available_days = current_filtered_available_days

    print("automation_checked_list = ", automation_checked_list)
    print("current_specific_shift_days = ", current_specific_shift_days)
    print("tracked_specific_shift_days = ", tracked_specific_shift_days)
    if current_specific_shift_days != tracked_specific_shift_days:
        tracked_specific_shift_days = current_specific_shift_days
    
        if automation_checked_list:
            for day in automation_checked_list:
                current_specific_shift_days.remove(day)

        current_specific_shift_days = sorted(current_specific_shift_days, key=lambda x: (datetime.strptime(x.split(" - ")[0], "%A, %d of %B").month, datetime.strptime(x.split(" - ")[0], "%A, %d of %B").day))
        current_specific_shift_days = "\n".join(current_specific_shift_days)
        automation_checked_list = "\n".join(automation_checked_list)

        if current_specific_shift_days:
            await client.get_channel(TARGET_CHANNEL_ID).send(DISCORD_USER_ID)
            await send_embed_message(TARGET_CHANNEL_ID, "Specific Shift Days", current_specific_shift_days, discord.Color.purple(), LOGIN_URL, link_text="Book now!")
        if automation_checked_list:
            await client.get_channel(TARGET_CHANNEL_ID).send(DISCORD_USER_ID)
            await send_embed_message(TARGET_CHANNEL_ID, "Automatically Added Shift", automation_checked_list, discord.Color.red(), LOGIN_URL, link_text="Check your bookings!") 
    if break_out_of_loop:
        break
    await asyncio.sleep(10)

async def send_embed_message(channel_id, title, description, color, url=None, link_text=None):
    embed = discord.Embed(title=title, color=color)
    embed.description = description
    if url:
        embed.description += f"\n\n[{link_text}]({url})"
    await client.get_channel(channel_id).send(embed=embed)

@client.event
async def on_message(message):
    if message.channel.id == TARGET_CHANNEL_ID and not message.author.bot:
        content = message.content.lower()
        
        # filter
        if content == 'f': # available and booked
            client.loop.create_task(run_script(True, True, True, True, False, False))
        elif content == 'fa': # available only
            client.loop.create_task(run_script(True, False, True, True, False, False))

        # automatically books desired shifts
        elif content == 'af': # filter available and booked
            client.loop.create_task(run_script(True, True, True, True, False, True))
        elif content == 'afa': # filter available days only
            client.loop.create_task(run_script(True, False, True, True, False, True))
        elif content == 'afb': # filter booked days only (no available days)
            client.loop.create_task(run_script(True, True, False, True, False, True))

        # all
        elif content == 'a': # all available and booked
            client.loop.create_task(run_script(False, True, True, True , False, False))
        elif content == 'aa': # all available only
            client.loop.create_task(run_script(False, False, True, True, False, False))

        # automatically books desired shifts
        elif content == 'a a': # loops all available and booked
            client.loop.create_task(run_script(False, True, True, True , False, True))
        elif content == 'a aa': # loops available days only
            client.loop.create_task(run_script(False, False, True, True , False, True))
        elif content == 'a ab': # filter booked days only (no available days)
            client.loop.create_task(run_script(True, False, True, True, False, True))

        elif content == 'b': # booked (loops once)
            client.loop.create_task(run_script(False, True, False, False, True, False))
        elif content == 's': # stop
            await message.channel.send("All executions have halted.")
            await client.close()

if __name__ == "__main__":
    asyncio.run(client.start(TOKEN))
