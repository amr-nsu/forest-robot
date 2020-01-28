import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE events (time int, event text, note text)')

cursor.execute('INSERT INTO events VALUES (1579079644, "Автоматический режим", "")')
cursor.execute('INSERT INTO events VALUES (1579079756, "Датчик движения", "")')
cursor.execute('INSERT INTO events VALUES (1579079759, "Опознано животное", "обезьяна")')
cursor.execute('INSERT INTO events VALUES (1579079769, "Опознано животное", "обезьяна")')
cursor.execute('INSERT INTO events VALUES (1579079770, "Опознано животное", "пантера")')
cursor.execute('INSERT INTO events VALUES (1579079756, "Датчик движения", "")')
cursor.execute('INSERT INTO events VALUES (1579079766, "Движение по камере", "")')
cursor.execute('INSERT INTO events VALUES (1579079770, "Опознано животное", "пантера")')
cursor.execute('INSERT INTO events VALUES (1579079786, "Движение по камере", "")')
cursor.execute('INSERT INTO events VALUES (1579079790, "Опознано животное", "пантера")')
cursor.execute('INSERT INTO events VALUES (1579079916, "Движение по камере", "")')
cursor.execute('INSERT INTO events VALUES (1579079756, "Датчик движения", "")')

conn.commit()

