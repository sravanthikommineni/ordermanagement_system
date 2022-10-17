from contextlib import nullcontext
import os 
import mysql.connector

database_connection= mysql.connector.connect(
  host="localhost",
  user="root",
  password="Srav123@",
  database="ordermanagement_system"
)
cursor = database_connection.cursor()

import sys

def create_order():
  get_id = """select order_id from orderline order by order_id desc limit 1"""
  cursor.execute(get_id)
  order_id_res = cursor.fetchall()
  if order_id_res:
      order_id = int(order_id_res[0][0])
      order_id = (str(order_id + 1), )
  else:
      order_id = ('1', )
  get_id = """insert into orderline(order_id) values (%s)"""
  cursor.execute(get_id, order_id)
  database_connection.commit()
  print("Order created with id ",order_id[0])

def  add_order_line(ord_id, prd_name, product_qnt):
  product_name = (prd_name, )
  quantity = str(product_qnt)
  order_id = (str(ord_id), )

  check_product = """select product_name from products where product_name=%s"""
  cursor.execute(check_product, product_name)
  check_product_res = cursor.fetchall()
  if not check_product_res:
      return "Product is not available"
      

  check_order_id = """select order_id from orderline where order_id=%s"""
  cursor.execute(check_order_id, order_id)
  order_id_res = cursor.fetchall()
  if not order_id_res:
      return "Order id is not available"
  update_product = "UPDATE orderline SET product_name = '{}', product_quantity = '{}', status = 'Draft' WHERE order_id = '{}'".format(product_name[0],quantity,order_id[0])
  cursor.execute(update_product)
  database_connection.commit()

  return "{} {} added to order {}".format(quantity, product_name[0], order_id[0])

def show_order_id(order_id):
  get_order = """select * from orderline where order_id=%s"""
  cursor.execute(get_order, (str(order_id), ))
  get_order_res = cursor.fetchall()
  for x in get_order_res:
    print("Order", x[0], "Draft", x[1])
    print(x[2], x[1], "Draft")

def show_orders():
  get_order = """select * from orderline"""
  cursor.execute(get_order)
  get_order_res = cursor.fetchall()
  for x in get_order_res:
    if x[2]:
      print("Order", x[0], "Draft", x[1])
      print(x[2], x[1], "Draft")

given_command = sys.argv[0]
if given_command == "CREATE_ORDER":
  create_order()
elif given_command == "ADD_ORDERLINE":
  order_id = sys.argv[2]
  product_name = sys.argv[3]
  product_qnt = sys.argv[4]
  response = add_order_line(order_id, product_name, product_qnt)
  print(response)
elif given_command == "SHOW_ORDER":
  show_order_id(sys.argv[2])
elif given_command == "SHOW_ORDERS":
  show_orders()

select=input("Please select any one option below \n 1.CREATE_ORDER\n 2.ADD_PRODUCT\n 3.SHOW_ORDER \n 4.SHOW_ORDERS\n")
if select=="CREATE_ORDER":
  create_order()
elif select=="ADD_PRODUCT":
  add_order_line()
elif select=="SHOW_ORDER":
  show_order_id()
elif select=="SHOW_ORDERS":  
 show_orders()
else :
 print("please select valid option")

