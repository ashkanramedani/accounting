from random import choice as r_ch

from faker import Faker


class Person:
    def __init__(self):
        self.unique_names = []
        self.fake = Faker()

    def iterate(self):
        return f'{self.fake.first_name()}-{self.fake.last_name()}'

    def generate_name(self, unique: bool = True):
        if not unique and self.unique_names:
            return r_ch(self.unique_names).split('-')
        tmp = self.iterate()
        while tmp in self.unique_names:
            tmp = self.iterate()
        self.unique_names.append(tmp)
        return tmp.split('-')


person = Person()
