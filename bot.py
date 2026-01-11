from logic import DB_Manager
from config import *
from telebot import TeleBot

bot = TeleBot(TOKEN)
manager = DB_Manager(DATABASE)
manager.create_tables()

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Я бот с рецептами 🍳\nЯ могу показывать рецепты, ингредиенты и категории блюд!")

@bot.message_handler(commands=['all_recipes'])
def all_recipes(message):
    recipes = manager.get_all_recipes()
    if recipes:
        response = "\n".join([f"{r[1]} ({r[2]}) - Рейтинг: {r[4]}" for r in recipes])
    else:
        response = "Пока нет рецептов."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['category'])
def category_recipes(message):
    category = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not category:
        bot.send_message(message.chat.id, "Введите команду так: /category <название категории>")
        return
    recipes = manager.get_recipe_by_category(category)
    if recipes:
        response = "\n".join([f"{r[1]} - Рейтинг: {r[4]}" for r in recipes])
    else:
        response = f"Рецептов в категории '{category}' не найдено."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['ingredients'])
def ingredients(message):
    try:
        recipe_id = int(message.text.split(maxsplit=1)[1])
        ingredients = manager.get_ingredients_for_recipe(recipe_id)
        if ingredients:
            response = "\n".join([f"{name} - {qty}" for name, qty in ingredients])
        else:
            response = "Ингредиенты не найдены."
    except:
        response = "Введите команду так: /ingredients <ID рецепта>"
    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
    bot.infinity_polling()
