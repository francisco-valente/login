''' 
    Lógica de acesso e escrita nas bases de dados
    Autor: Francisco
    Data: 24 fev 2023
'''

# Bibliotecas
import os
from Model import *
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime


def create_files(*args):
    for i in args:
        if not os.path.exists(i):
            write_key()


create_files('key.key')


def write_key():
    '''
        Generates a key and save it into a file
    '''
    key = Fernet.generate_key()
    
    with open('key.key', 'wb') as key_file:
        key_file.write(key)


def load_key():
    '''
        Loads the key from the current directory named 'key.key'
    '''
    return open('key.key', 'rb').read()

# Generate and write a new key
# write_key()


def encrypt_password(password):
    # load the previously generated key
    key = load_key()
    
    message = password.encode()

    # message = 'some secret message'.encode()

    # Initialize the Fernet class
    f = Fernet(key)

    # Encrypt the message
    encrypted = f.encrypt(message)

    return encrypted

# encrypted = encrypt_password("123")

# print how it looks
# print(encrypted)


def decrypt_password(encrypted):
    # load the previously generated key
    key = load_key()

    # Initialize the Fernet class
    f = Fernet(key)

    # decrypt the message
    decrypted_encrypted = f.decrypt(encrypted) 

    return decrypted_encrypted

# encrypted_password = decrypt_password(encrypted)

# print decrypted message
# print(encrypted_password)


def returnSession():
    USER="root"
    PASSWORD=""
    HOST="localhost"
    PORT=3306
    BD="login_system"
    CONN=f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{BD}'

    try:
        # Create a connection engine with information that has been received with parameters
        # Parameters: USER/PASSWORD/HOST/PORT/BD
        engine = create_engine(CONN, echo=True)
        # Create a connection has joined with engine has been created above
        Session = sessionmaker(bind=engine)
        # Session function will return the active session
        return Session()
    except Exception as e:
        print(f'erro {e}')


class DaoUser:

    @classmethod
    # Salve user
    def salve(cls, user:User):
        
        try:
            session = returnSession()
            user.password = encrypt_password(str(user.password))
            session.add(user)
            session.commit()
            print(f'O usuário {user.name} foi incluído com sucesso! ')
        except Exception as e:
            print(f'Erro {e}')


    @classmethod
    # Delete user
    def delete(cls, id):
        try:
            session = returnSession()
            # If user exists, delete it
            x = session.query(User).filter(User.id == id).one()
            session.delete(x)
            session.commit()
            print(f'O usuário {id} foi deletado com sucesso!')
            return True
        except Exception as e:
            print(f'erro {e}')
            return False

        
    @classmethod
    # Update user
    def update(cls, emailUpdate, user:User):
        print(emailUpdate, user.name, user.email, user.password)
        try:
            session = returnSession()
            # If user exists, update your information
            x = session.query(User).filter(User.email == emailUpdate).all()
            x[0].name = user.name
            x[0].email = user.email
            x[0].password = encrypt_password(user.password)
            session.commit()
            print(f'O usuário {user.name} foi atualizado com sucesso!')
            return True
        except Exception as e:
            print(f'erro {e}')
            return False


    @classmethod
    # Read user
    def read(cls, email):
        try:
            session = returnSession()
            # Filter user if email exists
            x = session.query(User).filter(User.email == email).all()
            # print(x[0].name)
            # print(x[0].email)
            # print(x[0].password)
            return x
        except Exception as e:
            print(f'Erro {e}')
            return None

    @classmethod
    # Read all users
    def readAll(cls):
        try:
            session = returnSession()
            x = session.query(User).all()
            print('--- Lista de usuários ---')
            print('Nome     E-mail')
            if len(x) > 1:
                for i, u in enumerate(x):
                    print(f'{u.name}    {u.email}')
            else:
                print(f'{x[0].name}     {x[0].email}')
            print('-------------------------')
        except Exception as e:
            print(f'Erro {e}')

class DaoLogin:

    @classmethod
    # Verify if email exists
    def existsEmail(cls, email):
        try:
            session = returnSession()
            # If email was finded, return UserID, userPassword otherwise None
            x = session.query(User).filter(User.email == email).all()
            if len(x) > 0:
                id = x[0].id
                ret = decrypt_password(x[0].password)
                # print(id, ret.decode())
                return id, ret.decode()
            else:
                print(f'O e-mail {email} não existe!')
                return None, None
        except Exception as e:
            print(f'Erro {e}')
            return None, None


    @classmethod
    # Salve login
    def salve(cls, login: Login):
        '''
            Login Class
            Parameters:
                email: User's email
                passoword: User's password
            Return:
                True
                False
        '''
        # Verify if email exists on user's register and return user's password otherwise None
        userId, userPassword = DaoLogin.existsEmail(login.email)
        # If it's True salve on login's register

        if userPassword != None:
            if userPassword == login.password:
                session = returnSession()
                x = session.query(Login).filter(Login.user_id == login.user_id).all()
                if len(x) > 0:
                    print('Usuário logado!')
                    return True
                else:
                    try:
                        login.user_id = userId
                        login.password = encrypt_password(login.password)
                        # login.lastLogin = datetime.now().strftime('%d/%m/%Y')
                        session.add(login)
                        session.commit()
                        print('Usuário logado!')
                        return True
                    except Exception as e:
                        print(f'Erro {e}')
                        return False
            else:
                print('O Usuário e/ou a Senha estão errados!')    
                return False
        else:
            print('O Usuário e/ou a Senha estão errados!')    
            return False

          
# user1 = User(name="Mimi",
#              email="mimi@gmail.com",
#              password="123"
#             )


# user2 = User(name="lili"
#              , email="lili@gmail.com"
#              , password="321" 
#         )


# DaoUser.salve(user2)
# DaoUser.delete(4)
# DaoUser.update("li@gmail.com",user2)
# r = DaoUser.read('mimi@gmail.com')
# print(r[0].name, r[0].email, r[0].password)

# id = 4
# DaoLogin.existsEmail('mimi@gmail.com')
# print(datetime.now().strftime('%d/%m/%Y'))
# DaoLogin.salve(Login(email="mimi@gmail.com", password="123", user_id=0, lastLogin = datetime.now().strftime('%Y/%m/%d %H:%M')))

# print(decrypt_password("gAAAAABkEE1aqw1AVsr5gU_ScAUUK4Lr6C4qU-WHwJvqZxdM3QZIRqxqaMso2W3nO20EIajY3y4oej2JYaFgrl21HwmIF-Ys1w=="))

# DaoUser.readAll()
