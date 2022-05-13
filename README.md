# terminally
A simple gui framework using Tkinter in python. Can be compiled with other python classes and call the functions included therein.

-------- HOW TO USE -------

1. The default way of using terminally is by creating a class of static methods to be called by the terminal once in operation.
"terminally_compiler.py" will read through the python files stored (by default) under "./packages" that you configure and load the contents of the class chosen, and any required external modules for the file, as a string. For example:

![image](https://user-images.githubusercontent.com/90655952/168394304-92af4346-09d4-4c6e-989a-2ef1b682cdf5.png)

![image](https://user-images.githubusercontent.com/90655952/168394592-c76bfc2b-0bca-4ceb-a26a-e64d0558a59d.png)

^ "test.py" will load "from webbrowser import open_new" and the contents of myclass

2. Once loaded, "terminally_compiler.py" will paste the full copy of the loaded files into a copy of "terminally.py" (called "terminally_compiled.py") at the line the exact string "# {COMPILE FROM HERE}" is included:

![image](https://user-images.githubusercontent.com/90655952/168394822-2e84aaaa-358c-4eb5-85b9-073179fadcfc.png)

![image](https://user-images.githubusercontent.com/90655952/168394881-28711bc4-c41f-4087-bb1d-76cf5939f28d.png)

^ and boom, just like that the compiled terminal is ready to go.

For configuration, you also need to update "PROCEDURES" in the base file which is a list of dictionaries that includes the name, icon file path, and class to be used for a procedure in the terminal. And changing "APPLICATION_NAME" will update it to whatever you want the terminal to be called.

The end result of the terminal looks like this:

![image](https://user-images.githubusercontent.com/90655952/168395368-6eb9e01c-c5c6-4df0-bd9f-f32fb9d7e9fa.png)

I hope you find it useful ;)
