import sqlite3
from tkinter import *


# define database to use
def db_conn():
    conn = sqlite3.connect('db/contactlist.db')
    return conn


def add_person(app):
    if app.text_first_name.get() == "" or app.text_last_name.get() == "":
        return

    insert_row = (app.text_first_name.get(), app.text_last_name.get(), app.text_email.get(),
                  app.text_phone_number.get(), app.text_address.get())
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO tbl_contactlist (col_fname, col_lname, col_email, col_phone, col_address)
                        VALUES (?, ?, ?, ?, ?)""",
                    insert_row)
        conn.commit()
    conn.close()
    clear_form_fields(app)
    load_contactlist(app)


def edit_person(app):
    if app.text_first_name.get() == "" or app.text_last_name.get() == "":
        return
    update_row = (app.text_first_name.get(), app.text_last_name.get(), app.text_email.get(),
                  app.text_phone_number.get(), app.text_address.get(), app.text_id.get(),)
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("""UPDATE tbl_contactlist SET col_fname=?, col_lname=?, col_email=?, col_phone=?, col_address=?
                        WHERE ID=?""",
                    update_row)
        conn.commit()
    conn.close()
    clear_form(app)
    load_contactlist(app)


def delete_person(app):
    delete_row = (app.text_id.get(),)
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("""DELETE FROM tbl_contactlist WHERE ID=?""", delete_row)
        conn.commit()
    conn.close()
    clear_form(app)
    load_contactlist(app)


def create_db():
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tbl_contactlist ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "col_fname TEXT,"
                    "col_lname TEXT,"
                    "col_email TEXT,"
                    "col_phone TEXT,"
                    "col_address TEXT);")
        conn.commit()
    conn.close()
    first_run()


def first_run():
    data1 = ('John', 'Doe', 'john@mail.com', '123-456-7890', '123 Main St.',)
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur, count = count_records(cur)
        if count < 1:
            cur.execute("""INSERT INTO tbl_contactlist (col_fname, col_lname, col_email, col_phone, col_address)
                        VALUES (?, ?, ?, ?, ?)""",
                        data1)
            conn.commit()
    conn.close()


def count_records(cur):
    cur.execute("SELECT COUNT(*) FROM tbl_contactlist")
    count = cur.fetchone()[0]
    return cur, count


def load_contactlist(app):
    app.contactlist_entry_names = []
    app.contactlist_entry_ids = []
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT ID, col_fname, col_lname FROM tbl_contactlist ORDER BY LOWER(col_lname) ASC")
        rows = cur.fetchall()
    conn.close()
    for row in rows:
        app.contactlist_entry_names.append(row[1] + " " + row[2])
        app.contactlist_entry_ids.append(row[0])
    print_contactlist(app)


def print_contactlist(app):
    app.contactlist_box.delete(0, END)
    if app.contactlist_entry_names:

        # code below is for when you want to re-sort the list of names in contactlist before printing them in listbox
        # however we are sorting by last name from the SQL query, so the name list doesn't need to be sorted again.
        '''
        temp_entry_ids = []
        for v in app.contactlist_entry_ids:
            temp_entry_ids.append(v)

        sorted_ids = sorted(range(len(app.contactlist_entry_names)),
                            key=lambda k: app.contactlist_entry_names[k].split()[1])
        app.contactlist_entry_names = sorted(app.contactlist_entry_names, key=lambda n: n.split()[1])

        for i, v in enumerate(sorted_ids):
            app.contactlist_entry_ids[i] = temp_entry_ids[v]
        '''

        # put name list into listbox
        for i, n in enumerate(app.contactlist_entry_names):
            app.contactlist_box.insert(i, n)


def select_entry(app):
    index = app.contactlist_box.curselection()[0]
    query_id = (app.contactlist_entry_ids[index],)
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbl_contactlist WHERE ID = ?", query_id)
        entry = cur.fetchone()
    conn.close()
    for i in range(len(app.contactlist_fields)):
        app.contactlist_fields[i].set(entry[i])
    set_action_buttons(app, False)


def clear_form(app):
    clear_form_fields(app)
    set_action_buttons(app)
    app.action_frame.focus()
    app.contactlist_box.selection_clear(0, END)


def clear_form_fields(app):
    for i in app.contactlist_fields:
        i.set('')


def set_action_buttons(app, add=True):
    if add:
        app.btn_edit_person.grid_remove()
        app.btn_delete_person.grid_remove()
        app.btn_clear_form.grid_remove()
        app.btn_add_person.grid()
    else:
        app.btn_add_person.grid_remove()
        app.btn_edit_person.grid()
        app.btn_delete_person.grid()
        app.btn_clear_form.grid()
