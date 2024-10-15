from abc import ABC, abstractmethod
from datetime import datetime

def menu():
    print("\n" + "="*34)
    print(" " * 14 + "MENU")
    print("="*34)
    print("1. Criar nova conta")
    print("2. Realizar depósito")
    print("3. Realizar saque")
    print("4. Exibir histórico de transações")
    print("0. Sair")
    print("="*34)

def criar_conta(clientes):
    print("\n" + "-"*30)
    print(" " * 10 + "Criação de Conta")
    print("-"*30)
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    numero_conta = len(clientes) + 1
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    cliente.adicionar_conta(conta)
    clientes.append(cliente)
    print("\n=== Conta criada com sucesso! ===")

def encontrar_conta(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente.contas[0]
    return None

def main():
    clientes = []
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            criar_conta(clientes)
        elif opcao == '2':
            cpf = input("CPF do cliente: ")
            conta = encontrar_conta(clientes, cpf)
            if conta:
                valor = float(input("Valor do depósito: "))
                deposito = Deposito(valor)
                conta.cliente.realizar_transacao(conta, deposito)
            else:
                print("\n@@@ Conta não encontrada. @@@")
        elif opcao == '3':
            cpf = input("CPF do cliente: ")
            conta = encontrar_conta(clientes, cpf)
            if conta:
                valor = float(input("Valor do saque: "))
                saque = Saque(valor)
                conta.cliente.realizar_transacao(conta, saque)
            else:
                print("\n@@@ Conta não encontrada. @@@")
        elif opcao == '4':
            cpf = input("CPF do cliente: ")
            conta = encontrar_conta(clientes, cpf)
            if conta:
                print("\n" + "-"*30)
                print(" " * 10 + "Histórico de Transações")
                print("-"*30)
                for transacao in conta.historico.transacoes:
                    print(f"{transacao['tipo']} - {transacao['valor']} - {transacao['data']}")
            else:
                print("\n@@@ Conta não encontrada. @@@")
        elif opcao == '0':
            break
        else:
            print("\n@@@ Opção inválida. @@@")

if __name__ == "__main__":
    main()


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
