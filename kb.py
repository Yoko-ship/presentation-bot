from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove

# Создаем меню бота
menu = [
    [InlineKeyboardButton(text="📝 Генерировать текст",callback_data="generate_text"),
    InlineKeyboardButton(text="Сделать презентацию",callback_data="generate_presentation")],
    [InlineKeyboardButton(text="🔎 Помощь",callback_data="help")],
]
slides = [
    [InlineKeyboardButton(text="8 ",callback_data="slides 8",),
     InlineKeyboardButton(text="10 ",callback_data="slides 10",),
     InlineKeyboardButton(text="12 ",callback_data="slides 12",),
    ]
]
text = [
    [InlineKeyboardButton(text="Формальный",callback_data="text Формальный"),
     InlineKeyboardButton(text="Обычный",callback_data="text Обычный"),
     InlineKeyboardButton(text="Профессиональный",callback_data="text Профессиональный")
     ]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
slides = InlineKeyboardMarkup(inline_keyboard=slides)
text=InlineKeyboardMarkup(inline_keyboard=text)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]],resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню",callback_data="menu")]])