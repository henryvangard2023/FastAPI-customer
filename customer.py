from curses.ascii import isdigit
import email
import mysql.connector

###########################################################################
# STATUS:   9/20/2022 12:08 PM                                            #
#                                                                         #
# DELETE statement completed and tested successfully both by name and ID   #
#                                                                         #
# Project is complete.                                                    #
#                                                                         #
# Please add the NOT FOUND feature for UPDATE and DELETE  if time permits #
#                                                                         #
# Next phase:  add GUI by tkinter                                         #
###########################################################################


def ConnectDB():
    global mydb, myCursor

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2597",
        database="customer"  # this is the database to use
    )

    myCursor = mydb.cursor()


#
# Disconnect/close the DB connection
#

def DisconnectDB():
    myCursor.close()


#
# Answer choices
#
choices = [1, 2, 3, 4, 100]

#################################
# The table name is: 'customer' #
#################################

# INSERT statement
insertSQL = 'INSERT INTO customer(customer_id, first_name, last_name, house_no, street, city, state, zip_code, phone_no, email) \
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

# SELECT statements
# by name
searchNameSQL = 'SELECT * FROM customer WHERE first_name = %s OR last_name = %s'

# by ID
searchIDSQL = 'SELECT * FROM customer WHERE customer_id = %s'
selectAll = 'SELECT * FROM customer'

# DELETE statments
# by name
delNameSQL = 'DELETE FROM customer WHERE first_name = %s or last_name = %s'

# by ID
delIDSQL = 'DELETE FROM customer WHERE customer_id = %s'

# All - not recommended
delAll = 'DELETE FROM customer'

# UPDATE statement
'''
updateSQL = 'UPDATE customer SET \
                first_name = %s, \
                last_name = %s, \
                house_no = %s, \
                street = %s,\
                city = %s, \
                state = %s, \
                zip_code = %s, \
                phone_no = %s, \
                email = %s \
                WHERE customer_id = %s'

cursor.execute(updateSQL, (valStr))
'''

# When a user pressed Enter instead of typing in a value, the field will be blank.
# The fields MUST NOT be blank.
# The user will be repeatedly prompted for a non blank/non empty value.
# This is mainly used for INSERT


def EnterCustomerID():
    id = ''
    while id == '':
        print('Please enter a value and do NOT just press the Enter key!')
        id = input('Customer ID: ')
    return id


def EnterFirstName():
    fn = ''
    while fn == '':
        print('Please enter a value and do NOT just press the Enter key!')
        fn = input('First Name: ')
    return fn


def EnterLastName():
    ln = ''
    while ln == '':
        print('Please enter a value and do NOT just press the Enter key!')
        ln = input('Last Name: ')
    return ln


def EnterHouseNo():
    hn = ''
    while hn == '':
        print('Please enter a value and do NOT just press the Enter key!')
        hn = input('House Number: ')
    return hn


def EnterStreet():
    st = ''
    while st == '':
        print('Please enter a value and do NOT just press the Enter key!')
        st = input('Street: ')
    return st


def EnterCity():
    city = ''
    while city == '':
        print('Please enter a value and do NOT just press the Enter key!')
        city = input('City: ')
    return city


def EnterState():
    st = ''
    while st == '':
        print('Please enter a value and do NOT just press the Enter key!')
        st = input('State: ')
    return st


def EnterZipCode():
    zip = ''
    while zip == '':
        print('Please enter a value and do NOT just press the Enter key!')
        zip = input('Zip Code: ')
    return zip


def EnterPhoneNo():
    ph = ''
    while ph == '':
        print('Please enter a value and do NOT just press the Enter key!')
        ph = input('Phone No: ')
    return ph


def EnterEmail():
    em = ''
    while em == '':
        print('Please enter a value and do NOT just press the Enter key!')
        em = input('Email: ')
    return em


# -------------#
# AddCustomer #
# -------------#


