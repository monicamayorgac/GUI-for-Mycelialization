import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb_to_hsv

class MyceliumDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Mycelium Analysis (Demo)")
        self.root.geometry("1100x700")

        # Variables
        self.current_folder = ""
        self.image_list = []
        
        # --- (GUI) ---
        
        # Bottons
        top_frame = tk.Frame(root, bg="#ddd", pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        
        btn_load = tk.Button(top_frame, text="Select Folder", command=self.load_folder, font=("Arial", 12))
        btn_load.pack(side=tk.LEFT, padx=20)
        
        self.label_info = tk.Label(top_frame, text="No folder selected", bg="#ddd")
        self.label_info.pack(side=tk.LEFT)

        # Upper pannel
        main_panel = tk.Frame(root)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Files
        self.listbox = tk.Listbox(main_panel, width=30)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.listbox.bind('<<ListboxSelect>>', self.analyze_image) # Al hacer clic, analiza

        # Matplotlib
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax_original = self.figure.add_subplot(121) # Gráfica izquierda
        self.ax_mask = self.figure.add_subplot(122)     # Gráfica derecha
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_panel)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        
        self.current_folder = folder
        self.label_info.config(text=f"Folder: {os.path.basename(folder)}")
        
        self.listbox.delete(0, tk.END)
        self.image_list = []
        
        files = sorted(os.listdir(folder))
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.listbox.insert(tk.END, f)

    def analyze_image(self, event):

        selection = self.listbox.curselection()
        if not selection:
            return
        filename = self.listbox.get(selection[0])
        path = os.path.join(self.current_folder, filename)

        pil_img = Image.open(path).convert("RGB")
        img_array = np.array(pil_img)

        img_norm = img_array / 255.0
        hsv_img = rgb_to_hsv(img_norm)
        
        saturation = hsv_img[..., 1]
        value = hsv_img[..., 2]
        
        mask = (saturation < 0.4) & (value > 0.4)
        
        total_pixels = mask.size
        white_pixels = np.count_nonzero(mask)
        percentage = (white_pixels / total_pixels) * 100

        self.ax_original.clear()
        self.ax_mask.clear()

        self.ax_original.imshow(img_array)
        self.ax_original.set_title("Original Image")
        self.ax_original.axis('off')

        self.ax_mask.imshow(mask, cmap='gray')
        self.ax_mask.set_title(f"Detected Growth: {percentage:.1f}%")
        self.ax_mask.axis('off')

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyceliumDemo(root)
    root.mainloop()