from aiogram import types,F, Router,flags
from aiogram.types import Message,CallbackQuery,FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import geminiAI
from states import Gen
import kb
import text
import os
router = Router()

@router.message(Command("start"))
async def start_hanlder(msg:Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name),reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg:Message):
    await msg.answer(text.menu,reply_markup=kb.menu)

@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck:CallbackQuery,state:FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit,reply_markup=kb.exit_kb)

@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg:Message,state:FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    res = await geminiAI.get_gemini_response(prompt)
    if not res:
        return await mesg.edit_text(text.gen_error,reply_markup=kb.iexit_kb)
    await mesg.edit_text(res + text.text_watermark,disable_web_page_preview=True)

    
@router.callback_query(F.data == "generate_presentation")
async def input_text_presentation(call:CallbackQuery,state:FSMContext):
    await state.set_state(Gen.present_prompt)
    await call.message.edit_text(text.present_text)
    await call.message.answer(text.gen_exit,reply_markup=kb.exit_kb)


@router.message(Gen.present_prompt)
@flags.chat_action("typing")
async def generate_presentation(msg:Message,state:FSMContext):
    prompt = msg.text
    await state.update_data(prompt=prompt)
    await msg.answer(text.slides,reply_markup=kb.slides)
    
@router.callback_query(F.data.startswith("slides"))
async def get_slides(call:CallbackQuery,state:FSMContext):
    slide = call.data
    number_of_slides = slide.split(" ")[1]
    await state.update_data(slide=number_of_slides)
    await call.message.edit_text(text.text_wait.format(slide=number_of_slides),reply_markup=kb.text)

@router.callback_query(F.data.startswith("text"))
async def get_type_text(call:CallbackQuery,state:FSMContext):
    all_types = call.data
    type_of_text = all_types.split(" ")[1]
    data = await state.get_data()
    prompt = data.get("prompt")
    slide = data.get('slide')
    if not prompt:
        return await call.message.answer(text.gen_error)
    await call.message.answer(text.gen_wait)
    await geminiAI.create_presentation(prompt,slide,type_of_text)
    file = FSInputFile('presentation.pptx')
    if not file:
        return await call.message.answer(text.gen_error)
    await call.message.answer_document(file,caption="Вот ваша презентация")
    os.remove("presentation.pptx")