def AddCustomer():
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Add Menu <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('\n')

    customerID = input('Customer ID: ')
    firstName = input('First Name: ')
    lastName = input('Last Name: ')
    houseNo = input('House Number: ')
    street = input('Street: ')
    city = input('City: ')
    state = input('State: ')
    zipcode = input('Zip Code: ')
    phoneNo = input('Phone No: ')
    email = input('Email: ')

    valStr = (customerID, firstName, lastName, houseNo, street,
              city, state, zipcode, phoneNo, email)
    myCursor.execute(insertSQL, valStr)
    mydb.commit()


# -------------------------#
# Print the Search result #
# -------------------------#


def PrintSearch(myCur):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Results <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('\n')

    count = 1
    for customer in myCur:
        print(count, ' ', customer)
        count += 1


# --------------------------------------------#
# Create the ALL customer list from SELECT * #
# --------------------------------------------#

# Create the list of all customers returned from SELECT *
# This will be used to create the FAST API response

# 10/4/2022 5:58 PM

def CreateAllCustomers(myCur):
    global listCustomers

    listCustomers = []
    for customer in myCur:
        listCustomers.append(customer)


# ----------------#
# SearchCustomer #
# ----------------#

# Please add the NOT FOUND statement/try again


def SearchCustomer():
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Search Menu <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n')
    print('\n')

    print('1. By name\n')
    print('2. By customer ID\n')
    print('3. Update a customer\n')
    print('4. Search ALL\n')
    print('10. Return to Customer CRM - Main Menu\n')
    choice = input('Enter a choice: ')

    if int(choice) == 10:  # return to main menu
        return

    elif int(choice) == 1:  # by first or last name
        name = input('Enter the first or last name: ')
        myCursor.execute(searchNameSQL, (name, name))
        PrintSearch(myCursor)

    elif int(choice) == 2:  # by ID
        id = input('Enter the customer ID: ')
        myCursor.execute(searchIDSQL, (id,))
        PrintSearch(myCursor)

    elif int(choice) == 3:  # update a customer
        print('Pardon me!  This WILL NOT be implemented.')

    elif int(choice) == 4:  # search ALL
        myCursor.execute(selectAll)
        PrintSearch(myCursor)


# ----------------#
# UpdateCustomer #
# ----------------#

# cursor.execute ((UPDATE customer SET first_name = %s, ... email = %s WHERE customer_id = %s),
#                                  ('John', 'Vang', ...))

# Please add the NOT FOUND statement/try again

