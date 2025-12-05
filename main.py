# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlmodel import Session
import webbrowser
import threading
import time
import uvicorn

from database import engine, create_db_and_tables, get_session
from models import Employee, Hall, Supply, Ticket, Visitor, Exhibit, Movement, Restoration
from requests import (
    # Employees
    get_all_employees,
    get_employee_by_id,
    get_employees_by_position,
    create_employee,
    update_employee,
    delete_employee,

    # Exhibits
    get_all_exhibits,
    get_exhibit_by_id,
    find_exhibit_by_inventory_number,
    create_exhibit,
    update_exhibit,
    delete_exhibit,

    # Halls
    get_all_halls,
    get_hall_by_id,
    create_hall,
    update_hall,
    delete_hall,

    # Visitors
    get_all_visitors,
    get_visitor_by_id,
    create_visitor,
    update_visitor,
    delete_visitor,

    # Tickets
    get_all_tickets,
    get_ticket_by_id,
    create_ticket,
    update_ticket,
    delete_ticket,

    # Movements
    get_all_movements,
    create_movement,
    delete_movement,

    # Restorations
    get_all_restorations,
    create_restoration,
    update_restoration,
    delete_restoration,

    # Special queries
    get_exhibits_in_hall,
    get_visitors_with_tickets,
    get_exhibit_movement_history,
    get_current_restorations,
    get_exhibits_from_supply,
    get_movements_by_period,
    get_full_exhibit_info,
    get_halls_statistics
)
from seed_data import create_sample_data

# Create FastAPI application
app = FastAPI(
    title="Museum API System",
    description="",
    version="2.0.0"
)

# Configure CORS for browser work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables and test data on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_sample_data()
    print("✅ Database and test data created!")


# ====== ROOT ROUTE ======

@app.get("/")
def root_route():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Museum API System!",
        "version": "2.0.0",
        "documentation": "/docs",
        "available_endpoints": {
            "employees": [
                "GET /employees",
                "GET /employees/{id}",
                "GET /employees/position/{position}",
                "POST /employees",
                "PUT /employees/{id}",
                "DELETE /employees/{id}"
            ],
            "exhibits": [
                "GET /exhibits",
                "GET /exhibits/{id}",
                "GET /exhibits/inventory/{inventory_number}",
                "GET /exhibits/hall/{hall_number}",
                "GET /exhibits/{id}/full-info",
                "POST /exhibits",
                "PUT /exhibits/{id}",
                "DELETE /exhibits/{id}"
            ],
            "halls": [
                "GET /halls",
                "GET /halls/{id}",
                "POST /halls",
                "PUT /halls/{id}",
                "DELETE /halls/{id}"
            ],
            "visitors": [
                "GET /visitors",
                "GET /visitors/{id}",
                "POST /visitors",
                "PUT /visitors/{id}",
                "DELETE /visitors/{id}"
            ],
            "tickets": [
                "GET /tickets",
                "GET /tickets/{id}",
                "POST /tickets",
                "PUT /tickets/{id}",
                "DELETE /tickets/{id}"
            ]
        }
    }


# ====== EMPLOYEE ROUTES ======

@app.get("/employees", response_model=List[Employee])
def get_all_employees_api(db: Session = Depends(get_session)):
    """Get all museum employees"""
    return get_all_employees(db)


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee_by_id_api(employee_id: int, db: Session = Depends(get_session)):
    """Get employee by ID"""
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.get("/employees/position/{position}", response_model=List[Employee])
def get_employees_by_position_api(position: str, db: Session = Depends(get_session)):
    """Get employees by specific position"""
    employees = get_employees_by_position(db, position)
    if not employees:
        raise HTTPException(status_code=404, detail=f"Employees with position '{position}' not found")
    return employees


@app.post("/employees", response_model=Employee)
def create_employee_api(employee: Employee, db: Session = Depends(get_session)):
    """Create new employee"""
    return create_employee(db, employee.model_dump())


