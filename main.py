import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


URL = 'https://www.blocket.se/hela_sverige?q=&cg=1020&w=3&st=s&ps=&pe=14&mys=&mye=&ms=&me=&cxpf=&cxpt=&fu=&pl=&gb=&ca=11&l=0&md=th&cb=22&cbl1=20'

file = open("message.txt", "r", encoding='utf-8')
MESSAGE = file.read()

@bot.message_handler(commands = ['start'])
def sendInfo(message):
	bot.send_message(message.chat.id, MESSAGE, parse_mode = "Markdown")
	# print(MESSAGE)

def sendMessage(l, message):
	msg = 'Нове оголошення на сайті!\n'
	bot.send_message(message.chat.id, msg + l)
	# print(link)

@bot.message_handler(commands = ['link'])
def main(message):
	try:
		# ---------------------

		req = requests.get(URL).text
		html = BeautifulSoup(req, 'lxml')

		
		pastElLink = html.find('section', class_ = 'row').find('div', id = 'item_list').find('article', class_ = 'media item_row item_row_first ptm pbm nmt').find('a', title = 'Flera bilder')['href']
		# print(pastElLink	)
		sendMessage(pastElLink, message)
		while 1:
			req = requests.get(URL).text
			html = BeautifulSoup(req, 'lxml')
			elementLink = html.find('section', class_ = 'row').find('div', id = 'item_list').find('article', class_ = 'media item_row item_row_first ptm pbm nmt').find('a', title = 'Flera bilder')['href']
			if pastElLink != elementLink:
				sendMessage(elementLink, message)
			pastElLink = elementLink
		
	except Exception as e:
		print(e)


bot.polling()

