from datetime import datetime
from collections import defaultdict, deque


class ParkingTicket:
    available_id = 1
    
    def __init__(self, name, vehicle, parking_slot):
        self.id = self.getNewId()
        self.name = name
        self.vehicle = vehicle
        self.parking_slot = parking_slot
        self.entry_time = datetime.now()
        self.exit_time = None
        self.exited = False
        self.payment = None
        
    def getNewId(self):
        new_id = ParkingTicket.available_id
        ParkingTicket.available_id += 1
        return new_id

    def initExit(self):
        self.exit_time = datetime.now()
        self.payment = Payment(self)
        
    def completePayment(self, payment_method, account_number):
        self.payment.completePayment(payment_method, account_number)
        
    def exit(self):
        self.exited = True


class Payment:
    fee_structures = {
        "bike": {"base": 100, "hour": 50},
        "car": {"base": 500, "hour": 250},
        "truck": {"base": 1000, "hour": 500}
    }
    
    def __init__(self, parking_ticket):
        self.fee = self.calculateFee(parking_ticket)
        self.payment_method = None
        self.payment_done = False
        
    def calculateFee(self, parking_ticket):
        vehicle_type = parking_ticket.vehicle.type
        base_fee = Payment.fee_structures[vehicle_type]["base"]
        hour_fee = Payment.fee_structures[vehicle_type]["hour"]
        duration = (parking_ticket.exit_time - parking_ticket.entry_time).total_seconds()
        return base_fee + hour_fee * duration
        
    def completePayment(self, payment_method, account_number):
        self.payment_method = payment_method
        self.executePayment(payment_method, account_number)
        self.payment_done = True
        
    # Deduct the fee amount from the given account number using the given payment method.
    def executePayment(self, payment_method, account_number):
        return True


class ParkingSpace:
    def __init__(self, parking_slots_details):
        self.available_slots = defaultdict(deque)
        self.generateParkingSlots(parking_slots_details)
        
    def generateParkingSlots(self, parking_slots_details):
        for slot_type, floor, section, number in parking_slots_details:
            parking_slot = ParkingSlot(slot_type, floor, section, number)
            self.available_slots[slot_type].append(parking_slot)
        
    def getParkingSlot(self, vehicle_type):
        if len(self.available_slots[vehicle_type]) == 0:
            return None
        return self.available_slots[vehicle_type].popleft()
        
    def freeParkingSlot(self, parking_slot):
        self.available_slots[parking_slot.type].append(parking_slot)


class ParkingSlot:
    available_id = 1
    
    def __init__(self, slot_type, floor, section, number):
        self.id = self.getNewId()
        self.type = slot_type
        self.floor = floor
        self.section = section
        self.number = number
        
    def getNewId(self):
        new_id = ParkingSlot.available_id
        ParkingSlot.available_id += 1
        return new_id


class Vehicle:
    def __init__(self, vehicle_type, license_plate):
        self.type = vehicle_type
        self.license_plate = license_plate
        
        
class ParkingController:
    def __init__(self, parking_slots_details):
        self.parking_tickets = dict()
        self.parking_space = ParkingSpace(parking_slots_details)
        
    def startEntryProcess(self, vehicle_type):
        return self.parking_space.getParkingSlot(vehicle_type)

    def finishEntryProcess(self, name, parking_slot, vehicle_type, vehicle_license_plate):
        vehicle = Vehicle(vehicle_type, vehicle_license_plate)
        parking_ticket = ParkingTicket(name, vehicle, parking_slot)
        self.parking_tickets[parking_ticket.id] = parking_ticket
        return parking_ticket.id
        
    def startExitProcess(self, parking_ticket):
        parking_ticket.initExit()
        
    def performPayment(self, parking_ticket, payment_method, account_number):
        parking_ticket.completePayment(payment_method, account_number)
        
    def finishExitProcess(self, parking_ticket):
        parking_ticket.exit()
        self.parking_space.freeParkingSlot(parking_ticket.parking_slot)
        
    def start(self):
        while True:
            command = input("Enter action: ").lower()
            match command:
                case "entry":
                    vehicle_type = input("Enter vehicle type: ")
                    parking_slot = self.startEntryProcess(vehicle_type)
                    if not parking_slot:
                        print("No free parking slots available!!")
                        print()
                        continue
                    
                    entry_details = input("Enter 'name', 'vehicle license plate' separated by commas: \n")
                    entry_details = [item.strip() for item in entry_details.split(",")]
                    name, vehicle_license_plate = entry_details
                    parking_ticket_id = self.finishEntryProcess(name, parking_slot, vehicle_type, vehicle_license_plate)
                    print("Parking slot successfully booked.")
                    print(f"Your parking ticket ID: {parking_ticket_id}.")
                    print()
                case "exit":
                    parking_ticket_id = input("Enter parking ticket ID: ")
                    parking_ticket_id = int(parking_ticket_id)
                    if parking_ticket_id not in self.parking_tickets:
                        print("No parking ticket exists with the given ID!!")
                        print()
                        continue
                    
                    parking_ticket = self.parking_tickets[parking_ticket_id]
                    if parking_ticket.exited:
                        print("You have already exited!!")
                        print()
                        continue
                    
                    self.startExitProcess(parking_ticket)
                    
                    print(f"Your total payment is: ${parking_ticket.payment.fee}")
                    payment_details = input("Enter 'payment method (cash / card / upi)', 'account number' separated by commas: \n")
                    payment_details = [item.strip() for item in payment_details.split(",")]
                    payment_method, account_number = payment_details
                    self.performPayment(parking_ticket, payment_method, account_number)
                    print("Your payment has been successfully completed.")
                    print("You can now exit.")
                    print()
                    
                    self.finishExitProcess(parking_ticket)
                case "quit":
                    break
                case _:
                    continue


bike_slots_details = [("bike", "1", "A", "01"), ("bike", "1", "A", "02"), ("bike", "1", "B", "03"), ("bike", "1", "B", "04")]
car_slots_details = [("car", "2", "A", "05"), ("car", "2", "A", "06"), ("car", "2", "B", "07"), ("car", "2", "B", "08")]
truck_slots_details = [("truck", "3", "A", "09"), ("truck", "3", "A", "10"), ("truck", "3", "B", "11"), ("truck", "3", "B", "12")]
controller = ParkingController(bike_slots_details + car_slots_details + truck_slots_details)
controller.start()
