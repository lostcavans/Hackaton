import cv2
from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para cargar la imagen
def load_image():
    global image, gray_image, image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if image_path:
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        display_image(image)

# Función para mostrar la imagen en miniatura en la interfaz
def display_image(img):
    thumbnail_size = (200, 200)  # Tamaño de la miniatura
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil.thumbnail(thumbnail_size)
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.config(image=img_tk)
    panel.image = img_tk

# Función para detectar rostros
def detect_faces():
    if not image_path:
        messagebox.showwarning("Advertencia", "Primero carga una imagen.")
        return

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        messagebox.showinfo("Resultado", "No se encontraron rostros.")
        return
    
    output_dir = 'assets/output'
    os.makedirs(output_dir, exist_ok=True)
    
    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        face_pil = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        face_path = os.path.join(output_dir, f'face_{i+1}.jpg')
        face_pil.save(face_path)
        
    messagebox.showinfo("Éxito", f"Se han detectado y guardado {len(faces)} rostro(s) en '{output_dir}'.")

# Configuración inicial de la interfaz
root = tk.Tk()
root.title("Detector de Rostros")
root.geometry("400x400")  # Tamaño ajustado de la ventana

panel = tk.Label(root)
panel.pack(pady=20)

btn_load = tk.Button(root, text="Cargar Imagen", command=load_image)
btn_load.pack(side="left", padx=20)

btn_detect = tk.Button(root, text="Detectar Rostros", command=detect_faces)
btn_detect.pack(side="right", padx=20)

# Cargar el modelo de detección de rostros de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

root.mainloop()
