from tkinter import *
import mysql.connector

MYDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)

MYCURSOR = MYDB.cursor()
root = Tk()
root.geometry('600x400')

def tkinter_report():
    # Usuń stare dane
    for widget in root.winfo_children():
        if widget != btn and widget != add_btn:  # Nie usuwaj przycisków
            widget.destroy()

    results = report()
    if not results:
        select_label = Label(root, text="No products found")
        select_label.pack()
    else:
        select_label = Label(root, text="Name | Price | Quantity")
        select_label.pack()
        for result in results:
            product_info = f"{result[0]} | {result[1]} | {result[2]}"
            product_label = Label(root, text=product_info)
            product_label.pack()

def report():
    MYCURSOR.execute("SELECT * FROM products")
    results = MYCURSOR.fetchall()
    return results

def show_add_fields():
    name_label.pack()
    name_entry.pack()
    price_label.pack()
    price_entry.pack()
    quantity_label.pack()
    quantity_entry.pack()
    add_btn.pack_forget()  # Ukryj przycisk "Add" po kliknięciu
    submit_btn.pack()

def show_remove_fields():
    remove_label.pack()
    remove_entry.pack()
    remove_product_btn.pack()
    remove_btn.pack_forget()

def add_product():
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if name and price and quantity:
        sql = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
        val = (name, price, quantity)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        tkinter_report()  # Odśwież listę produktów po dodaniu nowego produktu
    else:
        error_label = Label(root, text="Wypełnij wszystkie pola!")
        error_label.pack()


def remove_product():
    remove_label.pack()
    remove_entry.pack()
    remove_btn.pack_forget()  # Ukryj przycisk "Remove" po kliknięciu
    add_btn.pack_forget()  # Ukryj przycisk "Add"
    btn.pack_forget()  # Ukryj przycisk "Pobierz produkty"
    remove_submit_btn.pack()  # Pokaż przycisk "Confirm Remove"
def confirm_remove_product():
    name = remove_entry.get()

    if name:
        sql = "DELETE FROM products WHERE name = %s"
        val = (name,)
        MYCURSOR.execute(sql, val)
        MYDB.commit()
        tkinter_report()  # Odśwież listę produktów po usunięciu produktu
    else:
        error_label = Label(root, text="Wpisz nazwę produktu do usunięcia!")
        error_label.pack()

name_label = Label(root, text="Name:")
name_entry = Entry(root)
price_label = Label(root, text="Price:")
price_entry = Entry(root)
quantity_label = Label(root, text="Quantity:")
quantity_entry = Entry(root)

add_btn = Button(root, text="Add", command=show_add_fields)
submit_btn = Button(root, text="Submit", command=add_product)

remove_label = Label(root, text="Remove product by name:")
remove_entry = Entry(root)
remove_btn = Button(root, text="Remove", command=show_remove_fields)
remove_product_btn = Button(root, text="Remove product", command=remove_product)
remove_submit_btn = Button(root, text="Confirm Remove", command=confirm_remove_product)


remove_btn.pack()  # Pokaż przycisk "Remove" na starcie

add_btn.pack()
btn = Button(root, text="Pobierz produkty", command=tkinter_report)
btn.pack()

root.mainloop()
