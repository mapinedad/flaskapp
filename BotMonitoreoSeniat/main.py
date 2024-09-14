#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.constants import ParseMode
from telegram.ext import (
	Application,
	CommandHandler,
	ContextTypes,
	ConversationHandler,
	MessageHandler,
	filters,
)

from statuses import *

# Enable logging
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# token del bot
BOT_TOKEN = '5284620951:AAFrPxNgKlP3KjcuzJ2LNJIbqFkrSuBxYQI'

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
	["Plataforma 💻", "Servicios 📱"],
	["Bases de Datos 💿", "Backups 💾"],
	["Salir ❌"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""Inicia la conversación y le indica al usuario que seleccione una opción."""
	user_name = update.message.from_user.first_name
	await update.message.reply_text(
		f"""Bienvenido, {user_name}. Te ayudaré con tus consultas respecto al estado de los servicios y bases de datos de SENIAT.""",
		reply_markup=markup,
	)

	return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""Verifica la opción escogida del usuario y a partir de esto ejecuta la función determinada."""
	text = update.message.text
	bot = context.bot
	chat_id = update.message.chat_id

	context.user_data["choice"] = text
	# await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

	if text == "Plataforma":
		# Llama a la función status_oas para entregar un informe del estado de toda la plataforma.
		message = status_oas(update, result)
		bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

	elif text == "Servicios":
		# Llama a la función StatusServices para entregar un informe del estado de los servicios.
		pass
	elif text == "Bases de Datos":
		# Llama a la función StatusDB para entregar un informe del estado de las bases de datos.
		pass
	elif text == "Backups":
		# Llama a la función StatusBks para entregar un informe del estado de los backups de las BD.
		pass
	else:
		# Indica que ha decidido terminar con el proceso.
		return ConversationHandler.END

	return TYPING_REPLY


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	"""Display the gathered info and end the conversation."""
	user_data = context.user_data
	if "choice" in user_data:
		del user_data["choice"]

	await update.message.reply_text(
		f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
		reply_markup=ReplyKeyboardRemove(),
	)

	user_data.clear()
	return ConversationHandler.END


def main() -> None:
	"""Run the bot."""
	# Create the Application and pass it your bot's token.
	application = Application.builder().token(BOT_TOKEN).build()

	# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler("start", start)],
		states={
			CHOOSING: [
				MessageHandler(
					filters.Regex("^(Plataforma|Servicios|Bases de Datos|Backups)$"), regular_choice
				)
			],
			TYPING_CHOICE: [
				MessageHandler(
					filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
				)
			]
		},
		fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
	)

	application.add_handler(conv_handler)

	# Run the bot until the user presses Ctrl-C
	application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()