# requests.py
from sqlmodel import select, Session
from models import *
from typing import List, Optional
from datetime import datetime


# ====== EMPLOYEE OPERATIONS ======

def get_all_employees(db: Session) -> List[Employee]:
    """Get all employees"""
    statement = select(Employee)
    results = db.exec(statement)
    return results.all()


def get_employee_by_id(db: Session, employee_id: int) -> Optional[Employee]:
    """Get employee by ID"""
    return db.get(Employee, employee_id)


def get_employees_by_position(db: Session, position: str) -> List[Employee]:
    """Get employees by position"""
    statement = select(Employee).where(Employee.position == position)
    results = db.exec(statement)
    return results.all()


def create_employee(db: Session, employee_data: dict) -> Employee:
    """Create new employee"""
    employee = Employee(**employee_data)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, update_data: dict) -> Optional[Employee]:
    """Update employee data"""
    employee = db.get(Employee, employee_id)
    if employee:
        for key, value in update_data.items():
            setattr(employee, key, value)
        db.commit()
        db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int) -> bool:
    """Delete employee"""
    employee = db.get(Employee, employee_id)
    if employee:
        db.delete(employee)
        db.commit()
        return True
    return False


# ====== EXHIBIT OPERATIONS ======

def get_all_exhibits(db: Session) -> List[Exhibit]:
    """Get all exhibits"""
    statement = select(Exhibit)
    results = db.exec(statement)
    return results.all()


def get_exhibit_by_id(db: Session, exhibit_id: int) -> Optional[Exhibit]:
    """Get exhibit by ID"""
    return db.get(Exhibit, exhibit_id)


def find_exhibit_by_inventory_number(db: Session, inventory_number: str) -> Optional[Exhibit]:
    """Find exhibit by inventory number"""
    statement = select(Exhibit).where(Exhibit.inventory_number == inventory_number)
    results = db.exec(statement)
    return results.first()


def create_exhibit(db: Session, exhibit_data: dict) -> Exhibit:
    """Create new exhibit"""
    exhibit = Exhibit(**exhibit_data)
    db.add(exhibit)
    db.commit()
    db.refresh(exhibit)
    return exhibit


def update_exhibit(db: Session, exhibit_id: int, update_data: dict) -> Optional[Exhibit]:
    """Update exhibit data"""
    exhibit = db.get(Exhibit, exhibit_id)
    if exhibit:
        for key, value in update_data.items():
            setattr(exhibit, key, value)
        db.commit()
        db.refresh(exhibit)
    return exhibit


def delete_exhibit(db: Session, exhibit_id: int) -> bool:
    """Delete exhibit"""
    exhibit = db.get(Exhibit, exhibit_id)
    if exhibit:
        db.delete(exhibit)
        db.commit()
        return True
    return False


# ====== HALL OPERATIONS ======

def get_all_halls(db: Session) -> List[Hall]:
    """Get all halls"""
    statement = select(Hall)
    results = db.exec(statement)
    return results.all()


def get_hall_by_id(db: Session, hall_id: int) -> Optional[Hall]:
    """Get hall by ID"""
    return db.get(Hall, hall_id)


def create_hall(db: Session, hall_data: dict) -> Hall:
    """Create new hall"""
    hall = Hall(**hall_data)
    db.add(hall)
    db.commit()
    db.refresh(hall)
    return hall


def update_hall(db: Session, hall_id: int, update_data: dict) -> Optional[Hall]:
    """Update hall data"""
    hall = db.get(Hall, hall_id)
    if hall:
        for key, value in update_data.items():
            setattr(hall, key, value)
        db.commit()
        db.refresh(hall)
    return hall


def delete_hall(db: Session, hall_id: int) -> bool:
    """Delete hall"""
    hall = db.get(Hall, hall_id)
    if hall:
        db.delete(hall)
        db.commit()
        return True
    return False


# ====== VISITOR OPERATIONS ======

def get_all_visitors(db: Session) -> List[Visitor]:
    """Get all visitors"""
    statement = select(Visitor)
    results = db.exec(statement)
    return results.all()


def get_visitor_by_id(db: Session, visitor_id: int) -> Optional[Visitor]:
    """Get visitor by ID"""
    return db.get(Visitor, visitor_id)


def create_visitor(db: Session, visitor_data: dict) -> Visitor:
    """Create new visitor"""
    visitor = Visitor(**visitor_data)
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor


def update_visitor(db: Session, visitor_id: int, update_data: dict) -> Optional[Visitor]:
    """Update visitor data"""
    visitor = db.get(Visitor, visitor_id)
    if visitor:
        for key, value in update_data.items():
            setattr(visitor, key, value)
        db.commit()
        db.refresh(visitor)
    return visitor


def delete_visitor(db: Session, visitor_id: int) -> bool:
    """Delete visitor"""
    visitor = db.get(Visitor, visitor_id)
    if visitor:
        db.delete(visitor)
        db.commit()
        return True
    return False


# ====== TICKET OPERATIONS ======

def get_all_tickets(db: Session) -> List[Ticket]:
    """Get all tickets"""
    statement = select(Ticket)
    results = db.exec(statement)
    return results.all()


def get_ticket_by_id(db: Session, ticket_id: int) -> Optional[Ticket]:
    """Get ticket by ID"""
    return db.get(Ticket, ticket_id)


