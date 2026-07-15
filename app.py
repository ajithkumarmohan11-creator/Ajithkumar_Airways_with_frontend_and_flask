from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

from db_engine import database_manager as dbm
import admin_ops as admin
import customer_ops as customer
import common_tools as common

app = Flask(__name__)
app.secret_key = "ajith_airways_secure_session_token_key" 

db = None

if os.path.exists("db_connect_details.json"):
    with open("db_connect_details.json", "r") as f:
        details = json.load(f)
    try:
        db = dbm(**details) 
    except Exception:
        db = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select-role', methods=['POST'])
def select_role():
    user_choice = request.form.get('choice')
    if user_choice == "1":
        return redirect(url_for('passenger_login_screen'))
    elif user_choice == "2":
        return redirect(url_for('admin_login_screen'))
    elif user_choice == "3":
        return "<h3>System Exit Success! Thank you for choosing Ajith Airways.</h3>"
    return redirect(url_for('home'))   

@app.route('/admin-login')
def admin_login_screen():
    return render_template('admin_login.html')

@app.route('/admin/verify-credentials', methods=['POST'])
def admin_verify_credentials():
    input_user_id = request.form.get('admin_id').strip()
    input_password = request.form.get('admin_pass').strip()
    
    if admin.authentication_admin(input_user_id, input_password):
        return redirect(url_for('admin_operations_dashboard', user_identity=input_user_id))
    else:
        flash("Access Denied! Invalid User ID or System Credentials.")
        return redirect(url_for('admin_login_screen'))

@app.route('/admin/operations')
def admin_operations_dashboard():
    user = request.args.get('user_identity', 'Admin')
    current_bound_schema = "Not selected"
    
    if db:
        try:
            current_bound_schema = admin.admin_operations(db, choice_for_operations="3", database_name=True)
            if not current_bound_schema:
                current_bound_schema = "Connected (No Database Selected)"
        except Exception:
            current_bound_schema = "Connected Context Active"
            
    return render_template('admin_dashboard.html', admin_name=user, active_db=current_bound_schema)

@app.route('/admin/operations/<operation_type>')
def admin_operation_action_gateways(operation_type):
    current_bound_schema = "Not selected"
    if db:
        try:
            current_bound_schema = admin.admin_operations(db, choice_for_operations="3", database_name=True)
            if not current_bound_schema:
                current_bound_schema = "Connected (No Database Selected)"
        except Exception:
            current_bound_schema = "Connected Context Active"

    if operation_type == "connect-db":
        return render_template('admin_action_form.html', dynamic_title="connect with database", current_icon="fas fa-plug", active_mode="connect-db")
    elif operation_type == "create-db":
        return render_template('admin_action_form.html', dynamic_title="create database", current_icon="fas fa-database", active_mode="create-db")
    elif operation_type == "create-table":
        return render_template('admin_action_form.html', dynamic_title="create table", current_icon="fas fa-table", active_mode="create-table", active_db=current_bound_schema)
    elif operation_type == "flight-auto":
        return render_template('admin_action_form.html', dynamic_title="flight automation", current_icon="fas fa-cogs", active_mode="flight-auto")
    else:
        return redirect(url_for('admin_operations_dashboard'))

@app.route('/admin/op/connect-db', methods=['POST'])
def admin_connect_db():
    global db  
    host = request.form.get('db_host').strip()
    user = request.form.get('db_user').strip()
    password = request.form.get('db_pass').strip()
    
    db_connect_details = {"user": user, "host": host, "password": password}
    
    try:
        db = dbm(**db_connect_details)
        with open("db_connect_details.json", "w") as f:
            json.dump(db_connect_details, f, indent=4)
        flash("MySQL Connection Established Successfully! Configurations Locked.", "success")
    except Exception as e:
        flash(f"Database Connection Failed: {str(e)}", "danger")
        
    return redirect(url_for('admin_operation_action_gateways', operation_type='connect-db'))

