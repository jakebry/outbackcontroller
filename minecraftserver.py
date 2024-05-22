import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Replace with your Discord Bot Token
DISCORD_BOT_TOKEN = 'Bot_Token_here'
# Replace with your Aternos login details
ATERNOS_USERNAME = 'YOUR_ATERNOS_USERNAME'
ATERNOS_PASSWORD = 'YOUR_ATERNOS_PASSWORD'

# Discord bot setup
bot = commands.Bot(command_prefix='/')

# Function to initialize the Selenium WebDriver
def start_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")  # Run in headless mode
    # Specify the path to the ChromeDriver if it's not in your PATH
    driver = webdriver.Chrome(options=options)
    return driver

# Function to login to Aternos
def login_to_aternos(driver):
    driver.get('https://aternos.org/go/')
    time.sleep(3)  # Wait for the page to load completely

    google_login_button = driver.find_element(By.XPATH, '//*[@id="google-login"]')
    google_login_button.click()
    time.sleep(3)  # Wait for the Google login page to load

    # Fill in the email field
    email_field = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    email_field.send_keys(ATERNOS_USERNAME)

    # Click on the next button
    next_button = driver.find_element(By.XPATH, '//*[@id="identifierNext"]')
    next_button.click()
    time.sleep(5)  # Wait for the password page to load

    # Fill in the password field
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    password_field.send_keys(ATERNOS_PASSWORD)

    # Click on the next button
    next_button = driver.find_element(By.XPATH, '//*[@id="passwordNext"]')
    next_button.click()
    time.sleep(5)  # Wait for the Aternos page to load

def check_and_start_server(driver):
    # Navigate to the server page
    driver.get('https://aternos.org/server/')
    time.sleep(5)  # Wait for the page to load

    start_button = driver.find_element(By.XPATH, '//*[@id="start-btn"]')

    if start_button.text.lower() == "start":
        start_button.click()
        return "Server is starting..."
    else:
        return "The OutBack is already LIVE"

@bot.command()
async def start(ctx):
    driver = start_webdriver()
    login_to_aternos(driver)
    status_message = check_and_start_server(driver)
    await ctx.send(status_message)
    driver.quit()  # Close the browser

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

bot.run(DISCORD_BOT_TOKEN)
