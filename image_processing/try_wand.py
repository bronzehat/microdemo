# -*- coding: utf-8 -*-
from wand.image import Image
from wand.font import Font
from wand.drawing import Drawing
from wand.color import Color
from utils.util import walk
import os
from textwrap import wrap


RESOURCE = "C:\\Users\\a.sayapova\\PycharmProjects\\Recovered\\test_data_ocr\\languages"
DEGREE = 10
ROI_SIDE = 400
FORMATS = [
    "bmp",
    "jpeg",
    "jpg",
    "jpe",
    "tif",
    "tiff",
    "gif"
]
FONTS_PATH = "C:\\Windows\\Fonts"
FONTS = {"Times New Roman": "times_new_roman",
         "Arial": "arial",
         "Calibri": "calibri",
         "Comic Sans MS": "comic_sans_ms"}
PANGRAMS = {
    "ru": [
        "Аэрофотосъёмка ландшафта уже выявила земли богачей и процветающих крестьян.",
        "— Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.",
        "Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф."],
    "en": [
        "Brick quiz whangs jumpy veldt fox!",
        "Quick wafting zephyrs vex bold Jim.",
        "Sphinx of black quartz judge my vow!"]
}
PANGRAMS_WITH_SPEC = {
    "ru": [
    "Аэрофотосъёмка ландшафта уже выявила земли богачей и процветающих крестьян.",
    "— Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.",
    "Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф."],
    "en": [
    "Brick quiz whangs jumpy veldt fox!",
    "Quick wafting zephyrs vex bold Jim.",
    "Sphinx of black quartz judge my vow!"]
}


def rotate():
    for file in list(walk([RESOURCE])):
        filename = os.path.basename(file)
        TARGET_PATH = os.path.join(PATH, filename)
        if not os.path.isdir(TARGET_PATH):
            os.makedirs(TARGET_PATH)
        with Image(filename=file) as img:
            print(filename, img.size)
            r = 1
            while r <= (int(360/DEGREE)):
                with img.clone() as i:
                    # i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
                    i.rotate(DEGREE * r)
                    i.save(filename=os.path.join(PATH, filename, "{}_{}".format(DEGREE*r, filename)))
                r += 1


def word_wrap(image, ctx, text, roi_width, roi_height):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    iteration_attempts = 100

    def eval_metrics(txt):
        """Quick helper function to calculate width/height of text."""
        metrics = ctx.get_font_metrics(image, txt, True)
        return (metrics.text_width, metrics.text_height)

    while ctx.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(mutable_message)
        if height > roi_height:
            ctx.font_size -= 0.75  # Reduce pointsize
            mutable_message = text  # Restore original text
        elif width > roi_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                mutable_message = '\n'.join(wrap(mutable_message, columns))
                wrapped_width, _ = eval_metrics(mutable_message)
                if wrapped_width <= roi_width:
                    break
            if columns < 1:
                ctx.font_size -= 0.75  # Reduce pointsize
                mutable_message = text  # Restore original text
        else:
            break
    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)
    return mutable_message


def create_image_with_text(text, output,
                           font_size=24, font_family="Times New Roman", font_style="normal",
                           gravity="center", im_format="png"):
    with Image(width=ROI_SIDE, height=ROI_SIDE, background=Color('white')) as img:
        with Drawing() as context:
            context.push()
            context.fill_color = Color('black')
            context.pop()
            context.font_style = font_style
            context.font_family = font_family
            context.font_size = font_size
            context.gravity = gravity
            text_indent = ROI_SIDE-5
            mutable_message = word_wrap(img,
                                        context,
                                        text,
                                        text_indent,
                                        text_indent)
            context.text(x=5,
                         y=5,
                         body=mutable_message)
            context.draw(img)
            img.format = im_format
            img.save(filename=os.path.join(PATH, "{}.{}".format(output, im_format)))


