#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import threading
import json
from time import sleep
import datetime
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class TeleBot(telegram.Bot):

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self):
        # Lee el token del bot desde el campo "token" en token.json
        with open("token.json", 'r') as token_file:  
            token = json.load(token_file)["token"]
        
        super().__init__(token)  # La verdad que ni uso funcionalidad heredada pero por las dudas
        updater = Updater(token, use_context=True)

        self.lista_nombres = []
        self.boludeo = True

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Commands
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(CommandHandler("putear", self.start_putear))
        dp.add_handler(CommandHandler("stop_putear", self.stop_putear))
        dp.add_handler(CommandHandler("toggle_boludeo", self.toggle_boludeo))
        
        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.echo))
        
        dp.add_error_handler(self.error)  # log all errors        
        updater.start_polling()  # Start the Bot

        t2 = threading.Thread(target=self.checkTime, daemon=True)
        t2.start()
        updater.idle()

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        context.bot.send_message(update.message.chat_id, text="Que tal?")


    def help(self, update, context):
        """Send a message when the command /help is issued."""
        context.bot.send_message(update.message.chat_id, text="Mi única función es llamar al unobot y decir puto el que lee")


    def echo(self, update, context):
        """Echo the user message."""
        especial_list = ['a', 'e', 'o', 'u', 'á', 'é', 'ó', 'ú']
        mensaje_alterado = update.message.text

        for c in especial_list:
            mensaje_alterado = mensaje_alterado.replace(c, 'i').replace(c.upper(), 'I')

        user = update.message.from_user
        nombre = user.first_name + " " + user.last_name
        print(user)
        if not user.is_bot:
            if self.boludeo:
                update.message.reply_text(f"{mensaje_alterado} jajajaj re gay")
                thread_delete = threading.Thread(target=self.delayed_delete, daemon=True, args=(context, update.message.chat_id, update.message.message_id))
                thread_delete.start()
            if nombre not in self.lista_nombres:
                context.bot.send_message(update.message.chat_id, text=f"Hola {nombre}! Ahora Unobotcaller sabe donde vives")
                self.lista_nombres.append(nombre)
        else:
            context.bot.send_message(update.message.chat_id, text="Alguien más huele a bot?")
            sleep(2)
            update.message.reply_text("Aca te encontré forro, sali de aca")
            context.bot.delete_message(update.message.chat_id, update.message.message_id)
            context.bot.kick_chat_member(update.message.chat_id, user.id)

    @staticmethod
    def delayed_delete(context, chat_id, message_id):
        sleep(1)
        try:
            context.bot.delete_message(chat_id, message_id)
        except:
            print("Faltan privilegios para borrar!")

    def toggle_boludeo(self, update, context):
        self.boludeo = not self.boludeo
        if self.boludeo:
             context.bot.send_message(update.message.chat_id, text="Boludeo activado")
        else:
            context.bot.send_message(update.message.chat_id, text="Boludeo desactivado")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        TeleBot.logger.warning('Update "%s" caused error "%s"', update, context.error)


    timeNotRepeated = True
    def checkTime(self):
        while True:
            today = datetime.datetime.now()
            if datetime.datetime.now().hour % 2 == 1:
                if TeleBot.timeNotRepeated:
                    self.sendMessage(-1001194076638, text="/start@unobot")
                    TeleBot.timeNotRepeated = False
            else:
                TeleBot.timeNotRepeated = True

    puteando = True
    def start_putear(self, update, context):
        TeleBot.puteando = True
        self.t = threading.Thread(target=TeleBot.putear, args=(update, context))
        self.t.start()
        
    @staticmethod
    def putear(update, context):
        while TeleBot.puteando:
            sleep(1)
            context.bot.send_message(update.message.chat_id, text="Puto el que lee")
        update.message.reply_text("._.")
        update.message.reply_text("Putazo")

    def stop_putear(self, update, context):
        if self.t is not None:
            TeleBot.puteando = False
            self.t.join()
        else:
            update.message.reply_text("El que lee no es puto")


def main():
    bot = TeleBot()


if __name__ == '__main__':
    main()