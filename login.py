import streamlit as st
from mysql_connection import my_Sql

# MySQL connection
conn, cursor = my_Sql('localhost', 'root', 'Janu19042002', 'ocr')

# Create table if not exists
def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_data(
            name VARCHAR(50),
            id VARCHAR(25) PRIMARY KEY, 
            Password VARCHAR(25)
        )
    ''')
    conn.commit()

# Store data in the table
def store_data(conn, cursor, name, user_id, password):
    query = '''
        INSERT INTO login_data (name, id, Password) 
        VALUES (%s, %s, %s)
    '''
    cursor.execute(query, (
        name,
        user_id,
        password
    ))
    conn.commit()

# Authenticate user
def authenticate_user(cursor, user_id, password):
    query = "SELECT name FROM login_data WHERE id = %s AND Password = %s"
    cursor.execute(query, (user_id, password))
    return cursor.fetchone()

# Create tables on start
create_tables(cursor)

# Streamlit UI
st.title('Streamlit Login and Registration Page')

menu = ['Login', 'Register']
choice = st.selectbox('Choose an option', menu)

if choice == 'Register':
    st.subheader('Register')
    user_name = st.text_input('Enter your name')
    user_id = st.text_input('Create an ID (e.g., dev310)')
    user_password = st.text_input('Create a password (A-Z, a-z, 0-9, special characters included)', type='password')
    
    if st.button('Register'):
        if user_name and user_id and user_password:
            try:
                store_data(conn, cursor, user_name, user_id, user_password)
                st.success('Registration successful!')
            except Exception as e:
                st.error(f'Error: {e}')
        else:
            st.warning('All fields are mandatory')

elif choice == 'Login':
    st.subheader('Login')
    login_id = st.text_input('Enter your ID')
    login_password = st.text_input('Enter your password', type='password')
    
    if st.button('Login'):
        if login_id and login_password:
            user = authenticate_user(cursor, login_id, login_password)
            if user:
                st.success(f'Welcome {user[0]}!')
            else:
                st.error("Incorrect ID or password, or you're not registered")
        else:
            st.warning('Please enter both ID and password')

# Close the cursor and connection when done
cursor.close()
conn.close()
