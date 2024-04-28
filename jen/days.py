from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import time

current_date = datetime.now()

def loop_available_days_and_booked_days(page, available_days, booked_days):
    for div_element in page:
        date_str = div_element.find_element(By.CSS_SELECTOR, ".tagsNr span:nth-child(2)").text
        month = div_element.find_element(By.CSS_SELECTOR, ".monatsNr").text
        date = datetime.strptime(f"{date_str} {month}", "%d %B")
        date = date.replace(year=current_date.year)  # sets the year to the current year
        day_of_week = date.strftime("%A")

        # checks if there is a time "td" attribute on the day
        time_td_elem = div_element.find_elements(By.XPATH, ".//table[@class='infos']/tbody/tr/td")
        availability = "Available" if "calendarday" in div_element.get_attribute("class") else "Unavailable"
        if time_td_elem:
            availability = "Booked"
            # retrieves and store the time text
            time_text = ' - ' + ' | '.join(td.text for td in time_td_elem)
        # stores in the respective list
        if availability == "Available":
            if (current_date.month < date.month) or (current_date.month == date.month and current_date.day < date.day):
                available_days.append(f"{day_of_week}, {date_str} of {month}")
        if availability == "Booked": 
            if (current_date.month < date.month) or (current_date.month == date.month and current_date.day <= date.day):
                booked_days.append(f"{day_of_week}, {date_str} of {month}{time_text}") # if the day is after current day, retrieves as normal
            else:
                booked_days.append(f"~~{day_of_week}, {date_str} of {month}{time_text}~~") # will be shown crossed out in discord

def loop_specific_days_and_shifts(driver, div_elements, current_specific_shift_days, weekday, weekday_time, automation_checked_list, auto_check=True):
    for div_element in div_elements:
        try:
            day_of_week = div_element.find_element(By.CSS_SELECTOR, ".tagsNr span:nth-child(1)").text.strip()
            if day_of_week == weekday and "calendarday" in div_element.get_attribute("class"):
                date_str = div_element.find_element(By.CSS_SELECTOR, ".tagsNr span:nth-child(2)").text.strip()
                month = div_element.find_element(By.CSS_SELECTOR, ".monatsNr").text.strip()
                date = datetime.strptime(f"{date_str} {month}", "%d %B")
                date = date.replace(year=current_date.year)  # sets the year to the current year
                day_of_week = date.strftime("%A")

                try:
                    ActionChains(driver).click(div_element).perform()
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@class='glyphicon glyphicon-info-sign']")))
                except:
                    continue

                shift_info_elems = driver.find_elements(By.XPATH, "//td[@title]//span[contains(@class, 'glyphicon-info-sign')]/following-sibling::span")

                # finds the checkbox status
                checkbox_elem = driver.find_element(By.XPATH, "//td[@title]/following-sibling::td/input[@class='form-check-input toggleShiftBooking']")
                checkbox_status = "Checked" if "checked" in checkbox_elem.get_attribute("outerHTML") else "Unchecked"
                
                check_box_list =[] # creates a list to store checkbox information for each day
                for shift_info_elem in shift_info_elems:
                    shift_info = shift_info_elem.text
                    checkbox_elem = shift_info_elem.find_element(By.XPATH, "../../td/input[@class='form-check-input toggleShiftBooking']")
                    checkbox_status = driver.execute_script("return arguments[0].checked;", checkbox_elem)
                    checkbox_status = "Checked" if checkbox_status else "Unchecked"
                    check_box_list.append(checkbox_status) # only used for the automation script
                print(check_box_list)
                
                for shift_info_elem in shift_info_elems:
                    shift_info = shift_info_elem.text
                    checkbox_elem = shift_info_elem.find_element(By.XPATH, "../../td/input[@class='form-check-input toggleShiftBooking']")
                    checkbox_status = driver.execute_script("return arguments[0].checked;", checkbox_elem)
                    checkbox_status = "Checked" if checkbox_status else "Unchecked"
                    
                    if (current_date.month < date.month) or (current_date.month == date.month and current_date.day < date.day):
                        if weekday_time in shift_info and "Con" in shift_info and checkbox_status == "Unchecked":
                            shift_info_message = f"{day_of_week}, {date_str} of {month} - {shift_info}"
                            current_specific_shift_days.append(shift_info_message)
                            if auto_check:
                                if all(i == 'Unchecked' for i in check_box_list):
                                    automation_checked_list.append(shift_info_message)
                                    checkbox_elem.click() # clicks the checkbox
                                    time.sleep(1)
                                else:
                                    continue
        except StaleElementReferenceException:
            print("StaleElementReferenceException occurred...")
            continue
            
