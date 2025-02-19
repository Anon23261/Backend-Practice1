from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

# Customer Table
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(Text, nullable=True)

    vehicles = relationship("Vehicle", back_populates="owner")
    service_tickets = relationship("ServiceTicket", back_populates="customer")

# Vehicle Table
class Vehicle(Base):
    __tablename__ = 'vehicles'

    vin = Column(String(17), primary_key=True)  # Vehicle Identification Number (VIN)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)

    owner = relationship("Customer", back_populates="vehicles")
    service_tickets = relationship("ServiceTicket", back_populates="vehicle")

# Mechanic Table
class Mechanic(Base):
    __tablename__ = 'mechanics'

    mechanic_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    salary = Column(DECIMAL, nullable=False)

    service_tickets = relationship("ServiceMechanic", back_populates="mechanic")

# Service Ticket Table
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String(17), ForeignKey('vehicles.vin'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    ticket_date = Column(DateTime, default=datetime.datetime.utcnow)
    service_description = Column(Text, nullable=False)
    cost = Column(DECIMAL, nullable=False)

    vehicle = relationship("Vehicle", back_populates="service_tickets")
    customer = relationship("Customer", back_populates="service_tickets")
    mechanics = relationship("ServiceMechanic", back_populates="service_ticket")

# Service Mechanic Table (Many-to-many relationship between Service Tickets and Mechanics)
class ServiceMechanic(Base):
    __tablename__ = 'service_mechanics'

    service_ticket_id = Column(Integer, ForeignKey('service_tickets.ticket_id'), primary_key=True)
    mechanic_id = Column(Integer, ForeignKey('mechanics.mechanic_id'), primary_key=True)

    service_ticket = relationship("ServiceTicket", back_populates="mechanics")
    mechanic = relationship("Mechanic", back_populates="service_tickets")


def create_customer(session, first_name, last_name, phone, email, address=None):
    new_customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address)
    session.add(new_customer)
    session.commit()
    return new_customer


def read_customers(session):
    return session.query(Customer).all()


def update_customer(session, customer_id, **kwargs):
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    for key, value in kwargs.items():
        setattr(customer, key, value)
    session.commit()


def delete_customer(session, customer_id):
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    session.delete(customer)
    session.commit()


def create_vehicle(session, vin, customer_id, make, model, year, license_plate):
    new_vehicle = Vehicle(vin=vin, customer_id=customer_id, make=make, model=model, year=year, license_plate=license_plate)
    session.add(new_vehicle)
    session.commit()
    return new_vehicle


def read_vehicles(session):
    return session.query(Vehicle).all()


def update_vehicle(session, vin, **kwargs):
    vehicle = session.query(Vehicle).filter_by(vin=vin).first()
    for key, value in kwargs.items():
        setattr(vehicle, key, value)
    session.commit()


def delete_vehicle(session, vin):
    vehicle = session.query(Vehicle).filter_by(vin=vin).first()
    session.delete(vehicle)
    session.commit()


def create_mechanic(session, first_name, last_name, email, phone=None, salary=None):
    new_mechanic = Mechanic(first_name=first_name, last_name=last_name, email=email, phone=phone, salary=salary)
    session.add(new_mechanic)
    session.commit()
    return new_mechanic


def read_mechanics(session):
    return session.query(Mechanic).all()


def update_mechanic(session, mechanic_id, **kwargs):
    mechanic = session.query(Mechanic).filter_by(mechanic_id=mechanic_id).first()
    for key, value in kwargs.items():
        setattr(mechanic, key, value)
    session.commit()


def delete_mechanic(session, mechanic_id):
    mechanic = session.query(Mechanic).filter_by(mechanic_id=mechanic_id).first()
    session.delete(mechanic)
    session.commit()


