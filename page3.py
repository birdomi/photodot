from tkinter import *
import cv2 as cv
import sys
import os
import threading
import smtplib
import numpy as np
from email.mime.text import MIMEText
from email.message import EmailMessage
from PIL import Image, ImageTk, ImageOps
from style_transfer.learn import StyleTransfer

import shutil

import time

_list = []

def reset_first():
    global _list
    _list=[]
    if os.path.exists('./file'):
        shutil.rmtree('./file', ignore_errors=True)
    os.mkdir('./file')


def reset():
    global _list
    _list=[]
    lbl_p3['text'] = str(_list)
    if os.path.exists('./file'):
        shutil.rmtree('./file', ignore_errors=True)
    os.mkdir('./file')

    convert_img = Image.open('변환.png')
    convert_img = convert_img.resize(size=[int(width/6), int(height/6)])
    imgtk = ImageTk.PhotoImage(image=convert_img, size = [width/8, height/8])
    img1.imgtk = imgtk
    img1.configure(image=imgtk)
    img2.imgtk = imgtk
    img2.configure(image=imgtk)
    img3.imgtk = imgtk
    img3.configure(image=imgtk)
    img4.imgtk = imgtk
    img4.configure(image=imgtk)

    btnToFrame4['state']=DISABLED
    btnToFrame6['state']=DISABLED
    resume()
    p6_ety.delete(0, 'end')
    p6_ety.insert(0, 'example@example.com')

def openFrame(frame):
    frame.tkraise()
    
reset_first()
window= Tk()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d"%(width, height))
window.attributes('-fullscreen', True)  

#### PAGE1
frame1=Frame(window, width = width, height = height)
img = Image.open('page1_main.png')
img = img.resize([width, height])
p1_img = ImageTk.PhotoImage(img)

lbl = Label(frame1, image=p1_img)
lbl.place(x=0,y=0)
btnToFrame2 = Button(frame1, text="사진 찍으러 고고!",command=lambda:[openFrame(frame2)], relief=GROOVE, font=("HY엽서M",20))


### PAGE 2
frame2=Frame(window, width = width, height = height)
img = Image.open('page2_main.png')
img = img.resize([width, height])
p2_img = ImageTk.PhotoImage(img)
lbl = Label(frame2, image=p2_img)
lbl.place(x=0,y=0)
btnToFrame3 = Button(frame2, text="네 알겠습니다!",command=lambda:[openFrame(frame3)], relief=GROOVE, font=("HY엽서M",20))

btnToFrame2to1 = Button(frame2, text="처음으로",command=lambda:[openFrame(frame1), reset()], relief = GROOVE, font=("HY엽서M",20))
btnToFrame2to1.place(bordermode=INSIDE, relx=0.1, rely=0.1, anchor=CENTER, width=300, height=50)
btnToFrame2to1.focus()

### PAGE 3
def changelist(i):
    if len(_list)<4 and i not in _list:
        _list.append(i)
    elif i in _list:
        _list.remove(i)
    lbl_p3['text'] = str(_list)
    if len(_list)==4:
        btnToFrame4['state']=NORMAL

im_1 = Image.open('img1.png')
im_1 = im_1.resize([346,195])
img_1 = ImageTk.PhotoImage(im_1)
img_2 = PhotoImage(file='img2.png')
img_3 = PhotoImage(file='img3.png')
img_4 = PhotoImage(file='img4.png')
img_5 = PhotoImage(file='img5.png')
img_6 = PhotoImage(file='img6.png')
img_7 = PhotoImage(file='img7.png')
img_8 = PhotoImage(file='img8.png')

frame3=Frame(window, width = width, height = height)

imgbtn1 = Button(frame3, image= img_1, command=lambda: changelist(1))
imgbtn2 = Button(frame3, image= img_2, command=lambda: changelist(2))
imgbtn3 = Button(frame3, image= img_3, command=lambda: changelist(3))
imgbtn4 = Button(frame3, image= img_4, command=lambda: changelist(4))
imgbtn5 = Button(frame3, image= img_5, command=lambda: changelist(5))
imgbtn6 = Button(frame3, image= img_6, command=lambda: changelist(6))
imgbtn7 = Button(frame3, image= img_7, command=lambda: changelist(7))
imgbtn8 = Button(frame3, image= img_8, command=lambda: changelist(8))

