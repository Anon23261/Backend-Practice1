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

# Create the SQLite database in memory (or use a file-based DB by changing the URI)
engine = create_engine('sqlite:///:memory:')

# Create all tables
Base.metadata.create_all(engine)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Example of adding data to the tables:
# Adding a customer
customer = Customer(first_name="John", last_name="Doe", phone="123-456-7890", email="john@example.com")
session.add(customer)
session.commit()

# Adding a vehicle for the customer
vehicle = Vehicle(vin="1HGBH41JXMN109186", make="Honda", model="Civic", year=2020, license_plate="ABC123", customer_id=customer.customer_id)
session.add(vehicle)
session.commit()

# Adding a mechanic
mechanic = Mechanic(first_name="Alice", last_name="Smith", email="alice@mechanics.com", salary=50000)
session.add(mechanic)
session.commit()

# Creating a service ticket
service_ticket = ServiceTicket(vin=vehicle.vin, customer_id=customer.customer_id, service_description="Oil change", cost=50.0)
session.add(service_ticket)
session.commit()

# Assigning the mechanic to the service ticket (many-to-many relationship)
service_mechanic = ServiceMechanic(service_ticket_id=service_ticket.ticket_id, mechanic_id=mechanic.mechanic_id)
session.add(service_mechanic)
session.commit()

# Querying the data
for ticket in session.query(ServiceTicket).all():
    print(f"Ticket ID: {ticket.ticket_id}, Vehicle VIN: {ticket.vin}, Customer: {ticket.customer.first_name} {ticket.customer.last_name}, Mechanics: {[sm.mechanic.first_name for sm in ticket.mechanics]}")

# Close session
session.close()
