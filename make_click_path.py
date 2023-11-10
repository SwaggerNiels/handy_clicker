import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import pyautogui as pa
import time

actions = [] # can be ('click', (x,y)) or ('type', 'some_string') or ('press', 'some_key_combination')
slider_values = []
descriptions = []
human_readable_to_pyautogui = {
    'Tab': '\t',
    'Enter': '\n',
    'Space': ' ',
    'Exclamation Mark': '!',
    'Double Quote': '"',
    'Hash': '#',
    'Dollar Sign': '$',
    'Percent': '%',
    'Ampersand': '&',
    'Single Quote': "'",
}

press_options = list(human_readable_to_pyautogui.keys())

def on_entry_focus_in(event): pass
def on_entry_focus_out(event): pass

def press_popup():
    popup = tk.Toplevel(root)
    popup.title("Select an Option")

    # Create a dropdown menu using the predefined list of items
    selected_option = tk.StringVar()
    selected_option.set(press_options[0])  # Set the default option

    dropdown = ttk.Combobox(popup, textvariable=selected_option, values=press_options)
    dropdown.pack(padx=20, pady=10)

    # Function to save the chosen option to a variable
    def save_choice():
        choice = selected_option.get()
        # You can save the chosen option to a variable or perform any desired action here
        popup.destroy()

    ok_button = tk.Button(popup, text="OK", command=save_choice)
    ok_button.pack(pady=10)
    return selected_option

def record_press(event=None):
    press_input = press_popup()
    actions.append(('press',press_input.get()))
    slider_var = tk.IntVar(value=50)
    slider_values.append(slider_var)
    description_var = tk.StringVar(value='')
    descriptions.append(description_var)
    update_actions()
    
def record_type(event=None):
    typed_input = sd.askstring(title='What to type?', prompt='your input')
    actions.append(('type',typed_input))
    slider_var = tk.IntVar(value=50)
    slider_values.append(slider_var)
    description_var = tk.StringVar(value='')
    descriptions.append(description_var)
    update_actions()

def record_click(event=None):
    mouse_x, mouse_y = pa.position()
    actions.append(('click',(mouse_x, mouse_y)))
    slider_var = tk.IntVar(value=50)
    slider_values.append(slider_var)
    description_var = tk.StringVar(value='')
    descriptions.append(description_var)
    update_actions()
    
def remove_action(index):
    if index < len(actions):
        # Destroy the "Remove" button and the actions label
        remove_button_widgets[index].destroy()
        action_label_widgets[index].destroy()
        slider_widgets[index].destroy()
        description_widgets[index].destroy()

        actions.pop(index)
        slider_values.pop(index)
        descriptions.pop(index)
        update_actions()

# Lists to keep track of button and label widgets
remove_button_widgets = []
action_label_widgets = []
slider_widgets = []
description_widgets = []

def set_action_labels():
    for i,label in enumerate(action_label_widgets):
        action = actions[i]
        t = slider_values[i].get()
        
        if action[0] == 'click':
            x,y = action[1]
            label.config(text=f"({x:<5}, {y:<5}) t={t:<5}")
        elif action[0] == 'type':
            typed_input = action[1]
            label.config(text=f"type: {typed_input} t={t:<5}")        
        elif action[0] == 'press':
            press_input = action[1]
            label.config(text=f"press: {press_input} t={t:<5}")        
            
def update_actions(event=None):
    action_text.config(state=tk.NORMAL)
    action_text.delete(1.0, tk.END)

    # Clear the widget lists
    for widget in remove_button_widgets:
        widget.destroy()
    for widget in action_label_widgets:
        widget.destroy()
    for widget in slider_widgets:
        widget.destroy()
    for widget in description_widgets:
        widget.destroy()

    remove_button_widgets.clear()
    action_label_widgets.clear()
    slider_widgets.clear()
    description_widgets.clear()

    for i, action in enumerate(actions):
        remove_button = tk.Button(action_text, text="Remove", command=lambda i=i: remove_action(i))
        remove_button.grid(row=i, column=0)
        remove_button_widgets.append(remove_button)
        
        slider = tk.Scale(action_text, from_=0, to=1000, orient="horizontal", variable=slider_values[i],
                          length=200, resolution=25, command=set_action_labels)
        slider_widgets.append(slider)
        slider.grid(row=i, column=2)
        slider.config(font=("Helvetica", 1))
        
        action_label = tk.Label(action_text)
        action_label.grid(row=i, column=1)
        action_label_widgets.append(action_label)
        set_action_labels()
        
        description = tk.Entry(action_text, width=30, textvariable=descriptions[i], )
        description.grid(row=i, column=3)
        description_widgets.append(description)
        description.bind('<FocusIn>', on_entry_focus_in)
        description.bind('<FocusOut>', on_entry_focus_out)

    action_text.config(state=tk.DISABLED)

def execute_program():
    for i, action in enumerate(actions): 
        
        if action[0] == 'click':
            x,y = action[1]
            pa.click(x, y)
        elif action[0] == 'type':
            pa.write(action[1])
        elif action[0] == 'press':
            pa.press(human_readable_to_pyautogui[action[1]])
            
        time.sleep(slider_values[i].get()/100)

def save_program():
    f = fd.asksaveasfile(title='Choose name to save to', mode='w', defaultextension=".prog")
    for (action,val),s,d in zip(actions, slider_values, descriptions):
        d = d.get() if d.get() != '' else 'None'
        if action == 'click':
            val = f'{val[0]}-{val[1]}'
        f.write(f'{action}; {val}, {s.get()}, {d}\n')
    f.close()

def load_program():
    global actions, slider_values, descriptions
    f = fd.askopenfile(title='Choose program to open')
    
    actions = []
    slider_values = []
    descriptions = []

    for line in f.readlines():
        a,s,d = line.split(',')
        (action, val) = a.split(';')
        if action == 'click':
            val = tuple(val.split('-'))
        d = d.strip()
        d = d if d != 'None' else ''
        actions.append( (action,val) ) 
        slider_values.append( tk.IntVar(value=int(s)) )
        descriptions.append( tk.StringVar(value=d) )
    f.close()

    on_entry_focus_out(None)

    update_actions()
        
# Create the main window
root = tk.Tk()
root.title("Mouse actions Recorder")

# Create a text widget to display the recorded actions
action_text = tk.Text(root, height=10, width=10, state=tk.DISABLED)
action_text.pack(pady=20, padx=20)

# Create a button to click all the recorded actions
type_btn = tk.Button(root, text="Add button press", command=record_press)
type_btn.pack()
type_btn = tk.Button(root, text="Add typing text", command=record_type)
type_btn.pack()
execute_btn = tk.Button(root, text="Execute program", command=execute_program)
execute_btn.pack()
load_btn = tk.Button(root, text="Load program", command=load_program)
load_btn.pack()
save_btn = tk.Button(root, text="Save program", command=save_program)
save_btn.pack()

# Bind the space key to record_click function
def on_entry_focus_in(event): 
    root.unbind('<space>')  # Unbind the Space key
    root.bind('<Return>', lambda event : root.focus_set())  # Unbind the Space key
def on_entry_focus_out(event): 
    root.bind('<space>', record_click)  # Rebind the Space key
    root.unbind('<Return>')
on_entry_focus_out(None)
root.bind('<Escape>', lambda event : root.destroy())

update_actions()

# Start the tkinter main loop
root.mainloop()

print(actions)