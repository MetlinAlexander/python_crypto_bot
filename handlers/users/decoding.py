from decrypt import solve_decrypt
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from states.decode import Decode
from decrypt import solve_decrypt

@dp.message_handler(Text(equals=["Расшифровать"]))
async def enter_test(message: types.Message):
    await message.answer("Вы начали процесс расшифрования.")
    await message.answer("Сначала отправте пароль, по которому происходило шифрование.")
    # Вариант 1 - с помощью функции сет
    await Decode.Q_password.set()

@dp.message_handler(state=Decode.Q_password)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(answer1=answer)

    await message.answer("Теперь отправте фото, \n"
                         "куда было зашифровано сообщение."
                         )
    await Decode.next()

@dp.message_handler(state=Decode.Q_photo, content_types=['photo'])
async def answer_q3(message: types.Message, state: FSMContext):
    # Даем совет пользователю
    await message.answer("Совет: отправте изображение как файл")

@dp.message_handler(state=Decode.Q_photo, content_types=['document'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # Достаем переменные
        # проверка на то, что отправили именно фото
    document = message.document
    tupes = ["image/png", 
            "image/x-citrix-png",
            "image/x-png"
            ]
    if not(document["mime_type"] in tupes):
        print("stop")
        #await state.finish()
        #print(document["mime_type"])
        await message.answer("Недопустимый формат файла")
        return None
    # Достаем переменные
    await message.document.download(file_name+'.png')
    data = await state.get_data()
    answer1 = data.get("answer1")
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")
    # расшифровка
    solved = solve_decrypt(file_name+'.png', answer1)
    if solved =="Error":
        await message.answer("При расшифровки произошла ошибка.")
    else:
        await message.answer(solved)    
        await message.answer("Ваше сообщение было успешно расшифровано!")
    # Выходим из текущего состояния
    await state.finish()