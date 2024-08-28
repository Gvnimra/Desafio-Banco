
menu = """

         ***  BANCO DIGITAL ***

Olá, seja bem-vindo ao nosso banco digital!
Por favor, selecione uma das opções abaixo:

[d] - Depositar
[s] - Sacar
[e] - Extrato
[q] - Sair

Opção Selecionada: """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Depósito")
    
    elif opcao == "s":
        print("Saque")
    
    elif opcao == "e":
        print("Extrato")
    
    elif opcao == "q":
        break