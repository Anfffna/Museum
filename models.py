# models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=255)
    position: str = Field(max_length=100)
    personnel_number: str = Field(max_length=50)
    access_level: str = Field(default="user", max_length=50)

    # Relationships
    supplies: List["Supply"] = Relationship(back_populates="employee")
    movements: List["Movement"] = Relationship(back_populates="responsible_employee")


class Hall(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: Optional[int] = None
    exposition_name: Optional[str] = Field(default=None, max_length=255)
    type: str = Field(default="hall", max_length=50)

    # Relationships
    exhibits: List["Exhibit"] = Relationship(back_populates="hall")


class Supply(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: str = Field(unique=True, max_length=100)
    date: date
    supplier: str = Field(max_length=255)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    # Relationships
    employee: Optional[Employee] = Relationship(back_populates="supplies")
    exhibits: List["Exhibit"] = Relationship(back_populates="supply")


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: str = Field(unique=True, max_length=100)
    date_time: datetime = Field(default_factory=datetime.now)
    type: str = Field(max_length=50)
    price: float = Field(ge=0)
    payment_status: str = Field(default="not paid", max_length=50)

    # Relationships
    visitor: Optional["Visitor"] = Relationship(back_populates="ticket")


class Visitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    age: int = Field(ge=0)
    phone: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=255)
    ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")

    # Relationships
    ticket: Optional[Ticket] = Relationship(back_populates="visitor")


class Exhibit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_number: str = Field(unique=True, max_length=100)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    creation_date: Optional[date] = None
    author: Optional[str] = Field(default=None, max_length=255)
    condition: Optional[str] = Field(default=None, max_length=100)
    storage_location: Optional[str] = Field(default=None, max_length=255)
    hall_id: Optional[int] = Field(default=None, foreign_key="hall.id")
    supply_id: Optional[int] = Field(default=None, foreign_key="supply.id")

    # Relationships
    hall: Optional[Hall] = Relationship(back_populates="exhibits")
    supply: Optional[Supply] = Relationship(back_populates="exhibits")
    movements: List["Movement"] = Relationship(back_populates="exhibit")
    restorations: List["Restoration"] = Relationship(back_populates="exhibit")


class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exhibit_id: int = Field(foreign_key="exhibit.id")
    from_location: Optional[str] = Field(default=None, max_length=255)
    to_location: Optional[str] = Field(default=None, max_length=255)
    date: datetime = Field(default_factory=datetime.now)
    responsible_employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    reason: Optional[str] = Field(default=None, max_length=255)

    # Relationships
    exhibit: Exhibit = Relationship(back_populates="movements")
    responsible_employee: Optional[Employee] = Relationship(back_populates="movements")


class Restoration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exhibit_id: int = Field(foreign_key="exhibit.id")
    start_date: date
    end_date: Optional[date] = None
    executor: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="in progress", max_length=50)

    # Relationships
    exhibit: Exhibit = Relationship(back_populates="restorations")