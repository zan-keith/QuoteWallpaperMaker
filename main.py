from tkinter import *
from tkinter.ttk import *
import numpy as np
import textwrap
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
import os.path
from tkinter import filedialog as fd, colorchooser

root = Tk()
root.geometry('800x600')

text_loc_Y = DoubleVar()
text_loc_X = DoubleVar()
TXTwrap = IntVar()
quote_text = StringVar()
author = StringVar()
image_file_name = StringVar()
FONTSIZE = IntVar()
AUTHFONTSIZE = IntVar()

LinePadding = IntVar()

(QuoteBgColor, QuoteFgColor, QuoteBgColorO, QuotePad) = (StringVar(),
        StringVar(), IntVar(), IntVar())

(AuthorFgColor, AuthorBgColor, AuthorBgColorO, AuthorPad) = \
    (StringVar(), StringVar(), IntVar(), IntVar())

image_path = 'Images\\SampleImage.jpg'
font_path = 'Fonts\\fira.ttf'
OGimage = Image.open(image_path)
image = OGimage.copy()

quote_text.set('Sample Text')
TXTwrap.set(15)
FONTSIZE.set(4)
AUTHFONTSIZE.set(3)
f_Realimage = 0
text_loc_X.set(50)
text_loc_Y.set(50)

QuoteFgColor.set('#ffffff')
QuoteBgColor.set('#000000')
QuoteBgColorO.set(100)
QuotePad.set(1)

AuthorFgColor.set('#ffffff')
AuthorBgColor.set('#000000')
AuthorBgColorO.set(200)
AuthorPad.set(0)

def Update(a,b,c,save=False,):
    global image, IMAGE

    LinePad = LinePadding.get()
    if save == False:
        IMAGE = f_Realimage.copy()
    else:
        IMAGE = Image.open(image_path)

    Qpad = int(QuotePad.get() / 100 * IMAGE.size[1])
    Apad = int(AuthorPad.get() / 100 * IMAGE.size[1])

    I1 = ImageDraw.Draw(IMAGE)

    myFont = ImageFont.truetype(font_path, int(FONTSIZE.get() / 100
                                * IMAGE.size[0]))
    AuthFont = ImageFont.truetype(font_path, int(AUTHFONTSIZE.get()
                                  / 100 * IMAGE.size[0]))

    text_location_x = int(text_loc_X.get() / 100 * IMAGE.size[0])
    text_location_y = int(text_loc_Y.get() / 100 * IMAGE.size[1])

    if TXTwrap.get() < 1:
        TXTwrap.set(1)

    Quote_Bg_Color = ImageColor.getcolor(QuoteBgColor.get(), 'RGB')
    Quote_Bg_Color = Quote_Bg_Color + (QuoteBgColorO.get(), )

    Author_Bg_Color = ImageColor.getcolor(AuthorBgColor.get(), 'RGB')
    Author_Bg_Color = Author_Bg_Color + (AuthorBgColorO.get(), )

    sizex = myFont.getsize(str(quote_text.get()))
    lines = textwrap.wrap(str(quote_text.get()), width=TXTwrap.get())
    y_text = text_location_y

    for line in lines:

        size = myFont.getsize(line)

        bgBox = Image.new(mode='RGBA', size=(size[0], sizex[1]),
                          color=Quote_Bg_Color)
        IMAGE.paste(bgBox, (int(text_location_x - size[0] / 2),
                    int(y_text - sizex[1] / 2)), bgBox)
        draw = ImageDraw.Draw(IMAGE)
        draw.text((text_location_x, y_text), line, fill=str(QuoteFgColor.get()),
                  font=myFont, anchor='mm')

        y_text += sizex[1] + Qpad

    y_text += Apad
    size = AuthFont.getsize(str(author.get()))
    bgBox = Image.new(mode='RGBA', size=(size[0], size[1]),
                      color=Author_Bg_Color)
    IMAGE.paste(bgBox, (int(text_location_x - size[0] / 2), int(y_text
                - size[1] / 2)), bgBox)
    draw = ImageDraw.Draw(IMAGE)
    draw.text((text_location_x, y_text), author.get(), fill=str(AuthorFgColor.get()),
              font=AuthFont, anchor='mm')

    image = ImageTk.PhotoImage(image=IMAGE)
    canvas.config(width=IMAGE.size[0], height=IMAGE.size[1])
    canvas.itemconfig(imageContainer, image=image)