@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee_api(employee_id: int, employee: Employee, db: Session = Depends(get_session)):
    """Update employee data"""
    updated_employee = update_employee(db, employee_id, employee.model_dump(exclude_unset=True))
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee


@app.delete("/employees/{employee_id}")
def delete_employee_api(employee_id: int, db: Session = Depends(get_session)):
    """Delete employee"""
    success = delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee successfully deleted"}


# ====== EXHIBIT ROUTES ======

@app.get("/exhibits", response_model=List[Exhibit])
def get_all_exhibits_api(db: Session = Depends(get_session)):
    """Get all museum exhibits"""
    return get_all_exhibits(db)


@app.get("/exhibits/{exhibit_id}", response_model=Exhibit)
def get_exhibit_by_id_api(exhibit_id: int, db: Session = Depends(get_session)):
    """Get exhibit by ID"""
    exhibit = get_exhibit_by_id(db, exhibit_id)
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit


@app.get("/exhibits/inventory/{inventory_number}", response_model=Exhibit)
def find_exhibit_by_inventory_number_api(inventory_number: str, db: Session = Depends(get_session)):
    """Find specific exhibit by inventory number"""
    exhibit = find_exhibit_by_inventory_number(db, inventory_number)
    if not exhibit:
        raise HTTPException(status_code=404, detail=f"Exhibit with inventory number '{inventory_number}' not found")
    return exhibit


@app.get("/exhibits/hall/{hall_number}", response_model=List[Exhibit])
def get_exhibits_in_hall_api(hall_number: int, db: Session = Depends(get_session)):
    """Get all exhibits in specified hall"""
    exhibits = get_exhibits_in_hall(db, hall_number)
    return exhibits