def create_ticket(db: Session, ticket_data: dict) -> Ticket:
    """Create new ticket"""
    ticket = Ticket(**ticket_data)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def update_ticket(db: Session, ticket_id: int, update_data: dict) -> Optional[Ticket]:
    """Update ticket data"""
    ticket = db.get(Ticket, ticket_id)
    if ticket:
        for key, value in update_data.items():
            setattr(ticket, key, value)
        db.commit()
        db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int) -> bool:
    """Delete ticket"""
    ticket = db.get(Ticket, ticket_id)
    if ticket:
        db.delete(ticket)
        db.commit()
        return True
    return False


# ====== MOVEMENT OPERATIONS ======

def get_all_movements(db: Session) -> List[Movement]:
    """Get all movements"""
    statement = select(Movement)
    results = db.exec(statement)
    return results.all()


def create_movement(db: Session, movement_data: dict) -> Movement:
    """Create new movement"""
    movement = Movement(**movement_data)
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def delete_movement(db: Session, movement_id: int) -> bool:
    """Delete movement"""
    movement = db.get(Movement, movement_id)
    if movement:
        db.delete(movement)
        db.commit()
        return True
    return False


# ====== RESTORATION OPERATIONS ======

def get_all_restorations(db: Session) -> List[Restoration]:
    """Get all restorations"""
    statement = select(Restoration)
    results = db.exec(statement)
    return results.all()


def create_restoration(db: Session, restoration_data: dict) -> Restoration:
    """Create new restoration"""
    restoration = Restoration(**restoration_data)
    db.add(restoration)
    db.commit()
    db.refresh(restoration)
    return restoration


def update_restoration(db: Session, restoration_id: int, update_data: dict) -> Optional[Restoration]:
    """Update restoration data"""
    restoration = db.get(Restoration, restoration_id)
    if restoration:
        for key, value in update_data.items():
            setattr(restoration, key, value)
        db.commit()
        db.refresh(restoration)
    return restoration


def delete_restoration(db: Session, restoration_id: int) -> bool:
    """Delete restoration"""
    restoration = db.get(Restoration, restoration_id)
    if restoration:
        db.delete(restoration)
        db.commit()
        return True
    return False


# ====== SPECIAL QUERIES ======

def get_exhibits_in_hall(db: Session, hall_number: int) -> List[Exhibit]:
    """Get all exhibits in specified hall"""
    hall_statement = select(Hall).where(Hall.number == hall_number)
    hall = db.exec(hall_statement).first()

    if not hall:
        return []

    statement = select(Exhibit).where(Exhibit.hall_id == hall.id)
    results = db.exec(statement)
    return results.all()


def get_visitors_with_tickets(db: Session) -> List[Visitor]:
    """Get visitors with ticket information"""
    statement = select(Visitor)
    results = db.exec(statement)
    return results.all()


def get_exhibit_movement_history(db: Session, exhibit_id: int) -> List[Movement]:
    """Get movement history for specific exhibit"""
    statement = (select(Movement)
                 .where(Movement.exhibit_id == exhibit_id)
                 .order_by(Movement.date))
    results = db.exec(statement)
    return results.all()


def get_current_restorations(db: Session) -> List[Restoration]:
    """Get all current (unfinished) restorations"""
    statement = (select(Restoration)
                 .where(Restoration.status == "in progress"))
    results = db.exec(statement)
    return results.all()


def get_exhibits_from_supply(db: Session, supply_id: int) -> List[Exhibit]:
    """Get all exhibits from specific supply"""
    statement = select(Exhibit).where(Exhibit.supply_id == supply_id)
    results = db.exec(statement)
    return results.all()


def get_movements_by_period(db: Session, start: datetime, end: datetime) -> List[Movement]:
    """Get all movements for specified period"""
    statement = (select(Movement)
                 .where(Movement.date >= start)
                 .where(Movement.date <= end)
                 .order_by(Movement.date))
    results = db.exec(statement)
    return results.all()


def get_full_exhibit_info(db: Session, exhibit_id: int):
    """Get full exhibit information including hall, supply, movements and restorations"""
    exhibit = db.get(Exhibit, exhibit_id)
    if not exhibit:
        return None

    hall = db.get(Hall, exhibit.hall_id) if exhibit.hall_id else None
    supply = db.get(Supply, exhibit.supply_id) if exhibit.supply_id else None

    movement_statement = (select(Movement)
                         .where(Movement.exhibit_id == exhibit_id)
                         .order_by(Movement.date))
    movements = db.exec(movement_statement).all()

    restoration_statement = (select(Restoration)
                            .where(Restoration.exhibit_id == exhibit_id)
                            .order_by(Restoration.start_date))
    restorations = db.exec(restoration_statement).all()

    return {
        'exhibit': exhibit,
        'hall': hall,
        'supply': supply,
        'movements': movements,
        'restorations': restorations
    }


def get_halls_statistics(db: Session):
    """Get statistics on number of exhibits in each hall"""
    halls_statement = select(Hall)
    halls = db.exec(halls_statement).all()

    statistics = []
    for hall in halls:
        exhibits_statement = select(Exhibit).where(Exhibit.hall_id == hall.id)
        count = len(db.exec(exhibits_statement).all())

        statistics.append({
            'hall_id': hall.id,
            'hall_number': hall.number,
            'exposition_name': hall.exposition_name,
            'type': hall.type,
            'exhibits_count': count
        })

    return statistics