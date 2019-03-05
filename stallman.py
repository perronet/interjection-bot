from telegram.ext import Updater, MessageHandler, CommandHandler, Handler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import telegram, time, logging, time, datetime
import re

token = #API token goes here
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
updater = Updater(token)
dispatcher = updater.dispatcher
log = open("log", "w+")
non_free = 0
language = "en"

en_text_opensource = ("Open Source misses the point of Free Software, "
"the terms \"free software\" and \"open source\" stand for almost the same range of programs. "
"However, they say deeply different things about those programs, based on different values.\n"
"The free software movement campaigns for freedom for the users of computing; it is a movement for freedom "
"and justice. By contrast, the open source idea values mainly practical advantage and does not campaign for principles.\n"
"This is why we do not agree with open source, and do not use that term.")

it_text_opensource = ("L\'Open Source non coglie gli obiettivi del Software Libero. "
"I termini \"software libero\" e \"open source\" rappresentano quasi la stessa gamma di programmi, "
"tuttavia dicono cose profondamente diverse su di essi, basate su valori diversi.\n"
"Il movimento del software libero promuove la libertà per gli utenti; è un movimento per la libertà e la giustizia. "
"Al contrario, l\'idea dell\'Open Source valorizza principalmente il vantaggio pratico e non promuove i nostri principi.\n"
"Per questo motivo non siamo d\'accordo con l\'Open Source e non usiamo questo termine.")

en_text_gnulinux = ("I\'d just like to interject for a moment.  What you\'re referring to as Linux, "
"is in fact, GNU/Linux, or as I\'ve recently taken to calling it, GNU plus Linux.\n"
"Linux is not an operating system unto itself, but rather another free component "
"of a fully functioning GNU system made useful by the GNU corelibs, shell "
"utilities and vital system components comprising a full OS as defined by POSIX.\n"
"Many computer users run a modified version of the GNU system every day, "
"without realizing it.  Through a peculiar turn of events, the version of GNU "
"which is widely used today is often called \"Linux\", and many of its users are "
"not aware that it is basically the GNU system, developed by the GNU Project.\n"
"There really is a Linux, and these people are using it, but it is just a "
"part of the system they use.  Linux is the kernel: the program in the system "
"that allocates the machine\'s resources to the other programs that you run.\n"
"The kernel is an essential part of an operating system, but useless by itself; "
"it can only function in the context of a complete operating system.  Linux is "
"normally used in combination with the GNU operating system: the whole system "
"is basically GNU with Linux added, or GNU/Linux.  All the so-called \"Linux\" "
"distributions are really distributions of GNU/Linux.")

it_text_gnulinux = ("Mi piacerebbe solo intervenire per un momento. Ciò a cui ti stai riferendo come Linux, "
"è in effetti, GNU/Linux, o come ho recentemente cominciato a chiamarlo, GNU+Linux.\n"
"Linux non è un sistema operativo in sé, ma piuttosto un altro componente gratuito "
"di un sistema GNU pienamente funzionante reso utile dai corelibs GNU, utilities della shell "
"e componenti vitali del sistema i quali formano un sistema operativo completo come definito da POSIX.\n"
"Molti utenti eseguono una versione modificata del sistema GNU ogni giorno, "
"senza rendersene conto. Attraverso un particolare giro di eventi, la versione di GNU "
"che è ampiamente usata oggi è spesso chiamata \"Linux\" e molti dei suoi utenti "
"non sanno che è fondamentalmente il sistema GNU, sviluppato dal Progetto GNU.\n"
"C\'è davvero un Linux, e queste persone lo stanno usando, ma è solo una "
"parte del sistema che usano. Linux è il kernel: il programma nel sistema "
"che assegna le risorse della macchina agli altri programmi che vengono eseguiti.\n"
"Il kernel è una parte essenziale di un sistema operativo, ma inutile da solo; "
"può funzionare solo nel contesto di un sistema operativo completo. Linux è "
"normalmente utilizzato in combinazione con il sistema operativo GNU: l\'intero sistema "
"è fondamentalmente GNU con Linux aggiunto, o GNU/Linux. Tutte le cosiddette "
"distribuzioni di \"Linux\" sono realmente distribuzioni di GNU/Linux.")

help_text = """
/start - start the bot
/lang - change language
/nonfree - see amount of interjections
/help - get help
"""

def interjection_gnulinux(bot, update):
    update_log(update)
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(5)    
    update.message.reply_text(text=en_text_gnulinux if language == "en" else it_text_gnulinux, quote=True)

def interjection_opensource(bot, update):
    update_log(update)
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(5)    
    update.message.reply_text(text=en_text_opensource if language == "en" else it_text_opensource, quote=True)

def update_log(update):
    with open("log", "a") as log:
        global non_free
        non_free += 1
        message = "{0} ({1}) wrote: '{2}'".format(update.effective_user.username, update.effective_user.first_name, 
                                                 update.effective_message.text)
        print(message)
        print("Interjections: {0}\n".format(non_free))
        log.write("[{0}] {1}\n".format(str(datetime.datetime.now()).split('.')[0], message))

def lang(bot, update):
    buttons = [[
    InlineKeyboardButton(text="English", callback_data="en"),
    InlineKeyboardButton(text="Italian", callback_data="it")
    ]]
    bot.send_message(chat_id=update.message.chat_id, text="Please select a language\n", 
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

def select_lang(bot, update):
    global language
    if update.callback_query.data == "en":
        language = "en"
        print("Changed language to English")
    elif update.callback_query.data == "it":
        language = "it"
        print("Changed language to Italian")
    else:
        print("Error")
    #When the user presses any button, delete inline keyboard message
    bot.delete_message(chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id)

#Command handlers
start_handler = CommandHandler("start", lambda bot, update : lang(bot, update))
lang_handler = CommandHandler("lang", lang)
help_handler = CommandHandler("help", lambda bot, update : bot.send_message(chat_id=update.message.chat_id, text=help_text))
nonfree_handler = CommandHandler("nonfree", lambda bot, update : bot.send_message(chat_id=update.message.chat_id, 
                                text="Interjections: {0}".format(non_free)))

#Regex to filter incoming messages
pattern_gnulinux = re.compile("(?<!GNU/)(?<!GNU\+)(?<!GNU )(?<!GNU plus )linux", re.IGNORECASE)
pattern_opensource = re.compile("(open\s*source)|(software\s*libero)", re.IGNORECASE)
syntax_check_gnulinux = MessageHandler(Filters.regex(pattern_gnulinux), interjection_gnulinux)
syntax_check_opensource = MessageHandler(Filters.regex(pattern_opensource), interjection_opensource)  

dispatcher.add_handler(start_handler)
dispatcher.add_handler(lang_handler)
dispatcher.add_handler(CallbackQueryHandler(select_lang))
dispatcher.add_handler(help_handler)
dispatcher.add_handler(nonfree_handler)
dispatcher.add_handler(syntax_check_gnulinux) #Overrides opensource if a message contains both
dispatcher.add_handler(syntax_check_opensource)

updater.start_polling(poll_interval=3, timeout=10, clean=False, bootstrap_retries=-1, 
                     read_latency=2.0, allowed_updates=None)
