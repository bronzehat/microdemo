import cv2
from skimage.metrics import structural_similarity
import os
from PIL import Image


os.environ["OPENCV_IO_ENABLE_JASPER"] = "1"


ORIG = OUT = "2yn_left_90.bmp"
EXTRACTED = "IMAGE_3.jpg"
exception_ext = True if ORIG.split(".")[-1] in ["gif", "tga", "pcx"] else False


# Получаем размеры изображения
if not exception_ext:
    original = cv2.imread(ORIG)
    orig_height, orig_width = original.shape[:-1]
else:
    original = Image.open(ORIG)
    orig_width, orig_height = original.size

extracted = cv2.imread(EXTRACTED)
height, width = extracted.shape[:-1]

# Приводим размер изображения к размерам извлеченного,
# сохраняя измененную копию отдельным файлом (можно будет приложить в случае фейла)
if orig_height != height or orig_width != width:
    OUT = "".join([ORIG.split(".")[0],
                   "_resized.jpg"])
    if not exception_ext:
        resized = cv2.resize(original, (width, height))
        cv2.imwrite(OUT, resized)
    else:
        resized = original.resize((width, height))
        if resized.mode != "RGB":
            resized = resized.convert("RGB")
        resized.save(OUT)

# Конвертируем изображения в серые тона - выше точность сравнения
grayA = cv2.cvtColor(cv2.imread(OUT), cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(cv2.imread(EXTRACTED), cv2.COLOR_BGR2GRAY)

# Вычисляем индекс cходства изображений по структуре (SSIM),
# убеждаясь, что возвращены и сами различия (diff)
(score, diff) = structural_similarity(grayA, grayB, full=True)

# Можно будет для excepted_ext сделать условие ассерта чуть поменьше,
# там коэффициент снижается (0.88844 против обычного 0.93137)
print("SSIM: {}".format(score))
