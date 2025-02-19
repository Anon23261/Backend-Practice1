import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from practice1 import Base, Customer, Vehicle, Mechanic, ServiceTicket

class TestCRUDOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        # Create a unique customer for testing
        self.customer = Customer(first_name='John', last_name='Doe', phone='1234567890', email='john@example.com')
        self.session.add(self.customer)
        self.session.commit()

    def tearDown(self):
        self.session.query(Customer).delete()  # Clear customers after each test
        self.session.query(Vehicle).delete()  # Clear vehicles after each test
        self.session.query(Mechanic).delete()  # Clear mechanics after each test
        self.session.query(ServiceTicket).delete()  # Clear service tickets after each test
        self.session.commit()
        self.session.close()

    def test_create_customer(self):
        customer = Customer(first_name='Jane', last_name='Doe', phone='0987654321', email='jane@example.com')
        self.session.add(customer)
        self.session.commit()
        print(f"Created customer: {customer.first_name} {customer.last_name}")
        self.assertEqual(customer.customer_id, 2)

    def test_read_customer(self):
        customer = self.session.query(Customer).first()
        print(f"Read customer: {customer}")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.first_name, 'John')

    def test_update_customer(self):
        customer = self.session.query(Customer).first()
        print(f"Updating customer: {customer}")
        customer.first_name = 'Jane'
        self.session.commit()
        updated_customer = self.session.query(Customer).first()
        print(f"Updated customer: {updated_customer}")
        self.assertEqual(updated_customer.first_name, 'Jane')

    def test_delete_customer(self):
        customer = self.session.query(Customer).first()
        print(f"Deleting customer: {customer}")
        self.session.delete(customer)
        self.session.commit()
        deleted_customer = self.session.query(Customer).first()
        print(f"Deleted customer: {deleted_customer}")
        self.assertIsNone(deleted_customer)

    # Vehicle Tests
    def test_create_vehicle(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109186', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='ABC123')
        self.session.add(vehicle)
        self.session.commit()
        print(f"Created vehicle: {vehicle.vin}")
        self.assertEqual(vehicle.vin, '1HGBH41JXMN109186')

    def test_read_vehicle(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109186', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='ABC123')
        self.session.add(vehicle)
        self.session.commit()
        vehicle = self.session.query(Vehicle).first()
        print(f"Read vehicle: {vehicle}")
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.make, 'Honda')

    def test_update_vehicle(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109186', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='ABC123')
        self.session.add(vehicle)
        self.session.commit()
        vehicle = self.session.query(Vehicle).first()
        print(f"Updating vehicle: {vehicle}")
        vehicle.make = 'Toyota'
        self.session.commit()
        updated_vehicle = self.session.query(Vehicle).first()
        print(f"Updated vehicle: {updated_vehicle}")
        self.assertEqual(updated_vehicle.make, 'Toyota')

    def test_delete_vehicle(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109186', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='ABC123')
        self.session.add(vehicle)
        self.session.commit()
        vehicle = self.session.query(Vehicle).first()
        print(f"Deleting vehicle: {vehicle}")
        self.session.delete(vehicle)
        self.session.commit()
        deleted_vehicle = self.session.query(Vehicle).first()
        print(f"Deleted vehicle: {deleted_vehicle}")
        self.assertIsNone(deleted_vehicle)

    # Mechanic Tests
    def test_create_mechanic(self):
        mechanic = Mechanic(first_name='Alice', last_name='Smith', email='alice@example.com', phone='555-1234', salary=50000)
        self.session.add(mechanic)
        self.session.commit()
        print(f"Created mechanic: {mechanic.first_name} {mechanic.last_name}")
        self.assertEqual(mechanic.email, 'alice@example.com')

    def test_read_mechanic(self):
        mechanic = Mechanic(first_name='Alice', last_name='Smith', email='alice@example.com', phone='555-1234', salary=50000)
        self.session.add(mechanic)
        self.session.commit()
        mechanic = self.session.query(Mechanic).first()
        print(f"Read mechanic: {mechanic}")
        self.assertIsNotNone(mechanic)
        self.assertEqual(mechanic.first_name, 'Alice')

    def test_update_mechanic(self):
        mechanic = Mechanic(first_name='Alice', last_name='Smith', email='alice@example.com', phone='555-1234', salary=50000)
        self.session.add(mechanic)
        self.session.commit()
        mechanic = self.session.query(Mechanic).first()
        print(f"Updating mechanic: {mechanic}")
        mechanic.first_name = 'Bob'
        self.session.commit()
        updated_mechanic = self.session.query(Mechanic).first()
        print(f"Updated mechanic: {updated_mechanic}")
        self.assertEqual(updated_mechanic.first_name, 'Bob')

    def test_delete_mechanic(self):
        mechanic = Mechanic(first_name='Alice', last_name='Smith', email='alice@example.com', phone='555-1234', salary=50000)
        self.session.add(mechanic)
        self.session.commit()
        mechanic = self.session.query(Mechanic).first()
        print(f"Deleting mechanic: {mechanic}")
        self.session.delete(mechanic)
        self.session.commit()
        deleted_mechanic = self.session.query(Mechanic).first()
        print(f"Deleted mechanic: {deleted_mechanic}")
        self.assertIsNone(deleted_mechanic)

    # Service Ticket Tests
    def test_create_service_ticket(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109187', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='XYZ789')
        self.session.add(vehicle)
        self.session.commit()
        service_ticket = ServiceTicket(vin=vehicle.vin, customer_id=self.customer.customer_id, service_description='Oil Change', cost=50.0)
        self.session.add(service_ticket)
        self.session.commit()
        print(f"Created service ticket: {service_ticket.ticket_id}")
        self.assertEqual(service_ticket.service_description, 'Oil Change')

    def test_read_service_ticket(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109187', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='XYZ789')
        self.session.add(vehicle)
        self.session.commit()
        service_ticket = ServiceTicket(vin=vehicle.vin, customer_id=self.customer.customer_id, service_description='Oil Change', cost=50.0)
        self.session.add(service_ticket)
        self.session.commit()
        service_ticket = self.session.query(ServiceTicket).first()
        print(f"Read service ticket: {service_ticket}")
        self.assertIsNotNone(service_ticket)
        self.assertEqual(service_ticket.service_description, 'Oil Change')

    def test_update_service_ticket(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109187', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='XYZ789')
        self.session.add(vehicle)
        self.session.commit()
        service_ticket = ServiceTicket(vin=vehicle.vin, customer_id=self.customer.customer_id, service_description='Oil Change', cost=50.0)
        self.session.add(service_ticket)
        self.session.commit()
        service_ticket = self.session.query(ServiceTicket).first()
        print(f"Updating service ticket: {service_ticket}")
        service_ticket.service_description = 'Tire Rotation'
        self.session.commit()
        updated_service_ticket = self.session.query(ServiceTicket).first()
        print(f"Updated service ticket: {updated_service_ticket}")
        self.assertEqual(updated_service_ticket.service_description, 'Tire Rotation')

    def test_delete_service_ticket(self):
        vehicle = Vehicle(vin='1HGBH41JXMN109187', customer_id=self.customer.customer_id, make='Honda', model='Civic', year=2020, license_plate='XYZ789')
        self.session.add(vehicle)
        self.session.commit()
        service_ticket = ServiceTicket(vin=vehicle.vin, customer_id=self.customer.customer_id, service_description='Oil Change', cost=50.0)
        self.session.add(service_ticket)
        self.session.commit()
        service_ticket = self.session.query(ServiceTicket).first()
        print(f"Deleting service ticket: {service_ticket}")
        self.session.delete(service_ticket)
        self.session.commit()
        deleted_service_ticket = self.session.query(ServiceTicket).first()
        print(f"Deleted service ticket: {deleted_service_ticket}")
        self.assertIsNone(deleted_service_ticket)

if __name__ == '__main__':
    unittest.main()