imgbtn1.place(x=width/8 , y=height*1/4, anchor=CENTER)
imgbtn2.place(x=width*3/8 , y=height*1/4, anchor=CENTER)
imgbtn3.place(x=width*5/8 , y=height*1/4, anchor=CENTER)
imgbtn4.place(x=width*7/8 , y=height*1/4, anchor=CENTER)
imgbtn5.place(x=width/8 , y=height*3/4, anchor=CENTER)
imgbtn6.place(x=width*3/8 , y=height*3/4, anchor=CENTER)
imgbtn7.place(x=width*5/8 , y=height*3/4, anchor=CENTER)
imgbtn8.place(x=width*7/8 , y=height*3/4, anchor=CENTER)

lbl_p3 = Label(frame3, text=str(_list), relief = GROOVE, font=("HY엽서M",20))
lbl_p3.place(x=width/2, y=height/2, anchor=CENTER)
ll_p3 = Label(frame3, text="원하시는 변환 방식을 네 가지 선택해주세요", font=("HY엽서M",20))
ll_p3.place(x=width/2, y=height*9/10, anchor=CENTER)

btnToFrame4 = Button(frame3, text="선택완료!",command=lambda:[openFrame(frame4)], relief = GROOVE, font=("HY엽서M",20))
btnToFrame4['state']=DISABLED

btnToFrame3to1 = Button(frame2, text="처음으로",command=lambda:[openFrame(frame1), reset()], relief = GROOVE, font=("HY엽서M",20))
btnToFrame3to1.place(bordermode=INSIDE, relx=0.1, rely=0.1, anchor=CENTER, width=300, height=50)
btnToFrame3to1.focus()

### PAGE 4
frame4=Frame(window, width = width, height = height)

fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False

lmain = Label(frame4, compound=CENTER, anchor=CENTER, relief=RAISED, width=width, height=height)
lmain.pack()

def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True 
    button1 = Button(frame4, text="Good Image!", command=saveAndExit, relief = GROOVE, font=("HY엽서M",20))
    button2 = Button(frame4, text="Try Again", command=resume, relief = GROOVE, font=("HY엽서M",20))
    button1.place(anchor=CENTER, relx=0.2, rely=0.9)
    button2.place(anchor=CENTER, relx=0.8, rely=0.9)
    button1.focus()

def saveAndExit(event = 0):
    global prevImg
    lmain.after_cancel(v)
 
    if (len(sys.argv) < 2):
        filepath = "file/imageCap.png"
    else:
        filepath = sys.argv[1]
 
    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    openFrame(frame5)
    
    for img_num, i in enumerate(_list):
        t = threading.Thread(target=convert, args=[i, img_num])
        t.start()

    t = threading.Thread(target=final_start, args=[_list])
    t.start()
    #final(temp_image)
    
def final_start(_list):
    time.sleep(2)
    
    is_generated = [False, False, False, False]

    for n, i in enumerate(_list):
        is_generated[n] = os.path.exists('file/result{}.png'.format(i))
    
    if is_generated[0] * is_generated[1] * is_generated[2] * is_generated[3] == 1:
        final(im_lbl)
    else:
        final_start(_list)

    
def resume(event = 0):
    global button1, button2, button, lmain, cancel
    lmain.after_cancel(v)
 
    cancel = False
    button1.place_forget()
    button2.place_forget()
 
    frame4.bind('<Return>', prompt_ok)
    button.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
    lmain.after(10, show_frame)

def prompt(event=0):
    global v
    button.place_forget()
    v = lmain.after(2000, prompt_ok)

button = Button(frame4, text="Capture", command=prompt, relief = GROOVE, font=("HY엽서M",20))
lab = Label(frame4, text="클릭 후 3초뒤에 촬영됩니다", relief = GROOVE, font=("HY엽서M",20))
button.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
lab.place(relx=0.5, rely=0.1, anchor=CENTER)
button.focus()

btnToFrame4to1 = Button(frame4, text="처음으로",command=lambda:[openFrame(frame1), reset()], relief = GROOVE, font=("HY엽서M",20))
btnToFrame4to1.place(bordermode=INSIDE, relx=0.1, rely=0.1, anchor=CENTER, width=300, height=50)
btnToFrame4to1.focus()

cap = cv.VideoCapture(0)
capWidth = cap.get(3)
capHeight = cap.get(4)

