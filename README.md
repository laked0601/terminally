# terminally
A simple gui framework using Tkinter in python. Can run with other python classes and call the functions included therein.

![image](https://user-images.githubusercontent.com/90655952/173206798-86beb5d4-6d5c-4b28-b145-f9fd17f6b62d.png)

-------- HOW TO USE -------

	1. Clone this repository to a location of your choosing.
	
	2. In a new python file, import the 'base_window' class from terminally.py
	
	3. Create a class of functions of your choosing. Terminally will use any arguments provided in the functions as input required 
	   by the user. This means that all functions must be staticmethods or the user will be required to provide the self argument 
	   (which is impossible)
	
	4. Create your base_window object and supply the application name, an iterable of the classes to be supplied to the terminal 
	   (eg a list) and (optionally) a dictionary detailing the style.
	   
	4.1 An example of the styling is this:
		
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
		
	
	5. Start the application by calling *your base_window object*.mainloop(), as it inherits from tkinter Tk
