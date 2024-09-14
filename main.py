import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import getpass


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\n
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco, senha):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf  # CPF já armazenado sem separadores
        self.endereco = endereco
        self.senha = senha
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"  # Número fixo da agência
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
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

    def sacar(self, *, saldo, valor, extrato, limite, numero_saques, limite_saques):
        """Função que só recebe argumentos por nome (keyword only)"""
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            saldo -= valor
            numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        return saldo, extrato

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))  # Adiciona transação ao extrato
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0  # Controla o número de saques realizados

    def sacar(self, valor):
        saldo, extrato = super().sacar(
            saldo=self.saldo,
            valor=valor,
            extrato=self.historico.transacoes,
            limite=self._limite,
            numero_saques=self._numero_saques,
            limite_saques=self._limite_saques
        )
        self._saldo = saldo
        self.historico.adicionar_transacao(Saque(valor))  # Adiciona transação ao extrato

    # Modificando para exibir extrato corretamente
    def exibir_extrato(self, saldo, /, *, extrato):
        """Função que recebe argumentos por posição e nome"""
        print("\n================ EXTRATO ================")
        for transacao in extrato:
            print(f"{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}")
        print(f"\nSaldo:\n\tR$ {saldo:.2f}")
        print("==========================================")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = [
            transacao for transacao in self.transacoes
            if datetime.strptime(transacao['data'], "%d-%m-%Y %H:%M:%S").date() == data_atual
        ]
        return transacoes


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
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ").strip()
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return None

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    senha = getpass.getpass("Crie uma senha: ")

    cliente = Cliente(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco, senha=senha)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")
    return cliente


def criar_conta(contas, cliente):
    numero_conta = len(contas) + 1  # Número sequencial de conta
    conta = ContaCorrente(numero=numero_conta, cliente=cliente)
    cliente.contas.append(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")
    return conta


def filtrar_cliente(cpf, clientes):
    """Filtra o cliente pelo CPF, retorna None se não encontrado."""
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def login(clientes):
    cpf = input("Informe o CPF: ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return None
    senha = getpass.getpass("Informe a senha: ")
    if cliente.senha != senha:
        print("\n@@@ Senha incorreta! @@@")
        return None
    print("\n=== Login realizado com sucesso! ===")
    return cliente


def menu_preliminar():
    print("\n=============== BOAS VINDAS! ===============")
    print("[1] Criar Novo Perfil")
    print("[2] Login")
    print("[q] Sair")
    return input("Escolha uma opção: ")


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [mc]\tMudar conta
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def mudar_conta(cliente_logado):
    """Permite ao usuário mudar a conta ativa"""
    if len(cliente_logado.contas) < 2:
        print("\n@@@ O usuário possui apenas uma conta! @@@")
        return cliente_logado.contas[0]  # Se tiver só uma conta, retorna ela

    print("\n=== Escolha uma das contas abaixo ===")
    for i, conta in enumerate(cliente_logado.contas, 1):
        print(f"[{i}] Agência: {conta.agencia}, Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}")

    opcao = int(input("Escolha o número da conta: "))
    if 1 <= opcao <= len(cliente_logado.contas):
        return cliente_logado.contas[opcao - 1]
    else:
        print("\n@@@ Opção inválida! Selecionando a primeira conta por padrão. @@@")
        return cliente_logado.contas[0]


def main():
    clientes = []
    contas = []
    cliente_logado = None
    conta_ativa = None  # Adicionando a conta ativa

    while True:
        if not cliente_logado:
            opcao = menu_preliminar()

            if opcao == "1":
                cliente_logado = criar_cliente(clientes)
                if cliente_logado:
                    conta_ativa = criar_conta(contas, cliente_logado)

            elif opcao == "2":
                cliente_logado = login(clientes)
                if cliente_logado:
                    conta_ativa = cliente_logado.contas[0]  # Seleciona a primeira conta por padrão

            elif opcao == "q":
                break

            else:
                print("\n@@@ Operação inválida! Tente novamente. @@@")


        else:
            opcao = menu()

            if opcao == "d":
                valor = float(input("Informe o valor do depósito: "))
                conta_ativa.depositar(valor)

            elif opcao == "s":
                valor = float(input("Informe o valor do saque: "))
                conta_ativa.sacar(valor)

            elif opcao == "e":
                print(conta_ativa)
                print(conta_ativa.saldo)
                conta_ativa.exibir_extrato(conta_ativa.saldo, extrato=conta_ativa.historico.transacoes)

            elif opcao == "nc":
                conta_ativa = criar_conta(contas, cliente_logado)

            elif opcao == "lc":
                listar_contas(cliente_logado.contas)

            elif opcao == "mc":
                conta_ativa = mudar_conta(cliente_logado)  # Mudar conta ativa

            elif opcao == "q":
                cliente_logado = None
                conta_ativa = None  # Reseta a conta ativa
                print("\n=== Logout realizado com sucesso! ===")

            else:
                print("\n@@@ Operação inválida! Tente novamente. @@@")


if __name__ == "__main__":
    main()
