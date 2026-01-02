from abc import ABC, abstractmethod,
abstractproperty
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
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
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
    sucessso_transacao = conta.depositar(self.valor)

    if sucessso_transacao:
            conta.historico.adicionar_transacao(self)

