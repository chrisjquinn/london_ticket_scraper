import telegram.bot
import os
import pandas as pd
import time

# Scraper import
# This will trigger them to run 
# (could do with changing)
from scrapers import todaytix
from scrapers import lovetheatre

TOKEN = None
CHATID = None
try:
    token_file = open("secrets/telegram_token")
    chat_id_file = open("secrets/telegram_chatid")
    TOKEN = str(token_file.read())
    CHATID = str(chat_id_file.read())
except IOError:
    print("Token file not accessible")
finally:
    token_file.close()
    chat_id_file.close()


'''
run.py will just check two file outputs from the todaytix and lovetheatre scrapers
taking the cheaper of the two
'''

today_tix_df = pd.read_csv('data/todaytix.csv')
lovetheatre_df = pd.read_csv('data/lovetheatre.csv')

notif_todaytix = today_tix_df[today_tix_df['Price'] <= 15]
# notif_lovetheatre = lovetheatre_df[lovetheatre_df['Price'] <= 15]



musicals = notifier_tix[notifier_tix['Genre'].str.contains('Musical')]
plays = notifier_tix[notifier_tix['Genre'].str.contains('Play')]
others = notifier_tix.drop(index = musicals.index).drop(index = plays.index)


########
# Notifications
########


# if TOKEN and CHATID:
# 	print("Notifying to telegram...")
# 	bot = telegram.bot.Bot(token=TOKEN)
# 	bot.send_message(chat_id=CHATID, text="---- SUNDAY SCRAPE ----")
# 	time.sleep(3)

# 	bot.send_message(chat_id=CHATID, text="Musicals:")
# 	for index, row in musicals.iterrows():
# 		message = f"{row['Name']}, £{int(row['Price'])}.\n{row['URL']}"
# 		bot.send_message(chat_id=CHATID, text=message)
# 		time.sleep(2)

# 	time.sleep(3)

# 	# bot.send_message(chat_id=CHATID, text="Plays:")
# 	# for index, row in plays.iterrows():
# 	# 	message = f"{row['Name']}, £{int(row['Price'])}.\n{row['URL']}"
# 	# 	bot.send_message(chat_id=CHATID, text=message)
# 	# 	time.sleep(2)

# 	# time.sleep(3)

# 	bot.send_message(chat_id=CHATID, text="Everything else:")
# 	for index, row in others.iterrows():
# 		message = f"{row['Name']}, £{int(row['Price'])}.\n{row['URL']}"
# 		bot.send_message(chat_id=CHATID, text=message)
# 		time.sleep(2)

# 	print("Notifying completed.")
# else:
# 	pass
