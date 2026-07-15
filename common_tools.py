print("common tools")

import secrets
import string
from datetime import datetime,timedelta
import msvcrt
import os

def universal_input_handler(prompt_message, validation_funcion, error_msg, max_attempts=3):
        for attempt in range(1, max_attempts + 1):
            try:
                user_data = input(f"\n{prompt_message} (Attempt {attempt}/{max_attempts}): ").strip()
                if validation_funcion(user_data):
                    return user_data
                else:
                    print(f"{error_msg}")
            except Exception as e:
                print(f"Error: {e}")
        
        return None

def generate_otp():
    length=6
    digits = string.digits
    otp = ''.join(secrets.choice(digits) for _ in range(length))
    return otp

def validate_otp(otp,customer_otp):    
    if otp==customer_otp:
        return True
    else:
        return False
    
def authorize_user():
        otp=generate_otp()
        print(f"your otp {otp} ")
        def otp_validate(user_otp):
            return validate_otp(otp,user_otp)
        user_otp=universal_input_handler(
                "enter otp :",
                otp_validate,
                "Invalid otp"
                                        )
        if user_otp:
            return True
        else:
            return False     
    
def validate_gender(gender):
    if gender=="1":
        gender="male"
        return gender
    elif gender=="2":
        gender="female"
        return gender
    elif gender=="3":
        gender="shemale(others)"
        return gender
    else:
        return False

def authorize_gender():
    print("gender\n1.male\n2.female\n3.shemale(others)")
    user_gender=universal_input_handler(
        "your gender :".strip(),
        validate_gender,
        "invalid gender option"
    )      
    if user_gender:
        gender=validate_gender(user_gender)
        return gender
    else:
        return False 

def calculate_age(dob):
        dob=str(dob)

        if dob!="" and len(dob)==10: 
        
            if dob[4] == "-": 
                dob_str= dob
            else:
                dob_str=date_db_format(dob)
            if dob:
                dob_obj=datetime.strptime(dob_str,"%Y-%m-%d").date() 
                today=datetime.today().date()


                if dob_obj > today:
                    return False

                age=today.year-dob_obj.year

                if(today.month,today.day)<(dob_obj.month,dob_obj.day):
                    age-=1

                if age > 150:
                    return False
                #print("calculate_age :",age)
                return age
            else :
                return False
        
def date_db_format(date_str):
    # DD-MM-YYYY to YYYY-MM-DD
    return "-".join(date_str.split("-")[::-1])

def date_is_future(date_str):
    try:
        input_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        return input_date >= datetime.now().date()
    except ValueError:
        return False

def dob_validation():
    dob=universal_input_handler(
        "enter your date of birth (DD-MM-YYYY) :".strip(),
        calculate_age,
        "enter valid date of birth"
    )
    if dob:
        dob=date_db_format(dob)
        return dob

def validate_mobile_number(mobile_number): 
    if mobile_number.isdigit():   
        if len(mobile_number)==10:
            return mobile_number
        else:
            return False
    else:
        return False  

def authorize_mobile_number():
    user_moblie_number=universal_input_handler(
                "enter mobile_number (10 digits-india) :".strip(),
                validate_mobile_number,
                "Invalid mobile number "
                                        )
    if user_moblie_number:
        return user_moblie_number
    else:
        print("enter valid mobile number")
        return False       

def validate_upi(upi_id):
    upi_id = upi_id.lower().strip()
    if " " in upi_id or upi_id.count("@") != 1:
        return False
        
    parts = upi_id.split("@")
    username = parts[0]
    handle = parts[1] 

    if len(username) < 3 or len(handle) < 2:
        return False

    if username[0] in ".-" or username[-1] in ".-":
        print("Username cannot start or end with a dot/hyphen!")
        return False
        
    if handle[0] in ".-" or handle[-1] in ".-":
        print("Handle cannot start or end with a dot/hyphen!")
        return False
    
    allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789.-")
    
    if not all(char in allowed_chars for char in username):
        return False
        
    if not all(char in allowed_chars for char in handle):
        return False
        
    return True

def validate_card(**kwargs):
    card_no=kwargs["card_no"]
    expiry=kwargs["expiry_date"]
    cvv=kwargs["cvv"]

    if len(card_no) == 16 and card_no.isdigit() and len(cvv) == 3:
        try:
            expiry_month, expiry_year = map(int, expiry.split("/"))

            now = datetime.now()
            current_year = int(str(now.year)[2:]) 
            current_month = now.month

            if expiry_year > current_year:
                return 1 <= expiry_month <= 12
            
            elif expiry_year== current_year:
                return current_month<= expiry_month <= 12
            
            else:
                print("Card has already expired!")
                return False
                
        except:
            print("Invalid format! Use MM/YY.")
            return False
            
    return False

