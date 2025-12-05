# seed_data.py
from database import create_db_and_tables, get_session
from models import *
from datetime import datetime, date
from sqlmodel import select, text


def create_sample_data():
    """Создание тестовых данных с принудительным обновлением"""

    with next(get_session()) as session:
        print("🔄 Creating/updating test data...")

        # УДАЛЯЕМ СТАРЫЕ ДАННЫЕ
        session.exec(text("DELETE FROM restoration"))
        session.exec(text("DELETE FROM movement"))
        session.exec(text("DELETE FROM exhibit"))
        session.exec(text("DELETE FROM visitor"))
        session.exec(text("DELETE FROM ticket"))
        session.exec(text("DELETE FROM supply"))
        session.exec(text("DELETE FROM hall"))
        session.exec(text("DELETE FROM employee"))
        session.commit()

        # 1. Создаем сотрудников
        employee1 = Employee(
            full_name="Иванов Иван Иванович",
            position="кассир",
            personnel_number="T001",
            access_level="staff"
        )

        employee2 = Employee(
            full_name="Петров Петр Петрович",
            position="экскурсовод",
            personnel_number="T002",
            access_level="staff"
        )

        employee3 = Employee(
            full_name="Сидорова Анна Александровна",
            position="хранитель фондов",
            personnel_number="T003",
            access_level="manager"
        )

        session.add_all([employee1, employee2, employee3])
        session.commit()

        # 2. Создаем залы
        hall1 = Hall(
            number=1,
            exposition_name="Древние артефакты",
            type="выставочный зал"
        )

        hall2 = Hall(
            number=2,
            exposition_name="Живопись XIX века",
            type="выставочный зал"
        )

        hall3 = Hall(
            number=100,
            exposition_name="Основное хранилище",
            type="хранилище"
        )

        session.add_all([hall1, hall2, hall3])
        session.commit()

        # 3. Создаем поставку
        supply1 = Supply(
            number="P-2025-10-01",
            date=date(2025, 10, 1),
            supplier='Галерея "Альфа"',
            employee_id=employee3.id
        )

        session.add(supply1)
        session.commit()

        # 4. Создаем билеты
        ticket1 = Ticket(
            number="B5001",
            date_time=datetime(2025, 10, 20, 11, 0),
            type="взрослый",
            price=500.00,
            payment_status="оплачен"
        )

        ticket2 = Ticket(
            number="B5002",
            date_time=datetime(2025, 10, 20, 12, 0),
            type="детский",
            price=250.00,
            payment_status="оплачен"
        )

        session.add_all([ticket1, ticket2])
        session.commit()

        # 5. Создаем посетителей
        visitor1 = Visitor(
            name="Алексей",
            age=35,
            phone="+7-900-111-22-33",
            email="alexey@example.com",
            ticket_id=ticket1.id
        )

        visitor2 = Visitor(
            name="Мария",
            age=12,
            phone="+7-900-222-33-44",
            email="maria@example.com",
            ticket_id=ticket2.id
        )

        session.add_all([visitor1, visitor2])
        session.commit()

        # 6. Создаем экспонаты
        exhibit1 = Exhibit(
            inventory_number="INV-1001",
            title="Икона Владимирская Богоматерь",
            description="Древняя икона в резной кипарисовой раме, XIV век",
            creation_date=date(1350, 1, 1),
            author="Неизвестный мастер",
            condition="хорошее",
            storage_location="витрина №1",
            hall_id=hall1.id,
            supply_id=supply1.id
        )

        exhibit2 = Exhibit(
            inventory_number="INV-1002",
            title='Картина "Закат над Волгой"',
            description="Масляная живопись на холсте, пейзаж",
            creation_date=date(1885, 1, 1),
            author="Архип Иванович Куинджи",
            condition="отличное",
            storage_location="стена зала №2",
            hall_id=hall2.id,
            supply_id=supply1.id
        )

        exhibit3 = Exhibit(
            inventory_number="INV-1003",
            title="Статуэтка льва из слоновой кости",
            description="Резная статуэтка льва в натуральную величину",
            creation_date=date(1750, 1, 1),
            author="Неизвестный резчик",
            condition="удовлетворительное",
            storage_location="хранилище 100-А",
            hall_id=hall3.id,
            supply_id=supply1.id
        )

        session.add_all([exhibit1, exhibit2, exhibit3])
        session.commit()

        # 7. Создаем перемещение
        movement1 = Movement(
            exhibit_id=exhibit3.id,
            from_location="хранилище 100-А",
            to_location="витрина №2 основного зала",
            date=datetime.now(),
            responsible_employee_id=employee3.id,
            reason='Временная выставка "Малые скульптуры Древнего Востока"'
        )

        session.add(movement1)

        # 8. Создаем реставрацию
        restoration1 = Restoration(
            exhibit_id=exhibit1.id,
            start_date=date(2025, 5, 1),
            end_date=date(2025, 7, 1),
            executor="Реставратор высшей категории Петров С.С.",
            description="Частичная реставрация лакового слоя, укрепление грунта",
            status="завершено"
        )

        session.add(restoration1)

        session.commit()

        print("✅ Russian test data successfully created!")
        print(f"   Создано: 3 сотрудника, 3 зала, 1 поставка, 2 билета")
        print(f"            2 посетителя, 3 экспоната, 1 перемещение, 1 реставрация")


if __name__ == "__main__":
    create_sample_data()