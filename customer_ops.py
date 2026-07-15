# print("customer operations ")

# # imports :
# from datetime import datetime
# import secrets

# import common_tools as common

# def authentication_customer(db,mobile_number):
#     already_exist=db.read_data_from_database("customer_details",
#                                              conditions_columns_values={"mobile_number":mobile_number},
#                                              mode="one")
#     if already_exist: 
#         return already_exist
#     else:
#          return False

# def user_personal_details(db,mobile_number):        
#                 gender=common.authorize_gender()
#                 if  not gender: return False
#                 full_name=common.user_name_validation()
#                 if not full_name: return False
#                 dob=common.dob_validation()
#                 if not dob: return False
#                 age=common.calculate_age(dob)
#                 email_id=common.email_id_validate_input()
#                 if not email_id : return False
#                 id_number=common.proof_of_identity_input()
#                 if not id_number:return False
#                 print("emergency cantact details ")
#                 emergency_contact=common.authorize_mobile_number()
#                 details={"mobile_number":mobile_number,"full_name":full_name,"gender":gender,"age":age,"date_of_birth":dob,"email_id":email_id,"id_proof_type":"aadhar","id_number":id_number,"emergency_contact":emergency_contact}
#                 customer_details(db,details)
#                 return True
                          
# def customer_details(db,details):
#     db.insert_data("customer_details",**details)

# def check_flight_availablity(db,**kwargs):
#         automate_flight_status(db)
#         kwargs["flight_status"]="scheduled"

#         found_flight_details=db.read_data_from_database(
#             "flight_details",
#             conditions_columns_values=kwargs,
#             mode="all")
        
#         if not found_flight_details:
#             return False
        
        
#         all_columns=db.get_table_columns("flight_details")
#         end_with_seats= [c.replace("_seats", "") for c in all_columns if c.endswith("_seats")]

#         valid_classes = []
#         for clas in end_with_seats:
#             if f"{clas}_seat_price" in all_columns:
#                 valid_classes.append(clas)
#         class_order=valid_classes

#         for flight in found_flight_details:
#             print()
#             print(f"Date : {flight["departure_date"]} | Time : {flight["departure_time"]} | Flight No : {flight["flight_no"]} | flight id {flight["flight_id"]}") 
#             print()
#             print(f"{"class":<15} {"seats":<7} price")
#             #cols=list(flight_cols )
#             #print(cols)

#             for clas in class_order:
#                 clas_name=clas
#                 clas_namee=clas_name.replace("_"," ").title()
#                 seats=f"{clas_name}_seats"
#                 price=f"{clas_name}_seat_price"
#                 print(f"{clas_namee:<15} : {flight[seats]:<5} {flight[price]}")   
# class ticket_booking_manager:
#     def __init__(self, database_manager):
#         self.dbm = database_manager

#     def initiate_booking(self,db,mobile_number,**kwargs): 
#         automate_flight_status(db)
#         kwargs["flight_status"]="scheduled"

#         self.flight_id=kwargs["flight_id"]
#         self.class_type=kwargs["class_type"]
#         self.no_of_seats=kwargs["no_of_seats"] 
        
#         flight = self.dbm.read_data_from_database("flight_details", {"flight_id": kwargs["flight_id"],"flight_status":"scheduled"}, mode="one")
#         if not flight:
#             print("Flight not found!")
#             return None
        
#         class_key=kwargs["class_type"].replace(" ","_")
#         seat_columns= f"{class_key}_seats"
#         price_columns= f"{class_key}_seat_price" 
#         total_price=flight[price_columns] * kwargs["no_of_seats"]
#         self.total_price=total_price

#         if flight[seat_columns] < kwargs["no_of_seats"]:
#             print(f"Sorry, {kwargs["class_type"]} is fully booked.")
#             return None 
        
#         new_seats = {
#             seat_columns: flight[seat_columns] - kwargs["no_of_seats"],
#             "total_available_seats": flight["total_available_seats"] -kwargs["no_of_seats"] 
#                     }
#         self.dbm.update_small_quantity_data_dictionary("flight_details", new_seats, {"flight_id": kwargs["flight_id"]})

#         pnr = f"AJI-{secrets.token_hex(3).upper()}"
#         self.pnr=pnr

#         booking_data = {
#             "pnr_no": pnr,
#             "customer_id": mobile_number,
#             "flight_id": kwargs["flight_id"],
#             "flight_no": flight['flight_no'],
#             "class_type": kwargs["class_type"],
#             "total_price": total_price,
#             "ticket_status": "pending"
#         }
#         self.dbm.insert_data("ticket_booking_details",**booking_data)
    
#         print(f"{kwargs["no_of_seats"]} Seat Locked! PNR: {pnr}. Please complete payment.")
#         result=common.select_payment_method(total_price)
#         if result:
#             self.finalize_booking(result)
#         else:
#             self.finalize_booking(result)   
              
