# Guvi Cinemas

Welcome to Guvi Cinemas, a streamlined movie ticket booking system built with Streamlit and MongoDB. This project enables users to register, login, browse available movies, and book tickets for their preferred shows.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)


## Features

- **User Authentication:** Users can register with their name, email, phone number, and password. Existing users can log in securely to access the booking system.
- **Movie Listings:** Displays a list of currently available movies with images and basic details.
- **Show Selection:** Users can select a movie and choose from available showtimes to book tickets.
- **Ticket Booking:** Enables users to book tickets for their desired showtime, with real-time updates on seat availability.
- **Payment Integration:** Simulates a payment gateway for ticket purchases, ensuring a seamless booking experience.
- **QR Code Generation:** Generates QR codes for each ticket booking, facilitating easy access to tickets at the cinema.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- Streamlit
- PyMongo
- Pillow (PIL)
- qrcode
- MongoDB Atlas (or local MongoDB server)

## Installation

1. Clone the repository:
```sh
git clone <repository-url>
```

2. Install the dependencies:
```sh
pip install -r requirements.txt
```

3. Run the application:
 ```sh
streamlit run ticket_booking.py
 ```

## Usage

1. Register as a new user or log in with existing credentials.
2. Browse the list of available movies and select your preferred movie.
3. Choose a showtime and enter the number of tickets you want to book.
4. Confirm the booking and complete the payment process.
5. Upon successful booking, a QR code will be generated for your tickets.

## Screenshots

![Login Page](screenshots/login.png)
*Login Page*

![Movie Selection](screenshots/movie_selection.png)
*Movie Selection*

![Ticket Booking](screenshots/ticket_booking.png)
*Ticket Booking*

## Contributing

Contributions are welcome! If you have any suggestions, bug fixes, or feature enhancements, feel free to submit a pull request.











