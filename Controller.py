from Model import User, Login
from DAO import DaoUser, DaoLogin
from datetime import datetime
import re
p = re.compile(r"[\s*\d+]")

class ControllerUser:
    def insertUser(self, name, email, password):
        x = DaoUser.read(email)
        if len(x) == 0:
            # print('usuário não existe!')
            if p.match(password):
                # print('Padrão OK')
                DaoUser.salve(User(name=name, email=email, password=password))
                return True
            else:
                print(p)
                print(f'A senha deve conter letras e números!')
                return False
        else:
            print('usuário já cadastrado!')
            return False


    def removeUser(self, removeEmail):
        x = DaoUser.read(removeEmail)
        # print(type(x))
        if len(x) <= 0:
            print('O usuário não existe!')
            return False
        else:
            # print(x[0].id)
            DaoUser.delete(x[0].id)
            print(f'O usuário {removeEmail} foi excluído com sucesso!')
            return True


    def updateUser(self, emailUpdate, name, email, password):
        user = DaoUser.read(emailUpdate)
        if len(user) <= 0:
            print('O usuário não existe!')
            return False
        else:
            DaoUser.update(emailUpdate, User(name = name, email = email, password = password))
            print(f'O usuário {user[0].email} foi atualizado com sucesso!')
            return True


    def listUsers(self):
        DaoUser.readAll()

class ControllerLogin:
    def login(self, email, password):
        if DaoLogin.salve(Login(email=email, password=password, lastLogin = datetime.now().strftime('%Y/%m/%d %H:%M'))):
            return True
        else:
            return False


# c = ControllerUser()
# c.insertUser('Teste2', 'teste2@gmail.com', 'teste2')
# c.removeUser("teste2@gmail.com")


c = ControllerLogin()
c.login("li@gmail.com", "123")