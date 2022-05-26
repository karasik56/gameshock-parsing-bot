from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""inline меню"""
inline_btn_xbox360 = InlineKeyboardButton('Xbox 360', callback_data='xbox360')
inline_btn_ps3 = InlineKeyboardButton('PS 3', callback_data='ps3')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_xbox360, inline_btn_ps3)