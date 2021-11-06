import subprocess
import sys
import os
from tkinter import *
from tkinter import messagebox
from desEncryptDecrypt import encrypt, decrypt, stringToHex

root = Tk()
root.title("DES Algorithm")
root.geometry("550x200")
  
def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)
 
def encryptClicked():
    if len(keyText.get()) == 8:
        hexKey = stringToHex(keyText.get())  
        result = encrypt(hexKey, letterText.get())
        messagebox.showinfo("Encrypted text - текст скопирован в буфер обмена", result)
        copy2clip(result)
    else:
        messagebox.showerror("Error", "Введённый ключ не 8 символов")
    
def decryptClicked():
    if len(keyText.get()) == 8:
        hexKey = stringToHex(keyText.get()) 
        result = decrypt(hexKey, letterText.get())
        messagebox.showinfo("Decrypted text - текст скопирован в буфер обмена", result)
        copy2clip(result)
    else:
        messagebox.showerror("Error", "Введённый ключ не 8 символов")

letterText = StringVar()
keyText = StringVar()
 
letter_label = Label(text="Введите текст:")
key_label = Label(text="Введите ключ(8 символов):")
 
letter_label.grid(row=0, column=0)
key_label.grid(row=1, column=0)
 
letter_entry = Entry(width="50", textvariable=letterText)
key_entry = Entry(width="50", textvariable=keyText)
 
letter_entry.grid(row=0, column=1)
key_entry.grid(row=1, column=1)
 
encryptButton = Button(text="Encrypt", command=encryptClicked)
encryptButton.grid(row=2, column=1)

decryptButton = Button(text="Decrypt", command=decryptClicked)
decryptButton.grid(row=3, column=1)
 
root.mainloop()