def select_payment_method(price):
    payment_success=False
    while not payment_success:
        print("1. UPI\n2. Debit/Credit Card\n3. Cancel Transaction")
        choice = input("Select payment method: ").strip()

        if choice=="3":
            return False
            
        if choice == "1":
            upi_id=universal_input_handler(
                    "enter upi id ",
                    validate_upi,
                    "Invalid upi id"
                                        )
            if upi_id:
                payment_validation=authorize_user()
                if payment_validation:
                    payment_success=Ajith_Kumar_National_Bank.withdraw_amount(price)
                    if payment_success:
                        return True
                    else:
                        print("insufficiant balance")
                        break
                else:
                    print("user validation failded") 
                    break   

            else:
                print("\nExceed your attempts")
                next_step = input("type 2 to switch card or 3 to cancel").strip().lower()
                    
                if next_step == "2":
                    choice = "2"
                    continue
                elif next_step=="3":
                    print("Transaction cancelled.")
                    return False
                else:
                    choice=None
                
        elif choice == "2":
            def card_details():
                card_details={
                    "card_no":input("Enter 16-digit Card Number: ").strip(),
                    "expiry_date": input("Enter Expiry (MM/YY): ").strip(),
                    "cvv":input("Enter 3-digit CVV: ").strip(),
                        }
                
                card_no = card_details["card_no"]
                return validate_card(**card_details)
                
            card_valid =universal_input_handler(
                "Press [ENTER] to start card entry", 
                card_details, 
                "Invalid Card Details! Let's try again from the start."
                                                )

            if card_valid:
                payment_validation =authorize_user()
                if payment_validation: 
                    payment_success=Ajith_Kumar_National_Bank(price)
                    if payment_success:
                        return True
                    else:
                        print("insufficiant balance")
                        break
                else:
                    print("user validation failed") 
                    break       
            else:
                print("\nCard entry failed!")
                next_step= input("Type 1 to switch upi or 3 to cancel: ").strip().upper()
                if next_step== "1": 
                    choice = "1"
                    continue
                elif next_step=="3":
                    print("Transaction cancelled.")
                    return False
                else:
                    choice=None
                    break
        else:
            print("invalid choice")
            return  False
    return False
    
class Ajith_Kumar_National_Bank:
    user_name ="ajithkumarm"
    balance = 100000

    @staticmethod    
    def withdraw_amount(price):
        if Ajith_Kumar_National_Bank.balance>price:
            Ajith_Kumar_National_Bank.balance=Ajith_Kumar_National_Bank.balance-price
            return True
        else:
            return False
        
    @staticmethod       
    def deposit_amount(refund):
        Ajith_Kumar_National_Bank.balance=Ajith_Kumar_National_Bank.balance+refund
        return True 
    
def valide_date_time(departure_date, departure_time):
    now = datetime.now()
    try:
        flight_date = departure_date if not isinstance(departure_date, str) else datetime.strptime(departure_date, "%Y-%m-%d").date()
        
        if isinstance(departure_time, timedelta):
            flight_time = (datetime.min + departure_time).time()
        else:
            flight_time = departure_time

        flight_timestamp = datetime.combine(flight_date, flight_time)
        return flight_timestamp > now
    except:
        return False 
    
def name_validation(name):
    if name!="" and name.replace(" ","").isalpha():
        return name
    else:
        return False

def user_name_validation():
    user_name=universal_input_handler(
        "Full name (as per your id proof) :".strip(),
        name_validation,
        "Full name not be a empty space or contain number"
                    )    
    if user_name:
        return user_name
    else:
        return False
    
def email_id_validate(email):
    import re
    email_pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if re.match(email_pattern, email):
        return True
    return False

    pass

def email_id_validate_input():
    email_id=universal_input_handler(
        "enter your email id :".lower().strip(),
        email_id_validate,
        "invalid email id"
    )
    if email_id:
        print("email id verification via otp")
        authorize_user()
        return email_id
    
def aadhar_number_validation(id_proof):
    if len(id_proof)==12 and id_proof.isdigit() and id_proof[0] not in ["0","1"]:
        return True
    else:
        return False

def proof_of_identity_input():
    id_proof=universal_input_handler(
        "enter your aadhar Number :",
        aadhar_number_validation,
        "invalid_aadhar number"
    )
    if id_proof:
        return id_proof
    else:
        return False
    
def universal_live_search(data_list, prompt):
    search_text = ""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{prompt}: {search_text}_")
        filtered = [item for item in data_list if str(item).lower().startswith(search_text.lower())]
        
        for i, item in enumerate(filtered[:10]):
            print(f"{'>>' if i == 0 else '  '} {item}")

        char = msvcrt.getch()

        try:
            key = char.decode('utf-8')
        except:
            continue

        if key == '\r':
            return filtered[0] if filtered else None
        
        elif key == '\x08':
            search_text = search_text[:-1]
            
        elif key.isalnum() or key in " -_":
            search_text += key          
      