#     def finalize_booking(self,payment_success):
#         if payment_success:
#             print(f"payment verified Confirming ticket for PNR: {self.pnr}")
#             self.dbm.update_small_quantity_data_dictionary(
#                 "ticket_booking_details", 
#                 {"ticket_status": "confirmed"},
#                  {"pnr_no":self.pnr}

#             )
#             print("Ticket Booked Successfully! ")
#         else:
#             print(f"Payment Failed or Cancelled. Releasing seat for PNR: {self.pnr}")

#             self.dbm.update_small_quantity_data_dictionary(
#                 "ticket_booking_details", 
#                 {"ticket_status": "cancelled"},
#                  {"pnr_no":self.pnr}
#             )
#             class_type=self.class_type.replace(" ","_")
#             seat_column = f"{class_type}_seats"
#             flight = self.dbm.read_data_from_database("flight_details", {"flight_id": self.flight_id}, mode="one")
            
#             new_seats = {
#                 seat_column: flight[seat_column] + self.no_of_seats,
#                 "total_available_seats": flight["total_available_seats"] + self.no_of_seats
#             }
            
#             self.dbm.update_small_quantity_data_dictionary("flight_details", new_seats, {"flight_id": self.flight_id})
#             print("Seat released back to the inventory") 

# def status_checking(db,pnr):
#         booking_status = db.read_data_from_database(
#         "ticket_booking_details", 
#         {"pnr_no": pnr}, 
#         mode="one"
#         )
#         if booking_status:
#             print("\n--- Ticket Status Details ---")
#             print(f"PNR         : {booking_status['pnr_no']}")
#             print(f"Customer ID : {booking_status['customer_id']}")
#             print(f"Status      : {booking_status['ticket_status'].upper()}")
#             print(f"Price Paid  : {booking_status['total_price']}")
#             print(f"Booked On   : {booking_status['booking_initiated_time']}")
#         else:
#             print(f" PNR {pnr} invalid.")  

# def cancel_ticket(db,pnr):
#         common.authorize_user()

#         booking = db.read_data_from_database("ticket_booking_details", {"pnr_no": pnr}, mode="one")
#         if not booking or booking['ticket_status'] == 'cancelled':
#             print("Invalid PNR or already cancelled.")
#             return

#         flight = db.read_data_from_database("flight_details", {"flight_id": booking['flight_id']}, mode="one")

#         departure_timestamp = datetime.combine(flight['departure_date'], (datetime.min + flight['departure_time']).time())
#         now = datetime.now()
        
#         time_diff = departure_timestamp - now
#         hours_remaining = time_diff.total_seconds() / 3600

#         if hours_remaining < 0:
#             print("Flight has already departed. No refund possible.")
#             return
#         elif hours_remaining < 4:
#             fee_percentage = 1.00  
#         elif hours_remaining < 24:
#             fee_percentage = 0.50  
#         elif hours_remaining < 72:
#             fee_percentage = 0.25  
#         else:
#             fee_percentage = 0.10  

#         original_price = int(booking['total_price'])
#         cancellation_fee = int(original_price * fee_percentage)
#         refund_amount = original_price - cancellation_fee

#         db.update_small_quantity_data_dictionary(
#             "ticket_booking_details", 
#             {"ticket_status": "cancelled"}, 
#             {"pnr_no": pnr}
#         )

#         target_flight_id = booking['flight_id']
#         chosen_class = booking['class_type'].lower()
#         seat_column = f"{chosen_class}_seats"
#         no_of_seats=booking.get("no_of_seats",1)

#         new_seats = {
#             seat_column: flight[seat_column] + no_of_seats,
#             "total_available_seats": flight["total_available_seats"] + no_of_seats
#         }
        
#         db.update_small_quantity_data_dictionary("flight_details", new_seats, {"flight_id": target_flight_id})
        
#         print("Booking status updated to 'cancelled'.")
#         #print(f"Seat released back to {chosen_class} inventory.") 

#         print(f"Deduction ({int(fee_percentage*100)}%): {original_price} - {cancellation_fee} = refund amount {refund_amount} ")

        
#         if refund_amount <= 0:
#             print("Notice: Last-hour cancellation. Not eligible for refund.")
#             return False
#         else:
#             return refund_amount
        
# def auto_refresh_and_validate(db):
#     all_flights = db.read_data_from_database("flight_details", mode="all")
    
#     for flight in all_flights:
#         if not common.valide_date_time(flight['departure_date'], flight['departure_time']):
#             db.update_small_quantity_data_dictionary(
#                 "flight_details", 
#                 {"flight_status": "departed"}, 
#                 {"flight_id": flight['flight_id']}
#             )      

