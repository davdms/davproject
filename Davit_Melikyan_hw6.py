# 1. Եկեք ստեղծենք հաճախորդի բանկային հաշվի կլաս.
#     - ունի 4 instance attribute-ներ՝ id, name, balance, currency, որոնք read-only են (հնարավոր չլինի ուղիղ ձևով փոխել)
#     - որպես class attribute տարբեր դրամային արժույթների համար ունենալ փոխանակման գործակիցներ
#     - ունի երեք մեթոդներ, credit, debit և transferTo
#     - credit - ավելացնել բալանսը տրված չափով
#     - debit - եթե հաշվի վրա բավարար գումար կա, նվազեցնել հաշվի գումարը տրված չափով
#     - transferTo - տրված չափով գումարը փոխանցել մեկ այլ բանկային հաշվի, հաշվի առնել currency-ն
#     - սահմանել __str__ մեթոդը։ Այս մեթոդը մեզ ցույց կտա հաշվի մնացորդը դոլարով

# 1. Let's create a customer bank account class.
# - has 4 instance attributes: id, name, balance, currency, which are read-only (can not be changed directly)
# - have exchange rates for different currencies as a class attribute
# - has three methods: credit, debit և transferTo
# - credit - increase the balance by the given amount
# - debit - if there is enough money in the account, reduce the amount of the account by the given amount
# - transferTo - transfer the given amount to another bank account, take into account the currency
# - define the __str__ method. This method will show us the account balance in dollars


class ReadOnlyException(Exception):
    def __init__(self, message='You can not change it'):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message

class Bankaccount:
    __currencychange = {'AMD': 1, 'USD': 480, 'EUR': 535, 'RUR': 5.5}

    def __init__(self, id, name, balance, currency='AMD'):
        if currency not in Bankaccount.__currencychange.keys():
            raise TypeError
        else:
            self.__id = id
            self.__name = name
            self.__balance = balance
            self.__currency = currency

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        raise ReadOnlyException

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        raise ReadOnlyException

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, val):
        raise ReadOnlyException

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, val):
        raise ReadOnlyException

    def __str__(self):
        return f'My balance in {self.name} is {self.balance} {self.currency}'

    @staticmethod
    def getdram(x):
        pass

    def credit(self, val, cur):
        if cur not in Bankaccount.__currencychange:
            raise TypeError
        elif cur == self.currency:
            self.__balance += val
        else:
            valtodram = val * Bankaccount.__currencychange[cur]
            mycurtodram = self.balance * Bankaccount.__currencychange[self.currency]
            mybalbydram = valtodram + mycurtodram
            newbal = mybalbydram / Bankaccount.__currencychange[self.currency]
            self.__balance = newbal

    def debit(self, val, cur):
        if cur not in Bankaccount.__currencychange:
            raise TypeError
        elif cur == self.currency:
            if val > self.balance:
                raise ValueError('Not enough money')
            else:
                self.__balance -= val
        else:
            valtodram = val * Bankaccount.__currencychange[cur]
            mycurtodram = self.balance * Bankaccount.__currencychange[self.currency]
            mybalbydram = mycurtodram - valtodram
            if mybalbydram < 0:
                raise ValueError('Not enough money')
            else:
                newbal = mybalbydram / Bankaccount.__currencychange[self.currency]
                self.__balance = newbal

    def transferTo(self, other):
        if type(other) != Bankaccount:
            raise TypeError
        else:
            valtodram = other.balance * Bankaccount.__currencychange[other.currency]
            mycurtodram = self.balance * Bankaccount.__currencychange[self.currency]
            mybalbydram = valtodram + mycurtodram
            newbal = mybalbydram / Bankaccount.__currencychange[self.currency]
            self.__balance = newbal

print('# 1')
a = Bankaccount(5, 'VTB', 2, 'USD')
print(a)
a.credit(7000,'AMD')
print(a)
a.debit(400, 'AMD')
print(a)
b = Bankaccount(6, 'Converse', 2, 'EUR')
a.transferTo(b)
print(a)
print('=================================')

# 2. Օգտագործելով Account կլասը, ստեղծել SavingsAccount(ավանդային հաշիվ) և CurrentAccount(ընթացիկ հաշիվ) կլասներ։
#     - ավանդային հաշիվը բանկային հաշվի ատրիբուտներից բացի պետք է ունենա նաև interest(տոկոսադրույք) և մեթոդ որով
#     կավելանա հաճախորդի հաշիվը տոկոսադրույքի չափով։
#     - ընթացիկ հաշիվը բանկային հաշվի ատրիբուտներից բացի պետք է ունենա overdraft limit ատրիբուտ
#     - ընթացիկ հաշվի բալասը կարող է մինուս արժեքներ ընդունել overdraft limit-ի չափով
#     - կարիքի դեպքում սուպերկլասի մեթոդները կարող են override արվել
#     - սահմանել հաշիվների իրար գումարումը, եթե նրանք նույն տիպի են
# 2. Using the Account class, create SavingsAccount and CurrentAccount classes.
# - deposit account in addition to bank account attributes must also have և interest (interest rate) և method by which
# will increase the customer's account by the interest rate.
# - The current account must have an overdraft limit attribute in addition to the bank account attributes
# - The current account balance can accept minus values in the amount of overdraft limit
# - Superclass methods can be override if needed
# - set the sum of accounts if they are of the same type

