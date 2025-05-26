# class FloatValidator:
#     def __init__(self, max_value, min_value):
#         self.min_value = min_value
#         self.max_value = max_value
#
# fv = FloatValidator(3,1)
#
#
# fv(3)


def one(name, sound):
    class Animal:
        def __init__(self, name):
            self.name = name

        def say(self):
            print(f'SAY {sound}')
        # def __str__(self):
        #     return Animal.__name__
    Animal.__name__ = name.capitalize()

    return Animal


Dog = one('Dog', 'Gav')
shar = Dog('Sharic')
shar.say()