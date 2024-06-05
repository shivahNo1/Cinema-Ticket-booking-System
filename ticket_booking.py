import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import qrcode
import io
from PIL import Image
import re

uri = "mongodb+srv://shivano1:shivaips32567@cluster0.h1pqbge.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.Guvi_cinemas
records1 = db.customer_data
records2 = db.movie_list
records3 = db.bookings



# Define the title text
title_text = "GUVI CINEMAS"

# Use HTML/CSS to center align the title
st.markdown(
    f"""
    <h1 style='text-align: center; color: black;'>{title_text}</h1>
    """,
    unsafe_allow_html=True
)


# Define a function to get or create session state
def get_session_state():
    session_state = st.session_state
    if "logged_in" not in session_state:
        session_state.logged_in = False
    return session_state

#LOGIN FUNCTION
def login(x,y):
    
    session_state = get_session_state()
    if session_state.logged_in:
        return True
    st.info("New user? please register")
    
    if st.button("Login"):
        user_data = records1.find_one({"Email": x})
        
        if user_data:
            email = user_data.get("Email")
            pwd = user_data.get("Password")
            name = user_data.get("Name")
            if x == email and y == pwd:
                st.success("Login Successful")
                st.subheader("WELCOME TO GUVI CINEMAS")
                st.write("-----------------", "{}".format(name.upper()), "-----------------")
                session_state.logged_in = True
                return name  # Return name if login successful
            else:
                st.error("Invalid credentials. Please check your email/password.")
        else:
            st.error("User not found.")
    return None  # Return None if login failed


#REGISTER FUNCTION
def register():
    st.subheader("Register")
    name = st.text_input("Enter your name:", key="name_input_unique")
    email = st.text_input("Enter your email:", key="email_input_unique")
    ph = st.text_input("Enter your phone number:", key="ph_input_unique")
    password = st.text_input("Enter your password:", type='password', key="pass_input_unique2")
    re_pass = st.text_input("Re-enter your password:", type='password', key="repass_input_unique")

    uploaded_file = st.file_uploader("Upload your photo:", type=["jpg", "jpeg", "png"])

    if st.button("Register"):
        if not re.match(r"[^@]+@gmail\.com$", email):
            st.error("Invalid email format. Please enter a valid email address.")
            return

        if not ph.isdigit() or len(ph) != 10:
            st.error("Invalid phone number. Please enter a 10-digit number.")
            return

        if re_pass != password:
            st.error("Passwords do not match. Please re-enter.")
            return

        if uploaded_file is None:
            st.error("Please upload your photo.")
            return

        # Read the uploaded image file as bytes
        image_bytes = uploaded_file.read()

        # Convert the image bytes to PIL Image
        im = Image.open(io.BytesIO(image_bytes))

        # Converting the image to PNG format
        png_image = io.BytesIO()
        im.save(png_image, format='PNG')

        # Storing user data and image in MongoDB
        biodata = {
            "Image": png_image.getvalue(),
            "Name": name,
            "Email": email,
            "Phone Number": ph,
            "Password": password
        }
        #data insertion to mongo db
        records1.insert_one(biodata)
        st.success("Registration successful!")
        

#DISPLAYING MOVIES
def displaying_movies():
    st.subheader("Movies list")

    # Define a layout with three columns
    col1, col2, col3 = st.columns(3)

    # Load and display the first image
    with col1:
        image_leo = Image.open("C:/Users/shiva_p/OneDrive/Desktop/leo das.jpg")
        image_leo.thumbnail((300, 300))  # Resize the image
        st.image(image_leo, caption='Leo')

    # Load and display the second image
    with col2:
        image_mb = Image.open("C:/Users/shiva_p/Downloads/Manjummel Boys.jpeg")
        image_mb.thumbnail((300, 600))  # Resize the image
        st.image(image_mb, caption='Manjumeel boys')

    # Load and display the third image
    with col3:
        image_g = Image.open("C:/Users/shiva_p/OneDrive/Desktop/ghilli.jpg")
        image_g.thumbnail((300, 300))  # Resize the image
        st.image(image_g, caption='Ghilli')


