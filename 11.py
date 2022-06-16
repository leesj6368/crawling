import telegram as tel

bot=tel.Bot(token="5555815826:AAESmlH829POH_XfKdLzL9E8W1rSH1RZM2E")


chat_id = bot.getUpdates()[-1].message.chat.id 

bot.sendMessage(chat_id=chat_id,text="test message")

