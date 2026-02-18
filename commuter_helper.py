import json
import os
from datetime import datetime


DATA_FILE = "commuter_data.json"


# this is data classes 

class User:
    def __init__(self, user_id, name, date_of_birth, contact_number, role):
        self.user_id = user_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.contact_number = contact_number
        self.role = role

    def to_dict(self):
        return self.__dict__


class Driver(User):
    def __init__(self, user_id, name, date_of_birth, contact_number, car_model):
        super().__init__(user_id, name, date_of_birth, contact_number, "Driver")
        self.car_model = car_model
        self.rating = 0.0

    def to_dict(self):
        return self.__dict__


class Commuter(User):
    def __init__(self, user_id, name, date_of_birth, contact_number, preferred_location):
        super().__init__(user_id, name, date_of_birth, contact_number, "Commuter")
        self.preferred_location = preferred_location

    def to_dict(self):
        return self.__dict__


class RideRequest:
    def __init__(self, request_id, commuter_id, pickup_location, destination, time):
        self.request_id = request_id
        self.commuter_id = commuter_id
        self.pickup_location = pickup_location
        self.destination = destination
        self.time = time
        self.status = "Pending"

    def to_dict(self):
        return self.__dict__


class Review:
    def __init__(self, review_id, driver_id, rating, comments):
        self.review_id = review_id
        self.driver_id = driver_id
        self.rating = rating
        self.comments = comments

    def to_dict(self):
        return self.__dict__


#file handling functions

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "rides": [], "reviews": []}

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


#basic features 

def register_user(data):
    user_id = len(data["users"]) + 1
    name = input("Enter Name: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    contact = input("Enter Contact Number: ").strip()
    role = input("Enter Role (Driver/Commuter): ").strip().lower()

    if role == "driver":
        car_model = input("Enter Car Model: ").strip()
        user = Driver(user_id, name, dob, contact, car_model)
    elif role == "commuter":
        location = input("Enter Preferred Location: ").strip()
        user = Commuter(user_id, name, dob, contact, location)
    else:
        print("Invalid role selected.")
        return

    data["users"].append(user.to_dict())
    save_data(data)
    print("User registered successfully.")


def post_ride_request(data, commuter_id):
    request_id = len(data["rides"]) + 1
    pickup = input("Pickup Location: ").strip()
    destination = input("Destination: ").strip()
    time = input("Time (HH:MM): ").strip()

    ride = RideRequest(request_id, commuter_id, pickup, destination, time)
    data["rides"].append(ride.to_dict())
    save_data(data)
    print("Ride request posted successfully.")


def view_pending_rides(data):
    for ride in data["rides"]:
        if ride["status"] == "Pending":
            print(ride)


def accept_ride_request(data, driver_id):
    view_pending_rides(data)
    ride_id = int(input("Enter Ride ID to accept: "))

    for ride in data["rides"]:
        if ride["request_id"] == ride_id and ride["status"] == "Pending":
            ride["status"] = "Accepted"
            ride["driver_id"] = driver_id
            save_data(data)
            print("Ride accepted successfully.")
            return

    print("Invalid ride selection.")


def submit_review(data):
    review_id = len(data["reviews"]) + 1
    driver_id = int(input("Enter Driver ID: "))
    rating = float(input("Enter Rating (1-5): "))
    comments = input("Enter Comments: ")

    if rating < 1 or rating > 5:
        print("Invalid rating.")
        return

    review = Review(review_id, driver_id, rating, comments)
    data["reviews"].append(review.to_dict())
    save_data(data)
    print("Review submitted successfully.")


#main function to run the system

def main():
    data = load_data()

    while True:
        print("\n===== Commuter Helper =====")
        print("1. Register")
        print("2. Post Ride Request")
        print("3. Accept Ride Request")
        print("4. Submit Review")
        print("5. Exit")

        choice = input("Select option: ")

        if choice == "1":
            register_user(data)

        elif choice == "2":
            commuter_id = int(input("Enter Commuter ID: "))
            post_ride_request(data, commuter_id)

        elif choice == "3":
            driver_id = int(input("Enter Driver ID: "))
            accept_ride_request(data, driver_id)

        elif choice == "4":
            submit_review(data)

        elif choice == "5":
            print("Exiting system.")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()