#LEO
def show_selection_leo(x,y):
    
    st.subheader("SHOWS AVAILABLE:")
           
    st.info(" Morning show - [9:00 am]/ Afternoon show - [1:00 pm] / Evening show - [7:00 pm]") 
          
    show = st.selectbox("Select show: ", ["None","Morning", "Afternoon", "Evening"])

    s= None
    if show=='Morning':
        s= '9:00 am'
    elif show=='Afternoon':
        s= '1:00 pm'
    elif show=='Evening':
        s= '7:00 pm'       
    # Getting the document for the Morning, Afternoon, and Evening shows for leo
    selected_show = None
    if show.upper() == 'MORNING':
        selected_show = records2.find_one({"_id": 11})
    elif show.upper() == 'AFTERNOON':
        selected_show = records2.find_one({"_id": 12})
    elif show.upper() == 'EVENING':
        selected_show = records2.find_one({"_id": 13})
    elif show.upper() == 'NONE':
        st.error("please select the show! ")
        
    if selected_show:
        if selected_show.get("seat_capacity", 0) == 0:
            st.error("{} Show is not available".format(s))
        else:
            st.success("{} Show is available".format(s))
            total_seats = selected_show.get("seat_capacity")
            st.write("Total seats available is :", total_seats)

            tickets = st.text_input("Number of tickets to book: ", key="tic_input_unique")
            st.button("Confirm")
            if tickets:
                if tickets and selected_show.get("seat_capacity", 0) >= int(tickets):
                    st.success("Tickets Available")
                    confirmation = st.radio("Are you sure you want to book {} Tickets?".format(tickets), ("None","Yes", "No"))

                    if confirmation: 

                        if confirmation == 'Yes':
                            amount = st.text_input("Please enter the amount ₹{}: ".format(int(tickets) * 245), key="amt2_input_unique")
                            button=st.button("pay")
                        
                            
                            if amount:
                                if amount == str(int(tickets) * 245):  
                                    st.success("PAYMENT SUCCESSFUL")

                                    dt_string1 = datetime.now().strftime("%d/%m/%Y")
                                    dt_string2 = datetime.now().strftime("%H:%M:%S")

                                    st.write("******************************************************************")
                                    st.subheader("*GUVI CINEMAS*")
                                    st.markdown("###### Booking time: {} ---------- Booking date: {} ######".format(dt_string2, dt_string1))
                                    st.markdown("###### MOVIE: Leo ######")
                                    st.markdown("###### SHOWTIME: {} ######".format(s.upper()))
                                    st.markdown("###### Tickets: {} -------{} X ₹245--------------TOTAL AMOUNT PAID = ₹{}".format(tickets, tickets, int(tickets) * 245))

                                    qr_data = ("GUVI CINEMAS----Leo----{} SHOW----".format(s.upper()), tickets, "TICKETS")

                                    

                                    # Adjust error correction level to minimize size
                                    error_correction = qrcode.constants.ERROR_CORRECT_L

                                    img = qrcode.make(qr_data, error_correction=error_correction)

                                    # Convert the image to bytes
                                    img_bytes = io.BytesIO()
                                    img.save(img_bytes, format='PNG')

                                    # Display the QR code in Streamlit
                                    st.image(img_bytes, caption="QR Code", use_column_width=True)

                                    st.write("******************************************************************")


                                    my_query = {"_id": selected_show.get("_id")}
                                    update = {"$inc": {"seat_capacity": -int(tickets)}}
                                    records2.update_one(my_query, update)

                                    # Update record3 collection
                                    user_data = records1.find_one({"Email": x})
                                    name = user_data.get("Name")
                                    booking_data = {
                                        "customer_name": name,  
                                        "movie_name": "Leo",  
                                        "no_of_tickets": int(tickets),
                                        "total_amount_paid": int(tickets) * 245,
                                        "show_timing": s, 
                                        "booking_date": dt_string1,
                                        "booking_Time":dt_string2   
                                    }
                                    records3.insert_one(booking_data)
                                

                                else:
                                    st.error("WARNING: The amount you have PAID is insufficient or wrong. Please try booking again")
                        elif confirmation =='None':
                            st.error("please select yes/no")
                        else:
                            st.error("Please try booking again")
                            
                else:
                    st.error("SORRY TICKETS NOT AVAILABLE, TRY WITH LESSER TICKETS")
        




