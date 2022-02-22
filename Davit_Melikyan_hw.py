g# 1. Create a custom integer class. The class should have one instance attribute as
# its value. Now, your class must
# satisfy the following criteria:
#    a) we can use Python arithmetic operators to add, subtract, multiply and
#    divide the values.
#    b) create another class called Inf. For the sake of consistency, this
#    class may inherit from int class.
#    c) if we divide by zero, we don't get an exception. Instead, we get inf,
#    which was implemented in our previous step
#    d) when we print our class, we want it to be represented as nicely as possible.
#    As our class represents an integer
#    number, we want to see the value when we print it or cast it to a string.
#    e) as with every number, we want to be able to compare our integer instances
#    using the logical operators.
#    Implement those as well.
#    f) finally, there is one thing that all Python objects have in common.
#    If we neglect 0, '', None, False etc., then
#    every object holds a value of True when casted to bool. We want our Integer
#    to behave as a normal integer in this
#    sense. When we cast an Integer to bool, we must get False, if the value
#    of our object is 0. True otherwise.

class Int:
    def __init__(self, value):
        if type(value) == int:
            self.value = value
        else:
            raise TypeError

    def __str__(self):
        return str(self.value)

    def __truediv__(self, other):
        if isinstance(other, Int) and other.value != 0:
            return self.value / other.value
        else:
            return Inf

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value <= other.value

    def __bool__(self):
        if self.value != 0:
            return True
        else:
            return False

class Inf(Int):
    def __init__(self, value):
        super().__init__(value)


a = Int(6)
b = Int(0)
print(a)
print(a / b)
# print(a < b)
# print(a > b)
print(bool(a))
print(bool(b))
print('_____________________')


# 2. Create a Color class. This will hold 3 instance variables, red, green, blue (RGB).
#Each parameter (red, green, and blue) defines the intensity of the color as an integer between 0 and 255. We want to be able to get new
# colors if we add instances of the color class. I'm not sure how much sense it will make to also subtract the colors,
# but lets do it for fun! In summary, we can add 2 or more colors and get a new color object with added RGB values
# (don't forget about the boundaries!), subtract them to get a new color object with subtracted values. When printed,
# we want to have a nice representation of our color (maybe even the color itself?). One more fun thing! As colors
# are quite often represented in hexadecimals, lets override the corresponding function such that when hex() is called
# on our class, we get the hex color code for our color.

#VERSION 1
print('#VERSION 1')
from colorit import *

class Color:
    def __init__(self, red, green, blue):
        if red in range(256) and green in range(256) and blue in range(256):
            self.red = red
            self.green = green
            self.blue = blue
        else:
            raise TypeError

    def __str__(self):
        return f'Red is: {self.red}, Green is: {self.green}, Blue is: {self.blue}'

    def myhex(self):
        return f'Red: {hex(self.red)}, Green: {hex(self.green)}, Blue: {hex(self.blue)}'

    def showcolor(self):
        return color_front('This is my color', self.red, self.green, self.blue)

mycolor = Color(0, 255, 0)
chr = 255
chg = -255
chb = 0
newcolor = Color(mycolor.red + chr, mycolor.green + chg, mycolor.blue + chb)

print('Old color -', mycolor)
print('New color -', newcolor)
print(newcolor.myhex())
showmycolor = mycolor.showcolor()
shownewcolor = newcolor.showcolor()
print('Old color -', showmycolor)
print('New color -', shownewcolor)
print('_______________________')

#VERSION 2
print('#VERSION 2')
from colorit import *

class Color:
    def __init__(self, red, green, blue):
        if red in range(256) and green in range(256) and blue in range(256):
            self.red = red
            self.green = green
            self.blue = blue
        else:
            raise TypeError

    def __add__(self, other):
        if isinstance(other, Color) and self.red + other.red <= 255:
            cr = self.red + other.red
        else:
            cr = 255

        if isinstance(other, Color) and self.green + other.green <= 255:
           cg = self.green + other.green
        else:
            cg = 255

        if isinstance(other, Color) and self.blue + other.blue <= 255:
            cb = self.blue + other.blue
        else:
            cb = 255

        return Color(cr, cg, cb)

    def __sub__(self, other):
        if isinstance(other, Color) and self.red - other.red < 0:
            cr = self.red - other.red
        else:
            cr = 0

        if isinstance(other, Color) and self.green - other.green < 0:
           cg = self.green - other.green
        else:
            cg = 0

        if isinstance(other, Color) and self.blue - other.blue < 0:
            cb = self.blue - other.blue
        else:
            cb = 0

        return Color(cr, cg, cb)

    def __str__(self):
        return f'Red is: {self.red}, Green is: {self.green}, Blue is: {self.blue}'

    def myhex(self):
        return f'Red: {hex(self.red)}, Green: {hex(self.green)}, Blue: {hex(self.blue)}'

    def showcolor(self):
        return color_front('This is my color', self.red, self.green, self.blue)

mycolor = Color(50, 100, 178)
changecolor = Color(100, 50, 30)
newcolor = mycolor + changecolor

print('Old color -', mycolor)
print('New color -', newcolor)
print(newcolor.myhex())
showmycolor = mycolor.showcolor()
shownewcolor = newcolor.showcolor()
print('Old color -', showmycolor)
print('New color -', shownewcolor)