def create_service_ticket(session, vin, customer_id, ticket_date, service_description, cost):
    new_service_ticket = ServiceTicket(vin=vin, customer_id=customer_id, ticket_date=ticket_date, service_description=service_description, cost=cost)
    session.add(new_service_ticket)
    session.commit()
    return new_service_ticket


def read_service_tickets(session):
    return session.query(ServiceTicket).all()


def update_service_ticket(session, ticket_id, **kwargs):
    service_ticket = session.query(ServiceTicket).filter_by(ticket_id=ticket_id).first()
    for key, value in kwargs.items():
        setattr(service_ticket, key, value)
    session.commit()


def delete_service_ticket(session, ticket_id):
    service_ticket = session.query(ServiceTicket).filter_by(ticket_id=ticket_id).first()
    session.delete(service_ticket)
    session.commit()


def create_service_mechanic(session, service_ticket_id, mechanic_id):
    new_service_mechanic = ServiceMechanic(service_ticket_id=service_ticket_id, mechanic_id=mechanic_id)
    session.add(new_service_mechanic)
    session.commit()
    return new_service_mechanic


def read_service_mechanics(session):
    return session.query(ServiceMechanic).all()


def update_service_mechanic(session, service_ticket_id, mechanic_id, **kwargs):
    service_mechanic = session.query(ServiceMechanic).filter_by(service_ticket_id=service_ticket_id, mechanic_id=mechanic_id).first()
    for key, value in kwargs.items():
        setattr(service_mechanic, key, value)
    session.commit()


def delete_service_mechanic(session, service_ticket_id, mechanic_id):
    service_mechanic = session.query(ServiceMechanic).filter_by(service_ticket_id=service_ticket_id, mechanic_id=mechanic_id).first()
    session.delete(service_mechanic)
    session.commit()


