import os
import pandas as pd
import re
import tkinter as tk
import tkinter.filedialog as fd

class sample_importer():
    replace_dictionary = {
        'plaatsz.h.'    : 'TRUE POSITION',
        'afstand x'     : 'LINEAR',
        'afstand y'     : 'LINEAR',
        'afstand z'     : 'LINEAR',

        'afstand xy'    : 'LINEAR',
        'afstand xz'    : 'LINEAR',
        'afstand yz'    : 'LINEAR',

        'positie x'     : 'LINEAR',
        'positie y'     : 'LINEAR',
        'positie z'     : 'LINEAR',

        'formule berekening' : 'LINEAR',
        'Concentriciteit' : 'CONCENTRICITY',
        'EVENWIJDIGHEID' : 'PARALLELISM',

        'ZX-HOEK'       : 'ANGULAR',
        'XY-HOEK'       : 'ANGULAR',
        'YZ-HOEK'       : 'ANGULAR',
        
        'VLAKHEID'      : 'FLATNESS',
        'POSITIE VAN VLAK' : 'TRUE POSITION',
        
        'CILINDRICITEIT'    : 'CYLINDRICITY',
        'HOEKZUIVERHEID'    : 'ANGULARITY',
        'HAAKSHEID'         : 'PERPENDICULARITY',
        'COAXIALITEIT'      : 'CONCENTRICITY',
        
        'RADIUS'        : 'RADIAL',
        'RONDHEID'      : 'CIRCULARITY',
        'RECHTHEID'     : 'STRAIGHTNESS',

        'Profielzuiverheid Vlak' : 'SURFACE PROFILE',
        'Profielzuiverheid LIJN' : 'LINE PROFILE',

        'SYMMETRIE TOL. AS ELEMENT'     : 'SYMMETRY',
        'SYMMETRIE TOL. PUNT ELEMENT'   : 'SYMMETRY',
        'SYMMETRIE TOL. VLAK ELEMENT'   : 'SYMMETRY',

        'SLAG RADIAAL'  : 'CIRCULAR RUNOUT',
        'SLAG AXIAAL'   : 'TOTAL RUNOUT',
        
        'HOEK X' : 'ANGULAR',
        'HOEK Y' : 'ANGULAR',
        'HOEK Z' : 'ANGULAR',

        'KEGELHOEK' : 'ANGULAR',
        'Hoek Y' : 'ANGULAR',
        'POSITIE VAN AS' : 'TRUE POSITION',
        
        'afstand' : 'LINEAR',
        'POSITIE' : 'LINEAR', 
    }
    
    def __init__(self, root : tk.Tk, wait_done : tk.StringVar, files):
        
        self.root = root
        self.wait_done = wait_done
        
        self.file_paths = []
        self.folder = None

        try:
            self.get_files()
        except:
            print('Files could not be registered')

    def __del__(self):
        self.wait_done.set('Failed')

    def get_files(self):
        self.files = fd.askopenfilenames(parent=self.root, title='Choose xls-files')
        self.files = sorted(self.files)
        self.folder,self.files = ('\\'.join(self.files[0].split('/')[:-1]), [file.split('/')[-1] for file in self.files])
        self.convert_files()

    def get_folder(self):
        self.folder = fd.askdirectory(parent=self.root, title='Choose a folder with xls-files')
        self.files = sorted(self.files)
        self.files = list(filter(lambda x : x.endswith('xls'),next(os.walk(self.folder), (None, None, []))[2]))
        self.convert_files()

    def convert_files(self):
        self.file_paths.clear()

        for file in self.files:
            path = self.folder+'\\'+file

            if file.endswith('.csv'):
                self.file_paths.append(path)
                print('path added')
                continue
            
            if not file.endswith('.xls'):
                continue

            df = pd.read_excel(path, engine='xlrd')

            for key,val in self.replace_dictionary.items():
                # pattern = f',{key}[^,]*,'
                df.iloc[:,0] = df.iloc[:,0].str.replace(pat=key, repl=val, flags=re.I)

            df.to_csv(path[:-3]+'csv', index=False,  escapechar="\\", doublequote=False, sep="\t")

            self.file_paths.append(path.replace('xls','csv'))
    
        self.wait_done.set('Done')
    
    def get_file_paths(self):
        return(self.file_paths)
