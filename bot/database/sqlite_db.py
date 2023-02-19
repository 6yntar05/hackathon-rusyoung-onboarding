import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('users.db')
    cur = base.cursor()
    if base:
        print('Data base connected!')
    base.execute('CREATE TABLE IF NOT EXISTS user(id INT PRIMARY KEY, last_name TEXT, first_name TEXT, daterod TEXT)')
    base.commit()

async def create_profile(id):
    user = cur.execute("SELECT 1 FROM user WHERE id == '{key}'".format(key=id)).fetchone()
    if not user:
        cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (id, '','',''))
        base.commit()

async def edit_profile(state, id):
    async with state.proxy() as data:
        cur.execute("UPDATE user SET  last_name = '{}', first_name = '{}', daterod = '{}' WHERE id == '{}'".format(
            data['last_name'], data['first_name'], data['daterod'], id))
        base.commit()

async def is_user_logged_in(id):

    cur.execute("SELECT 1 FROM user WHERE id = {}".format(id))
    result = cur.fetchone()

    if result and result[0]:
        return True
    else:
        return False