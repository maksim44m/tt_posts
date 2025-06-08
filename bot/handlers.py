from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (Message, 
                           CallbackQuery, 
                           InlineKeyboardMarkup, 
                           InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import DB
from utils.log import logging


logger = logging.getLogger(__name__)


router = Router()


@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    logger.info(f'Пользователь {message.from_user.id} начал диалог')
    await message.answer(
        'Добро пожаловать! Используйте команду /posts для просмотра всех постов.'
    )


@router.message(Command('posts'))
async def posts_handler(message: Message, db: DB) -> None:
    """Обработчик команды /posts - показывает список постов"""
    logger.info(f'Пользователь {message.from_user.id} запросил список постов')
    async for session in db.get_session():
        posts = await db.get_posts(session)
        
    if not posts:
        await message.answer('Посты не найдены.')
        return
    
    keyboard = await keyboard_builder(posts)
    
    await message.answer(
        'Выберите пост для просмотра:',
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith('post_'))
async def post_details_handler(callback: CallbackQuery, 
                               db: DB) -> None:
    """Обработчик нажатия на кнопку поста"""
    logger.info(f'Пользователь {callback.from_user.id} запросил детальную информацию о посте')
    post_id = int(callback.data.split('_')[1])
    
    async for session in db.get_session():
        post = await db.get_post(session, post_id)
    
    if not post:
        await callback.answer('Пост не найден')
        return
    
    created_at: datetime = post['created_at']
    created_str = created_at.strftime('%d.%m.%Y %H:%M')
    
    back_button = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text='← Назад к списку постов',
            callback_data='back_to_posts'
        )
    ]])
    
    await callback.message.edit_text(
        f'<b>{post["title"]}</b>\n\n'
        f'{post["content"]}\n\n'
        f'<i>Дата создания: {created_str}</i>',
        parse_mode='HTML',
        reply_markup=back_button
    )


@router.callback_query(F.data == 'back_to_posts')
async def back_to_posts_handler(callback: CallbackQuery,
                                db: DB) -> None:
    """Обработчик кнопки "Назад к списку постов" """
    logger.info(f'Пользователь {callback.from_user.id} вернулся к списку постов')
    async for session in db.get_session():
        posts = await db.get_posts(session)
    
    if not posts:
        await callback.message.edit_text('Посты не найдены.')
        return
    
    keyboard = await keyboard_builder(posts)
    
    await callback.message.edit_text(
        'Выберите пост для просмотра:',
        reply_markup=keyboard
    )

async def keyboard_builder(posts: list[dict]) -> InlineKeyboardMarkup:
    """Создание клавиатуры с кнопками постов"""
    builder = InlineKeyboardBuilder()
    for post in posts:
        builder.add(InlineKeyboardButton(
            text=post['title'],
            callback_data=f'post_{post["id"]}'
        ))
    builder.adjust(1)
    return builder.as_markup()