# def automate_flight_status(db):
#     today = datetime.now().strftime("%Y-%m-%d")
#     now = datetime.now().strftime("%H:%M:%S")

#     query1 = "UPDATE flight_details SET flight_status = 'departed' WHERE departure_date < %s AND flight_status = 'scheduled'"
#     db.write_into_database(query1, [today])

#     query2 = "UPDATE flight_details SET flight_status = 'departed' WHERE departure_date = %s AND departure_time < %s AND flight_status = 'scheduled'"
#     db.write_into_database(query2, [today, now])    

# def get_serviceable_locations(db, column_name, filter_dict=None):
#     result = db.read_data_from_database(
#         "flight_details", 
#         conditions_columns_values=filter_dict,
#         optional_column=f"DISTINCT {column_name}", 
#         mode="all"
#     )
#     if result:
#         return [row[column_name] for row in result]
#     return []    

                                             


print("customer operations Aligned with Web Gateway Processors")

# imports :
from datetime import datetime
import secrets
import common_tools as common

def authentication_customer(db, mobile_number):
    already_exist = db.read_data_from_database(
        "customer_details",
        conditions_columns_values={"mobile_number": mobile_number},
        mode="one"
    )
    if already_exist: 
        return already_exist
    else:
         return False

def user_personal_details(db, mobile_number):        
    gender = common.authorize_gender()
    if not gender: return False
    full_name = common.user_name_validation()
    if not full_name: return False
    dob = common.dob_validation()
    if not dob: return False
    age = common.calculate_age(dob)
    email_id = common.email_id_validate_input()
    if not email_id: return False
    id_number = common.proof_of_identity_input()
    if not id_number: return False
    print("emergency contact details ")
    emergency_contact = common.authorize_mobile_number()
    details = {
        "mobile_number": mobile_number, "full_name": full_name, "gender": gender,
        "age": age, "date_of_birth": dob, "email_id": email_id,
        "id_proof_type": "aadhar", "id_number": id_number, "emergency_contact": emergency_contact
    }
    customer_details(db, details)
    return True
                          
def customer_details(db, details):
    db.insert_data("customer_details", **details)

def check_flight_availablity(db, **kwargs):
    automate_flight_status(db)
    kwargs["flight_status"] = "scheduled"

    found_flight_details = db.read_data_from_database(
        "flight_details",
        conditions_columns_values=kwargs,
        mode="all"
    )
    
    if not found_flight_details:
        return False
    
    all_columns = db.get_table_columns("flight_details")
    end_with_seats = [c.replace("_seats", "") for c in all_columns if c.endswith("_seats")]

    valid_classes = []
    for clas in end_with_seats:
        if f"{clas}_seat_price" in all_columns:
            valid_classes.append(clas)
    class_order = valid_classes

    for flight in found_flight_details:
        print()
        print(f"Date : {flight['departure_date']} | Time : {flight['departure_time']} | Flight No : {flight['flight_no']} | flight id {flight['flight_id']}") 
        print()
        print(f"{'class':<15} {'seats':<7} price")

        for clas in class_order:
            clas_name = clas
            clas_namee = clas_name.replace("_", " ").title()
            seats = f"{clas_name}_seats"
            price = f"{clas_name}_seat_price"
            print(f"{clas_namee:<15} : {flight[seats]:<5} {flight[price]}")   

class ticket_booking_manager:
    def __init__(self, database_manager):
        self.dbm = database_manager

    # 🎯 WEB COMPATIBLE INTEGRATION: Removed console loops to avoid browser process freeze blocks!
    def initiate_booking(self, db, mobile_number, **kwargs): 
        automate_flight_status(db)
        kwargs["flight_status"] = "scheduled"

        self.flight_id = kwargs["flight_id"]
        self.class_type = kwargs["class_type"]
        self.no_of_seats = kwargs["no_of_seats"] 
        
        flight = self.dbm.read_data_from_database(
            "flight_details", 
            {"flight_id": kwargs["flight_id"], "flight_status": "scheduled"}, 
            mode="one"
        )
        if not flight:
            raise Exception("Reservation Reference Error: Aligned target Flight ID is not active or departed!")
        
        class_key = kwargs["class_type"].replace(" ", "_")
        seat_columns = f"{class_key}_seats"
        price_columns = f"{class_key}_seat_price" 
        total_price = flight[price_columns] * kwargs["no_of_seats"]
        self.total_price = total_price

        if flight[seat_columns] < kwargs["no_of_seats"]:
            raise Exception(f"Seat Mismatch: Sorry, requesting class inventory balance limits exceeded!")
        
        # Deduct quantities mapping data updates log registries
        new_seats = {
            seat_columns: flight[seat_columns] - kwargs["no_of_seats"],
            "total_available_seats": flight["total_available_seats"] - kwargs["no_of_seats"] 
        }
        self.dbm.update_small_quantity_data_dictionary("flight_details", new_seats, {"flight_id": kwargs["flight_id"]})

        pnr = f"AJI-{secrets.token_hex(3).upper()}"
        self.pnr = pnr

        # 🎯 WEB COMPATIBLE AUTO-CONFIRMATION MATRIX ENGINE (No interactive console breaks)
        booking_data = {
            "pnr_no": pnr,
            "customer_id": mobile_number,
            "flight_id": kwargs["flight_id"],
            "flight_no": flight['flight_no'],
            "class_type": kwargs["class_type"],
            "total_price": total_price,
            "ticket_status": "confirmed" # Direct web routing confirmation state locked!
        }
        self.dbm.insert_data("ticket_booking_details", **booking_data)
        print(f"[AJITH AIRWAYS SYSTEM WORKSPACE] Core Web Booking finalized successfully for PNR: {pnr}")
        return pnr

