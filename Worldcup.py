# Assignment 3: 2026 FIFA World Cup Simulator

team_name = input("Enter your country name: ")
morale = 100
strength = 100
injuries = 0

print(f"\n Welcome to the 2026 FIFA World Cup! \n Team {team_name} is ready to compete on the world stage! \n")

print("\n========== PRE-TOURNAMENT PREPARATION ==========")
prep_done = False
while prep_done == False:
    print("\nWhat do you want to do?")
    print("1. Train the team (+10 strength)")
    print("2. Play a friendly match (+5 morale)")
    print("3. Rest and recover (-5 injuries)")
    print("4. Start the tournament")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        strength += 10
        print(f"Training complete! Strength: {strength}")
    elif choice == "2":
        morale += 5
        print(f"Friendly won! Morale: {morale}")
    elif choice == "3":
        if injuries == 0:
            print("No injuries to recover from, skipping...")
            continue  # skip back to top of loop
        injuries -= 5
        print(f"Recovery done! Injuries: {injuries}")
    elif choice == "4":
        print("Starting the tournament!")
        prep_done = True
    else:
        pass  

print("\n========== GROUP STAGE ==========")
group_matches = ["Match 1", "Match 2", "Match 3"]
group_wins = 0

for match in group_matches:
    print(f"\n{match} - Your strength: {strength}, Morale: {morale}")
    result = input("Did you win this match? (yes/no): ")

    if result.lower() == "yes":
        group_wins += 1
        morale += 10
        print(f"You won! Morale up! Total wins: {group_wins}")
    else:
        morale -= 10
        injuries += 5
        print(f"You lost. Morale down. Injuries: {injuries}")

        if morale <= 50:
            print("Morale too low! Team is struggling...")
            continue  # skip to next match

if group_wins < 2:
    print(f"\nSorry !!!  {team_name} failed to qualify from the group stage. Better luck next time!")
else:
    print(f"\nYaayyy!!! {team_name} qualified for the knockout stage with {group_wins} wins!")

  
    knockout_stages = ["Round of 16", "Quarter-Final", "Semi-Final", "Final"]

    for stage in knockout_stages:
        print(f"\n========== {stage.upper()} ==========")
        print(f"Strength: {strength} | Morale: {morale} | Injuries: {injuries}")

        result = input(f"Did {team_name} win the {stage}? (yes/no): ")

        if result.lower() == "yes":
            morale += 15
            strength += 5
            print(f"{team_name} won the {stage}!")

            if stage == "Final":
                print(f"\n{team_name} WON THE 2026 FIFA WORLD CUP! ")
                break  # tournament over, exit loop
        else:
            print(f" {team_name} lost in the {stage}. Eliminated!")
            break  # knocked out, exit loop