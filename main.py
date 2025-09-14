from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os

#Кнопки
class Buttons():

    def timetable_button(self):
        return InlineKeyboardButton("Расписание", callback_data="timetable_data")
        
    def app_button(self):
        return InlineKeyboardButton("Приложение", url="https://roove.ru/app")
    
    def report_button(self):
        return InlineKeyboardButton("Сообщить об ошибке 💅", callback_data="error_data")
    
    def suggest_improvement_button(self):
        return InlineKeyboardButton("Ваши идеи", callback_data="suggest_improvement_data")
    

#Специальные кнопки
class SpecialButtons():

    def return_button(self):
        return InlineKeyboardButton("Назад", callback_data="return_data")

#Сборка специальных кнопок
class KeyboardsSpecial():

    def build_a_spectial_buttons(self):
        buttons = SpecialButtons()

        spectial_buttons = buttons.return_button()

        keyboards = [[spectial_buttons]]

        return InlineKeyboardMarkup(keyboards)

#Сборка кнопок
class Keyboards():

    def build_a_buttons(self):

        #Создание объекта build_buttons
        build_buttons = Buttons()

        #Кнопка приложения
        button_app = build_buttons.app_button()

        #Кнопка ошибок
        button_report = build_buttons.report_button()

        #Кнопка желаний
        button_suggest_improvement = build_buttons.suggest_improvement_button()

        button_timetable = build_buttons.timetable_button()

        #Массив с кнопками
        keyboards = [
            [button_app], 
            [button_timetable,], 
            [button_suggest_improvement],
            [button_report]]

        
        return InlineKeyboardMarkup(keyboards)

#Обрабатывает действия с кнопками
class UserDataHandlers():

    #async функция для обработки нажатий на кнопки
    async def button_activity(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        #Переменная которая служит для получения данных о нажатой кнопке
        button = update.callback_query

        #Ответ на нажатие кнопки
        await button.answer()

        data = button.data
        user = button.from_user

        #if button.data == "suggest_improvement_data":
        #    await button.message.reply_text("Принял")
        #error_data, suggest_improvement_data

        main_markup = Keyboards().build_a_buttons()
        specital_buttons = KeyboardsSpecial().build_a_spectial_buttons()

        match data:
            case "error_data":

                cansel = "Отмена"
                await button.message.edit_text(f"В сообщение ниже, опишите вашу проблему! Если вы передумали, нажмите кнопку {cansel}.", reply_markup=specital_buttons)
                
            case "suggest_improvement_data":
                await button.message.edit_text("В сообщение ниже, опишите ваше предложение по улучшению бота!",reply_markup=specital_buttons)

            case "timetable_data":
                await button.message.edit_text("Расписание: ", reply_markup=specital_buttons)

            case "return_data":
                await button.message.edit_text("В списке ниже, Вы можете повторно выбрать, куда вернётесь.", reply_markup=main_markup)

class UserDataHandlersReturn():
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


        #Объект класса UserDataHandlers
        self.user_data = UserDataHandlers()

        #Объект класса Keyboards
        self.buttons = Keyboards()
        #Команды бота
        self.app.add_handler(CommandHandler("start", self.start))

        #Обработчик кнопок
        self.app.add_handler(CallbackQueryHandler(self.user_data.button_activity))
        


    #Start
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        #Переменная с классом Keyboards и методом build_a_buttons() - сборка
        reply_markup = self.buttons.build_a_buttons()
        #Вывод кнопок и приветственного сообщения
        await update.message.reply_text("Привет! Я бот от команды Roove! \nЯ могу присылать расписание и разные события в ваши беседы и личные сообщения! \n Выберите действие.", reply_markup=reply_markup)

    #Запуск бота
    def run(self):
        self.app.run_polling()
    

bot = Bot()

bot.run()