def show_frame():
    global cancel, prevImg, button
 
    _, frame = cap.read()
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    prevImg = Image.fromarray(cv2image)
    prevImg = prevImg.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)
show_frame()

temp_image = PhotoImage(file='변환.png')

def convert(style_num, img_num):
    original_img = Image.open('file/imageCap.png')
    if style_num == 1:
        artwork = original_img
    else:
        style = StyleTransfer(use_amp=True, preserve_color='style', adam=True, avg_pool=False, lr=10, logging=10)

        style_img = Image.open('./style/style{}.jpg'.format(style_num))
        original_img = np.array(original_img)[:, :, :3]
        artwork = style(Image.fromarray(original_img), style_img, iter=100)
    artwork.save('file/result{}.png'.format(style_num))

    convert_img = Image.open('file/result{}.png'.format(style_num))
    convert_img = convert_img.resize(size=[int(width/6), int(height/6)])
    imgtk = ImageTk.PhotoImage(image=convert_img, size = [width/8, height/8])
    if img_num == 0:
        img1.imgtk = imgtk
        img1.configure(image=imgtk)
    elif img_num == 1:
        img2.imgtk = imgtk
        img2.configure(image=imgtk)
    elif img_num == 2:
        img3.imgtk = imgtk
        img3.configure(image=imgtk)
    elif img_num == 3:
        img4.imgtk = imgtk
        img4.configure(image=imgtk)

#### Frame5
frame5=Frame(window, width = width, height = height)
img1 = Label(frame5, compound=CENTER, anchor=CENTER)
img2 = Label(frame5, compound=CENTER, anchor=CENTER)
img3 = Label(frame5, compound=CENTER, anchor=CENTER)
img4 = Label(frame5, compound=CENTER, anchor=CENTER)

lab5 = Label(frame5, text="변환에 20초 정도 소요됩니다.", relief = GROOVE, font=("HY엽서M",20))
lab5.place(relx=0.5, rely=0.1, anchor=CENTER)


convert_img = Image.open('변환.png')
convert_img = convert_img.resize(size=[int(width/6), int(height/6)])
imgtk = ImageTk.PhotoImage(image=convert_img, size = [width/8, height/8])
img1.imgtk = imgtk
img1.configure(image=imgtk)
img2.imgtk = imgtk
img2.configure(image=imgtk)
img3.imgtk = imgtk
img3.configure(image=imgtk)
img4.imgtk = imgtk
img4.configure(image=imgtk)

img1.place(x=width/8 , y=height*2/4, anchor=CENTER)
img2.place(x=width*3/8 , y=height*2/4, anchor=CENTER)
img3.place(x=width*5/8 , y=height*2/4, anchor=CENTER)
img4.place(x=width*7/8 , y=height*2/4, anchor=CENTER)

btnToFrame6 = Button(frame5, text="변환완료!",command=lambda:[openFrame(frame6)], relief = GROOVE, font=("HY엽서M",20))
btnToFrame6['state']=DISABLED

def final(temp_img):
    # a = PhotoImage(file='file/result{}.png'.format(_list[0]))
    # b = PhotoImage(file='file/result{}.png'.format(_list[1]))
    # c = PhotoImage(file='file/result{}.png'.format(_list[2]))
    # d = PhotoImage(file='file/result{}.png'.format(_list[3]))
    a = Image.open('file/result{}.png'.format(_list[0]))
    a = a.resize([590, 443])

    b = Image.open('file/result{}.png'.format(_list[1]))
    b = b.resize([590, 443])

    c = Image.open('file/result{}.png'.format(_list[2]))
    c = c.resize([590, 443])

    d = Image.open('file/result{}.png'.format(_list[3]))
    d = d.resize([590, 443])

    size = a.size
    new_image = Image.new('RGB',(size[0]+20, size[1]*4+130),(2,150,150))
    new_image.paste(a,(10,10))
    new_image.paste(b,(10,20+size[1]))
    new_image.paste(c,(10,30+2*size[1]))
    new_image.paste(d,(10,40+3*size[1]))
    e = Image.open("캡처.jpg")
    new_image.paste(e,(120,50+4*size[1]))
    new_image.save("file/final.jpg","JPEG")
    
    new_image = ImageOps.contain(new_image, (width, height-150))
    new_image = ImageTk.PhotoImage(image=new_image)
    temp_img.imgtk = new_image
    temp_img.configure(image=new_image)
    # temp_img.configure(image = new_image)
    btnToFrame6['state']=NORMAL




