#The login system
print("---------------Welcome to the E-commerce website!-------------------")
Name = input("Enter your name: ")
Access = input("Please enter your Access category: ")
password = input("Please enter your password: ")    

if Access == "Admin" and password == "Adm1n123":
    role = "admin"
elif Access == "Seller" and password == "Sell3r123":
    role = "seller"
elif Access == "Buyer" and password == "Buy3r123":
    role = "Buyer"   
else:
    print("Invalid Access category or password. Please try again.")
    
print(f"Login successful! \n Welcome, {Name}!")

if role in ["admin", "seller", "Buyer"]:
    subtotal = float(input("Please enter the subtotal amount: "))
    if subtotal <= 0:
        print("Invalid subtotal amount. Please enter a positive number.")
    else:
        if subtotal >= 100000:
            discount_rate = 0.20
            print("Congratulations! You have received a 20% discount.")
        elif subtotal >= 50000:
            discount_rate = 0.15
            print("Congratulations! You have received a 15% discount.")
        elif subtotal >= 10000:
            discount_rate = 0.10
            print("Congratulations! You have received a 10% discount.")
        else:
            discount_rate = 0.0
            print("No discount applied.")

    coupon = input("Enter coupon code (or press Enter to skip): ")
    if coupon == "SAVE10":
        discount_rate += 0.10
        print("Congratulations! You have received an additional 10% discount.")
    elif coupon == "SAVE20":
        discount_rate += 0.20
        print("Congratulations! You have received an additional 20% discount.")
    elif coupon != "":
        print("Invalid coupon code. No additional discount applied.")
        
    locaton = input("Please enter your location (City, State): ")
    match locaton:
        case "Kampala":
            tax_rate = 0.18
            print("A tax rate of 18% will be applied to your purchase.")
        case "Nairobi":
            tax_rate = 0.16 
            print("A tax rate of 16% will be applied to your purchase.")
        case "Entebbe":
            tax_rate = 0.20
            print("A tax rate of 20% will be applied to your purchase.")
        case _:
            tax_rate = 0.10 
            print("A default tax rate of 10% will be applied to your purchase.")
    discount_amount = subtotal * discount_rate
    discounted_price = subtotal - discount_amount
    tax_amount = discounted_price * tax_rate
    total_price = discounted_price + tax_amount

    print(f"==================================================== \n E-commerce Receipt \n ====================================================\n Name: {Name}\n Role: {role}\n Subtotal: UGX{subtotal:.2f}\n Discount ({discount_rate*100:.0f}%): UGX{discount_amount:.2f}\n Tax ({tax_rate*100:.0f}%): UGX{tax_amount:.2f}\n ================================================\n Total Price: UGX{total_price:.2f}")
    