@app.route('/admin/op/create-db', methods=['POST'])
def admin_create_db():
    global db 
    db_name = request.form.get('database_name').strip()
    
    if not db:
        flash("System Mismatch: No active MySQL server bound! Please run Option 1 (Connect DB) first.", "danger")
        return redirect(url_for('admin_operation_action_gateways', operation_type='create-db'))
        
    try:
        db = admin.admin_operations(db, choice_for_operations="2", database_name=db_name)
        flash(f"Database instance configuration success: '{db_name}' initialized completely!", "success")
    except Exception as e:
        flash(f"Schema instantiation failed alert: {str(e)}", "danger")
        
    return redirect(url_for('admin_operation_action_gateways', operation_type='create-db'))

@app.route('/admin/op/create-table', methods=['POST'])
def admin_create_table():
    global db
    
    if not db:
        flash("System Logic Error: No active connection found! Please execute Option 1 first.", "danger")
        return redirect(url_for('admin_operation_action_gateways', operation_type='create-table'))
        
    target_table = request.form.get('table_name').strip()
    fields_names_array = request.form.getlist('col_name[]')
    fields_syntax_array = request.form.getlist('col_type[]')
    
    columns_dictionary = {}
    for index in range(len(fields_names_array)):
        column_key = fields_names_array[index].lower().strip()
        syntax_val = fields_syntax_array[index].strip()
        if column_key:
            columns_dictionary[column_key] = syntax_val
            
    try:
        db = admin.admin_operations(db, choice_for_operations="3", table_name=target_table, columns=columns_dictionary)
        flash(f"Table operational configuration success: '{target_table}' created successfully inside schema!", "success")
    except Exception as e:
        flash(f"Table structural creation failed: {str(e)}", "danger")
        
    return redirect(url_for('admin_operation_action_gateways', operation_type='create-table'))

@app.route('/admin/op/flight-automation', methods=['POST'])
def admin_flight_automation():
    global db
    
    if not db:
        flash("System Mismatch Error: No active connection found! Please execute Option 1 first.", "danger")
        return redirect(url_for('admin_operation_action_gateways', operation_type='flight-auto'))
        
    try:
        automation_payload = {
            "flight_no": request.form.get('flight_no').strip(),
            "total_available_seats": int(request.form.get('total_available_seats')),
            "origine": request.form.get('origine').strip(),
            "destination": request.form.get('destination').strip(),
            "departure_date": request.form.get('departure_date').strip(),
            "departure_time": request.form.get('departure_time').strip(),
            "base_price": float(request.form.get('base_price'))
        }
        db = admin.admin_operations(db, choice_for_operations="4", **automation_payload)
        flash("Flight Automation Engine Executed Successfully! 30-day timelines generated.", "success")
    except Exception as e:
        flash(f"Automation Matrix Generation Failed: {str(e)}", "danger")
        
    return redirect(url_for('admin_operation_action_gateways', operation_type='flight-auto'))

@app.route('/passenger/dashboard')
def passenger_dashboard():
    # 🎯 ALWAYS FETCH FROM SECURE FLASK SESSION VAULT!
    user_mobile = session.get('passenger_mobile', '').strip()
    
    if not user_mobile:
        # Fallback tracking if session was manually bypassed
        user_mobile = request.args.get('mobile_number', '').strip()
        if user_mobile:
            session['passenger_mobile'] = user_mobile
            
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))
        
    return render_template('passenger_dashboard.html', current_mobile=user_mobile)

