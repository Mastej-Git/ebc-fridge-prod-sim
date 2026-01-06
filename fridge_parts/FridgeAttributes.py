from enum import Enum

class FridgeAttributes:

    class Cover:

        class Material(Enum):
            STEEL = "steel"
            ALLUMINUM = "alluminum"

        class Color(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

    class Doors(Enum):

        class Material(Enum):
            STEEL = "steel"
            ALLUMINUM = "alluminum"

        class Machine(Enum):
            ICE = "ice"
            WATER = "water"

        class FrontPanel(Enum):
            YES = True
            NO = False  

    class Shelves(Enum):

        class Material(Enum):
            PLASTIC = "plastic"
            GLASS = "glass"

        class Number(Enum):
            SIX = 6
            SEVEN = 7
            EIGHT = 8

        class Adjustable(Enum):
            YES = True
            NO = False 

    class CoolingSystem(Enum):

        class Type(Enum):
            NOFROST = "NoFrost"
            FROSTFREE = "FrostFree"
            STATIC = "Static"

        class EnergyClass(Enum):
            APPP = "A+++"
            AP = "A+"
            B = "B"

    class Lights(Enum):
        
        class Type(Enum):
            LED = "led"
            FLUORESCENT = "fluorescent"

        class Automatic(Enum):
            YES = True
            NO = False 
            