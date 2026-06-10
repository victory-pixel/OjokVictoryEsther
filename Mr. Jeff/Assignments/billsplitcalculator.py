# Ojok Victory Esther 24/U/10591/PS
# Bill Split Calculator 
bill = float(input("Enter the bill amount: "))
if bill <=0:
    print("Bill amount must be greater than zero.")
else:
    num_people = int(input("Enter the number of people to split the bill: "))
    if num_people <= 0:
        print("Number of people must be greater than zero.")
    else:
        print("Choose a tip percentage:")
        print("1. 10%")
        print("2. 15%")
        print("3. 20%")
        print("4. Custom tip percentage")
        choice = int(input("Enter your choice (1-4): "))
        if choice == 1:
            tip_percentage = 10/100
        elif choice == 2:
            tip_percentage = 15/100
        elif choice == 3:
            tip_percentage = 20/100
        elif choice == 4:
            custom_tip = float(input("Enter your custom tip percentage: "))
            tip_percentage = custom_tip / 100
        else:
            print("Invalid choice. Using default tip percentage of 10%.")
            tip_percentage = 10/100

        tip_amount = bill * tip_percentage
        total_bill = bill + tip_amount
        amount_per_person = total_bill / num_people
        print(f"------------------------------------- \n This is the receipt: \n Number of patrons: {num_people} \n Bill amount: UGX {bill:.2f} \n Tip percentage: {tip_percentage *100}% \n Tip amount: UGX {tip_amount:.2f} \n Total bill: UGX{total_bill:.2f} \n Amount per person: UGX {amount_per_person:.2f} \n -------------------------------------")



    



    
    
    
    

    