import requests
import json
import cv2
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Variables globales
image = None
image_path = None

# Credenciales y URL de la API de Watson
api_key = ' zofEDYVYsJY0vhlJt_C-genDPw2UpvE2NDVFqnLWmuHQ'
url = 'https://api.us-south.assistant.watson.cloud.ibm.com/instances/f3be9265-70c7-4bcd-adeb-158c5e34ef2b '
version = '2024-08-25'

# Función para cargar la imagen
def load_image():
    global image, image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if image_path:
        image = cv2.imread(image_path)
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

# Función para detectar rostros usando Watson
def detect_faces():
    if not image_path:
        messagebox.showwarning("Advertencia", "Primero carga una imagen.")
        return

    # Llamada a la API de Watson
    with open(image_path, 'rb') as image_file:
        files = {'images_file': image_file}
        params = {'version': version}
        response = requests.post(url, params=params, files=files, auth=('apikey', api_key))

    # Procesar la respuesta
    response_json = response.json()
    if 'images' in response_json:
        faces = response_json['images'][0].get('faces', [])
        
        if not faces:
            messagebox.showinfo("Resultado", "No se encontraron rostros.")
            return

        output_dir = 'assets/output'
        os.makedirs(output_dir, exist_ok=True)

        for i, face in enumerate(faces):
            x = face['face_location']['left']
            y = face['face_location']['top']
            w = face['face_location']['width']
            h = face['face_location']['height']

            # Recortar el rostro y guardarlo
            face_img = image[y:y+h, x:x+w]
            face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
            face_path = os.path.join(output_dir, f'face_{i+1}.jpg')
            face_pil.save(face_path)

        messagebox.showinfo("Éxito", f"Se han detectado y guardado {len(faces)} rostro(s) en '{output_dir}'.")
    else:
        messagebox.showerror("Error", "Ocurrió un error con la API de Watson.")

# Configuración inicial de la interfaz
root = tk.Tk()
root.title("Detector de Rostros con Watson")
root.geometry("400x400")  # Tamaño ajustado de la ventana

panel = tk.Label(root)
panel.pack(pady=20)

btn_load = tk.Button(root, text="Cargar Imagen", command=load_image)
btn_load.pack(side="left", padx=20)

btn_detect = tk.Button(root, text="Detectar Rostros", command=detect_faces)
btn_detect.pack(side="right", padx=20)

root.mainloop()
