from tkinter import Tk, ttk, Frame, Entry, X, Y, BOTH, LEFT, RIGHT, BOTTOM, TOP, PhotoImage, Button
from types import FunctionType

CLASSES = {}
# {COMPILE FROM HERE}
# CLASSES = {'compiled_class_name':classobj, 'other_compiled_class_name':classobj, ...)
APPLICATION_NAME = "{Your Application Name}"
PROCEDURES=[
    {"name":"test.py",
    "icon":"favicon.png",
    "proc":"myclass",
     },
    {"name": "name_ager.py",
     "proc":"name_ager"
     },
    {"name": "hello"}
]

class base_window(Tk):
    class toptab_class():
        def __init__(self, rootobj, application_name, procedures=[]):
            self.rootobj = rootobj
            self.toptab = Frame(rootobj)
            self.nameframe = Frame(self.toptab, bg="#90fcad", height=32)
            tt_name = ttk.Label(self.nameframe, text=application_name, font=("Arial", 18))
            tt_name.place(x=0, y=0)
            self.nameframe.pack(fill=X)
            self.procedures_tab = Frame(self.toptab, bg="#69db88", height=80)
            self.procedures_tab.pack(fill=X)
            self.toptab.pack(fill=BOTH)
            for proc in procedures:
                self.add_procedure(proc)
        def add_procedure(self, proc_dict):
            if "name" not in proc_dict or "proc" not in proc_dict:
                return
            proc = Frame(self.procedures_tab, width=64, height=64)
            proc.pack(side=LEFT, pady=12, padx=12)
            if "icon" not in proc_dict:
                self.rootobj.images.append(PhotoImage(file="no_image.png"))
            else:
                self.rootobj.images.append(PhotoImage(file=proc_dict["icon"]))
            Button(proc, command=lambda: self.rootobj.load_class(proc_dict["proc"]),
                   text=proc_dict["name"], image=self.rootobj.images[-1], compound=BOTTOM,
                   width=64, height=64).pack(side=TOP, fill=BOTH)
    class sidebar_class():
        def __init__(self,rootobj):
            self.rootobj = rootobj
            self.sidebar = Frame(self.rootobj, bg="#a7c0fa", width=234)
            self.sidebar.pack(fill=BOTH, side=LEFT, expand=False)
        def add_methods(self,classobj):
            i = 0
            self.rootobj.functions = []
            for widget in self.sidebar.winfo_children():
                widget.destroy()
            for func_name in dir(classobj):
                # print(type(getattr(classobj, func_name)))
                if (len(func_name) > 4 and func_name[0:2] + func_name[-2:] == "____") or (not callable(getattr(classobj, func_name))): # ignore magic methods and non functions
                    continue
                self.rootobj.functions.append(getattr(classobj, func_name))
                func = Frame(self.sidebar,height=16)
                func.pack()
                Button(func,command=lambda i=i: self.rootobj.exec_function(i),text=func_name,width=32).pack(side=LEFT,fill=BOTH)
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
            if funcobj.__code__.co_argcount == 0:
                funcobj()
            else:
                self.input(funcobj.__code__.co_varnames,funcobj)
                self.rootobj.awaiting_user_input = True
        def output(self,*output_obj):
            if len(output_obj) != 0:
                for obj in output_obj:
                    for widget in self.maintab.winfo_children():
                        widget.destroy()
                    print(len(self.statement_queue),self.maintab.winfo_height())
                    while len(self.statement_queue) > self.maintab.winfo_height() // 20:
                        self.statement_queue.pop(0)
                    self.statement_queue.append(repr(obj))
                    for smt in self.statement_queue:
                        lbl = ttk.Label(self.maintab,text=smt)
                        lbl.pack(fill=BOTH)
        def submit(self,funcobj):
            input_list = [x.get() for x in self.button_list]
            try:
                res = funcobj(*input_list)
                if res is not None:
                    self.output(repr(res))
            except Exception as e:
                self.output(repr(e))
            self.rootobj.awaiting_user_input = False
        def cancel(self):
            self.rootobj.awaiting_user_input = False
            self.output("Cancel")
        def input(self,argument_names,funcobj):
            self.rootobj.awaiting_user_input = True
            self.button_list = []
            for arg in argument_names:
                lbl = ttk.Label(self.maintab,text=arg)
                ent = Entry(self.maintab,width=16)
                ent.pack()
                lbl.pack()
                self.button_list.append(ent)
            Button(self.maintab,command=lambda x=funcobj: self.submit(x), text="submit",width=8).pack()
            Button(self.maintab, command=lambda :self.cancel(), text="cancel", width=8).pack()
    def __init__(self,application_name,procedures,classes={}):
        super().__init__()
        self.title(APPLICATION_NAME)
        self.minsize(800, 500)
        self.images = []
        self.awaiting_user_input=False
        self.functions = []
        self.classes = classes # {classname as str: classobj}
        self.toptab = self.toptab_class(self,application_name,procedures)
        self.sidebar = self.sidebar_class(self)
        self.maintab = self.maintab_class(self)
    def load_class(self,classname):
        if classname not in self.classes:
            raise LookupError(f"Classname '{classname}' was not found in compiled classes")
        self.sidebar.add_methods(self.classes[classname])
    def exec_function(self,i):
        self.maintab.run_function(self.functions[i])
ROOT = base_window(APPLICATION_NAME,PROCEDURES,CLASSES)
ROOT.mainloop()