def open_image_file():
    global image_path, f_Realimage, f_Realwidth, f_Realheight

    filetypes = (('JPEG files', '*.jpg'), ('PNG files', '*.png'),
                 ('All files', '*.*'))

    f = fd.askopenfile(filetypes=filetypes)
    if f is None:
        return


    print(os.path.abspath(f.name))
    image_path = os.path.abspath(f.name)

    (f_Realimage, f_Realwidth, f_Realheight) = \
        Fix_Image(Image.open(image_path))
    Update(1, 1, 1)


def open_font_file():

    global font_path
    filetypes = (('ttf files', '*.ttf'), ('All files', '*.*'))


    f = fd.askopenfile(filetypes=filetypes)
    if f is None:
        return

    print(os.path.abspath(f.name))
    font_path = os.path.abspath(f.name)
    Update(1, 1, 1)


def Fix_Image(image):

    fixed_height = 250
    height_percent = fixed_height / float(image.size[1])
    width_size = int(float(image.size[0]) * float(height_percent))
    image = image.resize((width_size, fixed_height), Image.NEAREST)
    image.convert('RGBA')
    return (image, width_size, fixed_height)


style = Style()

style.configure('Section.TLabelframe', borderwidth=10)
style.configure('My.TFrame', background='red')
style.configure('My.TLabel', foreground='Gray', font=('Helvetica', 15,
                'bold', 'underline'))
style.configure('btn1.TButton', font=('Helvetica', 12),
                foreground='black', background='white')
style.configure('btnReset.TButton', font=('Helvetica', 12),
                foreground='black', background='red', padding=0)
style.configure('btnSave.TButton', font=('Helvetica', 12),
                foreground='black', background='blue', padding=0)

w = Label(root, text='Quote Wallpaper Maker', style='My.TLabel',
          font='50')
w.pack()

(f_Realimage, f_Realwidth, f_Realheight) = Fix_Image(OGimage)

frame = Frame(root, style='My.TFrame')
frame.pack()

bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10)

bottomframex = Frame(root)
bottomframex.pack(side=BOTTOM, expand=True, fill=BOTH)

leftframe = Frame(root)
leftframe.pack(side=LEFT, expand=True, fill=BOTH, padx=10)

leftframex = Frame(root)
leftframex.pack(side=LEFT, expand=True, fill=BOTH)

rightframe = Frame(root)
rightframe.pack(side=RIGHT, expand=True, fill=BOTH)

Label(leftframe, text='Quote: ').grid(row=0, column=0, sticky='w')
e1 = Entry(leftframe, textvariable=quote_text, width=30).grid(row=0,
        column=1, pady=5, columnspan=2)

Label(leftframe, text='Quoted By: ').grid(row=1, column=0, sticky='w')
e2 = Entry(leftframe, textvariable=author).grid(row=1, column=1,
        pady=5, columnspan=2)

Label(leftframe, text='Quote Font Size :').grid(row=2, column=0,
        pady=5, sticky='w')
Spinbox(leftframe, from_=1, to=50, width=5,
        textvariable=FONTSIZE).grid(row=2, column=1, pady=5)

Label(leftframe, text='Author Font Size :').grid(row=3, column=0,
        pady=5, sticky='w')
Spinbox(leftframe, from_=1, to=50, width=5,
        textvariable=AUTHFONTSIZE).grid(row=3, column=1, pady=5)

Label(leftframe, text='Word Wrap :').grid(row=4, column=0, sticky='w')
Wrap = Spinbox(leftframe, from_=5, to=50, width=30,
               textvariable=TXTwrap).grid(pady=5, row=4, column=1,
        columnspan=2)


def Btn1_Onclick():
    text_loc_X.set(50)
    text_loc_Y.set(50)


bloadFont_button = Button(leftframe, text='Load Font',
                          style='btn1.TButton',
                          command=open_font_file).grid(row=5, column=0)
bloadImg_button = Button(leftframe, text='Load Image',
                         style='btn1.TButton',
                         command=open_image_file).grid(row=5, column=1)