@app.route('/passenger/operations/<operation_type>')
def passenger_operation_action_gateways(operation_type):
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))
    
    # Prefill handlers backup mapping data if redirected from search framework
    prefill_flight_id = request.args.get('prefill_flight_id', '').strip()
    eco_p = request.args.get('eco_p', '0')
    prem_p = request.args.get('prem_p', '0')
    bus_p = request.args.get('bus_p', '0')
    fst_p = request.args.get('fst_p', '0')
    
    # 🎯 FETCH CUSTOMER PROFILE RECORDS FOR AUTOMATED DATA INJECTION
    customer_profile_record = None
    fetched_aadhar_id = ""
    try:
        customer_profile_record = customer.authentication_customer(db, user_mobile)
        if customer_profile_record:
            # Safely fetch active identity numbers logs
            fetched_aadhar_id = customer_profile_record.get('id_number', '')
    except Exception as fetch_err:
        print(f"[AJITH AIRWAYS] Profile data query log fallback: {str(fetch_err)}")
    
    flights_list = []
    if operation_type == "check-availability":
        try:
            flights_list = db.read_data_from_database("flight_details", conditions_columns_values={"flight_status": "scheduled"}, mode="all")
        except:
            flights_list = []
            
    return render_template('passenger_action_form.html', 
                           dynamic_title=operation_type.replace("-", " "), 
                           current_icon="fas fa-search-location" if "avail" in operation_type else "fas fa-ticket-alt", 
                           active_mode=operation_type,
                           flights_list=flights_list,
                           current_mobile=user_mobile,
                           current_customer_id_proof=fetched_aadhar_id, # Dynamic auto mask injector variable pass
                           prefill_flight_id=prefill_flight_id,
                           eco_p=eco_p, prem_p=prem_p, bus_p=bus_p, fst_p=fst_p,
                           searched=False)

@app.route('/passenger/op/check-availability', methods=['POST'])
def web_check_availability():
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))
        
    origine = request.form.get('origine').strip()
    destination = request.form.get('destination').strip()
    departure_date = request.form.get('departure_date').strip()
    
    search_payload = {"origine": origine, "destination": destination, "departure_date": departure_date, "flight_status": "scheduled"}
    found_flights = []
    try:
        customer.automate_flight_status(db)
        raw_flights = db.read_data_from_database("flight_details", conditions_columns_values=search_payload, mode="all")
        
        unique_tracker = set()
        for flight in raw_flights:
            uniqueness_token = (flight.get('flight_no'), flight.get('departure_date'), flight.get('departure_time'))
            if uniqueness_token not in unique_tracker:
                unique_tracker.add(uniqueness_token)
                found_flights.append(flight)
                
    except Exception as e:
        flash(f"Search Failure Mismatch: {str(e)}", "danger")
        
    return render_template('passenger_action_form.html', 
                           dynamic_title="Available Flight Schedules Search Result View", 
                           current_icon="fas fa-search-location", 
                           active_mode="check-availability",
                           flights_list=found_flights,
                           total_flights_found=len(found_flights), # Count indicator variable
                           current_mobile=user_mobile,
                           searched=True)

@app.route('/passenger/op/book-ticket', methods=['POST'])
def web_book_ticket():
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))

    payment_payload = {
        "flight_id": int(request.form.get('flight_id')),
        "class_type": request.form.get('class_type').strip().lower(),
        "no_of_seats": int(request.form.get('no_of_seats')),
        "mobile_number": user_mobile,
        "total_price": float(request.form.get('total_price_hidden', request.form.get('total_price', 1000))),
        "payment_choice": request.form.get('payment_method', 'upi')
    }
    
    active_profile_email_address_string = ""
    active_profile_id_proof_string = ""
    try:
        user_profile_data_ledger = customer.authentication_customer(db, user_mobile)
        if user_profile_data_ledger:
            active_profile_email_address_string = user_profile_data_ledger.get('email_id', '')
            active_profile_id_proof_string = user_profile_data_ledger.get('id_number', '')
    except Exception as data_query_err:
        print(f"[AJITH AIRWAYS ENGINE] Dynamic context extraction fallback: {str(data_query_err)}")
        
    import secrets
    simulated_pay_otp = "".join(secrets.choice("0123456789") for _ in range(6))
    
    return render_template('passenger_action_form.html',
                           dynamic_title=f"Secure Bank Gateway Payment Verification",
                           current_icon="fas fa-shield-alt text-success",
                           active_mode=f"process-{payment_payload['payment_choice']}",
                           pay_meta=payment_payload,
                           current_mobile=user_mobile,
                           current_customer_email=active_profile_email_address_string,
                           current_customer_id_proof=active_profile_id_proof_string, # Mapped securely into the payment gateway template render context!
                           backend_pay_otp=simulated_pay_otp)

