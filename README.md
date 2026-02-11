## About
TrackPrice is a price tracking tool that monitors product prices from various online stores and notifies users via Discord when prices drop. Also, it stores the product information in a CSV file for easy access.

## Features
- Track prices of different products from multiple shops
- Receive notifications once the prices drop
- Setup is simple and straightforward (see Configuration section below)

## Configuration
1. Clone the repository `git clone https://github.com/shihabhasan0161/trackprice.git`
2. Create virtual env `python -m venv .venv`, then activate it and install the packages `pip install -r requirements.txt`
3. Create a .env file in the root directory
4. Go to discord.com/developers/applications and create a new application
5. Go to the "Bot" tab and change username if you want
6. Click on "Reset Token" and copy the token and use it as DISCORD_TOKEN in your .env file
7. Scroll down and enable "MESSAGE CONTENT INTENT"
8. Go to the "OAuth2" tab and then "URL Generator"
9. Select "bot" in SCOPES
10. Select "Send Messages" and "Read Message History" in BOT PERMISSIONS
11. Copy the generated URL and open it in your browser to add the bot to your server
12. If you haven't turned on Developer Mode in Discord, go to User Settings > Advanced > Developer Mode and enable it
13. Right click on the channel you want to use and click on "Copy ID"
14. Use the copied ID as CHANNEL_ID in your .env file

## How to Use
1. Run `python local.py` and copy paste any amazon or playstation product links you want to track
2. This will create a `products.csv` file in the root directory
3. You may enter 'q' to stop adding products
4. To check for price updates, run `python local.py` again
5. If you wish to run this script every 24 hours, you can use crontab to run it.

## Why I built this
I built this scrapper for amazon and playstation store because I recently needed to purchase a game. I wanted to wait for a price drop, as I couldn't find an existing free tool to do this. So, I decided to build this myself just for a fun project. Feel free to use it!

## Disclaimer
For educational purposes only. Scraping may violate site TOS. Read the sites' terms before use. Not affiliated with any mentioned companies.

## Future Improvements
- Add more shops to track prices from
- Add a streamlit web app for easier management
- Integrate other notifier methods (e.g., email, whatsapp, telegram)
- Improve error handling and logging
- More user friendly messages and notifications