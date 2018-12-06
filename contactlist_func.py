import sqlite3
from tkinter import *


# define database to use
def db_conn():
    conn = sqlite3.connect('db/contactlist.db')
    return conn


def add_person(app):
    # return if first name or last name empty
    # TODO: add alert to notify first, last name required
    if app.text_first_name.get() == "" or app.text_last_name.get() == "":
        return

    # put input fields into tuple
    insert_row = (app.text_first_name.get(), app.text_last_name.get(), app.text_email.get(),
                  app.text_phone_number.get(), app.text_address.get())
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        sql_query = "INSERT INTO tbl_contactlist (col_fname, col_lname, col_email, col_phone, col_address)"\
                    "VALUES (?, ?, ?, ?, ?)"
        cur.execute(sql_query, insert_row)
        conn.commit()
    conn.close()
    clear_form_fields(app)
    load_contactlist(app)


def edit_person(app):
    if app.text_first_name.get() == "" or app.text_last_name.get() == "":
        return
    update_row = (app.text_first_name.get(), app.text_last_name.get(), app.text_email.get(),
                  app.text_phone_number.get(), app.text_address.get(), app.text_id.get())
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        sql_query = "UPDATE tbl_contactlist SET col_fname=?, col_lname=?, col_email=?, col_phone=?, col_address=?"\
                    "WHERE ID=?"
        cur.execute(sql_query, update_row)
        conn.commit()
    conn.close()
    clear_form(app)
    load_contactlist(app)


def delete_person(app):
    delete_row = (app.text_id.get(),)
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        sql_query = "DELETE FROM tbl_contactlist WHERE ID=?"
        cur.execute(sql_query, delete_row)
        conn.commit()
    conn.close()
    clear_form(app)
    load_contactlist(app)


def create_db():
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        sql_query = "CREATE TABLE IF NOT EXISTS tbl_contactlist ("\
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"\
                    "col_fname TEXT,"\
                    "col_lname TEXT,"\
                    "col_email TEXT,"\
                    "col_phone TEXT,"\
                    "col_address TEXT)"
        cur.execute(sql_query)
        conn.commit()
    conn.close()
    first_run()


def first_run():
    test_user = ('John', 'Doe', 'john@mail.com', '123-456-7890', '123 Main St.',)
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        cur, count = count_records(cur)
        if count < 1:
            sql_query = "INSERT INTO tbl_contactlist (col_fname, col_lname, col_email, col_phone, col_address)"\
                        "VALUES (?, ?, ?, ?, ?)"
            cur.execute(sql_query, test_user)
            conn.commit()
    conn.close()


def count_records(cur):
    sql_query = "SELECT COUNT(*) FROM tbl_contactlist"
    cur.execute(sql_query)
    count = cur.fetchone()[0]
    return cur, count


def load_contactlist(app):
    # clear contact list
    app.contactlist_list.clear()
    conn = db_conn()
    with conn:
        cur = conn.cursor()
        sql_query = "SELECT ID, col_fname, col_lname FROM tbl_contactlist ORDER BY LOWER(col_lname) ASC"
        cur.execute(sql_query)
        rows = cur.fetchall()
    conn.close()
    for row in rows:
        # put each ID and name into tuple and add to contactlist list
        app.contactlist_list.append((row[0], row[1] + " " + row[2]))
    print_contactlist(app)


def print_contactlist(app):
    app.contactlist_box.delete(0, END)
    if app.contactlist_list:
        # put name list into listbox
        for i, n in enumerate(app.contactlist_list):
            app.contactlist_box.insert(i, n[1])


def select_entry(app):
    index = app.contactlist_box.curselection()[0]
    print(str(index) + ", " + str(app.active_contactbox_index))
    # check if selected index is not already active
    # if already active, then no need to do everything below
    if index != app.active_contactbox_index:
        app.active_contactbox_index = index
        query_id = (app.contactlist_list[index][0],)
        conn = db_conn()
        with conn:
            cur = conn.cursor()
            sql_query = "SELECT * FROM tbl_contactlist WHERE ID = ?"
            cur.execute(sql_query, query_id)
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
    app.active_contactbox_index = -1


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
