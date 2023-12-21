import tkinter as tk
from PIL import Image, ImageTk
PATH1 = ".\handy_clicker\Openen_btn.png"
PATH2 = ".\handy_clicker\Sample_add_btn.png"

class FirstWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("First Window")
        self.master.geometry("400x400")

        #make and pack canvas
        self.canvas = tk.Canvas(self.master, width=300, height=300, bg="white")
        self.canvas.pack()

        #initialize image and tk image on canvas
        self.initial_image_path = PATH1  # Replace with your initial image path
        self.image = Image.open(self.initial_image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas_image = self.canvas.create_image(150, 150, image=self.tk_image)

        self.open_second_window_button = tk.Button(self.master, text="Open Second Window", command=self.open_second_window)
        self.open_second_window_button.pack(pady=20)

    def open_second_window(self):
        second_window = tk.Toplevel(self.master)
        SecondWindow(second_window, self)

    #make update canvas function using image to generate tk image
    def update_canvas_image(self, updated_image):
        self.tk_image = ImageTk.PhotoImage(updated_image)
        self.canvas.itemconfig(self.canvas_image, image=self.tk_image)

class SecondWindow:
    def __init__(self, master, first_window):
        self.master = master
        self.master.title("Second Window")
        self.master.geometry("200x150")

        self.first_window = first_window

        label = tk.Label(self.master, text="Update Image on First Window Canvas:")
        label.pack()

        self.update_image_button = tk.Button(self.master, text="Update Image", command=self.update_canvas_image)
        self.update_image_button.pack()

    def update_canvas_image(self):
        updated_image_path = PATH2  # Replace with your updated image path
        updated_image = Image.open(updated_image_path)
        self.first_window.update_canvas_image(updated_image)
        self.master.destroy()

def main():
    root = tk.Tk()
    app = FirstWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