@app.route('/passenger/op/finalize-payment', methods=['POST'])
def web_finalize_payment():
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))
        
    flight_id = int(request.form.get('flight_id'))
    class_type = request.form.get('class_type').strip().lower()
    no_of_seats = int(request.form.get('no_of_seats'))
    
    total_price_raw = request.form.get('total_price')
    if not total_price_raw:
        total_price_raw = request.form.get('total_price_hidden', '1000')
    total_price = float(total_price_raw)
    
    try:
        customer_profile_record = customer.authentication_customer(db, user_mobile)
        fetched_aadhar_id = ""
        if customer_profile_record:
            fetched_aadhar_id = customer_profile_record.get('id_number', '')

        flight = db.read_data_from_database("flight_details", {"flight_id": flight_id}, mode="one")
        class_key = class_type.replace(" ", "_")
        seat_columns = f"{class_key}_seats"
        
        new_seats = {
            seat_columns: flight[seat_columns] - no_of_seats,
            "total_available_seats": flight["total_available_seats"] - no_of_seats
        }
        db.update_small_quantity_data_dictionary("flight_details", new_seats, {"flight_id": flight_id})
        
       
        import secrets
        pnr = f"AJI-{secrets.token_hex(3).upper()}"
        common.Ajith_Kumar_National_Bank.withdraw_amount(total_price)
        
        booking_data = {
            "pnr_no": pnr, 
            "customer_id": user_mobile, 
            "flight_id": flight_id,
            "flight_no": flight['flight_no'], 
            "class_type": class_type,
            "total_price": total_price, 
            "ticket_status": "confirmed", 
            "no_of_seats": no_of_seats   
        }
        db.insert_data("ticket_booking_details", **booking_data)
        
        flash("Payment Completed Successfully! Your ticket has been generated.", "success")
        return redirect(url_for('passenger_view_receipt', pnr_no=pnr))
                               
    except Exception as e:
        print(f"[AJITH AIRWAYS SYSTEM EXCEPTION]: {str(e)}")
        flash(f"Transaction Exception Matrix Failure: {str(e)}", "danger")
        return redirect(url_for('passenger_dashboard'))
    
@app.route('/passenger/op/status-checking', methods=['POST'])
def web_status_checking():
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    pnr_no = request.form.get('pnr_no').strip()
    try:
        booking = db.read_data_from_database("ticket_booking_details", {"pnr_no": pnr_no}, mode="one")
        if booking:
            return redirect(url_for('passenger_view_receipt', pnr_no=pnr_no))
        else:
            flash("No records matching the provided PNR string found inside tracking database.", "danger")
    except Exception as e:
        flash(f"System Error: {str(e)}", "danger")
    return redirect(url_for('passenger_operation_action_gateways', operation_type='status-checking'))

