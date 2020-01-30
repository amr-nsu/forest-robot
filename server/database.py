import sqlite3
import time
from datetime import datetime


conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def write(event, animal=''):
    cursor.execute('INSERT INTO events VALUES (%d, "%s", "%s")' % (time.time(), event, animal))
    conn.commit()


def read_all():
    response = ''
    for elem in cursor.execute('SELECT * FROM events'):
        response += '<p><font color="lightgray">%s</font> %s <font color="#00ff00">%s</font></p>' \
            % (datetime.fromtimestamp(elem[0]).strftime('%Y.%m.%d %H:%M:%S'),
               elem[1], elem[2])
    return response

    
def read_last(n):
    response = ''
    for elem in cursor.execute("""SELECT * FROM (
                                      SELECT * FROM events ORDER BY time DESC LIMIT %d
                                  ) sub ORDER BY time ASC""" % n):
        response += '<p><font color="lightgray">%s</font> %s <font color="#00ff00">%s</font></p>' \
            % (datetime.fromtimestamp(elem[0]).strftime('%Y.%m.%d %H:%M:%S'),
               elem[1], elem[2])
    return response


def claen():
    cursor.execute('DELETE FROM events')
    conn.commit()


def write_mode(auto):
    if auto:
        write('Автоматический режим')
    else:
        write('Ручной режим')
    

def init_demo():
    t = time.time()

    # cursor.execute('CREATE TABLE events (time int, event text, note text)')
    cursor.execute('DELETE FROM events')

    cursor.execute('INSERT INTO events VALUES (%d, "Автоматический режим", "")' % (t - 400))
    cursor.execute('INSERT INTO events VALUES (%d, "Датчик движения", "")' % (t - 300))
    cursor.execute('INSERT INTO events VALUES (%d, "Опознано животное", "обезьяна")' % (t - 250))
    cursor.execute('INSERT INTO events VALUES (%d, "Опознано животное", "обезьяна")' % (t - 200))
    cursor.execute('INSERT INTO events VALUES (%d, "Опознано животное", "лесной кот")' % (t -90))
    cursor.execute('INSERT INTO events VALUES (%d, "Датчик движения", "")' % (t - 60))
    cursor.execute('INSERT INTO events VALUES (%d, "Движение по камере", "")' % (t - 40))
    cursor.execute('INSERT INTO events VALUES (%d, "Опознано животное", "лесной кот")' % (t - 30))
    cursor.execute('INSERT INTO events VALUES (%d, "Движение по камере", "")' % (t - 20))
    cursor.execute('INSERT INTO events VALUES (%d, "Опознано животное", "лесной кот")' % (t - 10))
    cursor.execute('INSERT INTO events VALUES (%d, "Движение по камере", "")' % (t - 1))
    cursor.execute('INSERT INTO events VALUES (%d, "Ручной режим", "")' % (t))
    conn.commit()


if __name__ == '__main__':
    cursor.execute('CREATE TABLE events (time int, event text, note text)')

    cursor.execute('INSERT INTO events VALUES (1579079644, "Автоматический режим", "")')
    cursor.execute('INSERT INTO events VALUES (1579079756, "Датчик движения", "")')
    cursor.execute('INSERT INTO events VALUES (1579079759, "Опознано животное", "обезьяна")')
    cursor.execute('INSERT INTO events VALUES (1579079769, "Опознано животное", "обезьяна")')
    cursor.execute('INSERT INTO events VALUES (1579079770, "Опознано животное", "лесной кот")')
    cursor.execute('INSERT INTO events VALUES (1579079756, "Датчик движения", "")')
    cursor.execute('INSERT INTO events VALUES (1579079766, "Движение по камере", "")')
    cursor.execute('INSERT INTO events VALUES (1579079770, "Опознано животное", "лесной кот")')
    cursor.execute('INSERT INTO events VALUES (1579079786, "Движение по камере", "")')
    cursor.execute('INSERT INTO events VALUES (1579079790, "Опознано животное", "лесной кот")')
    cursor.execute('INSERT INTO events VALUES (1579079916, "Движение по камере", "")')
    cursor.execute('INSERT INTO events VALUES (1579079756, "Датчик движения", "")')

    conn.commit()
    print('database init')

