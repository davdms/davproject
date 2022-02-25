# 1. Create an Atom class. We will have predefined atoms for it, which are C - carbon, N - nitrogen, H - hydrogen,
# O - oxygen and P - phosphorus.
#     a) Now, the class has an instance variable called "name".
#     b) If you create an object with a name other than the 5 atoms mentioned, you should get an exception. But not any
#     kind of exception. This exception will be something that we have defined. So, define an exception class called
#     UnknownAtom. This must give us a detailed explanation why it is raised.
#     c) Define a new class called Molecule. The molecule has an instance variable, which is a list.
#     d) implement the __add__ method for our Atom class. Adding two atoms will return, you've guessed it, a Molecule!
#     e) We can also add an atom to a molecule. So implement that functionality as well!
#     f) Finally, do some cosmetic stuff, like implement the __str__ method for both of our classes.
# If you're into chemistry, feel free to add some logic like keeping charges of each atom, tracking valency and raising
# an error if two atoms can't make a molecule.

# Ստեղծել Atom կլաս։ Կլասի մեջ պետք է ունենանք 5 սահմանված ատոմ՝ C ածխածին, N ազոտ, H ջրածին, O թթվածին և P ֆոսֆոր։
#     a) Կլասը պետք է ունենա "name" կոչվող instance attribute
#     b) Եթե փորձենք ատոմ ստեղծել, որը չկա մեր ցուցակի մեջ, պետք է ստանանք exception։ Ստեղծել UnknownAtom կոչվող
#     exception, որը կստանանք, եթե վերը նշված դեպքը լինի։
#     c) Ստեղծել Molecule կլաս։ Մոլեկուլն ունի մեկ instance attribute, որը list է։
#     d) Սահմանելով գումարման օպերատորը, այնպես անել, որ երկու ատոմ իրար գումարելիս ստանանք մոլեկուլ:
#     e) Մոլեկուլին նույնպես պետք է կարողանանք ատոմ գումարել։ Դա նույնպես սահմանել։
#     f) Վերջապես, սահմանել __str__, __repr__ այս ֆունկցիաներից մեկը մեր բոլոր կլասերի համար, որպեսզի որպես սթրինգ
#     ներկայացումը գեղեցկանա
# Լրացուցիչ, եթե քիմիայի սիրահար եք, կարող եք ատոմներին ավելացնել լիցքեր, սահմանել վալենտականությունը և դրանց հիման վրա
# փոփոխել գումարման տրամաբանությունը։

class Atom:
    def __init__(self, name):
        if type(name) is str:
            self.name = name
        else:
            raise NameError

    @property
    def name(self):
        return self.__atomname

    @name.setter
    def name(self, name):
        self.__atomname = self.checkatom(name)

    @staticmethod
    def checkatom(v):
        if v not in {'C', 'N', 'H', 'O', 'P'}:
            raise TypeError('It can not be an atom')
        return v

    @staticmethod
    def type_check(other_atom):
        if not isinstance(other_atom, Atom):
            raise TypeError('It must be atom')

    def __str__(self):
        return f'My atom name is {self.name}'

    def __add__(self, other):
        self.type_check(other)
        mylist = []
        mylist.append(self.name)
        mylist.append(other.name)
        return mylist

class Molecule():
    def __init__(self, atomlist):
        if type(atomlist) is list and len(atomlist) > 1:
            self.atomlist = atomlist
        else:
            raise TypeError

    @staticmethod
    def checkmolecule(v):
        if not isinstance(v, Molecule) and not isinstance(v, Atom):
            raise TypeError('it is not molecule')
        else:
            return v

    def __add__(self, other):
        self.checkmolecule(other)
        mylist = []
        for i in range(len(self.atomlist)):
            mylist.append(self.atomlist[i])
        mylist.append(other.name)
        return mylist

    def __str__(self):
        return f'Molecule - {self.atomlist}'

myatom1 = Atom('H')
print(myatom1)

myatom2 = Atom('N')
print(myatom2)

myatom3 = Atom('P')
print(myatom3)

mymolecule = Molecule(myatom1 + myatom2)
print(mymolecule)

mymolecule2 = Molecule(mymolecule + myatom3)
print(mymolecule2)


# 2. Let's write a Music Player Class!
#    a) Create a Song class. The class will have 4 attributes - name, artist, album and the year.
#    b) Now let's create a Playlist. Playlist class will contain Songs. We should have a method that will load songs
#    into our playlist. A file called albums.txt is provided with this exercise. The method should take care of loading
#    the songs from the file and store them inside of our Playlist class.
#    c) Now, we need our Player itself. Create a Player class. The player may contain at least one playlist. A few
#    of its methods include play(), that will start playing from the beginning, show_now_playing, that will show the
#    information of the song that is playing now, next_song, that will start playing the next_song, prev_song, that does
#    the opposite and finally a stop() method, that stops the song that is playing.
#    d) Finally, implement __str__ method for our classes, so we can see a nice representation of each object.
# Note: The aforementioned points are necessary but it's not a complete description of a music player. Be creative
# and add more functionality wherever you'll find it useful!

