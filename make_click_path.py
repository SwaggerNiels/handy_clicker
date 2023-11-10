import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
from tkinter.scrolledtext import ScrolledText
import pyautogui as pa
import time

actions = [] # can be ('click', (x,y)) or ('type', 'some_string') or ('press', 'some_key_combination')
slider_values = []
descriptions = []

human_readable_to_pyautogui = {
    'Tab': '\t',
    'Enter': '\n',
    'Return': '\r',
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
    selected_option = tk.StringVar(master=root)
    choice = press_options[0]
    selected_option.set(choice)  # Set the default option

    dropdown = ttk.Combobox(popup, textvariable=selected_option, values=press_options)
    dropdown.pack(padx=20, pady=10)
    
    dropdown.wait_variable(selected_option)
    choice = selected_option.get()
    popup.destroy()

    return choice

# def record_picturepress(event=None):
#     press_input = press_popup()
#     actions.append(('press',press_input))
#     slider_var = tk.IntVar(value=50)
#     slider_values.append(slider_var)
#     description_var = tk.StringVar(value='')
#     descriptions.append(description_var)
#     update_actions()

def record_press(event=None):
    press_input = press_popup()
    actions.append(('press',press_input))
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
        slider_widgets[index][0].destroy()
        slider_widgets[index][1].destroy()
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

def set_action_labels(event=None):
    for i,label in enumerate(action_label_widgets):
        action = actions[i]
        
        if action[0] == 'click':
            x,y = action[1]
            label.config(text=f"click: ({x:<5}, {y:<5})")
        elif action[0] == 'type':
            typed_input = action[1]
            label.config(text=f"type: {typed_input}")        
        elif action[0] == 'press':
            press_input = action[1]
            label.config(text=f"press: {press_input}")        
            
def update_actions(event=None):
    # Clear the widget lists
    for widget in remove_button_widgets:
        widget.destroy()
    for widget in action_label_widgets:
        widget.destroy()
    for widgets in slider_widgets:
        for widget in widgets:
            widget.destroy()
    for widget in description_widgets:
        widget.destroy()

    remove_button_widgets.clear()
    action_label_widgets.clear()
    slider_widgets.clear()
    description_widgets.clear()

    fnt = 'Helvetica 10 bold'
    # tk.Label(action_text, text='Remove', justify='left', font=fnt).grid(row=0, column=0, sticky='W')
    tk.Label(action_text, text='Delay 1/100[s]', justify='left', font=fnt).grid(row=0, column=2, columnspan=2, sticky='W')
    tk.Label(action_text, text='Action', justify='left', font=fnt).grid(row=0, column=1, sticky='W')
    tk.Label(action_text, text='Description', justify='left', font=fnt).grid(row=0, column=4, sticky='W')

    for i, _ in enumerate(actions):
        remove_button = tk.Button(action_text, text="Remove", command=lambda i=i: remove_action(i))
        remove_button.grid(row=i+1, column=0)
        remove_button_widgets.append(remove_button)
        
        slider_label = tk.Label(action_text, textvariable=slider_values[i])
        slider_label.grid(row=i+1, column=2, sticky='W')
        slider = tk.Scale(action_text, from_=0, to=1000, orient="horizontal", variable=slider_values[i],
                          length=200, resolution=25, command=set_action_labels, showvalue=0)
        slider_widgets.append((slider_label,slider))
        slider.grid(row=i+1, column=3)
        
        action_label = tk.Label(action_text, wraplength=200, justify='left')
        action_label.grid(row=i+1, column=1, sticky='W')
        action_label_widgets.append(action_label)
        set_action_labels()
        
        description = tk.Entry(action_text, width=30, textvariable=descriptions[i], )
        description.grid(row=i+1, column=4)
        description_widgets.append(description)
        description.bind('<FocusIn>', on_entry_focus_in)
        description.bind('<FocusOut>', on_entry_focus_out)

    # action_text.config(state=tk.DISABLED)

def execute_program():

    def execute_actions():
        for i, action in enumerate(actions):
            if action[0] == 'click':
                x,y = action[1]
                pa.click(x, y)
            elif action[0] == 'type':
                pa.write(action[1])
            elif action[0] == 'press':
                pa.press(human_readable_to_pyautogui[action[1]])
            elif action[0] == 'picture_press_open':
                x1,y1,w,h = pa.locateOnScreen(r'C:\Users\roel\Desktop\Niels_prog\files_to_Inspection_Manager\Openen_btn.png',grayscale=True, confidence=.5)
                pa.click(x1+w/2, y1+h/2)
            elif action[0] == 'picture_press_sample':
                x1,y1,w,h = pa.locateOnScreen(r'C:\Users\roel\Desktop\Niels_prog\files_to_Inspection_Manager\Sample_add_btn.png',grayscale=True, confidence=.5)
                pa.click(x1+w*.98, y1+h*.95)
            elif action[0] == 'picture_press_create':
                x1,y1,w,h = pa.locateOnScreen(r'C:\Users\roel\Desktop\Niels_prog\files_to_Inspection_Manager\Create_btn.png',grayscale=True, confidence=.5)
                pa.click(x1+w/2, y1+h/2)
            elif action[0] == 'picture_press_import':
                x1,y1,w,h = pa.locateOnScreen(r'C:\Users\roel\Desktop\Niels_prog\files_to_Inspection_Manager\Import_btn.png',grayscale=True, confidence=.5)
                pa.click(x1+w*.25, y1+h/2)
                
            time.sleep(slider_values[i].get()/100)

    execute_actions()
    
    
    # if variable_program != None:
    #     pass
    # else:
    #     variable_program

def save_program():
    f = fd.asksaveasfile(title='Choose name to save to', mode='w', defaultextension=".prog")
    for (action,val),s,d in zip(actions, slider_values, descriptions):
        d = d.get() if d.get() != '' else 'None'
        if action == 'click':
            val = f'{val[0]}-{val[1]}'
        f.write(f'{action};{val},{s.get()},{d}\n')
    f.close()

def load_program():
    global actions, slider_values, descriptions
    f = fd.askopenfile(title='Choose program to open')
    
    actions = []
    slider_values = []
    descriptions = []

    for line in f.readlines():
        print(line)
        a,s,d = line.split(',')
        (action, val) = a.split(';')
        val = val.strip()
        if action == 'click':
            val = tuple( map(int,val.split('-')) )
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

# Create a button to click all the recorded actions
btn_frame = tk.Frame(root, background="#ffffff", height=10, width=10, borderwidth=3)

btn = tk.Button(btn_frame, text="Load program", command=load_program)
btn.grid(row=0,column=0,sticky='ew', pady=1)
btn = tk.Button(btn_frame, text="Save program", command=save_program)
btn.grid(row=0,column=1,sticky='ew', pady=1)
btn = tk.Button(btn_frame, text="Execute program", command=execute_program)
btn.grid(row=1,column=0,sticky='ew', pady=5, columnspan=2)
ttk.Separator(btn_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky='ew')
btn = tk.Button(btn_frame, text="Add button press", command=record_press)
btn.grid(row=3,column=0,sticky='ew', pady=12)
btn = tk.Button(btn_frame, text="Add typing text", command=record_type)
btn.grid(row=3,column=1,sticky='ew', pady=12)

btn_frame.grid_columnconfigure(0, weight=1)
btn_frame.grid_columnconfigure(1, weight=1)

btn_frame.pack(anchor='nw', expand=True, fill='x')

# Create a text widget to display the recorded actions
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
action_text = tk.Frame(canvas, background="#ffffff", height=10, width=10, borderwidth=3, relief='sunken')
action_text.pack(pady=20, padx=20)
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=action_text, anchor="nw")

action_text.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

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