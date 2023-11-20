import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
from idlelib.tooltip import Hovertip
import pyautogui as pa

import time
import re

from files_to_Inspection_Manager import import_window
from file_select_ids import file_id_selector
from pprint import pprint

MY_PATH = '\\'.join(__file__.split('\\')[:-1])
SIM_MODE = False

actions = [] 
# can be 
# ('click', (x,y)) or 
# ('type', 'some_string') or 
# ('press', 'some_key_combination')

slider_values = []
descriptions = []

file_paths = []
index_pairs = []
variable_paths = []
variable_program = {}

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

picture_press_dict = {
    'open' :    ((.5, .5),      'Openen_btn.png'),
    'sample' :  ((.98, .95),    'Sample_add_btn.png'),
    'create' :  ((.5, .5),      'Create_btn.png'),
    'import' :  ((.25, .5),     'Import_btn.png'),
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

def record_popup(event=None):
    popup_text = sd.askstring(title='What to display in popup?', prompt='your popup text (do not use "-")')
    actions.append(('popup',popup_text))
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

    if len(actions) == 0:
        print(header_widgets)
        for widget in header_widgets:
            widget.destroy()
    
        header_widgets.clear()

# Lists to keep track of button and label widgets
header_widgets = []
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
    for widget in header_widgets:
        widget.destroy()
    for widget in remove_button_widgets:
        widget.destroy()
    for widget in action_label_widgets:
        widget.destroy()
    for widgets in slider_widgets:
        for widget in widgets:
            widget.destroy()
    for widget in description_widgets:
        widget.destroy()

    header_widgets.clear()
    remove_button_widgets.clear()
    action_label_widgets.clear()
    slider_widgets.clear()
    description_widgets.clear()

    if len(actions) > 0:
        fnt = 'Helvetica 10 bold'
        # l0 = tk.Label(action_text, text='Remove', justify='left', font=fnt).grid(row=0, column=0, sticky='W')
        l1 = tk.Label(action_text, text='Delay 1/100[s]', justify='left', font=fnt)
        l1.grid(row=0, column=2, columnspan=2, sticky='W')
        header_widgets.append(l1)
        l2 = tk.Label(action_text, text='Action', justify='left', font=fnt)
        l2.grid(row=0, column=1, sticky='W')
        header_widgets.append(l2)
        l3 = tk.Label(action_text, text='Description', justify='left', font=fnt)
        l3.grid(row=0, column=4, sticky='W')
        header_widgets.append(l3)

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
    global variable_program

    def execute_actions(type_adapt = None, actions=actions):
        for i, action in enumerate(actions):
            if action[0].startswith('popup'):
                popup = sd.Dialog(root, title=action[1])
            elif action[0] == 'click':
                x,y = action[1]
                pa.click(x, y) if not SIM_MODE else print(f'click: {x},{y}')
            elif action[0] == 'type':
                if type_adapt != None:
                    new_action = action[1]
                    for adaption in type_adapt: #adaption = ('old_substring', 'new_substring')
                        old_s,new_s = adaption
                        new_action = new_action.replace(old_s,new_s)
                    pa.write(new_action) if not SIM_MODE else print('type: ',new_action)
                else:
                    pa.write(action[1]) if not SIM_MODE else print('type: ',action[1])
            elif action[0] == 'press':
                pa.press(human_readable_to_pyautogui[action[1]]) if not SIM_MODE else print('press: ',action[1])
            elif action[0].startswith('picture_press'):
                picture = action[0].split('-')[1]
                picture_file = picture_press_dict[picture][1]
                px, py = picture_press_dict[picture][0]
                try:
                    x1,y1,w,h = pa.locateOnScreen(MY_PATH + '\\' + picture_press_dict[picture][1],grayscale=True, confidence=.5)
                    pa.click(x1+px*w, y1+py*h) if not SIM_MODE else print(action[0])
                except:
                    print(f'Could not find picture: {picture_file}, should be in same directory as this executable')
                
            time.sleep(slider_values[i].get()/100)

    if variable_program == {}:
        execute_actions()
    else:
        for variable in variable_program.items():
            for value in variable[1]:
                execute_actions(type_adapt=[
                    ('<variable_path>',variable_paths[0]),
                    (variable[0],str(value)),
                    ('/','\\')
                    ])

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
    f = open(MY_PATH + r'\inspect_manager_load_samples.prog')
    
    actions = []
    slider_values = []
    descriptions = []

    for line in f.readlines():
        if line == '':
            continue
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

def load_files():
    global file_paths
    file_paths = []

    wait_done = tk.StringVar(value='Opening files')
    iw = import_window(root, wait_done, file_paths)
    file_paths = iw.get_file_paths()
    root.wait_variable(wait_done)
    iw.destroy()

    if wait_done.get() == 'Done':
        load_program()
    else:
        sd.Dialog(root,'Did not open files')

def set_file_ids():
    global file_paths, index_pairs

    wait_done = tk.StringVar(value='Opening files')
    fs = file_id_selector(root,wait_done,file_paths)
    root.wait_variable(wait_done)
    index_pairs = fs.get_indeces()
    fs.destroy()

    make_variable_program()
    execute_btn.config({'text' : f"Execute program ({len(index_pairs)})"})
    Hovertip(execute_btn, f'{variable_paths[0]} : {list(variable_program.items())[0]}')

def make_variable_program():
    global file_paths, variable_paths, variable_program

    variable_program['<i>'] = []
    for path, inds in zip(file_paths,index_pairs):
        parameter = path[inds[0]:inds[1]]
        variable_path = path[:inds[0]] + '<i>' + path[inds[1]:]
        variable_paths.append(variable_path)
        variable_program['<i>'].append(parameter)

# Create the main window
root = tk.Tk()
root.title("Mouse actions Recorder")

# Create a button to click all the recorded actions
btn_frame = tk.Frame(root, background="#ffffff", height=10, width=10)

row=0
btn = tk.Button(btn_frame, text="Load excel files", command=load_files)
btn.grid(row=row,column=0,sticky='ew', pady=1)
btn = tk.Button(btn_frame, text="Set sample references", command=set_file_ids)
btn.grid(row=row,column=1,sticky='ew', pady=1)
row=1
execute_btn = tk.Button(btn_frame, text="Execute program", command=execute_program)
execute_btn.grid(row=row,column=0,sticky='ew', pady=5, columnspan=2)
row=2
ttk.Separator(btn_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky='ew')
action_btn_frame = tk.Frame(btn_frame, background="#ffffff", height=10, width=10)
if True:
    row=0
    column=0
    btn = tk.Button(action_btn_frame, text="Add button press", command=record_press)
    btn.grid(row=row,column=column,sticky='ew')
    column=1
    btn = tk.Button(action_btn_frame, text="Add typing text", command=record_type)
    btn.grid(row=row,column=column,sticky='ew')
    column=2
    btn = tk.Button(action_btn_frame, text="Add popup window", command=record_popup)
    btn.grid(row=row,column=column,sticky='ew')

row=3
action_btn_frame.grid_columnconfigure([0,1,2], weight=1)
action_btn_frame.grid(row=row,column=0,sticky='ew', pady=12, columnspan=2)

btn_frame.grid_columnconfigure([0,1], weight=1)
btn_frame.pack(anchor='nw', expand=True, fill='x')

# Create a text widget to display the recorded actions
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
action_text = tk.Frame(canvas, background="#ffffff", height=10, width=10)
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

from pprint import pprint
pprint(actions)