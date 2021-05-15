from decrypt import solve_decrypt
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from states.decode import Decode
from decrypt import solve_decrypt

@dp.message_handler(Text(equals=["Расшифровать"]))
async def enter_test(message: types.Message):
    await message.answer("Вы начали процесс расшифрования.\n"
                         "Сначала отправте пароль по которому происходило шифрование."
                         )

    # Вариант 1 - с помощью функции сет
    await Decode.Q_password.set()

@dp.message_handler(state=Decode.Q_password)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(answer1=answer)

    await message.answer("Теперь отправте фото, \n"
                         "куда было зашифровано сообщение.\n"
                         "Совет: отправляйте только исходный файл фото,\n" 
                         "т.к. в противном случае сообщение не будет расшифровано.\n"
                         "Т.е. лучше отправить фото как документ"
                         )
    await Decode.next()

@dp.message_handler(state=Decode.Q_photo, content_types=['photo'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # Достаем переменные
    await message.photo[-1].download(file_name+'.bmp')
    data = await state.get_data()
    answer1 = data.get("answer1")
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")

    # расшифровака
    solved = solve_decrypt(file_name+'.bmp', answer1)
    if solved =="Error":
        await message.answer("При расшифровки произошла ошибка.")
    else:
        await message.answer(solved)    
        await message.answer("Ваше сообщение было успешно расшифровано!")
    # Вариант 1
    await state.finish()

@dp.message_handler(state=Decode.Q_photo, content_types=['document'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # Достаем переменные
    document = message.document
    await message.document.download(file_name+'.bmp')
    data = await state.get_data()
    answer1 = data.get("answer1")
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")

    # расшифровка
    solved = solve_decrypt(file_name+'.bmp', answer1)
    if solved =="Error":
        await message.answer("При расшифровки произошла ошибка.")
    else:
        await message.answer(solved)    
        await message.answer("Ваше сообщение было успешно расшифровано!")
    
    # Вариант 1
    await state.finish()