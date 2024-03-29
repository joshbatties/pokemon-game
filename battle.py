from __future__ import annotations
from enum import auto
from typing import Optional
import math

from base_enum import BaseEnum
from team import MonsterTeam
from monster_base import MonsterBase
from elements import Element, EffectivenessCalculator
from data_structures.referential_array import *
from helpers import Flamikin, Aquariuma, Vineon, Strikeon, Normake, Marititan, Leviatitan, Treetower, Infernoth


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        """initialises the Battle class
        Complexity: O(1)"""
        self.verbosity = verbosity
        self.team1_dead = False
        self.team2_dead = False

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.

        Complexity O(max(Comp(_choose_action), Comp(_swap), Comp(special), Comp(_attack), Comp(_end_turn), Comp(_check_for_win)): 
        """
        action1 = self.team1.choose_action(self.out1, self.out2)
        action2 = self.team2.choose_action(self.out2, self.out1)
        if action1 == Battle.Action.SWAP:
            self.out1 = self._swap(self.out1, self.team1)
        if action2 == Battle.Action.SWAP:
            self.out2 = self._swap(self.out2, self.team2)
        if action1 == Battle.Action.SPECIAL:
            self.out1 = self._special(self.out1, self.team1)
        if action2 == Battle.Action.SPECIAL:
            self.out2 = self._special(self.out2, self.team2)
        if action1 == Battle.Action.ATTACK and action2 == Battle.Action.ATTACK:
            self._both_attack()
        if action1 == Battle.Action.ATTACK and not action2 == Battle.Action.ATTACK:
            self._attack(self.out1, self.out2)
        if action2 == Battle.Action.ATTACK and not action1 == Battle.Action.ATTACK:
            self._attack(self.out2, self.out2)
        self._end_turn()
        win_result = self._check_for_win()
        if win_result:
            return win_result
    


    
    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        """Performs the battle between team 1 and 2
        Complexity: O(n * process_turn), where n is the number of turns in the battle"""
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result
    

    def _swap(self, currently_out: MonsterBase, team: MonsterTeam) -> MonsterBase:
        """Adds the currently out monster back to thw team and retrieves the next monster
        Complexity: O(Comp(add_to_team + retrieve_from_team))"""
        team.add_to_team(currently_out)
        new_out = team.retrieve_from_team()
        return new_out
    
    def _special(self, currently_out: MonsterBase, team: MonsterTeam) -> MonsterBase:
        """performs the special operation on the given team
        Complexity: O(Comp(add_to_team) + Comp(retrieve_from_team) + Comp(special))"""
        team.add_to_team(currently_out)
        team.special()
        new_out = team.retrieve_from_team()
        return new_out
    
    def _compute_damage(self, attacking_monster: MonsterBase, defending_monster: MonsterBase) -> int:
        """Calculates the effective damage for the attacking monster on the defending monster based on their stats and elements
        Complexity: O(Comp(get_effectiveness))"""
        attack = attacking_monster.get_attack()
        defense = defending_monster.get_defense()

        if defense < attack / 2:
            damage = attack - defense
        elif defense < attack:
            damage = attack * 5/8 - defense / 4
        else:
            damage = attack / 4


        attacking_monster_element = Element.from_string(attacking_monster.get_element())
        defending_monster_element = Element.from_string(defending_monster.get_element())

        damage_multiplier = EffectivenessCalculator.get_effectiveness(attacking_monster_element, defending_monster_element)
        effective_damage = math.ceil(damage * damage_multiplier)
        return effective_damage
    
    def _both_attack(self) -> None:
        """handles the situation where both monsters attack
        Faster monster attacks first, then the other monster attacks if its still alive after being attacked
        Complexity: O(comp(_compute_damage))"""
        if self.out1.get_speed() > self.out2.get_speed():
            self._attack(self.out1, self.out2)
            if self.out2.alive():
                self._attack(self.out2, self.out1)
        elif self.out1.get_speed() < self.out2.get_speed():
            self._attack(self.out2, self.out1)
            if self.out1.alive():
                self._attack(self.out1, self.out2)
        else:
            self._attack(self.out1, self.out2)
            self._attack(self.out2, self.out1)

    def _attack(self, attacking_monster: MonsterBase, defending_monster: MonsterBase) -> None:
        """subtracts the effective damage from the defending monster
        Complexity: O(Comp(_compute_damage))"""
        effective_damage = self._compute_damage(attacking_monster, defending_monster)
        defending_monster.set_hp(defending_monster.get_hp() - effective_damage)

    def _end_turn(self):
        """Handlex possible outcomes after each team has made their turn
        Complexity: O(Comp(retrieve_from_team))"""    
        if self.out1.alive() and self.out2.alive(): 
            self.out1.set_hp(self.out1.get_hp() - 1)
            self.out2.set_hp(self.out2.get_hp() - 1)
        
        if self.out2.alive() and not self.out1.alive():
            self.out2 = self.out2.level_up()
            try:
                self.out1 = self.team1.retrieve_from_team()
            except ValueError:
                self.team1_dead = True
        
        elif self.out1.alive() and not self.out2.alive():
            self.out1 = self.out1.level_up()
            try:
                self.out2 = self.team2.retrieve_from_team()
            except ValueError:
                self.team2_dead = True
            
        if not self.out1.alive() and not self.out2.alive():
            try:
                self.out1 = self.team1.retrieve_from_team()
            except ValueError:
                self.team1_dead = True
            try:
                self.out2 = self.team2.retrieve_from_team()
            except ValueError:
                self.team2_dead = True
        
    def _check_for_win(self):
        """Checks if either team has no remaining monsters
        Complexity: O(1)"""
        if self.team1_dead and self.team2_dead:
            return Battle.Result.DRAW
        elif self.team1_dead:
            return Battle.Result.TEAM2
        elif self.team2_dead:
            return Battle.Result.TEAM1
