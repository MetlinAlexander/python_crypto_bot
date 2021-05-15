def to_decode(name, password):
    def norm_pass(ps): # функция переводит пароль в нормальный вид
        norm = 0
        for i in ps:
            norm += ord(i)
        return int(norm)
    def transta_to_symbol(binary): # достаем из пикселя символ
        again = ""
        for i in binary:
            again += i
        binary = again[::]
        for j in range(len(again)):
            if again[j] != "0":
                break
            binary = again[j::]
        original = int(str(binary), base=2)
        return chr(original)
    def take_info(red, green, blue): # функция чтобы вытащить текст из пикселя
        # сканируем инфу из красного цвета пикселя
        new_r = bin(red)
        rb = new_r[2::]
        rb = (12 - len(rb))*"0" + rb
        rb = rb[8::]
        # сканируем инфу из зеленого цвета пикселя
        new_g = bin(green)
        gb = new_g[2::]
        gb = (12 - len(gb))*"0" + gb
        gb = gb[8::]
        # сканируем инфу из синего цвета пикселя
        new_b = bin(blue)
        bb = new_b[2::]
        bb = (12 - len(bb))*"0" + bb
        bb = bb[8::]
        return transta_to_symbol((rb, gb, bb))

    from PIL import Image, ImageDraw # импортируем библеотеку для работы с изображениями
    image = Image.open(name)  # Открываем изображение
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту

    password = norm_pass(password) # переводим пароль к числовому занчению
    max_len = width*height  
    rgb_im = image.convert('RGB') # конвертиреум изображение для считывания пикселей
    draw = ImageDraw.Draw(rgb_im)  # Создаем инструмент для рисования
    message = ""# переменная для хранения сообщения
    count=0
    # ------- начало расшифровки ----------
    # воссодзание случайной последовательности
    import random
    random.seed(password)
    generatoin = list()
    while True:
        while True:
            rand_gen = random.randint(1, max_len)
            if rand_gen in generatoin:
                continue
            generatoin.append(rand_gen)
            break
        x = rand_gen % width
        y = rand_gen // width
        r, g, b = rgb_im.getpixel((x, y)) #узнаём значение пикселя
        symbol = take_info(r, g, b) # вытаскиваем пиксель
        if symbol == "`" or count>=max_len or count>=1000:
            break
        message += symbol
        count +=1
    # удалением ненужный файл
    import os
    os.remove(name)
    return message

def solve_decrypt(put, pessword):
    try:
        return to_decode(put, pessword)
    except:
        return "Error"