@app.route('/passenger/op/cancel-ticket', methods=['GET', 'POST'])
def web_cancel_ticket():
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))
        
    # 🎯 FIX MULTI-METHOD SYNC VAULT: Fallback mapping checks both URL arguments query strings AND forms body vectors cleanly!
    pnr_no = request.args.get('pnr_no', '').strip()
    if not pnr_no:
        pnr_no = request.form.get('pnr_no', '').strip()
        
    action_step = request.args.get('action_step', '').strip()
    if not action_step:
        action_step = request.form.get('action_step', 'preview').strip()
    
    if not pnr_no:
        flash("Invalid tracking credentials payload missing parameter string token.", "danger")
        return redirect(url_for('passenger_dashboard'))
        
    try:
        # 1. Fetch live booking baseline verification metadata row details dynamically
        ticket_record = db.read_data_from_database("ticket_booking_details", {"pnr_no": pnr_no}, mode="one")
        if not ticket_record:
            flash("No active matched configuration record string PNR traces found inside systems logs.", "danger")
            return redirect(url_for('passenger_dashboard'))
            
        raw_profile = customer.authentication_customer(db, user_mobile)
        customer_profile_record = dict(raw_profile) if raw_profile else {}
        fetched_aadhar_id = customer_profile_record.get('id_number', '')
        
        # 🛡️ FLOW STEP A: SECURE INTERMEDIARY INDEPENDENT GATEWAY INTERFACE (OTP FORM MODE)
        if action_step == 'preview':
            if ticket_record.get('ticket_status') == 'cancelled':
                return redirect(url_for('passenger_view_receipt', pnr_no=pnr_no))

            import secrets
            simulated_cancel_otp = "".join(secrets.choice("0123456789") for _ in range(6))
            
            return render_template('ticket_receipt.html',
                                   ticket_data=ticket_record,
                                   customer_profile_record=customer_profile_record,
                                   aadhar_no=fetched_aadhar_id,
                                   cancel_flow_active=True,
                                   simulated_cancel_otp=simulated_cancel_otp)
                                   
        # 🎯 FLOW STEP B: PRODUCTION ENGINE SUBMISSION EXECUTION WITH PURE PERSISTENT CLEAN REDIRECTION VAULT
        elif action_step == 'execute_final_cancellation':
            db.update_small_quantity_data_dictionary("ticket_booking_details", {"ticket_status": "cancelled"}, {"pnr_no": pnr_no})
            
            try:
                refund = customer.cancel_ticket(db, pnr_no)
                if refund:
                    common.Ajith_Kumar_National_Bank.deposit_amount(refund)
            except:
                pass 
                
            flash("Ticket processed as cancelled successfully! Transformed state update complete.", "success")
            
            # 🎯 ZERO DUMP REDIRECT PERMANENT VAULT SYSTEM: Direct persistent route switch prevents dashboard jump completely!
            return redirect(url_for('passenger_view_receipt', pnr_no=pnr_no))
                                   
    except Exception as e:
        print(f"[AJITH AIRWAYS ENGINE SYSTEM FAULT CANCELLATION ENGINE]: {str(e)}")
        flash(f"Core Engine Operation Failed: {str(e)}", "danger")
        return redirect(url_for('passenger_dashboard'))

@app.route('/passenger-login')
def passenger_login_screen():
    session.pop('passenger_mobile', None)
    return render_template('passenger_login.html')

@app.route('/passenger/verify-mobile', methods=['POST'])
def passenger_verify_mobile():
    global db
    mobile = request.form.get('mobile_number').strip()
    
    if not common.validate_mobile_number(mobile):
        flash("Invalid Format: Please provide a valid 10-digit mobile number.", "danger")
        return redirect(url_for('passenger_login_screen'))
        
    existing_user = customer.authentication_customer(db, mobile)
    
    import secrets
    simulated_otp = "".join(secrets.choice("0123456789") for _ in range(6))
    print(f"[AJITH AIRWAYS SYSTEM LOGS] Dynamic Security OTP generated for {mobile}: {simulated_otp}")
    
    return render_template('passenger_login.html', 
                           otp_active=True, 
                           mobile_number=mobile, 
                           is_registered=bool(existing_user),
                           backend_otp=simulated_otp)

@app.route('/passenger/authenticate-session', methods=['POST'])
def passenger_authenticate_session():
    global db
    mobile = request.form.get('mobile_number').strip()
    user_otp = request.form.get('user_otp').strip()
    system_otp = request.form.get('backend_otp').strip()
    is_registered = request.form.get('is_registered') == 'True'
    
    if user_otp != system_otp:
        flash("Authentication Failure: The security OTP entered is invalid.", "danger")
        return render_template('passenger_login.html', otp_active=True, mobile_number=mobile, is_registered=is_registered, backend_otp=system_otp)
    
    if is_registered:
        session['passenger_mobile'] = mobile # 🎯 LOCK IN FLASK SESSION!
        user_data = customer.authentication_customer(db, mobile)
        flash(f"Welcome back, {user_data['full_name']}! Session encrypted.", "success")
        return redirect(url_for('passenger_dashboard'))
    else:
        flash("Identity Mismatch: Please register below to onboard.", "info")
        return render_template('passenger_signup.html', mobile_number=mobile)