#MANJUMAL BOYS
def show_selection_mb(x,y):
    
    st.subheader("SHOWS AVAILABLE:")
           
    st.info(" Morning show - [9:00 am]/ Afternoon show - [1:00 pm] / Evening show - [7:00 pm]") 
          
    show = st.selectbox("Select show: ", ["None","Morning", "Afternoon", "Evening"])

    s= None
    if show=='Morning':
        s= '9:00 am'
    elif show=='Afternoon':
        s= '1:00 pm'
    elif show=='Evening':
        s= '7:00 pm'       
    # Getting the document for the Morning, Afternoon, and Evening shows for Manjumal Boys
    selected_show = None
    if show.upper() == 'MORNING':
        selected_show = records2.find_one({"_id": 21})
    elif show.upper() == 'AFTERNOON':
        selected_show = records2.find_one({"_id": 22})
    elif show.upper() == 'EVENING':
        selected_show = records2.find_one({"_id": 23})
    elif show.upper() == 'NONE':
        st.error("please select the show! ")
        
    if selected_show:
        if selected_show.get("seat_capacity", 0) == 0:
            st.error("{} Show is not available".format(s))
        else:
            st.success("{} Show is available".format(s))
            total_seats = selected_show.get("seat_capacity")
            st.write("Total seats available is :", total_seats)

            tickets = st.text_input("Number of tickets to book: ", key="ticket_input_unique")
            st.button("Confirm")
            if tickets:
                if tickets and selected_show.get("seat_capacity", 0) >= int(tickets):
                    st.success("Tickets Available")
                    confirmation = st.radio("Are you sure you want to book {} Tickets?".format(tickets), ("None","Yes", "No"))

                    if confirmation: 

                        if confirmation == 'Yes':
                            amount = st.text_input("Please enter the amount ₹{}: ".format(int(tickets) * 245), key="amt_input_unique")
                            button=st.button("pay")
                        
                            
                            if amount:
                                if amount == str(int(tickets) * 245):  
                                    st.success("PAYMENT SUCCESSFUL")

                                    dt_string1 = datetime.now().strftime("%d/%m/%Y")
                                    dt_string2 = datetime.now().strftime("%H:%M:%S")

                                    st.write("******************************************************************")
                                    st.subheader("*GUVI CINEMAS*")
                                    st.markdown("###### Booking time: {} ---------- Booking date: {} ######".format(dt_string2, dt_string1))
                                    st.markdown("###### MOVIE: Manjumal Boys ######")
                                    st.markdown("###### SHOWTIME: {} ######".format(s.upper()))
                                    st.markdown("###### Tickets: {} -------{} X ₹245--------------TOTAL AMOUNT PAID = ₹{}".format(tickets, tickets, int(tickets) * 245))

                                    a = ("GUVI CINEMAS----MANJUMAL-BOYS----{} SHOW----".format(s.upper()), tickets, "TICKETS")

                                    img = qrcode.make(a, box_size=5, border=2)
                                    img_bytes = io.BytesIO()
                                    img.save(img_bytes, format='PNG')
                                    st.image(img_bytes, caption="QR Code", use_column_width=True)

                                    st.write("******************************************************************")


                                    my_query = {"_id": selected_show.get("_id")}
                                    update = {"$inc": {"seat_capacity": -int(tickets)}}
                                    records2.update_one(my_query, update)


                                    # Update record3 collection
                                    user_data = records1.find_one({"Email": x})
                                    name = user_data.get("Name")
                                    booking_data = {
                                        "customer_name": name,  
                                        "movie_name": "Manjumal boys",  
                                        "no_of_tickets": int(tickets),
                                        "total_amount_paid": int(tickets) * 245,
                                        "show_timing": s,  
                                        "booking_date": dt_string1,
                                        "booking_Time":dt_string2   
                                    }
                                    records3.insert_one(booking_data)

                                else:
                                    st.error("WARNING: The amount you have PAID is insufficient or wrong. Please try booking again")
                        elif confirmation =='None':
                            st.error("please select yes/no")
                        else:
                            st.error("Please try booking again")
                            
                else:
                    st.error("SORRY TICKETS NOT AVAILABLE, TRY WITH LESSER TICKETS")

