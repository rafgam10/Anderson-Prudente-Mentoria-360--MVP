from validate_docbr import CPF

# Validador de CPF do Aluno:
def validador_CPF(cpf):
    InstaCPF = CPF()
    if len(cpf) == 11 and InstaCPF.validate(cpf):
        print("CPF validado!")
    else:
        return ValueError
    
    return

