import tkinter as tk
import tkinter.font as tf
import tkinter.ttk as ttk

class file_id_selector(tk.Toplevel):
    def __init__(self, root, wait_done, file_paths):
        tk.Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.destroyer)

        self.file_paths = file_paths
        self.path_len = len(self.file_paths[0])
        self.file_len = len(self.file_paths[0].split('\\')[-1])
        self.folder_len = self.path_len-self.file_len
        self.wait_done = wait_done

        self.start = tk.IntVar(value=0)
        self.slider_start = tk.Scale(self, from_=self.folder_len, to=self.path_len-1, orient="horizontal", resolution=1,
                                     variable=self.start, showvalue=False)
        self.slider_start.bind("<ButtonRelease-1>", self.change_string_index)
        self.slider_start.grid(row=1, column=0, columnspan=self.path_len, sticky='WE', padx=(0,10))

        self.end = tk.IntVar(value=1)
        self.slider_end = tk.Scale(self, from_=self.folder_len, to=self.path_len-1, orient="horizontal", resolution=1, 
                                   variable=self.end, showvalue=False)
        self.slider_end.bind("<ButtonRelease-1>", self.change_string_index)
        self.slider_end.grid(row=2, column=0, columnspan=self.path_len, sticky='WE', padx=(10,0))
        
        self.file_labels = []
        for _ in file_paths:
            file_label = []
            for _ in range(self.path_len):
                file_label.append(None) 
            self.file_labels.append(file_label)
        
        self.change_string_index()
        
        self.ok_btn = tk.Button(self, text='Done', command=self.ok_btn_press)
        self.ok_btn.grid(row=0, column=0, columnspan=self.path_len)

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
            file_name = file_path[self.folder_len:]
            file_frame = tk.Frame(self)

            for column, t in enumerate(file_name):
                if self.folder_len + column < self.start.get() or self.folder_len + column > self.end.get():
                    # outside
                    fg_col = '#00f'
                    bg_col = '#fff'
                else:
                    # inside
                    fg_col = '#f00'
                    bg_col = '#0ff'

                if file_label[column] != None:
                    file_label[column].destroy()

                file_label[column] = tk.Label(file_frame, text=t, font=tkfont, image=self.image, width=w, height=h, compound=tk.LEFT, fg=fg_col, bg=bg_col)
                # if column == 0:
                #     file_label[column].grid(row=0, column=column, sticky='W', padx=(20,0))
                # elif column == self.file_len:
                #     file_label[column].grid(row=0, column=column, sticky='W', padx=(0,40))
                # else:
                file_label[column].grid(row=0, column=column, sticky='W')
            
            file_frame.grid(row=3+i, sticky='WE',padx=(20,20))

        self.grid_columnconfigure([0,self.file_len],weight=2)

    def get_indeces(self):
        index_pairs = []
        for _ in self.file_paths:
            index_pairs.append(( int(self.start.get()) , int(self.end.get())+1 ))

        return index_pairs


if __name__ == '__main__':
    root = tk.Tk()
    wait_done = tk.StringVar(value='')
    file_paths = [
        r'P:\Mitutoyo\Meetrapporten\Frencken Mechatronics\90050163 Pre Mounted Lateral Carriage 00437-00-144\2023\IM DATA\00437-00-143     volgnr-SAM 23-45-437-03444.csv',
        r'P:\Mitutoyo\Meetrapporten\Frencken Mechatronics\90050163 Pre Mounted Lateral Carriage 00437-00-144\2023\IM DATA\00437-00-143     volgnr-SAM 23-45-437-03443.csv',
    ]

    fs = file_id_selector(root=root, wait_done=wait_done, file_paths=file_paths)
    root.wait_variable(wait_done)
    index_pairs = fs.get_indeces()
    fs.destroy()

    from pprint import pprint
    print('\nindex_pairs:')
    pprint(index_pairs)
    for (i0,i1),f in zip(index_pairs,file_paths):
        print(f[i0:i1])

    tk.mainloop()