@app.get("/exhibits/{exhibit_id}/full-info")
def get_full_exhibit_info_api(exhibit_id: int, db: Session = Depends(get_session)):
    """Get full exhibit information including hall, supply, movements and restorations"""
    info = get_full_exhibit_info(db, exhibit_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Exhibit with ID {exhibit_id} not found")
    return info


@app.post("/exhibits", response_model=Exhibit)
def create_exhibit_api(exhibit: Exhibit, db: Session = Depends(get_session)):
    """Create new exhibit"""
    return create_exhibit(db, exhibit.model_dump())


@app.put("/exhibits/{exhibit_id}", response_model=Exhibit)
def update_exhibit_api(exhibit_id: int, exhibit: Exhibit, db: Session = Depends(get_session)):
    """Update exhibit data"""
    updated_exhibit = update_exhibit(db, exhibit_id, exhibit.model_dump(exclude_unset=True))
    if not updated_exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return updated_exhibit


@app.delete("/exhibits/{exhibit_id}")
def delete_exhibit_api(exhibit_id: int, db: Session = Depends(get_session)):
    """Delete exhibit"""
    success = delete_exhibit(db, exhibit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return {"message": "Exhibit successfully deleted"}


# ====== HALL ROUTES ======

@app.get("/halls", response_model=List[Hall])
def get_all_halls_api(db: Session = Depends(get_session)):
    """Get all museum halls"""
    return get_all_halls(db)


@app.get("/halls/{hall_id}", response_model=Hall)
def get_hall_by_id_api(hall_id: int, db: Session = Depends(get_session)):
    """Get hall by ID"""
    hall = get_hall_by_id(db, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall


@app.post("/halls", response_model=Hall)
def create_hall_api(hall: Hall, db: Session = Depends(get_session)):
    """Create new hall"""
    return create_hall(db, hall.model_dump())


@app.put("/halls/{hall_id}", response_model=Hall)
def update_hall_api(hall_id: int, hall: Hall, db: Session = Depends(get_session)):
    """Update hall data"""
    updated_hall = update_hall(db, hall_id, hall.model_dump(exclude_unset=True))
    if not updated_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    return updated_hall


@app.delete("/halls/{hall_id}")
def delete_hall_api(hall_id: int, db: Session = Depends(get_session)):
    """Delete hall"""
    success = delete_hall(db, hall_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hall not found")
    return {"message": "Hall successfully deleted"}


# ====== VISITOR ROUTES ======

@app.get("/visitors", response_model=List[Visitor])
def get_all_visitors_api(db: Session = Depends(get_session)):
    """Get all visitors with ticket information"""
    return get_all_visitors(db)


@app.get("/visitors/{visitor_id}", response_model=Visitor)
def get_visitor_by_id_api(visitor_id: int, db: Session = Depends(get_session)):
    """Get visitor by ID"""
    visitor = get_visitor_by_id(db, visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor


@app.post("/visitors", response_model=Visitor)
def create_visitor_api(visitor: Visitor, db: Session = Depends(get_session)):
    """Create new visitor"""
    return create_visitor(db, visitor.model_dump())


@app.put("/visitors/{visitor_id}", response_model=Visitor)
def update_visitor_api(visitor_id: int, visitor: Visitor, db: Session = Depends(get_session)):
    """Update visitor data"""
    updated_visitor = update_visitor(db, visitor_id, visitor.model_dump(exclude_unset=True))
    if not updated_visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return updated_visitor


@app.delete("/visitors/{visitor_id}")
def delete_visitor_api(visitor_id: int, db: Session = Depends(get_session)):
    """Delete visitor"""
    success = delete_visitor(db, visitor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return {"message": "Visitor successfully deleted"}


# ====== TICKET ROUTES ======

@app.get("/tickets", response_model=List[Ticket])
def get_all_tickets_api(db: Session = Depends(get_session)):
    """Get all tickets"""
    return get_all_tickets(db)


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket_by_id_api(ticket_id: int, db: Session = Depends(get_session)):
    """Get ticket by ID"""
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.get("/tickets/{ticket_id}/receipt")
def get_electronic_receipt(ticket_id: int, db: Session = Depends(get_session)):
    """Get electronic receipt for ticket"""
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {
        "receipt_number": f"Receipt-{ticket.number}",
        "ticket_number": ticket.number,
        "purchase_date": ticket.date_time,
        "ticket_type": ticket.type,
        "price": ticket.price,
        "payment_status": ticket.payment_status,
        "receipt": f"Payment for ticket {ticket.number} for amount {ticket.price} rub."
    }


@app.post("/tickets", response_model=Ticket)
def create_ticket_api(ticket: Ticket, db: Session = Depends(get_session)):
    """Create new ticket"""
    return create_ticket(db, ticket.model_dump())


@app.put("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket_api(ticket_id: int, ticket: Ticket, db: Session = Depends(get_session)):
    """Update ticket data"""
    updated_ticket = update_ticket(db, ticket_id, ticket.model_dump(exclude_unset=True))
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated_ticket


@app.delete("/tickets/{ticket_id}")
def delete_ticket_api(ticket_id: int, db: Session = Depends(get_session)):
    """Delete ticket"""
    success = delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket successfully deleted"}


# ====== MOVEMENT ROUTES ======

@app.get("/movements", response_model=List[Movement])
def get_all_movements_api(db: Session = Depends(get_session)):
    """Get all movements"""
    return get_all_movements(db)


@app.get("/movements/exhibit/{exhibit_id}", response_model=List[Movement])
def get_exhibit_movement_history_api(exhibit_id: int, db: Session = Depends(get_session)):
    """Get movement history for specific exhibit"""
    movements = get_exhibit_movement_history(db, exhibit_id)
    return movements


@app.post("/movements", response_model=Movement)
def create_movement_api(movement: Movement, db: Session = Depends(get_session)):
    """Create new movement"""
    return create_movement(db, movement.model_dump())


@app.delete("/movements/{movement_id}")
def delete_movement_api(movement_id: int, db: Session = Depends(get_session)):
    """Delete movement"""
    success = delete_movement(db, movement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movement not found")
    return {"message": "Movement successfully deleted"}


# ====== RESTORATION ROUTES ======

@app.get("/restorations", response_model=List[Restoration])
def get_all_restorations_api(db: Session = Depends(get_session)):
    """Get all restorations"""
    return get_all_restorations(db)


@app.get("/restorations/current", response_model=List[Restoration])
def get_current_restorations_api(db: Session = Depends(get_session)):
    """Get all current (unfinished) restorations"""
    restorations = get_current_restorations(db)
    return restorations


@app.post("/restorations", response_model=Restoration)
def create_restoration_api(restoration: Restoration, db: Session = Depends(get_session)):
    """Create new restoration"""
    return create_restoration(db, restoration.model_dump())


@app.put("/restorations/{restoration_id}", response_model=Restoration)
def update_restoration_api(restoration_id: int, restoration: Restoration, db: Session = Depends(get_session)):
    """Update restoration data"""
    updated_restoration = update_restoration(db, restoration_id, restoration.model_dump(exclude_unset=True))
    if not updated_restoration:
        raise HTTPException(status_code=404, detail="Restoration not found")
    return updated_restoration


@app.delete("/restorations/{restoration_id}")
def delete_restoration_api(restoration_id: int, db: Session = Depends(get_session)):
    """Delete restoration"""
    success = delete_restoration(db, restoration_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restoration not found")
    return {"message": "Restoration successfully deleted"}


# ====== COMPLEX ROUTES AND STATISTICS ======

@app.get("/statistics/halls")
def get_halls_statistics_api(db: Session = Depends(get_session)):
    """Get statistics on number of exhibits in each hall"""
    statistics = get_halls_statistics(db)
    return statistics


@app.get("/exhibits/supply/{supply_id}", response_model=List[Exhibit])
def get_exhibits_from_supply_api(supply_id: int, db: Session = Depends(get_session)):
    """Get all exhibits from specific supply"""
    exhibits = get_exhibits_from_supply(db, supply_id)
    return exhibits


# ====== AUTOMATIC BROWSER OPENING FUNCTION ======

def open_browser():
    """Opens browser with documentation 3 seconds after server start"""
    time.sleep(3)
    print("🌐 Opening documentation in browser...")
    webbrowser.open("http://127.0.0.1:8000/docs")
    print("✅ Documentation opened!")
    print("\n" + "=" * 60)
    print("🚀 MUSEUM API SUCCESSFULLY STARTED! (Version 2.0 - FULL CRUD)")
    print("=" * 60)
    print("📋 Quick testing links:")
    print("   • Documentation: http://127.0.0.1:8000/docs")
    print("   • All employees: http://127.0.0.1:8000/employees")
    print("   • All exhibits: http://127.0.0.1:8000/exhibits")
    print("   • All visitors: http://127.0.0.1:8000/visitors")
    print("   • Cashier employees: http://127.0.0.1:8000/employees/position/cashier")
    print("   • Exhibit INV-1001: http://127.0.0.1:8000/exhibits/inventory/INV-1001")
    print("   • Exhibits in hall 1: http://127.0.0.1:8000/exhibits/hall/1")
    print("   • Halls statistics: http://127.0.0.1:8000/statistics/halls")
    print("=" * 60)
    print("💡 All CRUD operations available: GET, POST, PUT, DELETE")
    print("=" * 60)


# ====== APPLICATION STARTUP ======

if __name__ == "__main__":
    print("🚀 Starting Museum API (Version 2.0 - Full CRUD)...")
    print("⏳ Server initialization...")

    # Start browser opening in separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Start server
    print("🖥️  Server starting on http://127.0.0.1:8000")
    print("⏳ Please wait...")

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        print("💡 Maybe port 8000 is busy. Try:")
        print("   • Close other terminal windows")
        print("   • Use port 8001")