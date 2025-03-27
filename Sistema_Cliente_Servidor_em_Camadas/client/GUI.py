import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

class ImageUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("Upload de Imagem")
        self.root.configure(bg="#f0f0f0")  
        self.root.geometry("500x600")  
        
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(expand=True)
        
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.button_frame.pack(pady=20)
        
        self.upload_label = tk.Label(self.button_frame, text="Selecione uma imagem para enviar:", bg="#f0f0f0", fg="#333", font=("Arial", 10, "bold"))
        self.upload_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.upload_button = tk.Button(self.button_frame, 
                               text="Enviar Imagem", 
                               command=self.upload_image, 
                               bg="#4CAF50", 
                               fg="white", 
                               font=("Arial", 10, "bold"), 
                               padx=10, pady=5, 
                               relief="flat", 
                               bd=5, 
                               highlightbackground="#3E8E41",  
                               highlightthickness=2, 
                               borderwidth=2, 
                               highlightcolor="#3E8E41")
        self.upload_button.grid(row=1, column=0, padx=5, pady=5)

        self.upload_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.filter_label = tk.Label(self.button_frame, text="Escolha um filtro:", bg="#f0f0f0", fg="#333", font=("Arial", 10, "bold"))
        self.filter_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.filter_var = tk.StringVar(root)
        self.filter_var.set("grayscale")  
        
        self.filter_menu = tk.OptionMenu(self.button_frame, self.filter_var, "grayscale", "invert", "mirror")
        self.filter_menu.config(
            bg="#FFDDC1",  
            fg="#333",  
            font=("Arial", 10),  
            relief="flat",  
            highlightthickness=2, 
            highlightcolor="#FF5722",  
            bd=2,  
            width=15  
        )

        self.filter_menu.grid(row=1, column=1, padx=5, pady=5)


        self.filter_menu.config(bg="#ddd", font=("Arial", 10))
        self.filter_menu.grid(row=1, column=1, padx=5, pady=5)
        
        self.original_label = tk.Label(self.main_frame, text="Imagem Original:", bg="#f0f0f0", fg="#333", font=("Arial", 12, "bold"))
        self.original_label.pack()
        self.original_image_label = tk.Label(self.main_frame, bg="#f0f0f0")
        self.original_image_label.pack()

        self.modified_label = tk.Label(self.main_frame, text="Imagem Alterada:", bg="#f0f0f0", fg="#333", font=("Arial", 12, "bold"))
        self.modified_label.pack()
        self.modified_image_label = tk.Label(self.main_frame, bg="#f0f0f0")
        self.modified_image_label.pack()
        

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return

        print(f"Enviando imagem: {file_path}")

        with open(file_path, 'rb') as img_file:
            response = requests.post('http://localhost:5000/upload', files={'image': img_file}, data={'filtro': self.filter_var.get()})

        print(f"Status da resposta: {response.status_code}")
        print(f"Conteúdo da resposta: {response.text}")

        if response.status_code == 200:
            data = response.json()
            self.show_images(data['original_url'], data['modified_url'])
        else:
            print("Erro no servidor:", response.text)
            messagebox.showerror("Erro", "Falha ao enviar a imagem.")
            

    def show_images(self, original_url, modified_url):
        base_url = "http://localhost:5000"  

        original_image_url = base_url + original_url
        original_response = requests.get(original_image_url)
        
        if original_response.status_code == 200:
            original_image = Image.open(BytesIO(original_response.content))
            original_image.thumbnail((300, 300))  
            original_photo = ImageTk.PhotoImage(original_image)
            self.original_image_label.config(image=original_photo)
            self.original_image_label.image = original_photo  

        modified_image_url = base_url + modified_url
        modified_response = requests.get(modified_image_url)

        if modified_response.status_code == 200:
            modified_image = Image.open(BytesIO(modified_response.content))
            modified_image.thumbnail((300, 300))  
            modified_photo = ImageTk.PhotoImage(modified_image)
            self.modified_image_label.config(image=modified_photo)
            self.modified_image_label.image = modified_photo


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploader(root)
    root.mainloop()
