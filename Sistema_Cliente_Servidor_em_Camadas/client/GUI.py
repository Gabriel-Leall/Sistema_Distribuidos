import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk

class ImageUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Upload de Imagem")
        
        self.label = tk.Label(root, text="Selecione uma imagem para enviar:")
        self.label.pack()

        self.upload_button = tk.Button(root, text="Enviar Imagem", command=self.upload_image)
        self.upload_button.pack()

        self.original_label = tk.Label(root, text="Imagem Original:")
        self.original_label.pack()
        self.original_image_label = tk.Label(root)
        self.original_image_label.pack()

        self.modified_label = tk.Label(root, text="Imagem Alterada:")
        self.modified_label.pack()
        self.modified_image_label = tk.Label(root)
        self.modified_image_label.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return

        print(f"Enviando imagem: {file_path}")

        with open(file_path, 'rb') as img_file:
            response = requests.post('http://localhost:5000/upload', files={'image': img_file})

        print(f"Status da resposta: {response.status_code}")
        print(f"Conteúdo da resposta: {response.text}")

        if response.status_code == 200:
            data = response.json()
            self.show_images(data['original_url'], data['modified_url'])
        else:
            print("Erro no servidor:", response.text)
            messagebox.showerror("Erro", "Falha ao enviar a imagem.")

    def show_images(self, original_url, modified_url):
        # Exibir a imagem original
        original_image = Image.open(original_url)
        original_image.thumbnail((300, 300))  # Redimensiona a imagem para caber na interface
        original_photo = ImageTk.PhotoImage(original_image)
        self.original_image_label.config(image=original_photo)
        self.original_image_label.image = original_photo  # Mantém uma referência à imagem

        # Exibir a imagem modificada
        modified_image = Image.open(modified_url)
        modified_image.thumbnail((300, 300))  # Redimensiona a imagem para caber na interface
        modified_photo = ImageTk.PhotoImage(modified_image)
        self.modified_image_label.config(image=modified_photo)
        self.modified_image_label.image = modified_photo  # Mantém uma referência à imagem

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploader(root)
    root.mainloop()