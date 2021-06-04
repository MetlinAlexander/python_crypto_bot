# файл с функциями для шифровки
def to_encode(name, user_text, password):
    def norm_pass(ps): # функция переводит пароль в нормальный вид
        norm = 0
        for i in ps:
            norm += ord(i)
        return int(norm)

    def make_spesial_line(symbol): # функция для создания удобного кортежа, чтобы в дальнейшем было легче работать
        line = str(to_encode(symbol))
        new = (12 - len(line))*"0" + line
        a = new[:4:]
        b = new[4:8:]
        c = new[8::]
        return (a, b, c)
    def to_encode(symbol): # функция для перевода символа в двоичный код
        symbol = ord(symbol)
        symbol = bin(symbol)
        b1 = symbol[2::]
        return b1

    def generation(size, colov_simvols, seed): # функция для распределиния символов по изображению 
        import random
        random.seed(seed)
        generatoin = list()
        while len(generatoin) < colov_simvols:
            a = random.randint(1,size)
            if a in generatoin:
                continue
            generatoin.append(a)
        return generatoin

    def make_normal_numbers(binary): #функция для перевода чисел из двоичной системы в десятичную
        again = binary
        for j in range(len(again)):
            if again[j] != "0":
                break
            binary = again[j::]
        original = int(str(binary), base=2)
        return original

    def make_new_rgb(symbol, red, green, blue): # функция для шифрования символа в пиксель
        # создание нвого красного цвета пикселя
        new_r = bin(red)
        rb = new_r[2::]
        rb = (12 - len(rb))*"0" + rb
        rb = rb[:8:] + symbol[0]
        rb = make_normal_numbers(rb)
        # создание нового зеленого цвета пикселя
        new_g = bin(green)
        gb = new_g[2::]
        gb = (12 - len(gb))*"0" + gb
        gb = gb[:8:] + symbol[1]
        gb = make_normal_numbers(gb)
        # создание нвого синего цвета пикселя
        new_b = bin(blue)
        bb = new_b[2::]
        bb = (12 - len(bb))*"0" + bb
        bb = bb[:8:] + symbol[2]
        bb = make_normal_numbers(bb)
        return rb, gb, bb
    if len(user_text)>1000:
        user_text = user_text[:1000]
    user_text += "`"
    from PIL import Image, ImageDraw # импортируем библеотеку для работы с изображениями
    image = Image.open(name)  # Открываем изображение
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту

    max_len = width*height # узнаем максимульную длину которую можно зашифровать внутрь картинки
    if len(user_text)> max_len: # проверяем подходит ли по длине данное сообщение
        user_text = user_text[:max_len:]
        print(len(user_text), "ok")

    password = norm_pass(password) # переводим пароль к числовому занчению
    text_tuple = tuple(make_spesial_line(i) for i in user_text) # формируем из введеного текста кортеж

    rand_generate = generation(max_len, len(user_text), password) # формируем list() с рандомным распределением, чтобы зашифровать тест случайны образом
    rgb_im = image.convert('RGB') # конвертиреум изображение для считывания пикселей
    draw = ImageDraw.Draw(rgb_im)  # Создаем инструмент для рисования
    # ------- начало шифрования ----------
    for i in range(len(user_text)):
        x = rand_generate[i] % width
        y = rand_generate[i] // width
        r, g, b = rgb_im.getpixel((x, y)) #узнаём значение пикселя
        new_rgb = make_new_rgb(text_tuple[i], red=r, green=g, blue=b) # шифруем в пиксель часть инфы
        draw.point((x, y), new_rgb) # перекрашиваем пиксель в новый цвет
    
    # удалением ненужный файл
    import os
    os.remove(name)
    # сохраняем результат
    rgb_im.save(name, "png")
    # Возвращаем результат
    return open(name, "rb")
def solve_encrypt(put, toxt, pessword):
    try:
        return to_encode(put, toxt, pessword)
    except ValueError as err:
        return f"Error {err}"