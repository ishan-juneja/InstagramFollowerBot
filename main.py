from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time

INSTAGRAM_EMAIL = os.environ["INSTAGRAM_EMAIL"]
INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]
ACCOUNT_USERNAME = "gordongram" # the username of the account we are after
chrome_driver_path = "/Users/ishanjuneja/Development/chromedriver_mac64"

#control how long selenium will take to perform its actions
#you may need to change it based on the computer you have and its speed
SHORT_WAIT = 1
MEDIUM_WAIT = 5
LONG_WAIT = 60

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

#Retrieve Instagram page and login
driver.get("https://www.instagram.com/")
time.sleep(MEDIUM_WAIT)

login_fields = driver.find_elements(By.CSS_SELECTOR, "input._aa4b")
login_fields[0].send_keys(INSTAGRAM_EMAIL)
login_fields[1].send_keys(INSTAGRAM_PASSWORD + Keys.RETURN)


#Bypass notifications alert
time.sleep(MEDIUM_WAIT)
allWindowHandles = driver.window_handles
try:
	decline_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")
	decline_button.click()
except NoSuchElementException:
	print("1")
	pass
#
# #Search for our desired profile
# time.sleep(SHORT_WAIT)
# search_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a")
# search_button.click()

# Go to our desired page
driver.get(f"https://www.instagram.com/{ACCOUNT_USERNAME}/posts")

time.sleep(MEDIUM_WAIT)
number_of_posts = driver.find_element(By.CSS_SELECTOR, "span._ac2a").text

number_of_rows_of_posts = int(number_of_posts.replace(",", "" )) % 3
if number_of_rows_of_posts > 10:
	number_of_rows_of_posts = 10

number_of_rows_of_posts = 4

time.sleep(SHORT_WAIT)
post = driver.find_element(By.XPATH,
                           f"/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div/div[1]/div[2]/a")
post.click()

# /html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[3]/div/div/section[2]/div/div/span/a
#Getting a hold of the followers who liked the post
time.sleep(MEDIUM_WAIT)
like_link = None
try:
	elements = driver.find_elements(By.CSS_SELECTOR, "a._a6hd")
	for element in elements:
		try:
			if element.text[len(element.text) - 5:] == "likes" or element.text[len(element.text) - 6:] == "others":
				like_link = element
		except IndexError:
			pass
except NoSuchElementException:
	pass


# Accessing the followers
like_link.click()
time.sleep(SHORT_WAIT)
counter = 1

while True:
	try:
		follow_button = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div[{counter}]/div/div/div/div[3]/div/button/div")
		print(follow_button.text)
		if (follow_button.text == "Following" or follow_button.text == "Requested"):
			pass
		else:
			follow_button.click()
		counter += 1
		time.sleep(SHORT_WAIT*2)
	except NoSuchElementException:
		print(f"Done: counter is at {counter}")
		break

# Close out of the followers
time.sleep(MEDIUM_WAIT)
close_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div")
driver.execute_script("arguments[0].click();", close_button)



# # Auto scroll through the posts on page
# for row in range(1, number_of_rows_of_posts):
# 	for column in range(1, 4):
# 		time.sleep(SHORT_WAIT)
# 		post = driver.find_element(By.XPATH,
# 		                           f"/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div/div[{row}]/div[{column}]/a")
# 		post.click()

while True:
	pass