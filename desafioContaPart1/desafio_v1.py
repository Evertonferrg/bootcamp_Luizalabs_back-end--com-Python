
import textwrap
from abc import ABC, abstractmethod

from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def ralizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        self.cpf = cpf

    
class Conta:

    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @abstractmethod
    def nova_conta(cls, cliente, numero):
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

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("#####Operação falhou! Saldo insuficiente.#####")

        elif valor > 0:
            self.saldo -= valor
            print(" #####Saque realizado com sucesso!#####")
            return True
        
        else:
            print(" #####Operação falhou! O valor informado é inválido.#####")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(" #####Deposito realizado com sucesso!#####")

        else: 
            print(" #####Operação falhou! O valor informado é inválido.#####")
            return False
        return True

    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    
    def sacar(self, valor):
        
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print(" #####Operação falhou! O valor do saque excede o limite.#####")

        elif excedeu_saques:
            print(" #####Operação falhou! Número máximo de saques excedido.#####")

        else:
            sucesso = super().sacar(valor)
            if sucesso:
                self.saques_realizados += 1
                return True
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:

    def __init__(self):
        self.transacoes = []

    @property
    def transacoes(self):
        return self._transacoes


    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
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
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.h

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        sucesso_transacao = conta.depositar(self.valor)

def menu():
    menu = """\n
    =====================MENU=====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    ==============================================
    => """
    return input(textwrap.dedent(menu))

def filtar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n*** Cliente não possui conta! ***")
        return
    
    # fixe nao permitir escolher entre a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.ralizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.ralizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    Transacao = conta.historico.transacoes

    extrato = ""
    if not Transacao:
        extrato += "\nNão foram realizadas movimentações."
    else:
        for Transacao in Transacao:
            extrato += f"\n{Transacao['tipo']}:\n\tR${Transacao['valor']:.2f}"
    
    print("\n =========================================")

def criar_cliente(clientes):

    cpf = input("Informe o CPF (somente números): ")
    cliente = filtar_cliente(cpf, clientes)

    if cliente:
        print("\n*** Já existe cliente com esse CPF! ***")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
                                

def criar_conta(numero_conta, clientes, contas):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado, fluxo de criação de conta encerrado! ***")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, 
                                     numero=numero_conta)
    

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()