def status_checking(db, pnr):
    booking_status = db.read_data_from_database(
        "ticket_booking_details", 
        {"pnr_no": pnr}, 
        mode="one"
    )
    if booking_status:
        print("\n--- Ticket Status Details ---")
        print(f"PNR         : {booking_status['pnr_no']}")
        print(f"Customer ID : {booking_status['customer_id']}")
        print(f"Status      : {booking_status['ticket_status'].upper()}")
        print(f"Price Paid  : {booking_status['total_price']}")
    else:
        print(f" PNR {pnr} invalid.")  

# 🎯 WEB COMPATIBLE INTEGRATION: Removed interactive terminal common.authorize_user() dependency loops block
def cancel_ticket(db, pnr):
    booking = db.read_data_from_database("ticket_booking_details", {"pnr_no": pnr}, mode="one")
    if not booking or booking['ticket_status'] == 'cancelled':
        raise Exception("Cancellation Error Matrix: Invalid PNR identifier reference or ticket state already cancelled logs!")

    flight = db.read_data_from_database("flight_details", {"flight_id": booking['flight_id']}, mode="one")

    departure_timestamp = datetime.combine(flight['departure_date'], (datetime.min + flight['departure_time']).time())
    now = datetime.now()
    
    time_diff = departure_timestamp - now
    hours_remaining = time_diff.total_seconds() / 3600

    if hours_remaining < 0:
        raise Exception("Operational Bounds Alert: Target flight has already departed! Refund parameters rejected.")
    elif hours_remaining < 4:
        fee_percentage = 1.00  
    elif hours_remaining < 24:
        fee_percentage = 0.50  
    elif hours_remaining < 72:
        fee_percentage = 0.25  
    else:
        fee_percentage = 0.10  

    original_price = int(booking['total_price'])
    cancellation_fee = int(original_price * fee_percentage)
    refund_amount = original_price - cancellation_fee

    db.update_small_quantity_data_dictionary(
        "ticket_booking_details", 
        {"ticket_status": "cancelled"}, 
        {"pnr_no": pnr}
    )

    target_flight_id = booking['flight_id']
    chosen_class = booking['class_type'].lower().replace(" ", "_")
    seat_column = f"{chosen_class}_seats"
    
    # Safely secure integer volume parameter checks strings keys
    no_of_seats = booking.get("no_of_seats", 1)

    new_seats = {
        seat_column: flight[seat_column] + no_of_seats,
        "total_available_seats": flight["total_available_seats"] + no_of_seats
    }
    
    db.update_small_quantity_data_dictionary("flight_details", new_seats, {"flight_id": target_flight_id})
    print(f"[AJITH AIRWAYS SYSTEM WORKSPACE] Web Cancellation processed logs for PNR: {pnr}")
    return refund_amount
        
def auto_refresh_and_validate(db):
    all_flights = db.read_data_from_database("flight_details", mode="all")
    for flight in all_flights:
        if not common.valide_date_time(flight['departure_date'], flight['departure_time']):
            db.update_small_quantity_data_dictionary(
                "flight_details", 
                {"flight_status": "departed"}, 
                {"flight_id": flight['flight_id']}
            )      

def automate_flight_status(db):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    query1 = "UPDATE flight_details SET flight_status = 'departed' WHERE departure_date < %s AND flight_status = 'scheduled'"
    db.write_into_database(query1, [today])

    query2 = "UPDATE flight_details SET flight_status = 'departed' WHERE departure_date = %s AND departure_time < %s AND flight_status = 'scheduled'"
    db.write_into_database(query2, [today, now])    

def get_serviceable_locations(db, column_name, filter_dict=None):
    result = db.read_data_from_database(
        "flight_details", 
        conditions_columns_values=filter_dict,
        optional_column=f"DISTINCT {column_name}", 
        mode="all"
    )
    if result:
        return [row[column_name] for row in result]
    return []