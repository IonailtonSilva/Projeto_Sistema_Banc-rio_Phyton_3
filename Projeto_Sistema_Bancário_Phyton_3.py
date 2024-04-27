import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


print("======= SEJA BEM VINDO A SUA CONTA ==========")
print("======== O QUE DESEJA FAZER HOJE?! ==========")

class cliente:
    def __init__(self, endereço):
        self.endereço = endereço
        self.contas = []
          
    def realizar_traansacao(self,conta, transacao):
        transacao.registrar(conta)

    def adcionar_conta(self, conta):
        self.conta.append(conta) 

class pessoaFisica(cliente):
    def __init__(self, nome, dataNascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dataNascimento = dataNascimento
        self.cpf = cpf

class conta:
    def __init__(self, numeroConta, usuario):
        self._saldo = 0
        self._numero = numeroConta
        self._agencia = "0001"
        self._usuario = usuario
        self._historico = historico()

    @classmethod
    def novaConta(cls, usuario, numeroConta):
        return cls(numeroConta, usuario)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._usuario
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):

        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n === Operação falhou! Você não tem saldo suficiente. ===")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n=== Operação falhou! O valor informado é inválido. ===")
            return False

        return True

class contaCorrente(conta):

    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numeroConta}
            Titular:\t{self.usuario.nome}
        """

class historico:
     
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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)    

class saque(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class deposito(transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():

    print("""

[1] - Depositar
[2] - Saque
[3] - Extrato
[4] - Novo Usuario
[5] - Nova Conta
[6] - Listar Usuarios                      
[7] - Sair

""")


def depositar(usuarios):

    cpf = input("Informe o CPF do cliente: ")
    usuario = filtrarUsuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    deposito = float(input("\nOk!...Quanto deseja depositar?: "))

    print("\n")
   
    saldo, extrato = depositar(usuario)  
    
    if deposito > 0:

        print(f"\n===== Seu depósito de: R${deposito: .2f}, foi realizado com sucesso!=====\n")

        saldo += deposito
        extrato += f"Você Efetuou Um Deposito de:R${deposito: .2f}\n"

    else:
        
        print("\n===== A OPERAÇÂO FALHOU, TENTE NOVAMENTE! =====\n")  

    return saldo, extrato


def sacar(saque, saldo, limite, extrato, quant_saques, limite_saques):

    if saque <= limite:

            print("\n===OPERAÇÃO REALIZADA COM SUCESSO! AGUARDE A CONTAGEM DAS CÉDULAS===\n")

    if saque > saldo:

            print("\n=====OPERACAO INVÁLIDA, SALDO INSUFICIENTE!=====\n")

    elif saque > limite:

            print("\n=====OPERACAO INVÁLIDA, LIMITE DE SAQUE EXCEDIDO!=====")

    elif quant_saques >= limite_saques:
        
            print("\n=====OPERACAO INVÁLIDA, LIMITE DE SAQUES DIARIOS EXCEDIDO!=====")

    elif saque > 0:

            saldo -= saque 
            extrato += f"Você realizou um saque de: R$ {saque:.2f} \n"
            quant_saques += 1
        

    else:

        print("=====OPERAÇAO INVÁLIDA, TENTE NOVAMENTE!=====")
    

    return saldo, extrato, 


def exibirExtrato(saldo, extrato):
     
    print("\nOK... Vamos Ao Seu Extrato!\n")
    print("=================Extrato====================\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================")


def novaConta(agencia, numeroConta, usuarios):

    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrarUsuario(cpf, usuarios)

    if usuario:
        print("\n\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numeroConta, "usuario": usuario}

    print("\n=== Usuário não encontrado, fluxo de criação de conta encerrado! ===")          


def novoUsuario(usuarios):

    print("Ok... Criando Um Novo Usuario")
    cpf = (input("Digite o Seu CPF: "))
    usuario = filtrarUsuario(cpf, usuarios)

    if usuario:
            print("\n=== Já existe usuário com esse CPF! ===")
            return
    
    nome = input("Digite Seu Nome: ")
    dataNascimento = input("digite sua data de nascimento (dd-mm-aa): ")
    endereco = input("Digite seu endereço(Rua,Nº - Bairro, cidade/UF): ")

    usuarios.append({"nome": nome, "data_nascimento": dataNascimento, "cpf": cpf, "endereco": endereco})

    print(f"\n=== Usuário criado com sucesso! ===")


def filtrarUsuario(cpf, usuarios):
        usuariosFiltrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
        return usuariosFiltrados[0] if usuariosFiltrados else None


def listarContas(contas):

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():


    opcao = 0
    saldo = 0
    limite = 500
    extrato = ""
    quant_saques = 0
    limite_saques = 3
    usuarios = []
    conta = []
    agencia = "0001"

    while opcao != 7:

        menu()

        opcao = int(input("Selecione Uma Das Opçoes Acima: "))

        if opcao == 1:

            print("\nVoce Escolheu a Opção de Depósito!")

            depositar(usuarios)

        elif opcao == 2:

            print("\nEntendi, Você Gostaria de Sacar!\n")

            sacar(saque, saldo, limite, extrato, quant_saques, limite_saques)
        elif opcao == 3:

            exibirExtrato(saldo, extrato = extrato)

        elif opcao == 4:

            novoUsuario(usuarios)

        elif opcao == 5:

            print("Vamos Iniciar o Processo de Criação de Conta...")

            numeroConta = len(contas) + 1
            conta = novaConta(agencia, numeroConta, usuarios)

            if conta:
                contas.append(conta)  

        elif opcao == 6:

            listarContas(contas)    

        elif opcao == 7:
        
            print("\n==========SISTEMA FINALIZADO!===========")
            print("\n=============VOLTE SEMPRE!==============")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
