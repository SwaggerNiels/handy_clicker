import tkinter as tk
import pyscreenshot as ps
import pyautogui as pa
from PIL import Image, ImageTk
import sys

# part of the screen
im=ps.grab(bbox=(10,10,500,500))
im.save("partial.png")

class KeyPressCounter():
    def __init__(self, master : tk.Toplevel):
        self.master = master

        self.count = 0
        self.photo_box = [0,0,0,0]
        
        self.image_path = ''
        self.coords = None

        self.label = tk.Label(master, text="Press 'space' key twice to make a photo.")
        self.label.pack(pady=20)

        self.master.bind("<space>", self.key_pressed)

    def key_pressed(self, event):
        if event.keysym == "space":
            self.count += 1
            if self.count == 2:
                (x2,y2) = pa.position()
                self.photo_box[2] = x2
                self.photo_box[3] = y2

                self.execute_action()
            (x1,y1) = pa.position()
            self.photo_box[0] = x1
            self.photo_box[1] = y1
            
    def execute_action(self):
        # Replace this with the action you want to execute
        im=ps.grab(bbox=self.photo_box)
        im.save("partial.png")

        self.master.image_path = 'partial.png'

        self.master.wait_pointed = tk.BooleanVar(self.master, value=False)
        _ = ImageCanvas(self.master, self.image_path)
        self.master.wait_variable(self.master.wait_pointed)
        self.master.wait_pointed_picture.set(True)
    
    def get_coordinates(self):
        return(self.coords)

class ImageCanvas():
    def __init__(self, master : tk.Toplevel, image_path):
        self.master = master

        # Load your image (replace 'image_file_path' with your image file path)
        updated_image = Image.open(image_path)
        self.master.set_image(updated_image)
        self.coords = (0,0)

        self.master.canvas.bind("<Button-1>", self.save_coordinates)

    def save_coordinates(self, event):
        x, y = event.x, event.y
        self.coords = (x, y)
        self.draw_dot(x, y)
        
        self.master.set_coords((x,y))

        self.master.wait_pointed.set(True)

    def draw_dot(self, x, y):
        dot_size = 5
        self.master.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill="red")
        self.master.canvas.update_idletasks()

def main():
    real_root = tk.Tk()
    real_root.title('first window')

    real_root.coords = None
    
    real_root.image_file_path = 'partial.png'
    real_root.image = tk.PhotoImage(file=real_root.image_file_path)
    real_root.canvas = tk.Canvas(width=real_root.image.width(), height=real_root.image.height())
    real_root.canvas_image = real_root.canvas.create_image(0, 0, anchor="nw", image=real_root.image)
    real_root.canvas.pack()

    def set_coords(coords): real_root.coords = coords
    def set_image(updated_image):
        real_root.tk_image = ImageTk.PhotoImage(updated_image)
        real_root.canvas.itemconfig(real_root.canvas_image, image=real_root.tk_image)

    real_root.set_coords = set_coords
    real_root.set_image = set_image
    
    #open and use the second window
    root = tk.Toplevel(master=real_root)
    root.title('second window')

    KeyPressCounter(root)

    real_root.mainloop()

    # root.wait_pointed_picture = tk.BooleanVar(root, value=False)
    # KeyPressCounter(root) #changes image_file_path and coords
    # root.wait_variable(root.wait_pointed_picture)
    # coords = root.coords
    # root.destroy()
    # print(f'main: {coords}')


    # dot_size = 5
    # x,y = root.coords
    # root.canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill="red")
    # root.canvas.update_idletasks()
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error ocurred:', e)

