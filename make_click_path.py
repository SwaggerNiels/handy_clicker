import tkinter as tk
import pyautogui as pa
import time

coordinates_list = []
slider_values = []
descriptions = []

def on_entry_focus_in(event): pass
def on_entry_focus_out(event): pass


def record_coordinates(event):
    mouse_x, mouse_y = pa.position()
    coordinates_list.append((mouse_x, mouse_y))
    slider_var = tk.IntVar(value=50)
    slider_values.append(slider_var)
    description_var = tk.StringVar(value='')
    descriptions.append(description_var)
    update_coordinates_text()

def remove_coordinate(index):
    if index < len(coordinates_list):
        # Destroy the "Remove" button and the coordinates label
        remove_button_widgets[index].destroy()
        coordinates_label_widgets[index].destroy()
        slider_widgets[index].destroy()
        description_widgets[index].destroy()

        coordinates_list.pop(index)
        slider_values.pop(index)
        descriptions.pop(index)
        update_coordinates_text()

# Lists to keep track of button and label widgets
remove_button_widgets = []
coordinates_label_widgets = []
slider_widgets = []
description_widgets = []

def update_slider_value(event=None):
    new_text = "New Text"  # Replace with your desired new text or logic
    for i,label in enumerate(coordinates_label_widgets):
        coord = coordinates_list[i]
        t = slider_values[i].get()
        label.config(text=f"({coord[0]:<5}, {coord[1]:<5}) t={t:<5}")

def update_coordinates_text(event=None):
    coordinates_text.config(state=tk.NORMAL)
    coordinates_text.delete(1.0, tk.END)

    # Clear the widget lists
    for widget in remove_button_widgets:
        widget.destroy()
    for widget in coordinates_label_widgets:
        widget.destroy()
    for widget in slider_widgets:
        widget.destroy()
    for widget in description_widgets:
        widget.destroy()

    remove_button_widgets.clear()
    coordinates_label_widgets.clear()
    slider_widgets.clear()
    description_widgets.clear()

    for i, coord in enumerate(coordinates_list):
        remove_button = tk.Button(coordinates_text, text="Remove", command=lambda i=i: remove_coordinate(i))
        remove_button.grid(row=i, column=0)
        remove_button_widgets.append(remove_button)
        
        slider = tk.Scale(coordinates_text, from_=0, to=1000, orient="horizontal", variable=slider_values[i],
                          length=200, resolution=25, command=update_slider_value)
        slider_widgets.append(slider)
        slider.grid(row=i, column=2)
        slider.config(font=("Helvetica", 1))
        
        t = slider_values[i].get()
        coordinates_label = tk.Label(coordinates_text, text=f"({coord[0]:<5}, {coord[1]:<5}) t={t:<5}")
        coordinates_label.grid(row=i, column=1)
        coordinates_label_widgets.append(coordinates_label)
        
        description = tk.Entry(coordinates_text, width=30, textvariable=descriptions[i], )
        description.grid(row=i, column=3)
        description_widgets.append(description)
        description.bind('<FocusIn>', on_entry_focus_in)
        description.bind('<FocusOut>', on_entry_focus_out)

    coordinates_text.config(state=tk.DISABLED)

def click_coordinates():
    for i, coord in enumerate(coordinates_list):
        pa.click(coord[0], coord[1])
        time.sleep(slider_values[i].get()/100)

# Create the main window
root = tk.Tk()
root.title("Mouse Coordinates Recorder")

# Create a text widget to display the recorded coordinates
coordinates_text = tk.Text(root, height=10, width=10, state=tk.DISABLED)
coordinates_text.pack(pady=20, padx=20)

# Create a button to click all the recorded coordinates
click_button = tk.Button(root, text="Click All Coordinates", command=click_coordinates)
click_button.pack()

# Bind the space key to record_coordinates function
def on_entry_focus_in(event): 
    root.unbind('<space>')  # Unbind the Space key
    root.bind('<Return>', lambda event : root.focus_set())  # Unbind the Space key
def on_entry_focus_out(event): 
    root.bind('<space>', record_coordinates)  # Rebind the Space key
    root.unbind('<Return>')
on_entry_focus_out(None)
root.bind('<Escape>', lambda event : root.destroy())

coordinates_list = [(1,2)]
slider_values = [tk.IntVar(value=25)]
descriptions = [tk.StringVar(value='hoi')]
update_coordinates_text()

# Start the tkinter main loop
root.mainloop()

print(coordinates_list)