### Frame6


def sendmsg(username):
    smtp = smtplib.SMTP('64.233.184.108', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('photographdot@gmail.com', 'tmigblaiujpvuuit')
    msg=EmailMessage()
    msg['Subject']="사진이DOT사진입니닷"
    file = 'file/final.jpg'
    fp = open(file,'rb')
    file_data=fp.read()
    msg.add_attachment(file_data, maintype='image', subtype='image_type', filename='file/final.jpg')
    msg['From']='phtographdot@gmail.com'
    msg['To']=username
    try:
        smtp.send_message(msg)
    except:
        lbl_fail =  Label(frame6, text="전송에 실패하였습니다 다시 시도해주세요", relief = GROOVE, font=("HY엽서M,20"))
        p6_lbl.place(relx=0.5, rely=0.9, anchor=CENTER)
        openFrame(frame6)
    openFrame(frame7)
    smtp.quit()

frame6 = Frame(window, width = width, height = height)
im_lbl = Label(frame6, image = temp_image, relief = GROOVE)
p6_lbl = Label(frame6, text="전송을 원하시면 메일 주소를 입력해주세요 \n 원하지 않으시면 '처음으로'를 눌러주세요", relief = GROOVE, font=("HY엽서M",20))
im_lbl.place(relx=0.25, rely =0.0, anchor=N)
p6_lbl.place(relx=0.75, rely=0.45, anchor=CENTER)
p6_ety = Entry(frame6, relief = GROOVE, font=("HY엽서M,20"), width = 50)
p6_ety.place(relx=0.75, rely=0.5, anchor=CENTER)
p6_ety.insert(0, 'example@example.com')
p6_btn = Button(frame6, text="입력 완료", command = lambda:[sendmsg(p6_ety.get())], relief = GROOVE, font=("HY엽서M",20))
p6_btn.place(relx=0.75, rely=0.7, anchor=CENTER, width=300, height=50)

btnToFrame6to1 = Button(frame6, text="처음으로",command=lambda:[openFrame(frame1), reset()], relief = GROOVE, font=("HY엽서M",20))
btnToFrame6to1.place(bordermode=INSIDE, relx=0.75, rely=0.8, anchor=CENTER, width=300, height=50)
btnToFrame6to1.focus()


### Page 7
# frame1=Frame(window, width = width, height = height)
# img = Image.open('page1_main.png')
# img = img.resize([width, height])
# p1_img = ImageTk.PhotoImage(img)
# lbl = Label(frame1, image=p1_img)
# lbl.place(x=0,y=0)
# btnToFrame2 = Button(frame1, text="사진 찍으로 고고!",command=lambda:[openFrame(frame2)], relief=GROOVE, font=("HY엽서M",20))

frame7 = Frame(window, width = width, height = height)

img = Image.open('page7_main.png')
img = img.resize([width, height])
p8_img = ImageTk.PhotoImage(img)

p7_lbl = Label(frame7, image = p8_img, relief = GROOVE)
p7_lbl.place(x=0,y=0)

btnToFrame7to1 = Button(frame7, text="처음으로",command=lambda:[openFrame(frame1), reset()], relief = GROOVE, font=("HY엽서M",20))
btnToFrame7to1.place(bordermode=INSIDE, relx=0.5, rely=0.9, anchor=CENTER, width=300, height=50)
btnToFrame7to1.focus()

# btnToFrame7to1.place(x=50, y=50, anchor=CENTER)
btnToFrame4.place(x=width/2, y=height*1/2+50, anchor=CENTER)
btnToFrame2.place(x=width/2, y=height*3/4, anchor=CENTER)
btnToFrame3.place(x=width/2, y=height*3/4, anchor=CENTER)
btnToFrame6.place(x=width/2, y=height*3/4, anchor=CENTER)

frame1.place(x=0, y=0)
frame2.place(x=0, y=0)
frame3.place(x=0, y=0)
frame4.place(x=0, y=0)
frame5.place(x=0, y=0)
frame6.place(x=0, y=0)
frame7.place(x=0, y=0)

openFrame(frame1)
window.mainloop()