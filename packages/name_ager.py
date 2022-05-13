class name_ager():
    correct = False
    correct_name_age = ("Name","69")
    @staticmethod
    def verify(name, age):
        print(name,type(name),age,type(age))
        print(name_ager.correct_name_age)
        if (name,age) == name_ager.correct_name_age:
            print("Age supplied was correct")
        else:
            print("Age supplied was wrong")