@app.route('/passenger/execute-signup', methods=['POST'])
def passenger_execute_signup():
    global db
    mobile = request.form.get('mobile_number').strip()
    full_name = request.form.get('full_name').strip()
    gender = request.form.get('gender').strip()
    dob = request.form.get('date_of_birth').strip()
    email = request.form.get('email_id').strip().lower()
    aadhar = request.form.get('aadhar_number').strip()
    emergency = request.form.get('emergency_contact').strip()
    
    if not common.name_validation(full_name):
        flash("Validation Mismatch: Name cannot contain special characters or numbers.", "danger")
        return render_template('passenger_signup.html', mobile_number=mobile)
        
    if not common.aadhar_number_validation(aadhar):
        flash("Validation Mismatch: Aadhar must be a clean 12-digit sequence.", "danger")
        return render_template('passenger_signup.html', mobile_number=mobile)
        
    try:
        calculated_age = common.calculate_age(dob)
        
        signup_payload = {
            "mobile_number": mobile, "full_name": full_name, "gender": gender,
            "age": calculated_age, "date_of_birth": dob, "email_id": email,
            "id_proof_type": "aadhar", "id_number": aadhar, "emergency_contact": emergency
        }
        
        customer.customer_details(db, signup_payload)
        session['passenger_mobile'] = mobile 
        flash("Onboarding Complete! Your profile has been initialized securely.", "success")
        return redirect(url_for('passenger_full_profile', mobile_number=mobile))
    except Exception as e:
        flash(f"Signup Pipeline Failed: {str(e)}", "danger")
        return render_template('passenger_signup.html', mobile_number=mobile)

@app.route('/passenger/profile/<mobile_number>')
def passenger_full_profile(mobile_number):
    global db
    if not db:
        return redirect(url_for('passenger_login_screen'))
        
    user_data = customer.authentication_customer(db, mobile_number)
    if not user_data:
        return redirect(url_for('passenger_login_screen'))
        
    historical_reservation_list = []
    try:
        historical_reservation_list = db.read_data_from_database(
            "ticket_booking_details", 
            conditions_columns_values={"customer_id": mobile_number}, 
            mode="all"
        )
        
        if historical_reservation_list:
            historical_reservation_list.sort(
                key=lambda ticket: ticket.get('booking_initiated_time') if ticket.get('booking_initiated_time') else '', 
                reverse=True
            )
            
    except Exception as query_err:
        print(f"[AJITH AIRWAYS SYSTEM WORKSPACE] History sorting database log error drop: {str(query_err)}")
        historical_reservation_list = []
        
    return render_template(
        'passenger_profile.html', 
        profile=user_data, 
        history_list=historical_reservation_list
    )

@app.route('/passenger/ticket-receipt/<pnr_no>')
def passenger_view_receipt(pnr_no):
    global db
    user_mobile = session.get('passenger_mobile', '').strip()
    
    if not user_mobile:
        flash("Session expired! Please login again.", "warning")
        return redirect(url_for('passenger_login_screen'))
        
    try:
        ticket_record = db.read_data_from_database("ticket_booking_details", {"pnr_no": pnr_no}, mode="one")
        
        raw_profile = customer.authentication_customer(db, user_mobile)
        
        customer_profile_record = {}
        if raw_profile:
            if isinstance(raw_profile, dict):
                customer_profile_record = raw_profile
            elif isinstance(raw_profile, (list, tuple)) and len(raw_profile) > 0:
                customer_profile_record = dict(raw_profile)
            else:
                try:
                    customer_profile_record = dict(raw_profile)
                except:
                    customer_profile_record = {
                        'full_name': raw_profile[1] if len(raw_profile) > 1 else "",
                        'id_number': raw_profile[7] if len(raw_profile) > 7 else ''
                    }

        fetched_aadhar_id = customer_profile_record.get('id_number', '') if customer_profile_record else ''
            
        if ticket_record:
            return render_template('ticket_receipt.html', 
                                   ticket_data=ticket_record, 
                                   aadhar_no=fetched_aadhar_id,
                                   customer_profile_record=customer_profile_record)
        else:
            flash("Ticket record not found inside system tables ledger.", "danger")
            return redirect(url_for('passenger_dashboard'))
    except Exception as e:
        print(f"[AJITH AIRWAYS ENGINE CRITICAL FAULT]: {str(e)}")
        flash(f"Error loading independent ticket pass engine: {str(e)}", "danger")
        return redirect(url_for('passenger_dashboard'))
    
if __name__ == '__main__':
    app.run(debug=True)