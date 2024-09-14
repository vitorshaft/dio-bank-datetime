# dio-bank-datetime: Sistema de Gerenciamento Bancário com Múltiplas Contas e Operações

Este é um sistema de Gerenciamento Bancário desenvolvido em Python 3.9, com funcionalidades avançadas, como depósito, saque, extrato e gerenciamento de múltiplas contas. O sistema simula um ambiente bancário, permitindo que os usuários gerenciem várias contas, realizem operações e visualizem o histórico de transações de forma prática e direta.

O objetivo deste projeto é fornecer uma base sólida para o aprendizado de operações bancárias em Python, utilizando conceitos de POO (Programação Orientada a Objetos), iteração, controle de fluxo e autenticação simples.

## Funcionalidades

- **Depósito**: Adiciona dinheiro ao saldo da conta selecionada.
- **Saque**: Permite retirar dinheiro da conta, com verificações de saldo, limites de saque e número máximo de saques diários.
- **Extrato**: Exibe todas as transações realizadas na conta, incluindo depósitos e saques, com detalhes de data e valor.
- **Múltiplas Contas**: Um usuário pode ter mais de uma conta bancária e alternar entre elas para realizar operações.
- **Histórico de Transações**: Cada conta mantém um histórico completo de todas as transações realizadas.
- **Autenticação**: O sistema exige login por CPF e senha, além de validar a senha antes de cada operação.
- **Menu Interativo**: Interface baseada em texto, onde o usuário pode navegar e realizar as operações bancárias.

## Como Começar

### Pré-requisitos

- Python 3.9 ou superior instalado
- Um terminal ou linha de comando

### Executando o Programa

1. Clone este repositório:

    ```sh
    git clone https://github.com/vitorshaft/dio-bank-datetime.git
    ```

2. Navegue até o diretório do projeto:

    ```sh
    cd dio-bank-datetime
    ```

3. Execute o programa:

    ```sh
    python main.py
    ```

## Uso

Ao executar o programa, será exibido um **menu preliminar**, onde o usuário poderá criar um novo perfil ou fazer login. Após o login, será apresentada uma série de opções para realizar operações bancárias, como depósito, saque e extrato. 

### Menu Preliminar:

- `[1]` Criar Novo Perfil
- `[2]` Login
- `[q]` Sair

Após o login, o menu principal permite ao usuário escolher a conta com a qual deseja operar e realizar operações:

### Menu Principal:

- `[d]` Depositar
- `[s]` Sacar
- `[e]` Extrato
- `[nc]` Nova Conta
- `[lc]` Listar Contas
- `[mc]` Mudar Conta
- `[q]` Logout

### Operações Disponíveis:

- **Depósito**: O usuário pode adicionar um valor ao saldo da conta ativa.
- **Saque**: O usuário pode retirar dinheiro da conta, respeitando os limites de saque e saldo.
- **Extrato**: Exibe todas as transações realizadas na conta ativa, com data, tipo (depósito/saque) e valor.
- **Mudar Conta**: Se o usuário tiver mais de uma conta, pode alternar entre elas usando esta opção.
- **Listar Contas**: Exibe todas as contas associadas ao usuário logado.

## Exemplo de Operação

```sh
================= MENU ==================
[d]    Depositar
[s]    Sacar
[e]    Extrato
[nc]   Nova Conta
[lc]   Listar Contas
[mc]   Mudar Conta
[q]    Sair
=========================================
=> d
Informe o valor do depósito: 1000.00

=== Depósito realizado com sucesso! ===

================ EXTRATO ================
14-09-2024 11:57:58
Depósito:
        R$ 1000.00
Saldo:
        R$ 1000.00
=========================================
```
### Versão 1.1
- Adicionada funcionalidade de troca de conta para clientes com mais de uma conta bancária.
- Melhorias na exibição do extrato, incluindo data e hora das transações.
- Limites de saque diários e verificações de saldo implementados.

## Atualizações
### Versão 1.0
- Implementação básica das operações de depósito, saque e extrato.
- Gerenciamento de múltiplas contas para cada cliente.
- Login com autenticação por CPF e senha.
- Menu interativo com interface de texto.