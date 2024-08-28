
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
        valor = float(input("Informe o valor do depósito R$: "))
        
        if valor > 0:
            saldo += valor
            extrato += f"Depósito R$ {valor:.2f}\n"
        else:
            print("ERRO! O valor informado é inválido!")
    
    elif opcao == "s":
        valor = float(input("Informe o valor do saque R$: "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques > LIMITE_SAQUES

        if excedeu_saldo:
            print("ERRO! Infelizmente você não tem saldo suficiente para essa transação.")
        
        elif excedeu_limite:
            print("Operação invalida! O valor do saque excede o seu limite (R$500.00)")
        
        elif excedeu_saques:
            print("Operação invalida: Você excedeu o limite de saques diarios!")
        
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        
        else:
            print("Operação falhou! O valor informado é inválido!")
    
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        
        print(f"\nSaldo: R$ {saldo:.2f}")
        print()
        print("Obrigado por utilizar nossos serviços!")
        print("==========================================")
    
    elif opcao == "q":
        print("Obrigado por utilizar nosso serviços!")
        break
    else:
        print()
        print("Opção inválida, por favor selecione novamente a operação desejada.")
        print()