def validate(name, email : str, password, password_check, user):
    if user:
        message = 'Este e-mail já esta cadastrado.'
    elif len(email) < 4:
        message ='O e-mail deve ter mais que 3 caracteres.'
    elif len(email) > 100:
        message ='O e-mail deve ter menos que 100 caracteres.'
    elif len(name) < 2:
        message ='O nome deve ter mais que 1 caracter.'
    elif len(name) > 100:
        message ='O nome deve ter menos que 100 caracteres.'
    elif password != password_check:
        message ='As senhas não coincidem!'
    elif len(password) < 6:
        message ='A senha deve ter mais que 5 caracteres.'
    elif len(password) > 100:
        message ='A senha deve ter menos que 100 caracteres.'
    elif not email.endswith(".com"):
        message ='O e-mail cadastrado não é válido!'
    else:
        return 'Conta Criada com Sucesso!', True
    return message, False
    