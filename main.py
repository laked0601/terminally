from terminally import base_window
from random import randint
from packages.various_tests import myclass
from packages.name_ager import name_ager

APPLICATION_NAME = "test application"
class testClass():
    __name__ = "Secret Login"
    __icon__ = "favicon.png"
    secret_num = randint(1,200)
    function_info = {
        "method_1": {
            "NAME": "Print '214'",
            "HIDDEN": False
        },
        "get_user_name_and_password": {
            "NAME": "Login",
            "HIDDEN": False
        },
        "secret_function": {
            "NAME": "Secret Function",
            "HIDDEN": True
        }
    }
    def __init__(self):
        pass
    @staticmethod
    def method_1():
        ROOT.maintab.output("214")
    @staticmethod
    def get_user_name_and_password(name, password):
        if name == "name" and password == "password":
            ROOT.maintab.output("correct name and password")
            testClass.function_info["secret_function"]["HIDDEN"] = False
        else:
            ROOT.maintab.output("wrong name or password")
    @staticmethod
    def secret_function():
        ROOT.maintab.output(f"your secret number is {testClass.secret_num}")

ROOT = base_window(APPLICATION_NAME,[testClass()])
myclass.ROOT = ROOT
ROOT.add_class(myclass())
name_ager.ROOT = ROOT
ROOT.add_class(name_ager())
ROOT.refresh()

ROOT.mainloop()