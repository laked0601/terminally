from tkinter import Tk, ttk, Frame, Entry, X, Y, BOTH, LEFT, RIGHT, BOTTOM, TOP, PhotoImage, Button
class base_window(Tk):
    class toptab_class():
        def __init__(self, rootobj):
            self.rootobj = rootobj
            self.toptab = Frame(rootobj)
            self.nameframe = Frame(self.toptab, bg=rootobj.STYLES["TOP_TAB"], height=32)
            ttk.Label(self.nameframe, text=rootobj.APPLICATION_NAME, font=(rootobj.STYLES["FONT"], 18)).pack(side=LEFT, padx=(0, 16))
            Button(self.nameframe, command=lambda: self.rootobj.clear(), text="Clear Text", width=8).pack(side=LEFT)
            self.nameframe.pack(fill=X)
            self.procedures_tab = Frame(self.toptab, bg=rootobj.STYLES["TOP_TAB"], height=80)
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
            self.sidebar = Frame(self.rootobj, bg=rootobj.STYLES["SIDEBAR"], width=234)
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
            self.maintab.pack(fill=BOTH, side=LEFT, expand=True)
            self.statement_queue = []
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
                print(len(self.statement_queue), self.maintab.winfo_height())
                for obj in output_obj:
                    for widget in self.maintab.winfo_children():
                        widget.destroy()
                    while len(self.statement_queue) > self.maintab.winfo_height() // 20:
                        self.statement_queue.pop(0)
                    self.statement_queue.append(str(obj))
                    for smt in self.statement_queue:
                        lbl = ttk.Label(self.maintab,text=smt)
                        lbl.pack(fill=BOTH)
        def submit(self,funcobj):
            user_input_list = [x.get() for x in self.button_list]
            try:
                res = funcobj(*user_input_list)
                if res is not None:
                    print("true")
                    self.output(repr(res))
            except Exception as e:
                self.output(repr(e))
            self.rootobj.awaiting_user_input = False
            self.rootobj.refresh()
            self.output('')
        def cancel(self):
            self.rootobj.awaiting_user_input = False
            self.output("Cancelled")
        def input(self, argument_names, funcobj):
            self.rootobj.awaiting_user_input = True
            self.button_list = []
            for arg in argument_names:
                lbl = ttk.Label(self.maintab,text=arg)
                ent = Entry(self.maintab,width=16)
                ent.pack()
                lbl.pack()
                self.button_list.append(ent)
            Button(self.maintab, command=lambda x=funcobj: self.submit(x), text="submit",width=8).pack()
            Button(self.maintab, command=lambda :self.cancel(), text="cancel", width=8).pack()
    def __init__(self,application_name,classes=None,styles=None):
        super().__init__()
        self.APPLICATION_NAME = application_name
        if styles == None:
            self.STYLES = {"TOP_TAB": "#69db88", "APPLICATION_NAME": "#69db88", "SIDEBAR": "#a7c0fa", "FONT": "Arial"}
        else:
            self.STYLES = styles
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
        self.maintab.statement_queue = []
        self.maintab.output('')
