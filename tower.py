from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        """Initialises a tower
        Complexity: O(1)"""
        self.battle = battle or Battle(verbosity=0)
        self.user_team = None
        self.user_lives = 0
        self.all_enemy_teams = None
        self.all_enemy_lives = None
        self.enemy_lives_total = 0

    def set_my_team(self, team: MonsterTeam) -> None:
        """Sets the users team and lives
        Complexity: O(1)"""
        # Generate the team lives here too.
        self.user_team = team
        self.user_lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)
        

    def generate_teams(self, n: int) -> None:
        """Generates the enemy teams and their lives
        Complexity: O(n * Comp(MonsterTeam())), where n is the number of enemy teams"""
        self.all_enemy_teams = ArrayR(n)
        self.all_enemy_lives = ArrayR(n)
        for i in range(n):
            enemy_team = MonsterTeam(team_mode=MonsterTeam.TeamMode.BACK, selection_mode=MonsterTeam.SelectionMode.RANDOM)
            enemy_lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.all_enemy_teams[i] = enemy_team
            self.all_enemy_lives[i] = enemy_lives


    def battles_remaining(self) -> bool:
        """Checks if the user or all enemy teams are out of lives, aka if the tower is over
        Complexity: O(n) where n is the number of enemy teams"""
        if self.user_lives <= 0:
            return False
        for lives in self.all_enemy_lives:
            if lives > 0:
                return True
        return False

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """Determines and completes the next battle
        Complexity: O(n + Comp(Battle())), where n is the number of enemy teams"""
        enemy_to_battle = None
        for i, lives in enumerate(self.all_enemy_lives):
            if lives > 0:
                enemy_to_battle = i
                break
        if enemy_to_battle is None:
            return None
        self.user_team.regenerate_team()
        self.all_enemy_teams[enemy_to_battle].regenerate_team()
        battle_result = self.battle.battle(self.user_team, self.all_enemy_teams[enemy_to_battle])

        if battle_result == Battle.Result.TEAM1:
            self.all_enemy_lives[enemy_to_battle] -= 1
        elif battle_result == Battle.Result.TEAM2:
            self.user_lives -= 1
        else:
            self.user_lives -= 1
            self.all_enemy_lives[enemy_to_battle] -= 1
        self.enemy_lives_total = self._calculate_enemy_lives()
        return battle_result, self.user_team, self.all_enemy_teams[enemy_to_battle], self.user_lives, self.enemy_lives_total



        

    def out_of_meta(self) -> ArrayR[Element]:
        raise NotImplementedError
    
    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

    def _calculate_enemy_lives(self):
        """Calculates the total number of enemy lives
        Complexity: O(n), where n is the number of enemy teams"""
        for enemy_lives in self.all_enemy_lives:
            self.enemy_lives_total += enemy_lives
        return self.enemy_lives_total
def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError
