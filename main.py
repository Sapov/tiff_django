class A:
    def __init__(self, cd_dict: dict):
        # self.quantity = kwargs['quantity']
        self.material = cd_dict['material']
        # self.length = args['length']
        # print(args)
        print(self.material)


cd = {'quantity': 1.0, 'material': '<Material: Баннер 440 грамм ламинированный Широкоформатная печать>',
      'finishka': '<FinishWork: оставить белые поля по 5 см>', 'length': 0.4, 'width': 2.0}
cd['test'] = 'test'

ass = A(cd)
# print(dir(ass))
# print(ass.__dict__)
