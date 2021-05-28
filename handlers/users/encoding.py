from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from states.encode import Encode
from encrypt import solve_encrypt

# @dp.message_handler(Command("test"), state=None)
@dp.message_handler(Text(equals=["Шифровать"]))
async def enter_test(message: types.Message):
    await message.answer("Вы начали процесс шифрования.")
    await message.answer("Сначала отправте ваще сообщение.\n"
                         "Максимальная длина сообщения 1000 символов."
                         )

    # Меняем состояние
    await Encode.Q_message.set()

@dp.message_handler(state=Encode.Q_message)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(answer1=answer)

    await message.answer("Теперь отправте ваш пароль,\n"
                         "по которому будет происходить шифрование")
    # Меняем состояние
    await Encode.next()


@dp.message_handler(state=Encode.Q_password)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    await state.update_data(answer2=answer2)

    await message.answer("И последнее, что осталось\n"
                         "это фото в которое будет зашифровано сообщение.")
    # Меняем состояние
    await Encode.next()

@dp.message_handler(state=Encode.Q_photo, content_types=['photo'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # Достаем переменные
    await message.photo[-1].download(file_name+'.png')
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    print(answer1, answer2)
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")

    # шифрование
    solved = solve_encrypt(file_name+'.png', answer1, answer2)
    if isinstance(solved, str):
        await message.answer(solved)
    else:
        await message.answer_document(document=solved)
        await message.answer("Ваше сообщение было успешно зашифровано!")
    # удалением ненужный файл
    import os
    os.remove(file_name+".png")
    # Завершаем текущие состояние
    await state.finish()

@dp.message_handler(state=Encode.Q_photo, content_types=['document'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # проверка на то, что отправили именно фото
    document = message.document
    tupes = ["image/bmp", 
            "image/jpeg", 
            "image/png", 
            "image/x-citrix-jpeg",
            "image/x-citrix-png",
            "image/x-png",
            "image/x-ms-bmp"
            ]
    if not(document["mime_type"] in tupes):
        #await state.finish()
        #print(document["mime_type"])
        await message.answer("Недопустимый формат файла")
        return None
    # Достаем переменные
    await message.document.download(file_name+".png")
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    print(answer1, answer2)
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")
    # шифрование
    solved = solve_encrypt(file_name+".png", answer1, answer2)
    if isinstance(solved, str):
        await message.answer(solved)
    else:
        await message.answer_document(document=solved)
        await message.answer("Ваше сообщение было успешно зашифровано!")
    # удалением ненужный файл
    import os
    os.remove(file_name+".png")
    # Выходим из текущего состояния
    await state.finish()
