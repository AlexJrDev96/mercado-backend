import random


class UserDomain:
    def __init__(self, id, name, cnpj, email, celular, status, activation_code):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.status = status
        self.activation_code = activation_code
        

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
        }