def create_pangrams():
    for lang in PANGRAMS:
        concat = "\n".join([pangram for pangram in PANGRAMS[lang]])
        if not os.path.isdir(os.path.join(PATH, lang)):
            os.makedirs(os.path.join(PATH, lang))
        create_image_with_text(text=concat, output=os.path.join(lang, "all_together.png"))
        for pangram in PANGRAMS[lang]:
            output_img = "{}_pangram_{}.png".format(lang, PANGRAMS[lang].index(pangram) + 1)
            create_image_with_text(text=pangram, output=os.path.join(lang, output_img))


def convert_image_in_formats(original_image):
    with Image(filename=original_image) as img:
        for img_format in FORMATS:
            with img.convert(img_format) as i:
                i.save(filename=original_image.replace("png", img_format))


create_image_with_text(text=r"Съешь ещё этих мягких французских булок, да выпей же чаю !#$%&'()*+,-./;<=>?@\]^_`|{}~ ",
                       output="alphabet_ru_with_spec.png")
ru_lit = "Пьер Обье жил со своими родителями недалеко от сквера Клюни. Отец его был судьей; брат — шестью годами старше — с первых же дней войны ушел добровольцем. Истинно французская добропорядочная буржуазная семья, почтенные, добросердечные, прекраснодушные люди, ни разу в жизни не дерзнувшие высказать собственное суждение и, по всей вероятности, даже не подозревавшие о такой возможности. Неподкупно честный, проникнутый сознанием высокого значения обязанностей председателя суда, г-н Обье счел бы себя смертельно оскорбленным, если бы кто-нибудь заподозрил, что его приговоры могут быть продиктованы иными соображениями, чем те, которые внушают ему требования справедливости и голос совести. Однако его совесть никогда не высказывалась против правительства, даже шепотом. Она была прирожденным чиновником и всецело подчинялась официальным государственным установлениям, которые, даже меняясь, остаются непогрешимыми. Власти предержащие в глазах г-на Обье были чем-то святым и непреложным. Он искренне восхищался как бы отлитыми из бронзы душами великих судей прошлого, независимых и непреклонных, и, быть может, втайне считал себя их преемником. Это был совсем маленький Мишель де л'Опиталь, на которого столетие служения Республике наложило свой отпечаток. А г-жа Обье была в такой же мере доброй христианкой, в какой ее муж добрым республиканцем. И, подобно тому как ее прямодушный, неподкупный супруг соглашался быть послушным орудием правительства против всякой неузаконенной свободы, она, в простоте душевной, присоединяла свои молитвы к человекоубийственным молениям, возносимым во имя войны во всех странах Европы католическими аббатами и протестантскими пасторами, раввинами и священниками, газетами и всеми благомыслящими людьми того времени. Оба они — отец и мать — обожали своих детей, как истые французы, только к ним и питали глубокое, настоящее чувство, готовы были всем пожертвовать ради них, но, чтобы не отставать от других, не задумываясь, приносили их в жертву. Кому? Неведомому божеству. Во все времена Авраам отдавал Исаака на заклание. И это прославленное в веках безумие не перестало служить примером несчастному человечеству."
create_image_with_text(text=ru_lit,
                       output="large_ru_generated_with_indent.png")

for image in list(walk([PATH])):
    convert_image_in_formats(image)

for lang in PANGRAMS:
    size = 18
    while size <= 30:
        create_image_with_text(text=PANGRAMS[lang][0],
                               output="C:\\Users\\a.sayapova\\PycharmProjects\\Recovered\\test_data_ocr\\fontsizes\\{}_{}.png".format(lang, size),
                               font_size=size)
        size += 1

for font in FONTS:
    for lang in PANGRAMS:
        create_image_with_text(text=PANGRAMS[lang][0],
                               output="C:\\Users\\a.sayapova\\PycharmProjects\\Recovered\\test_data_ocr\\fonts\\{}_{}.png".format(lang, FONTS[font]),
                               font_family=font)

for text in ["first", "second", "third", "fourth"]:
    create_image_with_text(text=text, output=text)
