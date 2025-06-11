#Library for making QRCode
import qrcode

#For converting to image
from PIL import Image

import tkinter as tk
import qrcode.constants
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import filedialog
from PIL import ImageTk


qr_color="black"
logo_path=None

#To Generate The Actual Qr Code
def generate_qr():
    data=entry.get().strip()
    filename=filename_entry.get().strip().replace(" ","_") or "default"
    if not data:
        messagebox.showwarning("Input required","Please enter some data for the QR code")
        return
    try:
        qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=10,
            )
        qr.add_data(data)
        qr.make(fit=True)
        img=qr.make_image(fill_color=qr_color,back_color="white")
        if logo_path:
            try:
                logo=Image.open(logo_path).convert("RGBA")
                qr_width, qr_height=img.size
                logo_size=int(qr_width/6)
                logo=logo.resize((logo_size,logo_size))
                pos=((qr_width-logo_size)//2,(qr_height-logo_size)//2)
                img.paste(logo, pos, mask=logo)
            except FileNotFoundError:
                print("Sorry!The name which you have provided for logo file is not there")
            except Exception as e:
                print(f"Error in inserting logo:{e}")
        img.save(f"{filename}.png")
        preview_image=img.resize((200,200))
        qr_preview_image=ImageTk.PhotoImage(preview_image)
        qr_preview_label.config(image=qr_preview_image)
        qr_preview_label.image=qr_preview_image
        messagebox.showinfo("Success",f"Qr code generated and saved as {filename}.png")
    except Exception as e:
        messagebox.showerror("Error",f"{e}")

def pick_color():
    global qr_color
    color_code=colorchooser.askcolor(title="Choose a Color: ")
    if color_code[1]:
        qr_color=color_code[1]
        color_display_frame.config(bg=qr_color)

def choose_logo():
    global logo_path
    path=filedialog.askopenfilename(title="Select Logo Image",filetypes=[("Image Files","*.png;*.jpeg;*.jpg;*.bmp")])
    if path:
        logo_path=path
        logo_label.config(text="Logo Selected",fg="green")
    else:
        logo_path=None
        logo_label.config(text="No Logo Selected",fg="red")

root=tk.Tk()
root.title("Qr Code Generator")

tk.Label(root, text="Enter the data for QR Code: ",fg="black").pack()
entry=tk.Entry(width=40)
entry.pack(pady=20)

tk.Label(root, text="Enter the filename(optional): ", fg="black").pack()
filename_entry=tk.Entry(width=40)
filename_entry.pack(pady=20)

color_label=tk.Label(root, text="Choose Color of your QR Code: ",fg="black")
color_label.pack()

color_button=tk.Button(root, text="Selected color: ", command=pick_color)
color_button.pack()

color_display_frame=tk.Frame(root, width=20, height=20, bg=qr_color,relief="ridge", border=2,)
color_display_frame.pack(pady=5)

logo_label=tk.Label(root, text="No Logo Selected",fg=qr_color)
logo_label.pack()

logo_button=tk.Button(root, text="Choose Logo(Optional): ",command=choose_logo)
logo_button.pack(pady=5)

button=tk.Button(root, text="Generate Qr", command=generate_qr)
button.pack()

qr_preview_label=tk.Label(root)
qr_preview_label.pack(pady=10)

root.mainloop()
