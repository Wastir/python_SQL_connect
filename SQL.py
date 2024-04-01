import mysql.connector
import click
from tkinter import *

"""
Usage:

python SQL.py add <product_name> <product_price> <quantity>
python SQL.py list
python SQL.py remove <product_name>

"""


MYDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)

name = "poduszka"
price = 10
quantity = 5
MYCURSOR = MYDB.cursor()





@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if not ctx.invoked_subcommand:
        root = Tk()
        root.geometry('600x300')
        btn = Button(root, text="Pobierz produkty", command=lambda: tkinter_report(root))
        btn.pack()
        root.mainloop()


@cli.command()
@click.argument('name', type=str)
@click.argument('price', type=int)
@click.argument('quantity', type=int)
def add(name, price, quantity):
    try:
        MYCURSOR.execute("CREATE TABLE IF NOT EXISTS product (name VARCHAR(255), price REAL, quantity INT)")
        MYCURSOR.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        MYDB.commit()
        print("Product added successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Rollback the transaction if an error occurred
        MYDB.rollback()
    print(MYCURSOR.rowcount, "record inserted.")
    MYCURSOR.close()
    MYDB.close()
    

@cli.command()
def report():
    MYCURSOR.execute("SELECT * FROM products")
    results = MYCURSOR.fetchall()
    if not results:
        print("No products found")
    else:
        print(f"Name|Price|Quantity")
        for result in results:            
            print(f"{result[0]}, {result[1]}, {result[2]}")
    return results


    
@cli.command()
@click.argument('name', type=str)
def remove(name):
    MYCURSOR.execute("DELETE FROM products WHERE name = %s", (name,))
    MYDB.commit()
    print(MYCURSOR.rowcount, "record(s) deleted")
    MYCURSOR.close()
    MYDB.close()


if __name__ == '__main__':
    cli()
    #Tkinter
    