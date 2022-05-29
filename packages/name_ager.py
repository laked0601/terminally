class name_ager():
    correct = False
    correct_name_age = ("name","204")
    ROOT = None
    @staticmethod
    def verify_name_age_is_name_204(name, age):
        if (name,age) == name_ager.correct_name_age:
            name_ager.ROOT.maintab.output("Age supplied was correct")
        else:
            name_ager.ROOT.maintab.output("Age supplied was wrong")
