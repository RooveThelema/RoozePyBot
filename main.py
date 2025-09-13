from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os


#Кнопки
class Buttons():

    def timetable_button(self):
        return InlineKeyboardButton("Получить расписание", callback_data="timetable_data")
        

    def app_button(self):
        return InlineKeyboardButton("Приложение", url="https://roove.ru/app")
    
    def report_button(self):
        return InlineKeyboardButton("Отправить ошибку", callback_data="error_data")
    
    def suggest_improvement_button(self):
        return InlineKeyboardButton("Отправить идею", callback_data="suggest_improvement_data")

#Сборк кнопок
class Keyboards():

    def build_a_buttons(self):

        build_buttons = Buttons()

        button_app = build_buttons.app_button()
        button_report = build_buttons.report_button()
        button_suggest_improvement = build_buttons.suggest_improvement_button()

        #Массив с кнопками
        keyboards = [[button_app, button_report, button_suggest_improvement]]

        
        return InlineKeyboardMarkup(keyboards)
    
class UserDataHandlers():
    pass

#Сам бот
class Bot():

    
    #Инициализация
    def __init__(self):

        #Токен бота
        load_dotenv("token.env")
        self.TOKEN = os.getenv("BOT_TOKEN")
        #Создание приложения бота
        self.app = Application.builder().token(self.TOKEN).build()

        #объект класса Keyboards
        self.buttons = Keyboards()
        #Команды бота
        self.app.add_handler(CommandHandler("start", self.start))

    #Start
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        #Переменная с классом Keyboards и методом build_a_buttons() - сборка
        reply_markup = self.buttons.build_a_buttons()
        #Вывод кнопок и приветственного сообщения
        await update.message.reply_text("Привет! Я бот от команды Roove! \nЯ могу присылать расписание и разные события в ваши беседы и личные сообщения!", reply_markup=reply_markup)

    #Запуск бота
    def run(self):
        self.app.run_polling()
    

bot = Bot()

bot.run()