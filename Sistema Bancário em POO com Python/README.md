# Sistema Bancário em Programação Orientada a Objetos com Python

Este projeto eleva a arquitetura do sistema bancário monousuário através da aplicação dos conceitos de Programação Orientada a Objetos (POO) em Python. Os dados de clientes, transações e contas bancárias são representados por meio de objetos definidos a partir de um modelo de classes unificado (UML), proporcionando encapsulamento e extensibilidade.

## Arquitetura de Classes do Sistema

O sistema é estruturado através dos seguintes componentes de classe:

### 1. Modelo de Clientes
- **`Cliente`**: Classe base que contém o endereço e uma coleção de contas associadas ao cliente. Define a interface para a execução de transações.
- **`PessoaFisica`**: Especialização de `Cliente` que herda seus atributos básicos e adiciona características individuais do portador da conta: CPF, Nome Completo e Data de Nascimento.

### 2. Modelo de Contas
- **`Conta`**: Classe que implementa as propriedades comuns de contas bancárias (saldo, número, agência, histórico e proprietário) e as operações básicas de débito (`sacar`) e crédito (`depositar`).
- **`ContaCorrente`**: Especialização de `Conta` com imposição de regras de limite financeiro por transação (R$ 500,00) e limite de volume de operações de saque (até 3 saques diários).

### 3. Modelo de Histórico e Transações
- **`Historico`**: Classe responsável por armazenar a cronologia de transações efetuadas em uma conta, gerando carimbos de data/hora padronizados.
- **`Transacao`**: Classe Abstrata de Base (ABC) que define a interface de assinatura comum para todas as movimentações.
- **`Deposito` e `Saque`**: Classes concretas que herdam de `Transacao`. Implementam o método de registro que executa a transação no saldo e registra os eventos correspondentes no histórico.

---

## Estrutura de Arquivos

O diretório do projeto contém os seguintes arquivos:

- `sistema_bancario_poo.py`: Implementação completa contendo as declarações de classes e o menu interativo por console.
- `README.md`: Documentação conceitual e instruções operacionais.

---

## Instruções de Execução

### Pré-requisitos
Certifique-se de ter o Python 3.10 ou superior instalado na máquina.

### Execução

Navegue até a pasta do projeto no terminal e execute:

```bash
python sistema_bancario_poo.py
```

### Fluxo de Validação no Terminal

1. Inicie registrando um cliente em `nu` (Novo usuário).
2. Abra uma conta para o CPF correspondente em `nc` (Nova conta).
3. Visualize as contas cadastradas digitando `lc` (Listar contas).
4. Efetue depósitos e saques informando o CPF.
5. Emita um extrato consolidado em `e` para validar o histórico de transações com data/hora e o saldo atual.
