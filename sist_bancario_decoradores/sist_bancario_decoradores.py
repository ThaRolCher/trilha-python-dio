import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

# Definição do diretório raiz para gravação do arquivo de log
ROOT_PATH = Path(__file__).parent


def log_transacao(func):
    """Decorador que registra a execução de uma função no arquivo log.txt."""
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Evita quebras de linha no log para objetos com representação multiline
        if isinstance(resultado, (Cliente, Conta)):
            resultado_log = repr(resultado)
        else:
            resultado_log = str(resultado).replace("\n", " ")
            
        try:
            with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(
                    f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. "
                    f"Retornou {resultado_log}\n"
                )
        except IOError as e:
            print(f"\n@@@ Erro ao gravar o log no arquivo: {e} @@@")
        return resultado

    return envelope


class Cliente:
    """Representa um cliente do sistema bancário."""

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação na conta especificada, validando o limite diário."""
        # Limite diário de 10 transações
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Operação falhou! Você excedeu o número de transações permitidas para hoje. @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Associa uma nova conta ao cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Representa um cliente pessoa física, especializando a classe Cliente."""

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"


class Conta:
    """Representa uma conta bancária genérica."""

    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Fábrica para criar uma nova instância de conta."""
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
        """Debita um valor do saldo da conta, se houver saldo suficiente e valor for válido."""
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

    def depositar(self, valor):
        """Credita um valor no saldo da conta, se o valor informado for válido."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    """Especialização de Conta com limites de saque e quantidade diária de saques."""

    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar para validar limites específicos da conta corrente."""
        # Considera apenas os saques efetuados no dia de hoje
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes_do_dia()
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    """Mantém o registro histórico de transações de uma conta."""

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Registra uma transação no histórico com a data e hora do momento da execução."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def transacoes_do_dia(self):
        """Retorna a lista de transações efetuadas na data atual."""
        data_atual = datetime.now().date()
        transacoes_hoje = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_transacao == data_atual:
                transacoes_hoje.append(transacao)
        return transacoes_hoje


class Transacao(ABC):
    """Classe abstrata que define o comportamento padrão de uma transação bancária."""

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    """Transação de débito em conta."""

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
    """Transação de crédito em conta."""

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
    """Exibe o menu de opções e retorna a entrada do usuário."""
    menu_texto = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário (Cliente)
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def filtrar_cliente(cpf, clientes):
    """Filtra a lista de clientes por CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    """Retorna a conta do cliente (retorna a primeira por padrão)."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    """Interface de usuário para realizar um depósito."""
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        transacao = Deposito(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n@@@ Operação falhou! Digite um valor numérico válido. @@@")


@log_transacao
def sacar(clientes):
    """Interface de usuário para realizar um saque."""
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: R$ "))
        transacao = Saque(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n@@@ Operação falhou! Digite um valor numérico válido. @@@")


@log_transacao
def exibir_extrato(clientes):
    """Exibe o extrato consolidado detalhando cada transação com data e hora."""
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} ({transacao['data']})"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    """Interface de criação e inclusão de cliente Pessoa Física."""
    cpf = input("Informe o CPF (somente número): ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")
    return cliente


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    """Cria uma conta corrente e a associa ao cliente."""
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")
    return conta


def listar_contas(contas):
    """Lista os dados de todas as contas cadastradas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada no sistema. @@@")
        return

    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    """Função principal que gerencia o loop de execução do terminal."""
    clientes = []
    contas = []

    while True:
        opcao = menu().strip().lower()

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
            print("\nObrigado por utilizar o nosso sistema bancário!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
