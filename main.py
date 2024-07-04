import tkinter as tk
import AI
import numpy as np
from PIL import Image, ImageTk, ImageDraw

#menginisialisasi model AI
model = AI.load_ai()

#membuat jendela utama aplikasi
window = tk.Tk()

#membuat canvas untuk gambar
img = Image.new(mode="1", size=(500, 500), color=125)
tkimage = ImageTk.PhotoImage(img)
canvas = tk.Label(window, image=tkimage)
canvas.pack()

draw = ImageDraw.Draw(img)

#inisialisasi variabel
last_point = (0, 0)
prediction = tk.StringVar()
label = tk.Label(window, textvariable=prediction)

#untuk menggambar di canvas
def draw_image(event):
    global last_point, tkimage, prediction
    current_point = (event.x, event.y)
    draw.line([last_point, current_point], fill=255, width=50)
    last_point = current_point
    tkimage = ImageTk.PhotoImage(img)
    canvas['image'] = tkimage
    canvas.pack()
    img_temp = img.resize((28, 28))
    img_temp = np.array(img_temp)
    img_temp = img_temp.flatten()
    output = model.predict([img_temp])
    if(output[0] == 0):
        prediction.set("kotak")
    elif(output[0] == 1):
        prediction.set("lingkaran")
    else:
        prediction.set("segitiga")
    label.pack()

#untuk mencatat titik awal menggambar
def start_draw(event):
    global last_point
    last_point = (event.x, event.y)

#untuk mereset canvas ketika klik kanan pada mouse
def reset_canvas(event):
    global tkimage, img, draw
    img = Image.new(mode="1", size=(500, 500), color=0)
    draw = ImageDraw.Draw(img)
    tkimage = ImageTk.PhotoImage(img)
    canvas['image'] = tkimage
    canvas.pack()

#inisialisasi variabel penyimpanan gambar
kotak = 0
lingkaran = 0
segitiga = 0

# untuk menyimpan gambar yang digambar dengan menekan tombol 'k', 'l', atau 's' untuk kotak, lingkaran, dan segitiga.
def save_image(event):
    global kotak, lingkaran, segitiga
    img_temp = img.resize((28, 28))
    if(event.char == "k"):
        img_temp.save(f"kotak/{kotak}.png")
        kotak += 1
    elif(event.char == "l"):
        img_temp.save(f"lingkaran/{lingkaran}.png")
        lingkaran += 1
    elif(event.char == "s"):
        img_temp.save(f"segitiga/{segitiga}.png")
        segitiga += 1

#menghubungkan fungsi dengan event mouse dan keyboard
window.bind("<B1-Motion>", draw_image)
window.bind("<ButtonPress-1>", start_draw)
window.bind("<ButtonPress-3>", reset_canvas)
window.bind("<Key>", save_image)


label.pack()

window.mainloop()