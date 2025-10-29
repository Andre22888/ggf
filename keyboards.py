from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💵 Купить доступ', callback_data='buy')],
    [InlineKeyboardButton(text='🪛 Как активировать?', callback_data='how')],
    [InlineKeyboardButton(text='👤 Мой профиль', callback_data='profile')]
])

buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⭐️ Звезды', callback_data='stars')],
    [InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back')]
])

stars = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оплатить ⭐️', pay=True)]])
back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back')]])
accept = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ознакомлен и Согласен', callback_data='accept')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
])

main_access = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎟 Предъявить билет', web_app=WebAppInfo(url='https://andre22888.github.io/gamebus.github.io/ttt.html'))],
    [InlineKeyboardButton(text='🪛 Как активировать?', callback_data='how')],
    [InlineKeyboardButton(text='👤 Мой профиль', callback_data='profile')],
    [InlineKeyboardButton(text='📞 Feedback', callback_data='feedback')]
])

feedback = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back')]
])

admin_reply = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✉️ Ответить', callback_data='admin_reply')],
    [InlineKeyboardButton(text='❌ Закрыть', callback_data='close_ticket')]
])

profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔗 Реферальная ссылка", callback_data="ref_link")],
    [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back")]
])

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📊 Таблица пользователей", callback_data="admin_users")],
    [InlineKeyboardButton(text="🎁 Выдать подписку", callback_data="admin_give_sub"),
     InlineKeyboardButton(text="🚫 Забрать подписку", callback_data="admin_take_sub")],
    [InlineKeyboardButton(text="🔨 Забанить", callback_data="admin_ban"),
     InlineKeyboardButton(text="🔓 Разбанить", callback_data="admin_unban")],
    [InlineKeyboardButton(text="📋 Список забаненных", callback_data="admin_banned_list")],
    [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back")]
])

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_cancel")]
])