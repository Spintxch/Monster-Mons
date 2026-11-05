# Starting area
import main

STARTER_LIST = {"Pica", "WIP", "WIP"}
# First sequence
if main.perform_action(main.visit_area, "town_1"):
    while True:
        player_name = input("What is your name? ")
        if player_name.isalpha() and len(player_name) < 16:
            main.perform_action(main.change_name, player_name)
            break
        else:
            print("Make sure your name is only letters and less then 16 characters.")

    print(f"Welcome {main.player["name"]} to Monster Mons")
    print("Choose your starter:")
    print("Pica")
    print("WIP")
    print("WIP")

    while True:
        starter_choice = input()
        if starter_choice in STARTER_LIST:
            starter = main.get_mon_info(starter_choice)
            break
        else:
            print("That is not one of the choices")

    if main.perform_action(main.add_mon, starter):
        print(f"You got {starter.name}!")

# Any time after
else:
    print("Return")