class Account:
    def __init__(self, name, balance, currency='AMD'):
        self.name = name
        self.balance = balance
        self.currency = currency

    def __str__(self):
        return f'My Account balance in {self.name} is {self.balance} {self.currency}'

class SavingsAccount(Account):
    def __init__(self, name, balance, currency, interest):
        super().__init__(name, balance, currency)
        self.interest = interest

    def addpercent(self):
        self.balance += self.balance / 100 * self.interest

    def __str__(self):
        return f'My Savings Account balance in {self.name} is {self.balance} {self.currency}, ' \
               f'percent is {self.interest} %'

class CurrentAccount(Account):
    def __init__(self, name, balance, currency, overdraft_limit):
        super().__init__(name, balance, currency)
        self.overdraft_limit = overdraft_limit

    def minusbalance(self):
        if self.balance < -self.overdraft_limit:
            raise ValueError('There is overdraft limit')

    def __str__(self):
        self.minusbalance()
        return f'My Current Account balance in {self.name} is {self.balance} {self.currency}, ' \
               f'overdraft limit is {self.overdraft_limit} {self.currency}.'

print('# 2')
b = SavingsAccount('VTB', 300, 'USD', 10)
print(b)
b.addpercent()
print(b)
b.addpercent()
print(b)
c = CurrentAccount('VTB', -50, 'USD', 100)
print(c)
print('=================================')

# 3. Ստեղծել Person կլաս, որը կունենա երկու instance attribute՝ name և ssn(հանրային ծառայությունների համարանիշ) int տիպի
#     - սահմանել __str__ մեթոդը։ Այս մեթոդը մեզ ցույց կտա մարդու անունը
#     - սահմանել __hash__ մեթոդը։ Այս մեթոդը պետք է վերադարձնի մարդու հանրային ծառայությունների համարանիշը
# 3. Create a Person class that will have two instance attributes: name and ssn (social service number) int type
# - define the __str__ method. This method will show us the name of the person
# - define the __hash__ method. This method should return the person a public service number

class Person:
    def __init__(self, name, ssn):
        if type(name) != str or type(ssn) != int:
            raise TypeError
        if ssn < 1000000000 or ssn >= 10000000000:
            raise ValueError('SSN must have 10 simbols')
        else:
            self.name = name
            self.ssn = ssn

    def __str__(self):
        return f"Person's name by {self.ssn} social service number is {self.name}."

    def __hash__(self):
        return hash(self.ssn)

print('# 3')
a = Person('Davit', 1234567890)
print(a)
print(hash(a))
print('=================================')

# 4. Ստեղծել Bank կլաս, որի instance-ը իր մեջ կարող է պարունակել տարբեր տիպի բանկային հաշիվներ և որոնք կապված են որոշակի
#     անձանց հետ։ Մեկ անձը կարող է ունենալ մեկից ավելի հաշիվներ։
#     - հաշիվների ցուցակը կարող ենք պահել dictionary-ի մեջ
#     - բանկը պետք է ունենա մեթոդներ փոփոխելու համար հաշիվների բալանսը, օգտագործելով բանկային հաշիվների մեթոդները
#     - եթե հաշիվը overdraft-ում է, բանկը կարող է նամակ գրել հաշվին հապակցված անձին։
#     - բանկը պետք է հնարավորություն ունենա ssn-ի միջոցով ստուգել անձի բոլոր հաշիվների ընդհանուր գումարը՝
#     դոլարային արժույթով
# 4. Create a Bank class, the instance of which may contain different types of bank accounts և which are linked
# with persons. One person can have more than one account.
# - We can save the list of accounts in the dictionary
# - the bank must have methods to change the balance of the accounts using the bank account methods
# - if the account is overdraft, the bank can write a letter to the person associated with the account.
# - the bank should be able to check the total amount of the person's accounts via ssn in dollar currency

class Bank:
    overdraft_1 = 0
    current_account_1 = 0
    saving_account_1 = 0
    overdraft_2 = 10
    current_account_2 = 20
    saving_account_2 = 30
    accounttypes = {1234568890: [overdraft_1], 1233333333: [current_account_1, saving_account_1],
                    1234567890: [overdraft_2, current_account_2, saving_account_2]}
    def __init__(self, ssn, overdraftbalance=0, savingbalance=0, currentbalance=0, currency='AMD'):
        self.overdraftbalance = overdraftbalance
        self.savingbalance = savingbalance
        self.currentbalance = currentbalance
        self.currency = currency
        self.ssn = ssn

    def addbalance(self):
        for key in self.accounttypes.keys():
            if self.ssn == key:
                return self.accounttypes[key]

a = Bank(1234567890)
print(a.addbalance())