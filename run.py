import asyncio
import json
import os
import re
from datetime import datetime, timedelta

from aiogram.types import WebAppInfo, InputFile, FSInputFile
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, ChatMember
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import TOKEN, ADMIN_ID, amount, REFERAL_BONUS, DISCOUNTED_PRICE, REGULAR_PRICE, BOT_URL

import keyboards as kb

import os

if not os.path.exists('database'):
    os.makedirs('database')

bot = Bot(token=TOKEN)
dp = Dispatcher()

class quest(StatesGroup):
    id = State()
    code = State()

class FeedbackState(StatesGroup):
    waiting_for_feedback = State()
    admin_replying = State()

class AdminActions(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_ban_user_id = State()
    waiting_for_unban_user_id = State()
    waiting_for_give_sub_user_id = State()
    waiting_for_take_sub_user_id = State()

MAIN_MENU_IMAGE = 'https://i.ibb.co/GvbSt5Gx/Picsart-25-08-24-12-18-34-572.jpg'
PROFILE_IMAGE = 'https://i.ibb.co/sd0pt3dx/Picsart-25-08-24-12-19-50-105.jpg'
BUY_IMAGE = 'https://i.ibb.co/PZfWSYj1/Picsart-25-08-24-12-19-03-266.jpg'
HOW_IMAGE = 'https://i.ibb.co/v6K53nFz/Picsart-25-08-24-12-20-54-050.jpg'
FEEDBACK_IMAGE = 'https://i.ibb.co/JWf6BGF7/Picsart-25-08-24-12-42-15-056.jpg'

@dp.update.outer_middleware()
async def ban_middleware(handler, event, data):
    if isinstance(event, Message):
        user_id = event.from_user.id
    elif isinstance(event, CallbackQuery):
        user_id = event.from_user.id
    elif isinstance(event, PreCheckoutQuery):
        user_id = event.from_user.id
    else:
        return await handler(event, data)
    
    if os.path.exists(f'database/{user_id}.json'):
        with open(f'database/{user_id}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('banned', False):
                if isinstance(event, Message):
                    await event.answer("❌ Вы забанены и не можете использовать бота.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("❌ Вы забанены.", show_alert=True)
                return
    
    return await handler(event, data)

@dp.message(CommandStart())
async def start(message: Message, bot: Bot):
    user_id = message.from_user.id
    
    if os.path.exists(f'database/{user_id}.json'):
        with open(f'database/{user_id}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('banned', False):
                await message.answer("❌ Вы забанены и не можете использовать бота.")
                return
    if not os.path.exists('database'):
        os.makedirs('database')

    
    args = message.text.split()
    referrer_id = None
    
    if len(args) > 1:
        if args[1].startswith('ref_'):
            try:
                referrer_id = int(args[1].split('_')[1])
            except:
                pass
    
    if os.path.exists(f'database/{user_id}.json'):
        # print(f'{user_id} уже в базе')
        with open(f"database/{message.from_user.id}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        with open(f"database/{user_id}.json", "w+", encoding="utf-8") as file:
            data = {
                "id": user_id, 
                "access": 0, 
                "subscribe": 0,
                "referrals": [],
                "referrer": referrer_id,
                "feedback_messages": [],
                "banned": False,
                "ban_date": None,
                "original_subscription": 0
            }
            json.dump(data, file, indent=4)
        
        if referrer_id and os.path.exists(f'database/{referrer_id}.json'):
            with open(f"database/{referrer_id}.json", "r", encoding="utf-8") as file:
                referrer_data = json.load(file)
            
            if "referrals" not in referrer_data:
                referrer_data["referrals"] = []
            
            if user_id not in referrer_data["referrals"]:
                referrer_data["referrals"].append(user_id)
                
            with open(f"database/{referrer_id}.json", "w", encoding="utf-8") as file:
                json.dump(referrer_data, file, indent=4)
        
    if data["access"] == 1:
        if data["subscribe"] == 1:
            await message.answer_photo(photo=MAIN_MENU_IMAGE,
                                   caption=f'<b>✨ Привет!</b> \nЗдесь вы можете пользоваться <b>приложением</b>.',
                                   reply_markup=kb.main_access,
                                   parse_mode='HTML'
                                )
            
        else:
            await message.answer_photo(photo=MAIN_MENU_IMAGE,
                                   caption=f'<b>✨ Привет!</b> \nЗдесь вы можете приобрести доступ к <b>приложению</b>.',
                                   reply_markup=kb.main,
                                   parse_mode='HTML'
                                )
    else:
        try:
            await message.answer_document(
                document=FSInputFile("ps.docx"),
                caption="Перед началом использования бота и приложения вы обязаны ознакомиться и согласиться с Пользовательским соглашением. "
                       "Если вы не согласны - не используйте бота.",
                reply_markup=kb.accept
            )
        except Exception as e:
            print(f"Ошибка при отправке файла: {e}")
            await message.answer(
                "Перед началом пользования бота и приложения вы обязаны ознакомиться и согласиться с Пользовательским соглашением. "
                "Если вы не согласны - не используйте бота.",
                reply_markup=kb.accept
            )

@dp.callback_query(F.data == 'accept')
async def accept(callback: CallbackQuery):
    user_id = callback.from_user.id
    with open(f"database/{user_id}.json", encoding="utf-8") as file:
        data = json.load(file)
        
    data['access'] = 1
    
    with open(f"database/{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
    await callback.message.delete()    
    await callback.message.answer_photo(photo=MAIN_MENU_IMAGE,
                                   caption=f'<b>✨ Привет!</b> \nЗдесь вы можете приобрести доступ к <b>приложению</b>.',
                                   reply_markup=kb.main,
                                   parse_mode='HTML'
                                )

@dp.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы отказались от использования бота")

@dp.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    with open(f"database/{callback.from_user.id}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    if data["subscribe"] == 1:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=MAIN_MENU_IMAGE,
                caption=f'<b>✨ Привет!</b> \nЗдесь вы можете пользоваться <b>приложением</b>.',
                parse_mode='HTML'
            ),
            reply_markup=kb.main_access
        )
    else:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=MAIN_MENU_IMAGE,
                caption=f'<b>✨ Привет!</b> \nЗдесь вы можете приобрести доступ к <b>приложению</b>.',
                parse_mode='HTML'
            ),
            reply_markup=kb.main
        )
    
@dp.callback_query(F.data == 'buy')
async def buy(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=BUY_IMAGE,
            caption=f'<b>💼 Выберите способ оплаты: </b>',
            parse_mode='HTML'
        ),
        reply_markup=kb.buy
    )
    
@dp.callback_query(F.data == 'how')
async def how(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=HOW_IMAGE,
            caption=f'<b>🪛 Как активировать приложение:</b>\n\nВы приобретаете подписку за звезды, затем получаете доступ писать в фидбек, связываетесь с администратором и активируете приложение.',
            parse_mode='HTML'
        ),
        reply_markup=kb.back
    )
    
@dp.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    with open(f"database/{callback.from_user.id}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    if "referrals" not in data:
        data["referrals"] = []
        with open(f"database/{callback.from_user.id}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    if data["subscribe"] == 1:
        access = 'Активна'
    else:
        access = 'Не активна'
    
    referrals_count = len(data.get("referrals", []))
    referral_link = f"{BOT_URL}?start=ref_{callback.from_user.id}"
    
    if callback.from_user.id == ADMIN_ID:
        role_status = "👑 Администратор /admin"
    else:
        role_status = "👤 Пользователь"
        
    discount_status = "да" if referrals_count >= REFERAL_BONUS else "нет"
    discount_info = f"\n<b>🎫 Скидка:</b> {discount_status} ({referrals_count}/{REFERAL_BONUS} рефералов)"
        
    await callback.answer()
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=PROFILE_IMAGE,
            caption=f'<b>👤 Ваш профиль</b> @{callback.from_user.username}: \n\n'
                    f'<b>🆔 ID:</b> {callback.from_user.id} \n'
                    f'<b>💳 Подписка:</b> {access} \n'
                    f'<b>👥 Рефералы:</b> {referrals_count}'
                    f'{discount_info} \n'
                    f'<b>👤 Роль:</b> {role_status}\n\n'
                    f'<b>🔗 Реф. ссылка:</b> \n<code>{referral_link}</code>',
            parse_mode='HTML'
        ),
        reply_markup=kb.profile_keyboard
    )

@dp.callback_query(F.data == 'ref_link')
async def ref_link(callback: CallbackQuery):
    referral_link = f"{BOT_URL}?start=ref_{callback.from_user.id}"
    await callback.answer()
    await callback.message.answer(
        f"<b>🔗 Ваша реферальная ссылка:</b>\n<code>{referral_link}</code>\n\n"
        f"Поделитесь этой ссылкой с друзьями. За каждого приглашенного друга вы получите скидку!",
        parse_mode='HTML'
    )

@dp.callback_query(F.data == 'stars')
async def stars(callback: CallbackQuery):
    with open(f"database/{callback.from_user.id}.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if "referrals" not in data:
        data["referrals"] = []
        with open(f"database/{callback.from_user.id}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    referrals_count = len(data.get("referrals", []))
    final_amount = DISCOUNTED_PRICE if referrals_count >= REFERAL_BONUS else REGULAR_PRICE

    price_info = (
        "<b>💰 Цены на подписку:</b>\n\n"
        f"<b>📈 Стандартная цена:</b> ⭐️{REGULAR_PRICE}\n"
        f"<b>📉 Цена с учетом скидки:</b> ⭐️{DISCOUNTED_PRICE}\n\n"
        "<i>Получить скидку можно пригласив 3 человек по своей реферальной ссылке</i>"
    )
    await callback.message.answer(price_info, parse_mode="HTML", reply_markup=kb.profile_keyboard)

    prices = [LabeledPrice(label="XTR", amount=final_amount)]
    await callback.answer()
    await callback.message.answer_invoice(
        title="Доступ к приложению",
        description="Уникальный код доступа к приложению",
        prices=prices,
        provider_token="",
        payload="channel_support",
        currency="XTR",
        reply_markup=kb.stars
    )

@dp.callback_query(F.data == 'feedback')
async def feedback_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=FEEDBACK_IMAGE,
            caption="📞 Напишите ваше сообщение для администратора:"
        ),
        reply_markup=kb.feedback
    )
    await state.set_state(FeedbackState.waiting_for_feedback)

@dp.message(FeedbackState.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    with open(f"database/{user_id}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    if "feedback_messages" not in data:
        data["feedback_messages"] = []
    
    data["feedback_messages"].append({
        "text": message.text,
        "message_id": message.message_id
    })
    
    with open(f"database/{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    
    await bot.send_message(
        ADMIN_ID,
        f"📩 Новое сообщение от пользователя {user_id} (@{message.from_user.username}):\n\n{message.text}",
        reply_markup=kb.admin_reply
    )
    
    await message.answer("✅ Ваше сообщение отправлено администратору!")
    await state.clear()

@dp.callback_query(F.data == 'admin_reply')
async def admin_reply_start(callback: CallbackQuery, state: FSMContext):
    message_text = callback.message.text
    user_id_match = re.search(r'пользователя (\d+)', message_text)
    
    if user_id_match:
        user_id = int(user_id_match.group(1))
        await state.update_data(feedback_user_id=user_id)
        await callback.message.answer("💌 Введите ваш ответ пользователю:")
        await state.set_state(FeedbackState.admin_replying)
    else:
        await callback.answer("❌ Не удалось определить пользователя", show_alert=True)

@dp.message(FeedbackState.admin_replying)
async def process_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('feedback_user_id')
    
    if user_id:
        try:
            await bot.send_message(user_id, f"💌 Ответ от администратора:\n\n{message.text}")
            await message.answer("✅ Ответ отправлен пользователю!")
        except:
            await message.answer("❌ Не удалось отправить сообщение пользователю")
    
    await state.clear()

@dp.callback_query(F.data == 'close_ticket')
async def close_ticket(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Тикет закрыт")

# ПОКУПКА
@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
    
@dp.message(F.successful_payment)
async def progress_successful_payment(message: Message):
    user = message.from_user.first_name
    user_id = message.from_user.id
    
    with open(f"database/{user_id}.json", encoding="utf-8") as file:
        data = json.load(file)
    data['subscribe'] = 1
    
    with open(f"database/{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    await message.answer(
        text='🎉 Поздравляем с покупкой доступа к <b>приложению</b>. \n\nОжидайте, пока с вами свяжется администратор (вся переписка для удобства происходит в боте).',
        parse_mode='HTML'
    )
    
    await message.answer_photo(photo=MAIN_MENU_IMAGE,
                               caption=f'<b>✨ Привет!</b> \nЗдесь вы можете приобрести доступ к <b>приложению</b>.',
                               reply_markup=kb.main_access,
                               parse_mode='HTML'
                            )
    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Пользователь {user_id} купил подписку"
    )

@dp.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Панель администратора:", reply_markup=kb.admin_keyboard)
    else:
        await message.answer("Недостаточно прав")

@dp.callback_query(F.data == 'admin_users')
async def admin_users(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Недостаточно прав")
        return
    
    users_list = "👥 Все пользователи:\n\n"
    subscribed_users = "⭐️ Пользователи с подпиской:\n\n"
    banned_users = "🚫 Забаненные пользователи:\n\n"
    
    user_files = [f for f in os.listdir('database') if f.endswith('.json')]
    
    for user_file in user_files:
        user_id = user_file.split('.')[0]
        with open(f"database/{user_file}", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        try:
            user_info = await bot.get_chat(user_id)
            username = f"@{user_info.username}" if user_info.username else "Нет username"
            full_name = user_info.full_name if user_info.full_name else "Не указано"
        except:
            username = "Нет username"
            full_name = "Неизвестно"
        
        user_entry = f"ID: {user_id}, Имя: {full_name}, Username: {username}\n"
        users_list += user_entry
        
        if data.get("subscribe") == 1:
            subscribed_users += user_entry
            
        if data.get("banned", False):
            banned_users += user_entry
    
    await callback.message.answer(users_list)
    await callback.message.answer(subscribed_users)
    await callback.message.answer(banned_users)
    await callback.answer()

@dp.callback_query(F.data == 'admin_give_sub')
async def admin_give_sub(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Недостаточно прав")
        return
    
    await callback.message.answer("Введите ID пользователя для выдачи подписки:", reply_markup=kb.cancel_kb)
    await state.set_state(AdminActions.waiting_for_give_sub_user_id)

@dp.callback_query(F.data == 'admin_take_sub')
async def admin_take_sub(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Недостаточно прав")
        return
    
    await callback.message.answer("Введите ID пользователя для изъятия подписки:", reply_markup=kb.cancel_kb)
    await state.set_state(AdminActions.waiting_for_take_sub_user_id)

@dp.callback_query(F.data == 'admin_ban')
async def admin_ban(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Недостаточно прав")
        return
    
    await callback.message.answer("Введите ID пользователя для бана:", reply_markup=kb.cancel_kb)
    await state.set_state(AdminActions.waiting_for_ban_user_id)

@dp.callback_query(F.data == 'admin_unban')
async def admin_unban(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Недостаточно прав")
        return
    
    await callback.message.answer("Введите ID пользователя для разбана:", reply_markup=kb.cancel_kb)
    await state.set_state(AdminActions.waiting_for_unban_user_id)

@dp.callback_query(F.data == 'admin_banned_list')
async def admin_banned_list(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Недостаточно прав")
        return
    
    banned_users = "🚫 Забаненные пользователи:\n\n"
    
    user_files = [f for f in os.listdir('database') if f.endswith('.json')]
    
    for user_file in user_files:
        user_id = user_file.split('.')[0]
        with open(f"database/{user_file}", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        if data.get("banned", False):
            try:
                user_info = await bot.get_chat(user_id)
                username = f"@{user_info.username}" if user_info.username else "Нет username"
                full_name = user_info.full_name if user_info.full_name else "Не указано"
            except:
                username = "Нет username"
                full_name = "Неизвестно"
            
            ban_date = data.get("ban_date", "Неизвестно")
            banned_users += f"ID: {user_id}, Имя: {full_name}, Username: {username}, Дата бана: {ban_date}\n"
    
    if banned_users == "🚫 Забаненные пользователи:\n\n":
        banned_users = "🚫 Нет забаненных пользователей"
    
    await callback.message.answer(banned_users)
    await callback.answer()

@dp.callback_query(F.data == 'admin_cancel')
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Действие отменено")
    await callback.answer()

@dp.message(AdminActions.waiting_for_give_sub_user_id)
async def process_give_sub(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        
        if not os.path.exists(f'database/{user_id}.json'):
            await message.answer("❌ Пользователь с таким ID не найден")
            return
        
        with open(f'database/{user_id}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        data['subscribe'] = 1
        
        with open(f'database/{user_id}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        try:
            await bot.send_message(user_id, "🎉 Администратор выдал вам подписку!")
        except:
            pass
        
        await message.answer(f"✅ Подписка успешно выдана пользователю {user_id}")
        
    except ValueError:
        await message.answer("❌ Неверный формат ID. Введите числовой ID.")
    
    await state.clear()

@dp.message(AdminActions.waiting_for_take_sub_user_id)
async def process_take_sub(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        
        if not os.path.exists(f'database/{user_id}.json'):
            await message.answer("❌ Пользователь с таким ID не найден")
            return
        
        with open(f'database/{user_id}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        data['subscribe'] = 0
        
        with open(f'database/{user_id}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        try:
            await bot.send_message(user_id, "❌ Администратор изъял вашу подписку!")
        except:
            pass
        
        await message.answer(f"✅ Подписка успешно изъята у пользователя {user_id}")
        
    except ValueError:
        await message.answer("❌ Неверный формат ID. Введите числовой ID.")
    
    await state.clear()

@dp.message(AdminActions.waiting_for_ban_user_id)
async def process_ban(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        
        if not os.path.exists(f'database/{user_id}.json'):
            await message.answer("❌ Пользователь с таким ID не найден")
            return
        
        with open(f'database/{user_id}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        data['original_subscription'] = data.get('subscribe', 0)
        data['subscribe'] = 0
        data['banned'] = True
        data['ban_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(f'database/{user_id}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        try:
            await bot.send_message(user_id, "❌ Вы были забанены администратором и больше не можете использовать бота.")
        except:
            pass
        
        await message.answer(f"✅ Пользователь {user_id} успешно забанен")
        
    except ValueError:
        await message.answer("❌ Неверный формат ID. Введите числовой ID.")
    
    await state.clear()

@dp.message(AdminActions.waiting_for_unban_user_id)
async def process_unban(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        
        if not os.path.exists(f'database/{user_id}.json'):
            await message.answer("❌ Пользователь с таким ID не найден")
            return
        
        with open(f'database/{user_id}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        data['subscribe'] = data.get('original_subscription', 0)
        data['banned'] = False
        data['ban_date'] = None
        
        with open(f'database/{user_id}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        try:
            await bot.send_message(user_id, "✅ Вы были разбанены администратором и снова можете использовать бота.")
        except:
            pass
        
        await message.answer(f"✅ Пользователь {user_id} успешно разбанен")
        
    except ValueError:
        await message.answer("❌ Неверный формат ID. Введите числовой ID.")
    
    await state.clear()

@dp.message(Command('jopa'))
async def admin(message: Message):
    if ADMIN_ID == message.from_user.id:
        async def one(state: FSMContext):
            await state.set_state(quest.id)
            await message.answer("Введите ID: ")
            
        @dp.message(quest.id)
        async def one_two(message: Message, state: FSMContext):
            await state.update_data(name=message.text) 
            await state.set_state(quest.code)
            await message.answer('Введите код: ')
            
        @dp.message(quest.code)
        async def two(message: Message, state: FSMContext):
            data = await state.get_data()
            await state.update_data(name=message.text)
            await bot.send_message(text=f"Ваш код доступа: <code>{data['code']}</code>",
                                   chat_id=data['id'])
            await message.answer("Сообщение отправлено")
            await state.clear()           
    else:
        await message.answer(f"Недостаточно прав, id: {message.from_user.id}")
    
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



