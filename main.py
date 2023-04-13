from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import sys
import json
import uvicorn
import customer as CUS

#################################################################
# Status -- 12/4/2022
#
# Finished:
#
# Add a customer --
#
#   @app.post('/adduser/{id}')
#   async def AddUser(id: int, user: User):
#
# It added a user to the database.
#
# Update a customer -- DONE on 4/9/23
#
#################################################################


class User(BaseModel):
    ID: int = None
    firstName: str = None
    lastName: str = None
    houseNo: str = None
    street: str = None
    city: str = None
    state: str = None
    zipCode: str = None
    phoneNo: str = None
    email: str = None


app = FastAPI()


def GetAllCustomers():
    CUS.ConnectDB()
    CUS.myCursor.execute(CUS.selectAll)

    # Create and save the list of all customers
    CUS.CreateAllCustomers(CUS.myCursor)

    # The global list of all the customers in the database
    global allCustomers

    allCustomers = CUS.listCustomers
    CUS.DisconnectDB()


def VerifyCustomer(id: int):
    GetAllCustomers()

    for cus in allCustomers:
        if cus[0] == id:     # The first field is the ID
            return True      # The customer with this id is found

    return False             # The customer with this id is not found

#################################################################
# GET
#################################################################

# Root/home page


@app.get('/')
async def Home():
    return {'Message': 'Welcome to CUSTOMER web services using FastAPI!'}


# Get all the customers

@app.get('/users')
async def GetUsers():
    GetAllCustomers()
    return allCustomers


# Get a customer by his/her ID

@app.get('/users/{id}')
async def GetUserByID(id: int):
    CUS.ConnectDB()
    CUS.myCursor.execute(
        'SELECT * FROM customer WHERE customer_id = %s', (id,))
    oneUser = CUS.myCursor.fetchone()
    CUS.DisconnectDB()

    if oneUser is None:
        return {'Message': 'ID is not found!'}

    return oneUser


# Get the customer by his/her first or last name

@app.get('/usersbyname/{name}')
async def GetUserByName(name: str):
    # Get all the users/customers from the database.
    # and store them in allCustomers
    GetAllCustomers()

    customersFound = []
    for customer in allCustomers:
        # index 1 is the first name and index 2 is the last nanme
        if customer[1].lower() == name.lower() or customer[2].lower() == name.lower():
            print(customer)
            customersFound.append(customer)

    if len(customersFound) == 0:
        return {'Message': 'User is not found!!!'}
    else:
        # return the list of customers found because there could be more than one by the name
        return customersFound

#################################################################
# PUT - Update a customer with the provided fields.
#################################################################


#
# Will get {"Method not allowed!" unless Postman is used or use the "localhost:8000/docs" route.
#

# Status:  As of 4/9/23, it's DONE.


@app.put('/update/{id}')
async def UpdateUser(id: int, user: User):
    updateSQL = 'UPDATE customer SET first_name=%s, last_name=%s, house_no=%s, street=%s, city=%s, state=%s, \
                 zip_code=%s, phone_no=%s, email=%s WHERE customer_id = %s'

    CUS.ConnectDB()
    CUS.myCursor.execute(updateSQL,
                         (user.firstName, user.lastName, user.houseNo, user.street,
                          user.city, user.state, user.zipCode, user.phoneNo, user.email, id))  # ID is last for the WHERE clause
    CUS.mydb.commit()
    CUS.DisconnectDB()

    return {'Message': 'Successfully updated!'}


#################################################################
# POST - Create a new customer and add it to the database.
#################################################################


@app.post('/adduser/{id}')
async def AddUser(id: int, user: User):
    insertSQL = 'INSERT INTO customer(customer_id, first_name, last_name, house_no, street, city, state, zip_code, phone_no, email) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    CUS.ConnectDB()
    CUS.myCursor.execute(insertSQL,
                         (id, user.firstName, user.lastName, user.houseNo, user.street,
                          user.city, user.state, user.zipCode, user.phoneNo, user.email))
    CUS.mydb.commit()
    CUS.DisconnectDB()

    return {'Message': 'Successfully added!'}


#################################################################
# DELETE
#################################################################


@app.delete('/deleteuser/{id}')
async def DeleteUser(id: int):
    # if not VerifyCustomer(id):
    #     return {'User is not found!!!'}

    # DELETE statement:
    # by ID
    delIDSQL = 'DELETE FROM customer WHERE customer_id = %s'

    CUS.ConnectDB()
    CUS.myCursor.execute(delIDSQL, (id,))
    CUS.mydb.commit()
    CUS.DisconnectDB()

    return {'Message': 'Successfully deleted!'}


@app.delete('/deleteuserbyname/{name}')
async def DeleteUser(name: str):
    # userFound = VerifyCustomer(name)  # Verify by ID only, could implement by name later
    # if userFound == None:
    #     return ('User is not found!!!')

    # DELETE statements:
    # by name
    delNameSQL = 'DELETE FROM customer WHERE first_name = %s or last_name = %s'

    CUS.ConnectDB()
    CUS.myCursor.execute(delNameSQL, (name, name))
    CUS.mydb.commit()
    CUS.DisconnectDB()

    return {'Message': 'Successfully deleted!'}

# The End!
