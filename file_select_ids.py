import tkinter as tk
import tkinter.font as tf
import tkinter.ttk as ttk

class file_id_selector(tk.Toplevel):
    def __init__(self, root, wait_done, file_paths):
        tk.Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.destroyer)

        self.file_paths = file_paths
        self.path_len = max(len(s) for s in self.file_paths)
        self.file_len = max(len(s.split('\\')[-1]) for s in self.file_paths)
        self.folder_len = self.path_len-self.file_len
        self.wait_done = wait_done

        self.ok_btn = tk.Button(self, text='Done', command=self.ok_btn_press)
        self.ok_btn.grid(row=0, column=0, columnspan=self.path_len-5)
        
        self.switch_dir = tk.BooleanVar(self,False)
        self.switch_dir_box = tk.Checkbutton(self, text="switch alignment", variable=self.switch_dir, command=self.change_string_index)
        self.switch_dir_box.grid(row=1, column=self.path_len-5, columnspan=5, rowspan=2)

        self.start = tk.IntVar(value=0)
        self.slider_start = tk.Scale(self, from_=self.folder_len, to=self.path_len-1, orient="horizontal", resolution=1,
                                     variable=self.start, showvalue=False)
        self.slider_start.bind("<ButtonRelease-1>", self.change_string_index)
        self.slider_start.grid(row=1, column=0, columnspan=self.file_len, sticky='WE', padx=(0,10))

        self.end = tk.IntVar(value=1)
        self.slider_end = tk.Scale(self, from_=self.folder_len, to=self.path_len-1, orient="horizontal", resolution=1, 
                                   variable=self.end, showvalue=False)
        self.slider_end.bind("<ButtonRelease-1>", self.change_string_index)
        self.slider_end.grid(row=2, column=0, columnspan=self.file_len, sticky='WE', padx=(10,0))

        self.file_labels = []
        for _ in file_paths:
            self.file_names = self.file_paths[-self.file_len:]
            file_label = []
            for _ in range(self.file_len):
                file_label.append(None) 
            self.file_labels.append(file_label)
        
        self.change_string_index()

    def destroyer(self):
        self.wait_done.set('Failed')

    def ok_btn_press(self):
        self.wait_done.set('Done')

    def change_string_index(self, event=None):
        factor = .3
        tkfont = tf.Font(font=("Courier New", 10, 'bold'))
        w, h = tkfont.measure("W")*factor, tkfont.metrics("linespace")*factor
        self.image = tk.PhotoImage(data='')

        for i,file_path in enumerate(self.file_paths):
            file_label = self.file_labels[i]
            if not self.switch_dir.get():
                file_name = file_path[self.folder_len:].ljust(self.file_len)
            else:
                file_name = file_path[self.folder_len:].rjust(self.file_len)
            file_frame = tk.Frame(self)

            iterator = list(enumerate(file_name))
            print(iterator)
            for column, t in iterator:
                if self.folder_len + column < self.start.get() or self.folder_len + column > self.end.get():
                    # outside
                    fg_col = '#00f'
                    bg_col = '#fff'
                else:
                    # inside
                    fg_col = '#f00'
                    bg_col = '#0ff'

                if len(file_label) > column and file_label[column] != None:
                    file_label[column].destroy()

                file_label[column] = tk.Label(file_frame, text=t, font=tkfont, image=self.image, width=w, height=h, compound=tk.LEFT, fg=fg_col, bg=bg_col)
                file_label[column].grid(row=0, column=column, sticky='W')
            
            file_frame.grid(row=3+i, sticky='WE',padx=(20,20))

        # identifiers = self.get_identifiers()

        # for i,identifier in enumerate(identifiers):
        #     tk.Label(file_frame, text=identifier, font=tkfont, image=self.image, width=w, height=h).grid(row=3+i, column=column, sticky='W')

        self.grid_columnconfigure([0,self.file_len],weight=2)

    def get_indeces(self):
        index_pairs = []
        for file_path in self.file_paths:
            if self.switch_dir.get():
                file_name_rjust = file_path[self.folder_len:].rjust(self.file_len)
                file_name = file_path[self.folder_len:]
                index_shift = len(file_name_rjust)-len(file_name)
            else:
                index_shift = 0
            index_pairs.append(( int(self.start.get())-index_shift , int(self.end.get())+1-index_shift ))

        return index_pairs
    
    def get_identifiers(self):
        
        index_pairs = self.get_indeces()
        identifiers = []

        for file_path,index_pair in zip(self.file_paths,index_pairs):
            i0,i1 = index_pair
            identifiers.append(file_path[i0:i1])

        return identifiers


if __name__ == '__main__':
    root = tk.Tk()
    wait_done = tk.StringVar(value='')
    file_paths = ['P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-1 PO- 24-11-2023 9 17.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-1 PO- 24-11-2023 9 25.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-2 PO- 24-11-2023 9 30.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-3 PO- 24-11-2023 9 59.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-4 PO- 24-11-2023 10 6.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-5 PO- 24-11-2023 10 11.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-7_volledig PO- 24-11-2023 10 49.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-8_volledig PO- 24-11-2023 11 42.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-9_volledig PO- 24-11-2023 13 22.csv', 'P:\\Mitutoyo\\Meetrapporten\\VDL ETG Eindhoven B.V\\92620342 PA CU C-Chuck 4022-709-4146\\IM DATA\\4022.709.41462 rev01 Nr-10_volledig PO- 24-11-2023 14 14.csv']

    fs = file_id_selector(root=root, wait_done=wait_done, file_paths=file_paths)
    root.wait_variable(wait_done)
    index_pairs = fs.get_indeces()
    fs.destroy()

    from pprint import pprint
    print('\nindex_pairs:')
    pprint(index_pairs)
    for (i0,i1),f in zip(index_pairs,file_paths):
        print(f[i0:i1])

    try:
        tk.mainloop()
    except:
        root.destroy()