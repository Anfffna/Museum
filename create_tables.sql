-- ===============================================
-- create_tables.sql
-- Создание таблиц для предметной области "Музей"
-- ===============================================

-- На всякий случай очистим всё, если остались старые данные
DO
$$
DECLARE r RECORD;
BEGIN
  FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
    EXECUTE format('DROP TABLE IF EXISTS public.%I CASCADE;', r.tablename);
  END LOOP;
END;
$$;

-- ====== Таблица сотрудников ======
CREATE TABLE сотрудник (
    id SERIAL PRIMARY KEY,
    фио VARCHAR(255) NOT NULL,
    должность VARCHAR(100),
    табельный_номер VARCHAR(50),
    уровень_доступа VARCHAR(50) DEFAULT 'user'
);

-- ====== Таблица залов (локаций) ======
CREATE TABLE зал (
    id SERIAL PRIMARY KEY,
    номер INTEGER,
    название_экспозиции VARCHAR(255),
    тип VARCHAR(50) DEFAULT 'зал'  -- зал, хранилище, витрина
);

-- ====== Таблица поставок ======
CREATE TABLE поставка (
    id SERIAL PRIMARY KEY,
    номер VARCHAR(100) UNIQUE,
    дата DATE,
    поставщик VARCHAR(255),
    сотрудник_id INTEGER REFERENCES сотрудник(id) ON DELETE SET NULL
);

-- ====== Таблица билетов ======
CREATE TABLE билет (
    id SERIAL PRIMARY KEY,
    номер VARCHAR(100) UNIQUE,
    дата_и_время TIMESTAMP,
    тип VARCHAR(50),
    стоимость NUMERIC(10,2),
    статус_оплаты VARCHAR(50) DEFAULT 'не оплачен'
);

-- ====== Таблица посетителей ======
CREATE TABLE посетитель (
    id SERIAL PRIMARY KEY,
    имя VARCHAR(255),
    возраст INTEGER,
    телефон VARCHAR(50),
    email VARCHAR(255),
    билет_id INTEGER REFERENCES билет(id) ON DELETE SET NULL
);

-- ====== Таблица экспонатов ======
CREATE TABLE экспонат (
    id SERIAL PRIMARY KEY,
    инвентарный_номер VARCHAR(100) UNIQUE,
    название VARCHAR(255) NOT NULL,
    описание TEXT,
    дата_создания DATE,
    автор VARCHAR(255),
    состояние VARCHAR(100),
    место_хранения VARCHAR(255),
    зал_id INTEGER REFERENCES зал(id) ON DELETE SET NULL,
    поставка_id INTEGER REFERENCES поставка(id) ON DELETE SET NULL
);

-- ====== Таблица перемещений ======
CREATE TABLE перемещение (
    id SERIAL PRIMARY KEY,
    экспонат_id INTEGER NOT NULL REFERENCES экспонат(id) ON DELETE CASCADE,
    из_локация VARCHAR(255),
    в_локация VARCHAR(255),
    дата TIMESTAMP DEFAULT now(),
    ответственный_id INTEGER REFERENCES сотрудник(id) ON DELETE SET NULL,
    причина VARCHAR(255)
);

-- ====== Таблица реставраций ======
CREATE TABLE реставрация (
    id SERIAL PRIMARY KEY,
    экспонат_id INTEGER NOT NULL REFERENCES экспонат(id) ON DELETE CASCADE,
    дата_начала DATE,
    дата_окончания DATE,
    исполнитель VARCHAR(255),
    описание TEXT,
    статус VARCHAR(50) DEFAULT 'в процессе'
);

-- ====== Индексы ======
CREATE INDEX idx_экспонат_инвентарный ON экспонат(инвентарный_номер);
CREATE INDEX idx_поставка_номер ON поставка(номер);
CREATE INDEX idx_билет_номер ON билет(номер);