#GHILLI
def show_selection_ghilli(x,y):
    
    st.subheader("SHOWS AVAILABLE:")
           
    st.info(" Morning show - [9:00 am]/ Afternoon show - [1:00 pm] / Evening show - [7:00 pm]") 
          
    show = st.selectbox("Select show: ", ["None","Morning", "Afternoon", "Evening"])

    s= None
    if show=='Morning':
        s= '9:00 am'
    elif show=='Afternoon':
        s= '1:00 pm'
    elif show=='Evening':
        s= '7:00 pm'       
    # Get the document for the Morning, Afternoon, and Evening shows for Ghilli
    selected_show = None
    if show.upper() == 'MORNING':
        selected_show = records2.find_one({"_id": 31})
    elif show.upper() == 'AFTERNOON':
        selected_show = records2.find_one({"_id": 32})
    elif show.upper() == 'EVENING':
        selected_show = records2.find_one({"_id": 33})
    elif show.upper() == 'NONE':
        st.error("please select the show! ")
        
    if selected_show:
        if selected_show.get("seat_capacity", 0) == 0:
            st.error("{} Show is not available".format(s))
        else:
            st.success("{} Show is available".format(s))
            total_seats = selected_show.get("seat_capacity")
            st.write("Total seats available is :", total_seats)

            tickets = st.text_input("Number of tickets to book: ", key="ticc_input_unique")
            st.button("Confirm")
            if tickets:
                if tickets and selected_show.get("seat_capacity", 0) >= int(tickets):
                    st.success("Tickets Available")
                    confirmation = st.radio("Are you sure you want to book {} Tickets?".format(tickets), ("None","Yes", "No"))

                    if confirmation: 

                        if confirmation == 'Yes':
                            amount = st.text_input("Please enter the amount ₹{}: ".format(int(tickets) * 245), key="amt3_input_unique")
                            button=st.button("pay")
                        
                            
                            if amount:
                                if amount == str(int(tickets) * 245):  
                                    st.success("PAYMENT SUCCESSFUL")

                                    dt_string1 = datetime.now().strftime("%d/%m/%Y")
                                    dt_string2 = datetime.now().strftime("%H:%M:%S")

                                    st.write("******************************************************************")
                                    st.subheader("*GUVI CINEMAS*")
                                    st.markdown("###### Booking time: {} ---------- Booking date: {} ######".format(dt_string2, dt_string1))
                                    st.markdown("###### MOVIE: Ghilli ######")
                                    st.markdown("###### SHOWTIME: {} ######".format(s.upper()))
                                    st.markdown("###### Tickets: {} -------{} X ₹245--------------TOTAL AMOUNT PAID = ₹{}".format(tickets, tickets, int(tickets) * 245))

                                    a = ("GUVI CINEMAS----GHILLI----{} SHOW----".format(s.upper()), tickets, "TICKETS")

                                    img = qrcode.make(a, box_size=5, border=2)
                                    img_bytes = io.BytesIO()
                                    img.save(img_bytes, format='PNG')
                                    st.image(img_bytes, caption="QR Code", use_column_width=True)

                                    st.write("******************************************************************")


                                    my_query = {"_id": selected_show.get("_id")}
                                    update = {"$inc": {"seat_capacity": -int(tickets)}}
                                    records2.update_one(my_query, update)


                                    # Update record3 collection
                                    user_data = records1.find_one({"Email": x})
                                    name = user_data.get("Name")
                                    booking_data = {
                                        "customer_name": name,  
                                        "movie_name": "Ghilli",  
                                        "no_of_tickets": int(tickets),
                                        "total_amount_paid": int(tickets) * 245,
                                        "show_timing": s,  
                                        "booking_date": dt_string1,
                                        "booking_Time":dt_string2  
                                    }
                                    records3.insert_one(booking_data)

                                else:
                                    st.error("WARNING: The amount you have PAID is insufficient or wrong. Please try booking again")
                        elif confirmation =='None':
                            st.error("please select yes/no")
                        else:
                            st.error("Please try booking again")
                            
                else:
                    st.error("SORRY TICKETS NOT AVAILABLE, TRY WITH LESSER TICKETS")



def main():
    
    choice = st.sidebar.radio("Login/Register/Exit", ["Login", "Register","Exit"], key="choice_key_unique_key")
    
    if choice == "Login":
        x = st.text_input("Enter your mailid: ", key="mail_input_unique")
        y = st.text_input("Enter your password: ", type='password', key="pass_input_unique")

        
        if login(x,y):  # Check if login was successful
            displaying_movies()
            
            # Generate a fixed key for movie_selection
            movie_selection_key = "movie_selection"
            movie_selection = st.selectbox("Select movie:", ["None", "Leo", "Manjummel Boys", "Ghilli"], key=movie_selection_key)
            
            if movie_selection == "Leo":
                show_selection_leo(x,y)
            elif movie_selection == "Manjummel Boys":
                show_selection_mb(x,y)
            elif movie_selection == "Ghilli":
                show_selection_ghilli(x,y)
            elif movie_selection == 'None':
                st.write("Please select your movie!")
                    
    elif choice == "Register":
        register()
    elif choice == "Exit":
        st.subheader("Thank you for choosing Guvi cinemas! Have a great day ")

main()