def main():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Add Vehicle")
        print("6. View Vehicles")
        print("7. Update Vehicle")
        print("8. Delete Vehicle")
        print("9. Add Mechanic")
        print("10. View Mechanics")
        print("11. Update Mechanic")
        print("12. Delete Mechanic")
        print("13. Add Service Ticket")
        print("14. View Service Tickets")
        print("15. Update Service Ticket")
        print("16. Delete Service Ticket")
        print("17. Add Service Mechanic")
        print("18. View Service Mechanics")
        print("19. Update Service Mechanic")
        print("20. Delete Service Mechanic")
        print("21. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            address = input("Address (optional): ")
            create_customer(session, first_name, last_name, phone, email, address)
            print("Customer added!")

        elif choice == '2':
            customers = read_customers(session)
            for customer in customers:
                print(f'{customer.customer_id}: {customer.first_name} {customer.last_name}')

        elif choice == '3':
            customer_id = int(input("Customer ID to update: "))
            first_name = input("New First Name (leave blank to skip): ")
            last_name = input("New Last Name (leave blank to skip): ")
            phone = input("New Phone (leave blank to skip): ")
            email = input("New Email (leave blank to skip): ")
            update_customer(session, customer_id, first_name=first_name or None, last_name=last_name or None, phone=phone or None, email=email or None)
            print("Customer updated!")

        elif choice == '4':
            customer_id = int(input("Customer ID to delete: "))
            delete_customer(session, customer_id)
            print("Customer deleted!")

        elif choice == '5':
            vin = input("VIN: ")
            customer_id = int(input("Customer ID: "))
            make = input("Make: ")
            model = input("Model: ")
            year = int(input("Year: "))
            license_plate = input("License Plate: ")
            create_vehicle(session, vin, customer_id, make, model, year, license_plate)
            print("Vehicle added!")

        elif choice == '6':
            vehicles = read_vehicles(session)
            for vehicle in vehicles:
                print(f'{vehicle.vin}: {vehicle.make} {vehicle.model}')

        elif choice == '7':
            vin = input("VIN to update: ")
            make = input("New Make (leave blank to skip): ")
            model = input("New Model (leave blank to skip): ")
            year = input("New Year (leave blank to skip): ")
            license_plate = input("New License Plate (leave blank to skip): ")
            update_vehicle(session, vin, make=make or None, model=model or None, year=year or None, license_plate=license_plate or None)
            print("Vehicle updated!")

        elif choice == '8':
            vin = input("VIN to delete: ")
            delete_vehicle(session, vin)
            print("Vehicle deleted!")

        elif choice == '9':
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            phone = input("Phone (optional): ")
            salary = input("Salary (optional): ")
            create_mechanic(session, first_name, last_name, email, phone, salary)
            print("Mechanic added!")

        elif choice == '10':
            mechanics = read_mechanics(session)
            for mechanic in mechanics:
                print(f'{mechanic.mechanic_id}: {mechanic.first_name} {mechanic.last_name}')

        elif choice == '11':
            mechanic_id = int(input("Mechanic ID to update: "))
            first_name = input("New First Name (leave blank to skip): ")
            last_name = input("New Last Name (leave blank to skip): ")
            email = input("New Email (leave blank to skip): ")
            phone = input("New Phone (leave blank to skip): ")
            salary = input("New Salary (leave blank to skip): ")
            update_mechanic(session, mechanic_id, first_name=first_name or None, last_name=last_name or None, email=email or None, phone=phone or None, salary=salary or None)
            print("Mechanic updated!")

        elif choice == '12':
            mechanic_id = int(input("Mechanic ID to delete: "))
            delete_mechanic(session, mechanic_id)
            print("Mechanic deleted!")

        elif choice == '13':
            vin = input("VIN: ")
            customer_id = int(input("Customer ID: "))
            ticket_date = input("Ticket Date (YYYY-MM-DD): ")
            service_description = input("Service Description: ")
            cost = input("Cost: ")
            create_service_ticket(session, vin, customer_id, ticket_date, service_description, cost)
            print("Service Ticket added!")

        elif choice == '14':
            service_tickets = read_service_tickets(session)
            for service_ticket in service_tickets:
                print(f'{service_ticket.ticket_id}: {service_ticket.service_description}')

        elif choice == '15':
            ticket_id = int(input("Ticket ID to update: "))
            vin = input("New VIN (leave blank to skip): ")
            customer_id = input("New Customer ID (leave blank to skip): ")
            ticket_date = input("New Ticket Date (leave blank to skip): ")
            service_description = input("New Service Description (leave blank to skip): ")
            cost = input("New Cost (leave blank to skip): ")
            update_service_ticket(session, ticket_id, vin=vin or None, customer_id=customer_id or None, ticket_date=ticket_date or None, service_description=service_description or None, cost=cost or None)
            print("Service Ticket updated!")

        elif choice == '16':
            ticket_id = int(input("Ticket ID to delete: "))
            delete_service_ticket(session, ticket_id)
            print("Service Ticket deleted!")

        elif choice == '17':
            service_ticket_id = int(input("Service Ticket ID: "))
            mechanic_id = int(input("Mechanic ID: "))
            create_service_mechanic(session, service_ticket_id, mechanic_id)
            print("Service Mechanic added!")

        elif choice == '18':
            service_mechanics = read_service_mechanics(session)
            for service_mechanic in service_mechanics:
                print(f'{service_mechanic.service_ticket_id}: {service_mechanic.mechanic_id}')

        elif choice == '19':
            service_ticket_id = int(input("Service Ticket ID to update: "))
            mechanic_id = int(input("Mechanic ID to update: "))
            update_service_mechanic(session, service_ticket_id, mechanic_id)
            print("Service Mechanic updated!")

        elif choice == '20':
            service_ticket_id = int(input("Service Ticket ID to delete: "))
            mechanic_id = int(input("Mechanic ID to delete: "))
            delete_service_mechanic(session, service_ticket_id, mechanic_id)
            print("Service Mechanic deleted!")

        elif choice == '21':
            break

if __name__ == '__main__':
    main()
