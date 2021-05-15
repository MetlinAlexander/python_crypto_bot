from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from states.encode import Encode
from encrypt import solve_encrypt

# @dp.message_handler(Command("test"), state=None)
@dp.message_handler(Text(equals=["Шифровать"]))
async def enter_test(message: types.Message):
    await message.answer("Вы начали процесс шифрования.\n"
                         "Сначала отправте ваще сообщение. \n"
                         "Максимальная длина сообщения 1000 символов."
                         )

    # Вариант 1 - с помощью функции сет
    await Encode.Q_message.set()

@dp.message_handler(state=Encode.Q_message)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(answer1=answer)

    await message.answer("Теперь отправте ваш пароль, \n\n"
                         "по которому будет происходить шифрование")

    await Encode.next()


@dp.message_handler(state=Encode.Q_password)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    await state.update_data(answer2=answer2)

    await message.answer("И последнее, что осталось \n\n"
                         "это фото в которое будет зашифровано сообщение.")

    await Encode.next()

@dp.message_handler(state=Encode.Q_photo, content_types=['photo'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # Достаем переменные
    await message.photo[-1].download(file_name+'.bmp')
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    print(answer1, answer2)
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")

    # шифрование
    solved = solve_encrypt(file_name+'.bmp', answer1, answer2)
    if isinstance(solved, str):
        await message.answer(solved)
    else:
        await message.answer_document(document=solved)
        await message.answer("Ваше сообщение было успешно зашифровано!")
    # удалением ненужный файл
    import os
    os.remove("total.bmp")
    # Вариант 1
    await state.finish()

@dp.message_handler(state=Encode.Q_photo, content_types=['document'])
async def answer_q3(message: types.Message, state: FSMContext):
    # генерация имени файла
    import random
    import string
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    # Достаем переменные
    await message.document.download(file_name+".bmp")
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    print(answer1, answer2)
    await message.answer("Подождите.\n"
                        "Ваше фото находиться в обработке.")

    # шифрование
    solved = solve_encrypt(file_name+".bmp", answer1, answer2)
    if isinstance(solved, str):
        await message.answer(solved)
    else:
        await message.answer_document(document=solved)
        await message.answer("Ваше сообщение было успешно зашифровано!")
    # удалением ненужный файл
    import os
    os.remove("total.bmp")
    # Вариант 1
    await state.finish()
