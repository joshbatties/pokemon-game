from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.sorted_list_adt import *
from data_structures.array_sorted_list import ArraySortedList 

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        """Initialises a new instance of a MonsterTeam
        Commplexity: BACK, FRONT, OPTIMISE O(n), where n is the number of monsters in the team"""
        self.team_mode = team_mode
        self.team_maxsize = MonsterTeam.TEAM_LIMIT

        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            self.team = ArrayStack(self.team_maxsize)
            self.initial_team = ArrayStack(self.team_maxsize)
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            self.team = CircularQueue(self.team_maxsize)
            self.initial_team = CircularQueue(self.team_maxsize)
        
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            self.descending = True
            if "sort_key" not in kwargs:
                raise ValueError("sort_key is required for Optimise Team Mode")
            self.sort_key = kwargs["sort_key"]
            self.team = ArraySortedList(self.team_maxsize)
            self.initial_team = ArraySortedList(self.team_maxsize)

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(kwargs["provided_monsters"])
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
        
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            temp_stack = ArrayStack(self.team_maxsize)
            while not self.team.is_empty():
                temp_stack.push(self.team.pop())
            while not temp_stack.is_empty():
                monster = temp_stack.pop()
                self.team.push(monster)
                self.initial_team.push(monster)

        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            temp_queue = CircularQueue(self.team_maxsize)
            while not self.team.is_empty():
                temp_queue.append(self.team.serve())
            while not temp_queue.is_empty():
                monster = temp_queue.serve()
                self.team.append(monster)
                self.initial_team.append(monster)
        
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            for i in range(len(self.team)):
                monster_with_key = self.team[i]
                self.initial_team.add(ListItem(type(monster_with_key.value)(), monster_with_key.key))
                    
    def __len__(self) -> int:
        """Returns the number of monsters in the team
        Complexity: O(1)"""
        return len(self.team)
    
    def add_to_team(self, monster: MonsterBase) -> None:
        """adds a new monster to the team in the correct position
        Complexity: FRONT, BACK O(1), OPTIMISE O(log(n)), where n is the number of monsters in the team"""
        if len(self.team) >= self.TEAM_LIMIT:
            raise ValueError("Team is full")
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            self.team.push(monster)
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            self.team.append(monster)
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            monster_key = ListItem(monster, self._get_sort_key_value(monster))
            self.team.add(monster_key)

    def retrieve_from_team(self) -> MonsterBase:
        """returns the next monster in the team
        Complexity: FRONT, BACK O(1), OPTIMISE O(n), where n is the number of monsters in the team"""
        if len(self.team) == 0:
            raise ValueError("Team is empty")
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            return self.team.pop()
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            return self.team.serve()
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            return self.team.delete_at_index(0).value
            

    def special(self) -> None:
        """Perform special operation on the team
        Complexity: O(n), where n is the number of monsters in the team"""
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            self._front_special()
         
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            return self._back_special()

        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            if self.descending is True:
                self.descending = False
            else:
                self.descending = True
            self._resort_team()
            

    def regenerate_team(self) -> None:
        """Regenerate the team how it was at initialization
        Complexity: O(1)"""
        self.team = self.initial_team

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. 

        Complexity: O(n^2), where n is the number of monsters in the game.
        """
        while True:
            try:
                team_size = int(input("How many monsters are there?"))
                if 0 < team_size <= MonsterTeam.TEAM_LIMIT:
                    break
                else: 
                    print(f"Please enter a number between 1 and {MonsterTeam.TEAM_LIMIT}")
            except TypeError:
                print("Please enter a number")


        all_monster_array = get_all_monsters()
        for _ in range(team_size):
            print("MONSTERS Are:")
            for index, monster in enumerate(all_monster_array):
                spawnable_monster = "✔️" if monster().can_be_spawned() else "❌"
                print(f"{index + 1} {monster().get_name()} [{spawnable_monster}]")
            
            while True:
                 
                index = int(input("Which monster are you spawning?")) - 1
                if index < 0 or index >= len(all_monster_array) or not all_monster_array[index]().can_be_spawned():
                    print("This monster cannot be spawned")
                    continue
                
                self.add_to_team(all_monster_array[index]())
                break
                
    def select_provided(self, provided_monsters:ArrayR[type[MonsterBase]]):
        """
        Generates a team based on a list of already provided monster classes.
        Complexity: O(n * Comp(add_to_team)), where n is the number of monsters provided
        
        """
        if len(provided_monsters) > MonsterTeam.TEAM_LIMIT:
            raise ValueError(f"Too many monsters were provided, maximum is {MonsterTeam.TEAM_LIMIT}")
        for monster in provided_monsters:
            if not monster.can_be_spawned():
                raise ValueError(f"{monster.get_name()} can't be spawned")
            self.add_to_team(monster())


    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP
        
    def _get_sort_key_value(self, monster: MonsterBase) -> int:
        """
        Gets the value that the monster has for the given sort key
        Complexity: O(1)
        """
        if self.sort_key == MonsterTeam.SortMode.ATTACK:
            return -monster.get_attack() if self.descending else monster.get_attack()
        if self.sort_key == MonsterTeam.SortMode.DEFENSE:
            return -monster.get_defense() if self.descending else monster.get_defense()
        if self.sort_key == MonsterTeam.SortMode.SPEED:
            return -monster.get_speed() if self.descending else monster.get_speed()
        if self.sort_key == MonsterTeam.SortMode.HP:
            return -monster.get_hp() if self.descending else monster.get_hp()
        if self.sort_key == MonsterTeam.SortMode.LEVEL:
            return -monster.get_level() if self.descending else monster.get_level()
        else:
            raise ValueError("Invalid sort_key")
        
    def _resort_team(self) -> ArraySortedList:
        """Resorts the team after special has been called
        Complexity: O(n) where n is the number of monsters in the team"""
        resorted_team = ArraySortedList(self.team_maxsize)
        for monster_with_key in self.team:
            if monster_with_key:
                monster_with_reversed_key = ListItem(monster_with_key.value, self._get_sort_key_value(monster_with_key.value))
                resorted_team.add(monster_with_reversed_key)
        self.team = ArraySortedList(self.team_maxsize)
        for monster in resorted_team:
            if monster:
                self.team.add(monster)

    def _back_special(self) -> CircularQueue:
        """First half of the team is swapped with the second half 
        Complexity: O(n) where n is the number of monsters in the team"""
        temp1 = CircularQueue(len(self.team))
        temp2 = ArrayStack(len(self.team))
        new_team = CircularQueue(len(self.team))

        for _ in range(len(self.team) // 2):
            temp1.append(self.team.serve())

        while not self.team.is_empty():
            temp2.push(self.team.serve())

        while not temp2.is_empty():
            new_team.append(temp2.pop())

        while not temp1.is_empty():
            new_team.append(temp1.serve())
        self.team = new_team
        return self.team
    
    def _front_special(self) -> ArrayStack:
        """3 monsters at the front are reversed
        Complexity: O(n), where n is the number of monsters in the team"""
        temp = ArrayR(3)
        counter = 0
        for _ in range(3):
            if not self.team.is_empty():
                temp[counter] = self.team.pop()
                counter += 1
            else:
                break
            
        for i in range(counter):
            self.team.push(temp[i])
        return self.team