def UpdateCustomer():  # by customer ID only
    updateSQL = 'UPDATE customer SET '  # this has a blank at the end

    # this is the list of values which MUST be converted to a tuple with (valStr)
    # weird, it worked as a list
    valStr = []

    whereStr = 'WHERE customer_id = %s'

    # this is set to the first value
    # once the first value has been entered, this is set to False
    # then must prepend the ', ' the subsequent fields; otherwise, UPDATE won't be semantically correct
    firstVal = True

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Update Menu <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n')

    # this value is mandatory and cannot be blank because this is UPDATE by ID
    customerID = EnterCustomerID()

    print('\nEnter a value or press Enter to leave it blank.\n')

    #############################################################
    # START building the UPDATE command with the values entered #
    #############################################################

    firstName = input('First Name: ')
    if firstName != '':
        # concat to UPDATE command, always first
        updateSQL = updateSQL + 'first_name = %s '
        valStr.append(firstName)  # append the first name to the value string
        firstVal = False

    lastName = input('Last Name: ')
    if lastName != '':
        if firstVal:  # this is the first value entered by the user
            updateSQL = updateSQL + 'last_name = %s '
            firstVal = False
        else:  # this is not the first value, make sure it starts with the comma and a space
            updateSQL = updateSQL + ', last_name = %s '  # concat to UPDATE command
        valStr.append(lastName)

    houseNo = input('House Number: ')
    if houseNo != '':
        if firstVal:
            updateSQL = updateSQL + 'house_no = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', house_no = %s '  # concat to UPDATE command
        valStr.append(houseNo)

    street = input('Street: ')
    if street != '':
        if firstVal:
            updateSQL = updateSQL + 'street = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', street = %s '  # concat to UPDATE command
        valStr.append(street)

    city = input('City: ')
    if city != '':
        if firstVal:
            updateSQL = updateSQL + 'city = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', city = %s '  # concat to UPDATE command
        valStr.append(city)

    state = input('State: ')
    if state != '':
        if firstVal:
            updateSQL = updateSQL + 'state = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', state = %s '  # concat to UPDATE command
        valStr.append(state)

    zipcode = input('Zip Code: ')
    if zipcode != '':
        if firstVal:
            updateSQL = updateSQL + 'zip_code = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', zip_code = %s '  # concat to UPDATE command
        valStr.append(zipcode)

    phoneNo = input('Phone No: ')
    if phoneNo != '':
        if firstVal:
            updateSQL = updateSQL + 'phone_no = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', phone_no = %s '  # concat to UPDATE command
        valStr.append(phoneNo)

    email = input('Email: ')
    if email != '':
        if firstVal:
            updateSQL = updateSQL + 'email = %s '
            firstVal = False
        else:
            updateSQL = updateSQL + ', email = %s '  # concat to UPDATE command
        valStr.append(email)

    ###################################################################################
    # FINISH the UPDATE command with the WHERE clause and the tuple of values entered #
    ###################################################################################

    updateSQL = updateSQL + whereStr  # append the WHERE clause
    valStr.append(customerID)  # add the customer ID to the values

    # valStr is a list but it does NOT matter, execute () still works!!!
    # this is weird, it worked with valStr being a list (not a tuple)
    myCursor.execute(updateSQL, valStr)
    mydb.commit()  # commit the updates


# The following 2 functions are implemented for automated/batch processing:

# DELETE a customer by ID

def DeleteByID(id):
    myCursor.execute(delIDSQL, (id,))

# DELETE a customer by name


def DeleteByName(name):
    myCursor.execute(delNameSQL, (name, name))


# ----------------#
# DeleteCustomer #
# ----------------#

# Please add the NOT FOUND statement/try again

def DeleteCustomer():
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Delete Menu <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('\n')

    print('1. By name\n')
    print('2. By customer ID\n')
    print('10. Return to Customer CRM - Main Menu\n')
    choice = input('Enter a choice: ')

    if int(choice) == 10:  # return to main menu
        return

    elif int(choice) == 1:
        name = input('Enter the first or last name: ')
        # DeleteByName(name)
        myCursor.execute(delNameSQL, (name, name))

    elif int(choice) == 2:
        id = input('Enter the customer ID: ')
        # DeleteByID(id)
        myCursor.execute(delIDSQL, (id,))

    # commit the changes
    mydb.commit()


# -----------------------------------------------------------------------------------------------------------------#
# Main Menu #
# -----------------------------------------------------------------------------------------------------------------#

# If you're running this app stand alone

if __name__ == '__main__':
    ConnectDB()  # Connect to the DB

    choice = 0
    while int(choice) != 100:
        crmTitle = '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Customer CRM - Main Menu <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n'

        print(crmTitle)
        print('1. Add a customer\n')
        print('2. Search for a customer\n')
        print('3. Update a customer\n')
        print('4. Delete a customer\n')
        # 100 exits the loop right away with an if condition
        print('100. Exit\n')
        choice = input('Enter a number: ')

        if not choice.isdigit() or not int(choice) in choices:
            print('Please enter 1-4 or 100!')
            choice = 0
            continue

        if int(choice) == 1:    # Add a customer
            AddCustomer()
        elif int(choice) == 2:  # Search ...
            SearchCustomer()
        elif int(choice) == 3:  # Update a customer
            UpdateCustomer()
        elif int(choice) == 4:  # Delete a customer
            DeleteCustomer()
        elif int(choice) == 100:  # Exit
            DisconnectDB()      # Disconnect from database then break to exit
            break

# ------------------#
# End of Main Menu #
# ------------------#
