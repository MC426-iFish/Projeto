def validate(name, email : str, password, password_check, user):
    if user:
        message = 'Este email já esta cadastrado.'
    elif len(email) < 4:
        message ='O email deve ter mais que 3 caracteres.'
    elif len(email) > 100:
        message ='O email deve ter menos que 100 caracteres.'
    elif len(name) < 2:
        message ='O nome deve ter mais que 1 caracter'
    elif len(name) > 100:
        message ='O nome deve ter menos que 100 caracteres'
    elif password != password_check:
        message ='As senhas não coincidem.'
    elif len(password) < 6:
        message ='A senha deve ter mais que 5 caracteres'
    elif len(password) > 100:
        message ='A senha deve ter menos que 100 caracteres'
    elif not email.endswith(".com"):
        message ='O email cadastrado não existe'
    else:
        return 'Conta Criada com Sucesso!', True
    return message, False
    