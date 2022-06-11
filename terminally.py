from tkinter import Tk, Frame, Label, Entry, X, Y, BOTH, LEFT, RIGHT, BOTTOM, TOP, END, PhotoImage, Button, Listbox, Scrollbar
from os import path

class base_window(Tk):
    class toptab_class():
        def __init__(self, rootobj):
            self.rootobj = rootobj
            self.toptab = Frame(rootobj)
            self.nameframe = Frame(self.toptab, bg=rootobj.STYLES["toptab"]["color"], height=32)
            Label(self.nameframe, bg=rootobj.STYLES["toptab"]["color"], fg=rootobj.STYLES["title"]["color"],text=rootobj.APPLICATION_NAME, font=(rootobj.STYLES["title"]["font"], rootobj.STYLES["title"]["size"])).pack(side=LEFT, padx=(0, 16))
            Button(self.nameframe, command=lambda: self.rootobj.clear(), text="Clear Text", width=8).pack(side=LEFT)
            self.nameframe.pack(fill=X)
            self.procedures_tab = Frame(self.toptab, bg=rootobj.STYLES["toptab"]["color"], height=80)
            self.procedures_tab.pack(fill=X)
            self.toptab.pack(fill=BOTH)
            for classname, classobj in rootobj.CLASSES.items():
                self.add_procedure(classname, classobj)
        def add_procedure(self, classname, classobj):
            if "__icon__" in dir(classobj):
                if len(classobj.__icon__) > 4 and classobj.__icon__[-4:] == ".png":
                    icon_path = classobj.__icon__
                else:
                    print(f"WARNING: icon path was specified in class '{classname}' but was not a '.png' image. Terminally can only support this image type.")
                    icon_path = "no_image.png"
            else:
                icon_path = "no_image.png"
            proc = Frame(self.procedures_tab, width=64, height=64)
            proc.pack(side=LEFT, pady=12, padx=12)
            self.rootobj.images.append(PhotoImage(file=icon_path))
            Button(proc, command=lambda: self.rootobj.load_class(classname),
                   text=classname, image=self.rootobj.images[-1], compound=BOTTOM,
                   width=96, height=64).pack(side=TOP, fill=BOTH)
        def refresh(self):
            for widget in self.procedures_tab.winfo_children():
                widget.destroy()
            self.rootobj.images = []
            for classname, classobj in self.rootobj.CLASSES.items():
                self.add_procedure(classname, classobj)
    class sidebar_class():
        def __init__(self,rootobj):
            self.rootobj = rootobj
            self.sidebar = Frame(self.rootobj, bg=rootobj.STYLES["sidebar"]["color"], width=234)
            self.sidebar.pack(fill=BOTH, side=LEFT, expand=False)
        def add_methods(self,classobj):
            i = 0
            self.rootobj.functions = []
            for widget in self.sidebar.winfo_children():
                widget.destroy()
            if "function_info" in dir(classobj):
                function_info = classobj.function_info
            else:
                function_info = {}
            for func_name in dir(classobj):
                if (len(func_name) > 4 and func_name[0:2] + func_name[-2:] == "____") or (not callable(getattr(classobj, func_name))): # ignore magic methods and non functions
                    continue
                output_name = func_name
                if func_name in function_info:
                    if "HIDDEN" in function_info[func_name]:
                        if function_info[func_name]["HIDDEN"] == True:
                            continue
                    if "NAME" in function_info[func_name]:
                        output_name = function_info[func_name]["NAME"]
                self.rootobj.functions.append(getattr(classobj, func_name))
                func = Frame(self.sidebar,height=16)
                func.pack()
                Button(func,command=lambda i=i: self.rootobj.exec_function(i),text=output_name,width=32).pack(side=LEFT,fill=BOTH)
                i += 1
    class maintab_class():
        def __init__(self,rootobj):
            self.rootobj = rootobj
            self.maintab = Frame(self.rootobj, width=608)
            self.scrollbar = Scrollbar(self.maintab)
            self.scrollbar.pack(side=RIGHT,fill=Y)
            self.statement_queue = Listbox(self.maintab, bg=rootobj.STYLES["maintab"]["color"], yscrollcommand=self.scrollbar.set)
            self.statement_queue.pack(side=LEFT, fill=BOTH, expand=True)
            self.scrollbar.config(command=self.statement_queue.yview())
            self.maintab.pack(fill=BOTH, side=LEFT, expand=True)
        def run_function(self,funcobj):
            if self.rootobj.awaiting_user_input:
                return
            arg_names = funcobj.__code__.co_varnames[:funcobj.__code__.co_argcount]
            if funcobj.__code__.co_argcount == 0:
                funcobj()
            else:
                self.input(arg_names, funcobj)
                self.rootobj.awaiting_user_input = True
        def output(self,*output_obj):
            if len(output_obj) != 0:
                for i in output_obj:
                    self.statement_queue.insert(END, i)
                qsize = self.statement_queue.size()
                if qsize > 500:
                    self.statement_queue.delete(0,qsize-501)
                self.statement_queue.yview(END)
        def submit(self,funcobj):
            user_input_list = [x.get() for x in self.button_list]
            try:
                res = funcobj(*user_input_list)
                if res is not None:
                    self.output(repr(res))
            except Exception as e:
                self.output(repr(e))
            self.rootobj.awaiting_user_input = False
            self.input_frame.destroy()
        def cancel(self):
            self.rootobj.awaiting_user_input = False
            self.input_frame.destroy()
        def input(self, argument_names, funcobj):
            self.rootobj.awaiting_user_input = True
            self.input_frame = Frame(self.maintab, width=96)
            self.button_list = []
            for arg in argument_names:
                Label(self.input_frame,text=arg).pack()
                ent = Entry(self.input_frame,width=32)
                ent.pack()
                self.button_list.append(ent)
            Button(self.input_frame, command=lambda x=funcobj: self.submit(x), text="submit",width=8).pack()
            Button(self.input_frame, command=lambda :self.cancel(), text="cancel", width=8).pack()
            self.input_frame.pack()
    def validate_styles(self,styles):
        if not isinstance(styles,dict):
            raise TypeError(f"Styles was passed to terminally as {type(styles)} not dict")
        generic_template = {
                "toptab": {
                    "color": "#69db88"
                },
                "sidebar": {
                    "color": "#a7c0fa",
                },
                "maintab": {
                    "color": "#ffffff"
                },
                "title": {
                    "font": "Arial",
                    "size": 22,
                    "color": "black",
                }
            }
        if styles == {}:
            self.STYLES = generic_template
            return
        for key in generic_template.keys():
            if key not in styles:
                styles[key] = generic_template[key]
            else:
                for attr in generic_template[key]:
                    if attr not in styles[key]:
                        styles[key][attr] = generic_template[key][attr]
        self.STYLES = generic_template
    def __init__(self,application_name,classes=None,styles={}):
        if not path.exists("no_image.png"):
            with open("no_image.png",'wb') as f:
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x01oIDATXG\xed\x94OK\xc30\x18\xc6{m\xa1\x94~;\xbd\x88\x1e\xbd\x88\x1el\x15=\xb8\xb3\xe0\x17\x10\xbc\x08\x8a\xe2\xc1a\xe7\x14\xc1\xaf\xe0\xd9\x8b\x8a0\xd4`Y\xed\xd0\xd9&\xedk\x93\xb5\x9b\x9da\xfdc\xea\x0e\xf6\x81\x07\x9a\xe4}\xf3\xfc\x12B%\x98\xb2j\x80\x1a\xa0\x06\x98\x08 \xcb2H\x92\x94\xcb\x8a\xa2\xc4]\xc54\x11\x80n\xbcp\x020s\x98m\nP\x06"\x13\x80\x17\x96x\xbd\x9d\x1e\xab\xaa\xca\\D\xb9\x01\xcc\xf3\x10\x1e_\tx\x18\xc0\x8f|\xf7\x8cS\xe1\x895Mc}y\x95\x1b\xe0\xa9K\x00\x93x!\x12\t\x00\x1e\xd0\x08b\xf6\x80\xc0\xe2~\x87}\xd3\xbe\xbc\x10\x99\x00k-\x0c\xceG\x08A\x18O~S\xc7\xf6Y\xa0aa0\xadO\x98;\n`\xfe8(\x04\x91\x03\x80\x0cOY\xc4\x1bm"\x06\x80nfX\x83S\x15\xb1q\xe6\x8b\x03(c\xb3\x15L\xef\x06\x8c(\x1c\xb9a57\xb0\xdc\xec\xc3\xd6\xc5j\xcaK\xa7n\xaaf\xf3r\xf0b\x85\x02\xac4=\x16\xd6\xb8j\xfc\x00\xa0\xde\xb9\xdeeu\xc8\xf1Y/\xc1\x82\xdf\x00/\x94\xe7D\xb4G\x18\x00/h\xdc\xf7\xce-\xeb\xc1\xc1\xe8\xe7$\x04\x80\x176n\xbb\x8fX}\xcfw\x86s\x7f\x06\xe0z]Vk\xbf#\xd8\xbb\xd9N\xadU\x0e\xd0\xf3\xdeX\x1dzA\xdc\xf5_\x03\xe8\xba\xce6)k\xda\x9f\xa5l\xc4\x8aU\x03\xd4\x00\xff\x1d\x00\xe0\x0b\xa6\xb0[\xed\x08w\x08\xaf\x00\x00\x00\x00IEND\xaeB`\x82')
        super().__init__()
        self.title(application_name)
        self.APPLICATION_NAME = application_name
        self.validate_styles(styles)
        self.minsize(800, 500)
        self.images = []
        self.awaiting_user_input = False
        self.user_input_arguments = []
        self.functions = []
        self.CLASSES = {}
        self.CURRENT_CLASS = None
        if classes is not None:
            for classobj in classes:
                self.add_class(classobj)
        self.toptab = self.toptab_class(self)
        self.sidebar = self.sidebar_class(self)
        self.maintab = self.maintab_class(self)
    def add_class(self, classobj):
        if "__name__" in dir(classobj):
            nm = classobj.__name__
        else:
            nm = type(classobj).__name__
        if nm not in self.CLASSES:
            self.CLASSES[nm] = classobj
        else:
            print(f"WARNING: Class with name '{nm}' was ignored as this name was already present in loaded classes")
    def load_class(self,classname):
        if classname not in self.CLASSES:
            raise LookupError(f"Classname '{classname}' was not found in compiled classes")
        if self.awaiting_user_input:
            return
        self.CURRENT_CLASS = self.CLASSES[classname]
        self.sidebar.add_methods(self.CLASSES[classname])
    def exec_function(self,i):
        self.maintab.run_function(self.functions[i])
    def refresh(self):
        if self.awaiting_user_input:
            return
        self.toptab.refresh()
        self.sidebar.add_methods(self.CURRENT_CLASS)
    def clear(self):
        if self.awaiting_user_input:
            return
        self.maintab.statement_queue.delete(0,self.maintab.statement_queue.size())
