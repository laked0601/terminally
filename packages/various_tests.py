from webbrowser import open_new
class myclass():
    ROOT = None
    @staticmethod
    def output_hello_world():
        myclass.ROOT.maintab.output("hello world")
    @staticmethod
    def newline_test():
        myclass.ROOT.maintab.output("this is a test to see if\nnewlines\nwork")
    @staticmethod
    def multiply_two_integers(number_1, number_2):
        if number_1.isnumeric() and number_2.isnumeric():
            myclass.ROOT.maintab.output(int(number_1) * int(number_2))
    @staticmethod
    def test_of_number_conversion_to_string():
        myclass.ROOT.maintab.output("Integer then float:")
        myclass.ROOT.maintab.output(247)
        myclass.ROOT.maintab.output(247.345)
    @staticmethod
    def rick_roll():
        open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
