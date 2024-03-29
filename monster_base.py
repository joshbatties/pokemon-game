from __future__ import annotations
import abc


from stats import Stats

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode: bool=True, level: int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        :start_level: The starting level of this monster, used to check qualifification for evolutions.
        :hp: The current hit points of this monster
        """
        self.simple_mode = simple_mode
        self.level = level
        self.start_level = level
        self.hp = self.get_max_hp()

    def __str__(self) -> str:
        """String representation of the monster"""
        return f"LV.{self.level} {self.get_name()}, {self.hp}/{self.get_max_hp()} HP"

    def _get_hp_difference(self) -> int:
        """Internal method which returns the difference between the monsters Max HP and its current HP"""
        return self.get_max_hp() - self.hp
    
    def _get_stats_mode(self) -> Stats:
        """Internal method which returns the stats mode (simple or complex)"""
        return self.get_simple_stats() if self.simple_mode else self.get_complex_stats

    def get_level(self) -> int:
        """The current level of this monster instance"""
        return self.level

    def level_up(self) -> None:
        """Increase the level of this monster instance by 1 and force to evolve if possible"""
        prev_max_hp = self.get_max_hp()
        self.level += 1
        increase_hp = self.get_max_hp() - prev_max_hp 
        self.hp += increase_hp
        return self.evolve()

    def get_hp(self) -> int:
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val: int) -> None:
        """Set the current HP of this monster instance"""
        if not isinstance(val, int):
            raise ValueError("Invalid HP value")
        self.hp = val

    def get_attack(self) -> int:
        """Get the attack of this monster instance"""
        return self._get_stats_mode().get_attack()

    def get_defense(self) -> int:
        """Get the defense of this monster instance"""
        return self._get_stats_mode().get_defense()

    def get_speed(self) -> int:
        """Get the speed of this monster instance"""
        return self._get_stats_mode().get_speed()

    def get_max_hp(self) -> int:
        """Get the maximum HP of this monster instance"""
        return self._get_stats_mode().get_max_hp()

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.hp > 0

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP
        pass

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        return self.get_evolution() and self.level > self.start_level

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        if not self.ready_to_evolve() and self.level >= self.start_level:
            return self
        
        new_class = self.get_evolution()
        new_monster = new_class(self.simple_mode, self.level)
        new_monster.set_hp(new_monster.get_max_hp() - self._get_hp_difference())
        return new_monster

        


    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