b2_button = Button(leftframe, text='Reset', style='btnReset.TButton',
                   command=Btn1_Onclick).grid(row=5, column=2)


# ----------------------------------------------

def save():

    filetypes = (('PNG files', '*.png'), ('JPG files', '*.jpg*'))

    f = fd.asksaveasfile(mode='w', defaultextension='*.png',
                         title='Choose Destination',
                         filetypes=filetypes)
    if f is None:
        return
    Update(1, 1, 1, True)
    IMAGE.save(os.path.abspath(f.name))
    Update(1, 1, 1, False)


def btnclickupdate():
    Update(1, 1, 1)


save_button = Button(bottomframe, text='Save Image As',
                     style='btnSave.TButton', command=save).grid(pady=3)

QuoteSettingsSection = LabelFrame(bottomframex,
                                  text='Quote Text Advanced Settings',
                                  style='Section.TLabelframe')
QuoteSettingsSection.pack(expand=True, fill=BOTH, padx=10)

AuthorSettingsSection = LabelFrame(bottomframex,
                                   text='Author Text Advanced Settings'
                                   , style='Section.TLabelframe')
AuthorSettingsSection.pack(expand=True, fill=BOTH, padx=10)

# --------------------------------------------------------------------

t1 = Label(QuoteSettingsSection, text='ForeGround Color : '
           ).grid(row=0, column=0)
t2 = Label(QuoteSettingsSection, text='Background Color : '
           ).grid(row=1, column=0)
tx = Label(QuoteSettingsSection, text='Text Padding : ').grid(row=2,
        column=0)

box1 = Entry(QuoteSettingsSection, textvariable=QuoteFgColor,
             width=30).grid(row=0, column=1)
box2 = Entry(QuoteSettingsSection, textvariable=QuoteBgColor,
             width=30).grid(row=1, column=1)
box3 = Spinbox(QuoteSettingsSection, from_=0, to=255, width=5,
               textvariable=QuoteBgColorO).grid(row=1, column=2)
boxx = Spinbox(QuoteSettingsSection, from_=0, to=20, width=10,
               textvariable=QuotePad).grid(row=2, column=1)

button1 = Button(QuoteSettingsSection, text='Apply Changes',
                 command=btnclickupdate).grid(row=1, column=3, padx=5)

# --------------------------------------------------------------------

t3 = Label(AuthorSettingsSection, text='ForeGround Color : '
           ).grid(row=0, column=0)
t4 = Label(AuthorSettingsSection, text='Background Color : '
           ).grid(row=1, column=0)
t5 = Label(AuthorSettingsSection, text='Text Padding : ').grid(row=2,
        column=0)

box4 = Entry(AuthorSettingsSection, textvariable=AuthorFgColor,
             width=30).grid(row=0, column=1)
box5 = Entry(AuthorSettingsSection, textvariable=AuthorBgColor,
             width=30).grid(row=1, column=1)
box6 = Spinbox(AuthorSettingsSection, from_=0, to=255, width=5,
               textvariable=AuthorBgColorO).grid(row=1, column=2)

box7 = Spinbox(AuthorSettingsSection, from_=0, to=20, width=10,
               textvariable=AuthorPad).grid(row=2, column=1)
button2 = Button(AuthorSettingsSection, text='Apply Changes',
                 command=btnclickupdate).grid(row=1, column=3, padx=5)

x_slider = Scale(rightframe, from_=0, to=100, orient='horizontal',
                 variable=text_loc_X).pack(expand=True, fill=BOTH)

y_slider = Scale(
    leftframex,
    from_=0,
    to=100,
    length=250,
    orient='vertical',
    variable=text_loc_Y,
    ).pack(expand=True, fill=BOTH, pady=(29, 0))

img = ImageTk.PhotoImage(image=f_Realimage)
canvas = Canvas(rightframe, width=f_Realwidth, height=f_Realheight)

imageContainer = canvas.create_image(0, 0, image=img, anchor='nw')
canvas.pack()

text_loc_Y.trace('w', Update)
text_loc_X.trace('w', Update)
quote_text.trace('w', Update)
TXTwrap.trace('w', Update)
FONTSIZE.trace('w', Update)
author.trace('w', Update)
Update(1, 1, 1)
root.mainloop()
