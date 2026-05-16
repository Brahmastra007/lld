from abc import ABC, abstractmethod


class Item:
    available_id = 1
    
    def __init__(self, name, price, quantity):
        self.id = self.getAvailableId()
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @classmethod
    def getAvailableId(cls):
        new_id = cls.available_id
        cls.available_id += 1
        return new_id


class OrderItem:
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity


class PaymentStrategy(ABC):
    @abstractmethod
    def processPayment(self, amount):
        pass

class CashPaymentStrategy(PaymentStrategy):
    def processPayment(self, amount):
        # Process cash payment using the account details
        return True

class CardPaymentStrategy(PaymentStrategy):
    def processPayment(self, amount):
        # Process card payment using the account details
        return True
        
class UPIPaymentStrategy(PaymentStrategy):
    def processPayment(self, amount):
        # Process UPI payment using the account details
        return True


class Payment:
    def __init__(self, amount, payment_strategy):
        self.amount = amount
        self.payment_strategy = payment_strategy
        self.paid = False
        
    def processPayment(self):
        self.payment_strategy.processPayment(self.amount)
        self.paid = True


class Order:
    available_id = 1
    
    def __init__(self, order_details, inventory):
        self.id = self.getAvailableId()
        self.order_items = []
        self.buildOrder(order_details, inventory)
        self.amount = 0
        self.payment = None
        
    @classmethod
    def getAvailableId(cls):
        new_id = cls.available_id
        cls.available_id += 1
        return new_id
        
    def buildOrder(self, order_details, inventory):
        for name, quantity in order_details:
            item = inventory.getItemByName(name)
            order_item = OrderItem(item, quantity)
            self.order_items.append(order_item)
        
    def processOrder(self):
        self.amount = 0
        for order_item in self.order_items:
            self.amount += order_item.item.price * order_item.quantity
        
    def createPayment(self, payment_method):
        payment_strategy = None
        match payment_method:
            case "cash":
                payment_strategy = CashPaymentStrategy()
            case "card":
                payment_strategy = CardPaymentStrategy()
            case "upi":
                payment_strategy = UPIPaymentStrategy()
                
        self.payment = Payment(self.amount, payment_strategy)


class Inventory:
    def __init__(self, items_details):
        self.items = []
        self.item_map = dict()
        self.buildInventory(items_details)
        
    def buildInventory(self, items_details):
        for name, price, quantity in items_details:
            item = Item(name, price, quantity)
            self.items.append(item)
            self.item_map[name] = item
            
    def printInventory(self):
        for i, item in enumerate(self.items):
            print(f"{i + 1}) {item.name}: Price = ${item.price}, Available Quantity = {item.quantity}")
            
    def getItems(self):
        return self.items
        
    def getItemByName(self, name):
        return self.item_map[name]
        
    def checkItemAvailability(self, item_name, quantity):
        return quantity <= self.item_map[item_name].quantity
        
    def fulfillOrderFromInventory(self, order):
        for order_item in order.order_items:
            order_item.item.quantity -= order_item.quantity


class VendingMachine:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, items_details):
        if self._initialized:
            return
        self.current_order = None
        self.orders = []
        self.inventory = Inventory(items_details)
        self.__class__._initialized = True
            
    def checkItemAvailability(self, item_name, quantity):
        return self.inventory.checkItemAvailability(item_name, quantity)

    def processOrder(self, order_details):
        self.current_order = Order(order_details, self.inventory)
        self.current_order.processOrder()
        return self.current_order.amount
        
    def processPayment(self, payment_method):
        self.current_order.createPayment(payment_method)
        self.current_order.payment.processPayment()
        
    def dispenseOrder(self):
        # Dispense the order items
        return True
        
    def finishOrder(self):
        self.inventory.fulfillOrderFromInventory(self.current_order)
        self.orders.append(self.current_order)
        self.current_order = None


class VendingMachineController:
    def __init__(self, items_details):
        self.vending_machine = VendingMachine(items_details)
        
    def start(self):
        print("WELCOME!!")
        print("This is a vending machine simulator.")
        print()
        
        while True:
            print("To start selecting items, press enter.")
            print("To exit the vending machine, type 'quit'.")
            
            action = input()
            if action == "quit":
                break
            
            print("Available inventory:")
            self.vending_machine.inventory.printInventory()
            print()
            
            order_details = []
            print("You can now select the items.")
            print("In individual lines, type the name of item and quantity separated by commas.")
            print("When you are done, press double enter.")
            
            while True:
                y = input()
                if len(y.strip()) == 0:
                    break
                
                y = [x.strip() for x in y.split(",")]
                name, quantity = y[0], int(y[1])
                if not self.vending_machine.checkItemAvailability(name, quantity):
                    print("The provided quantity is not available.")
                else:
                    order_details.append((name, quantity))
                    
            if len(order_details) == 0:
                print("You have not selected any items!!")
                print()
            else:
                print("Your order is being processed. Please wait...")
                amount = self.vending_machine.processOrder(order_details)
                print(f"You have to pay: ${amount}")
                
                payment_method = input("Please provide your preferred payment method (cash / card / upi): ")
                print("Your payment is being processed. Please wait...")
                self.vending_machine.processPayment(payment_method)
                print("Payment has been successfully completed.")
                
                print("Dispensing items...")
                self.vending_machine.dispenseOrder()
                print("All items dispensed. Have a great day!!")
                print()
                self.vending_machine.finishOrder()
                

items_details = [("item1", 20.0, 2), ("item2", 50.0, 3)]
controller = VendingMachineController(items_details)
controller.start()
