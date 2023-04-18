import Controller
import pwinput

if __name__ == "__main__":
    while True:
        print('--- MENU PRINCIPAL ---')
        menu = int(input('Digite 0 para ( Login ) no sistema\n'
                     'Digite 1 para ( Cadastrar ) usuário\n'
                     'Digite 2 para ( Remover ) usuário\n'
                     'Digite 3 para ( Atualizar ) usuário\n'
                     'Digite 4 para ( Listar ) os usuários\n'
                     'Digite 9 para ( Sair )\n'
        ))
        if menu == 9:
            break
        elif menu == 0:
            log = Controller.ControllerLogin()
            while True:
                print('--- Login ---')
                email = input('Digite o email ou 0 para Sair\n')
                if email == "0":
                    break
                password = pwinput.pwinput('Digite a senha\n')
                if log.login(email, password):
                    print(F'{email} logado no sistema.')
                    break
        elif menu == 1:
            while True:
                print('--- Cadastrar Usuários ---')
                name = input('Digite o nome do usuário ou 0 para sair\n')
                if name == "0":
                    break
                email = input('Digite o e-mail do usuário\n')
                password = input('Digite a senha do usuário\n')

                user = Controller.ControllerUser()
                if user.insertUser(name, email, password):
                    break

        elif menu == 2:
            while True:
                print('--- Remover Usuários ---')
                emailRemover = input('Digite o email do usuário a ser removido ou 0 para sair\n')
                if emailRemover == "0":
                    break

                user = Controller.ControllerUser()
                if user.removeUser(emailRemover):
                    break
        elif menu == 3:
            while True:
                print('--- Atualizar Usuários ---')
                emailUpdate = input('Digite o e-mail do usuário a ser alterado ou 0 para Sair\n')
                if emailUpdate == "0":
                    break
                name = input('Digite o nome do usuário\n')
                email = input('Digite o e-mail do usuário\n')
                password = input('Digite a senha do usuário\n')

                user = Controller.ControllerUser()
                if user.updateUser(emailUpdate, name, email, password):
                    break

        elif menu == 4:
            user = Controller.ControllerUser()
            user.listUsers()
        else:
            print('Opção inválida!')
