import unittest

from utils.signup_validator import validate

class TestCadastro(unittest.TestCase):
    def test_already_signed_up(self):
        message, validation = validate("joca", "jotape@gmail.com",  "ABC123", "ABC123", True)
        exp_msg = 'Este email já esta cadastrado.'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)
    
    def test_mail(self):
        message, validation = validate("Joao Carlos", "jc",  "JCzik123", "JCzik123", False)
        exp_msg = 'O email deve ter mais que 3 caracteres.'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

        message, validation = validate("Joao Carlos", "jcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  "JCzik123", "JCzik123", False)
        exp_msg ='O email deve ter menos que 100 caracteres.'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

    def test_name_length(self):
        message, validation = validate("J", "jotape@gmail.com",  "JCzik123", "JCzik123", False)
        exp_msg = 'O nome deve ter mais que 1 caracter'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

        message, validation = validate("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "jotape@gmail.com",  "JCzik123", "JCzik123", False)
        exp_msg ='O nome deve ter menos que 100 caracteres'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

    def test_password(self):
        message, validation = validate("Jotape", "jotape@gmail.com",  "JCzik123", "JCziK123", False)
        exp_msg = 'As senhas não coincidem.'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

        message, validation = validate("Jotape", "jotape@gmail.com",  "JCcca", "JCcca", False)
        exp_msg = 'A senha deve ter mais que 5 caracteres'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

        message, validation = validate("Jotape", "jotape@gmail.com",  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", False)
        exp_msg = 'A senha deve ter menos que 100 caracteres'
        exp_val = False
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)

    def test_normal(self):
        message, validation = validate("Jotape", "jotape@gmail.com",  "jotapemonstro", "jotapemonstro", False)
        exp_msg = 'Conta Criada com Sucesso!'
        exp_val = True
        self.assertEqual(message, exp_msg)
        self.assertEqual(validation, exp_val)