import abc

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import *
from data_structures.sorted_list_adt import *
from data_structures.array_sorted_list import *

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    """
    Implementation of Stats initialisation in simple mode

    Attributes:
         attack (int): Attack Points
         defense (int): Defense Points
         speed (int): Speed Points
         max_hp (int): Maximum Hit Points
 
    """
    def __init__(self, attack: int, defense: int, speed: int, max_hp: int) -> None:
        Stats.__init__(self)
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp


    def get_attack(self):
        """returns the attack points of the monster"""
        return self.attack

    def get_defense(self):
        """ returns the defense points of the monster"""
        return self.defense

    def get_speed(self):
        """returns the speed points of the monster"""
        return self.speed

    def get_max_hp(self):
        """returns the maximum hit points of the monster"""
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        self.attack_formula = attack_formula
        self.defense_formula =defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula
        

    def get_attack(self, level: int) -> int:
        return self._calculate(self.attack_formula, level)

    def get_defense(self, level: int) -> int:
        return self._calculate(self.defense_formula, level)

    def get_speed(self, level: int) -> int:
        return self._calculate(self.speed_formula, level)

    def get_max_hp(self, level: int) -> int:
        return self._calculate(self.max_hp_formula, level)
    
    def _calculate(self, formula: ArrayR[str], level: int) -> int:
        stack = ArrayStack(len(formula))
        sorted_list = ArraySortedList(3)
        for element in formula:
            try: 
                number = float(element)
                stack.push(number)
            except ValueError:
                pass
            
            if element == "level":
                stack.push(float(level))

            elif element == "+":
                b, a = stack.pop(), stack.pop()
                stack.push(b + a)


            elif element == "-":
                b, a = stack.pop(), stack.pop()
                stack.push(a - b)

            elif element == "*":
                b, a = stack.pop(), stack.pop()
                stack.push(a * b)

            elif element == "/":
                b, a = stack.pop(), stack.pop()
                stack.push(a / b)

            elif element == "middle":
                for i in range(3):
                    number = stack.pop()
                    list_item = ListItem(number, number)
                    sorted_list.add(list_item)
                stack.push(sorted_list[1].value)


            elif element == "power":
                b, a = stack.pop(), stack.pop()
                stack.push(a ** b)
                

            elif element == "sqrt":
                stack.push(stack.pop() ** 0.5)

        return stack.pop()