# Եկեք ստեղծենք նվագարկիչի կլաս։ Կառուցվածքը հետևյալն է լինելու։ Ունենալու ենք երեք կլաս՝ Player, Playlist, Song:
# Song-ը պարունակելու է երգի մասին ինֆորմացիա, Playlist-ը պարունակելու է երգերը Song տիպի օբյեկտների տեսքով, իսկ
# Player-ը ունենալու է Playlist:
#    a) Ստեղծել Song կլաս։ Կլասը պետք է ունենա 4 ատրիբուտ - name, artist, album, year
#    b) Ստեղծենք Playlist կլասը։ Այն պարունակելու է երգերը։ Այս կլասը պետք է ունենա load songs մեթոդ։ Տվյալ տնայինի հետ
#    ձեզ եմ ուղարկում նաև albums.txt ֆայլը։ Ֆայլը պարունակում է հարյուրավոր երգերի անունները, հեղինակներին, ալբոմների
#    անունները և ձայնագրման թվականը։ Ամեն տողում մի երգի ինֆորմացիա է։ Ամեն տողի դաշտերը իրարից անջատված են tab-երով։
#    Վերոնշյալ մեթոդով պետք է կարդալ ֆայլը և բոլոր երգերը Song-ի տեսքով փոխանցենք Playlist-ին։
#    c) Ստեղծել Player կլասը։ Այն պետք է ունենա Playlist տիպի ատրիբուտ։ Այս կլասը պետք է ունենա նաև հետևյալ մեթոդները՝
#    play(), stop(), next_song(), previous_song(), show_current_song()։ Մեթոդները կանչելուց պետք է կոնսոլում տեսնենք,
#    թե որ երգն է տվյալ պահին միացած։ Նաև վալիդացիաներ են պետք։ Օրինակ, եթե նվագարկիչն անջատված է, հաջորդ երգին անցնել
#    կամ կրկին անջատել չենք կարող։
#    d) Որպեսզի ամեն երգերը ավելի գեղեցիկ ներկայացվեն, սահմանել __str__ մեթոդը։ Ցանկալի է բոլոր կլասերի համար։

# Այս կետերը պարտադիր են, սակայն չեն պարունակում նվագարկիչի ողջ բնութագրությունը։ Կարող եք ազատ ավելացնել հավելյալ
# տրամաբանություն։

class Player:
    def __init__(self, val):
        if isinstance(val, Playlist):
            self.val = val
        else:
            raise TypeError('It is not playlist')

    def play(self):
        pass

    def stop(self):
        pass

    def next_song(self):
        pass

    def previous_song(self):
        pass

    def show_current_song(self):
        pass

class Playlist:
    def __init__(self, filename):
        if type(filename) is str:
            self.filename = filename

    def fileopen(self, count):
        with open(self.filename, 'r') as f:
            while count > 0:
                print(f.readline())
                count -= 1

    def load_songs(self):
        myplaylist = []
        for i in song.split('	'):
            myplaylist.append(i)
        return myplaylist

class Song(Playlist):
    def __init__(self, name, artist, album, year):
        super().__init__(filename)
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year

    def songsplit(self):
        myplaylist = super().load_songs()
        self.album = myplaylist[1]
        self.artist = myplaylist[0]
        self.name = myplaylist[3]
        self.year = myplaylist[2]

my_playlist = Playlist('albums.txt')

Playlist.fileopen(my_playlist, 2)


# 3. Create a class named Length. The default unit for length is meter. The class must contain some conversions
# information, e.g. feet -> m, km -> m, yard -> m, mile -> m etc.
#    a) Create a dictionary that will hold the metrics. Keys will be the unit name and their values will be the
#    coefficients for converting that unit to meters.
#    b) The class will have 2 instance attributes. Units and the length value itself.
#    c) Now, we can add lengths of course. So implement that method. But be careful, we can't add yard to meters, so
#    you will need to convert everything before adding.
#    d) Implement the __str__ method. This method must show the length of our Length object in meters.
#    e) Implement the __repr__ method. This method must show the length in whichever units our class is.
# Feel free to add some more features if you find them useful.

# Ստեղծել Length կլաս։ Երկարության հիմնական միավորը կհամարենք մետրը։ Կլասը պետք է ունենա որոշակի ինֆորմացիա, թե ինչպես
# փոխակերպել այլ միավորը մետրի (feet, km, yard, mile etc.)
#    a) Ստեղծել բառարան, որը կպահի վերոնշյալ ինֆորմացիան։ Բանալիները կլինեն միավորների անունները, իսկ արժեքները կլինեն
#    այն գործակիցները, որոնց օգնությամբ այդ միավորից ստանում ենք մետր։
#    b) Կլասը պետք է ունենա երկու instance attributes։ Երկարության արժեքը և միավորը։
#    c) Մենք պետք է կարողանանք երկարությունները իրար գումարել։ Սահմանել համապատասխան մեթոդը։ Ուշադրություն դարձնել
#    միավորներին։ Մենք չենք կարող ուղղակիորեն մետրը գումարել մղոնի կամ հակառակը։
#    d) Սահմանել __str__ մեթոդը։ Այս մեթոդը մեզ ցույց կտա օբյեկտի երկարությունը մետրերով։
#    e) Սահմանել __repr__ մեթոդը։ Այս մեթոդը մեզ ցույց կտա օբյեկտի երկարությունը այն միավորով, որով սահմանվել է։
# Լրացուցիչ, կարող եք ավելացնել հավելյալ տրամաբանություն որտեղ ճիշտ կգտնեք։

class Length:
    def __init__(self, val, mylenght):
        if type(val) is int and type(mylenght) is str:
            self.mylenght = mylenght
            self.val = val
            self.valdict = {'metr': 1,'feet': 0.3048, 'km': 1000, 'yard': 1093.6, 'mile': 0.62}
        else:
            raise TypeError

    @property
    def mylenght(self):
        return self.__lenghtval

    @mylenght.setter
    def mylenght(self, mylenght):
        self.__lenghtval = self.checklenght(mylenght)

    @staticmethod
    def checklenght(v):
        if v not in {'feet', 'km', 'yard', 'mile'}:
            raise TypeError('Please enter again')
        return v

    def __str__(self):
        return f'{self.val} {self.mylenght} is {self.val * self.valdict[self.mylenght]} metters'

a = Length(5, 'feet')
print(a)