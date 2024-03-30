from random_gen import RandomGen
from helpers import get_all_monsters
from team import MonsterTeam
from battle import Battle


def main():
    # Initialize random generator seed for reproducibility in this example
    RandomGen.set_seed(42)

    # Load all available monsters
    all_monsters = get_all_monsters()

    # Dynamically select monsters for two teams by name
    team1_monster_names = ["Flamikin", "Aquariuma", "Vineon"]
    team2_monster_names = ["Strikeon", "Normake", "Marititan"]

    team1_monsters = [next(m() for m in all_monsters if m.get_name() == name) for name in team1_monster_names]
    team2_monsters = [next(m() for m in all_monsters if m.get_name() == name) for name in team2_monster_names]

    # Create teams with the selected monsters
    team1 = MonsterTeam(TeamMode.PROVIDED, SelectionMode.PROVIDED, provided_monsters=team1_monsters)
    team2 = MonsterTeam(TeamMode.PROVIDED, SelectionMode.PROVIDED, provided_monsters=team2_monsters)

    # Create and start a battle instance
    battle = Battle(verbosity=1)
    result = battle.battle(team1, team2)

    # Print the battle outcome
    if result == Battle.Result.TEAM1:
        print("Team 1 wins!")
    elif result == Battle.Result.TEAM2:
        print("Team 2 wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()


