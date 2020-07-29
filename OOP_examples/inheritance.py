# Before applying inheritance
class Dog_no_inheritance:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def convert_age(self, factor):
        human_age = self.age * factor
        return human_age


class Fish_no_inheritance:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def convert_age(self, factor):
        human_age = self.age * factor
        return human_age


dog1_no_inheritance = Dog_no_inheritance("Simba", 9)
dog1_human_age_no_inheritance = dog1_no_inheritance.convert_age(6)
print(dog1_human_age_no_inheritance)

fish1_no_inheritance = Fish_no_inheritance("Delicious", 3)
fish1_human_age_no_inheritance = fish1_no_inheritance.convert_age(4)
print(fish1_human_age_no_inheritance)


# After applying inheritance
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def convert_age(self, factor):
        human_age = self.age * factor
        return human_age


class Dog(Animal):
    def __init__(self, name, age):
        Animal.__init__(self, name, age)


class Fish(Animal):
    def __init__(self, name, age):
        Animal.__init__(self, name, age)


dog1 = Dog("Simba", 9)
dog1_human_age = dog1.convert_age(6)
print(dog1_human_age)

fish1 = Fish("Delicious", 3)
fish1_human_age = fish1.convert_age(4)
print(fish1_human_age)
