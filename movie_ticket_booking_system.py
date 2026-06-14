from collections import deque


class User:
    def __init__(self, name):
        self.name = name

class Seat:
    def __init__(self, row, number, price, show):
        self.row = row
        self.number = number
        self.price = price
        self.show = show
        self.booked = False
        
    def book(self):
        self.booked = True

class Ticket:
    def __init__(self, user, seat):
        self.user = user
        self.seat = seat

class CinemaHall:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self._shows = []
        
    def addShow(self, show):
        self._shows.append(show)
        show.cinema_hall = self
        
    def getShow(self, i):
        return self._shows[i]
    
    def displayAllShows(self):
        for i, show in enumerate(self._shows):
            print(f"{i}: {show.name} at {show.time}")

class Show:
    def __init__(self, name, time, cinema_hall = None):
        self.name = name
        self.time = time
        self.cinema_hall = cinema_hall
        self._seats = deque()
        
    def addSeat(self, row, number, price):
        seat = Seat(row, number, price, self)
        self._seats.append(seat)
        
    def bookSeats(self, count):
        if len(self._seats) < count:
            return (False, [])
        
        booked_seats = []
        for i in range(count):
            seat = self._seats.popleft()
            seat.book()
            booked_seats.append(seat)
            
        return (True, booked_seats)
        
class PaymentProcessor:
    def process(self, account_number, amount):
        print("Payment completed.")

class BookingController:
    def __init__(self):
        self._cinema_halls = []
        self.payment_processor = PaymentProcessor()
        
    def addCinemaHall(self, cinema_hall):
        self._cinema_halls.append(cinema_hall)
        
    def getCinemaHall(self, i):
        return self._cinema_halls[i]
        
    def displayAllCinemaHalls(self):
        for i, cinema_hall in enumerate(self._cinema_halls):
            print(f"{i}: {cinema_hall.name} ({cinema_hall.location})")
            
    def displayAllShows(self, cinema_hall):
        self.cinema_hall.displayAllShows()
        
    def processPayment(self, account_number, amount):
        self.payment_processor.process(account_number, amount)
        
    def bookTickets(self, user, show, count):
        success, booked_seats = show.bookSeats(count)
        if not success:
            return (False, 0, [])
        
        amount = 0
        tickets = []
        for seat in booked_seats:
            ticket = Ticket(user, seat)
            tickets.append(ticket)
            amount += seat.price
            
        return (True, amount, tickets)
        
    def displayBookingSeats(self, tickets):
        for i, ticket in enumerate(tickets):
            seat = ticket.seat
            print(f"{i}: Row {seat.row}, Number {seat.number}")
        
    
if __name__ == "__main__":
    booking_controller = BookingController()
    
    # Cinema Hall 1
    cinema_hall = CinemaHall("New York Cinema Hall", "New York")
    # Show 1
    show = Show("Transformers", "10:00 am")
    show.addSeat(1, 1, 150.00)
    show.addSeat(2, 1, 250.00)
    cinema_hall.addShow(show)
    # Show 2
    show = Show("Lord of the Rings", "12:30 pm")
    show.addSeat(1, 1, 180.00)
    cinema_hall.addShow(show)
    booking_controller.addCinemaHall(cinema_hall)
    
    # Cinema Hall 2
    cinema_hall = CinemaHall("Chicago Cinema Hall", "Chicago")
    # Show 1
    show = Show("Oppenheimer", "3:00 pm")
    show.addSeat(1, 1, 720.00)
    show.addSeat(1, 2, 350.00)
    show.addSeat(2, 1, 580.00)
    cinema_hall.addShow(show)
    booking_controller.addCinemaHall(cinema_hall)
    
    print("Welcome to Show Booking Service.")
    print()
    
    while True:
        print("To continue, press enter.")
        print("To exit, type 'exit'.")
        command = input()
        if command == "exit":
            break
        
        print("Here are all the cinema halls -")
        booking_controller.displayAllCinemaHalls()
        print()
        i = int(input("Type the index of the cinema hall: "))
        cinema_hall = booking_controller.getCinemaHall(i)
        
        print("Here are all the shows -")
        cinema_hall.displayAllShows()
        print()
        i = int(input("Type the index of the show: "))
        show = cinema_hall.getShow(i)
        
        count = int(input("Number of seats you want to book: "))
        user_name = input("Enter your name: ")
        user = User(user_name)
        success, amount, tickets = booking_controller.bookTickets(user, show, count)
        if not success:
            print("Not enough tickets available.")
            print()
            continue
        
        print(f"Total amount: {amount}")
        account_number = input("Account Number: ")
        booking_controller.processPayment(account_number, amount)
        print("Here are your seats -")
        booking_controller.displayBookingSeats(tickets)
        print()
