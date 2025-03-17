# Propósito

Um projeto de API para simular transações bancárias, criado com o propósito de desenvolver os conhecimentos sobre FastAPI e outros relacionados.

## Funcionalidades

O objetivo deste desafio é desenvolver uma API com as seguintes funcionalidades:

- **Cadastro de Transações**: Permita o cadastro de transações bancárias, como depósitos e saques.
- **Exibição de Extrato**: Implemente um endpoint para exibir o extrato de uma conta, mostrando todas \* as transações realizadas.
- **Autenticação com JWT**: Utilize JWT (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.

## Requisitos do Desafio

Para a realização deste desafio, você deve atender aos seguintes requisitos técnicos:

- **FastAPI:** Utilize FastAPI como framework para criar sua API. Aproveite os recursos assíncronos do framework para lidar com operações de I/O de forma eficiente.
- **Modelagem de Dados:** Crie modelos de dados adequados para representar contas correntes e transações. Garanta que as transações estão relacionadas a uma conta corrente, e que contas possam ter múltiplas transações.
- **Validação das operações:** Não permita depósitos e saques com valores negativos, valide se o usuário possui saldo para realizar o saque.
- **Segurança:** Implemente autenticação usando JWT para proteger os endpoints que necessitam de acesso autenticado.
- **Documentação com OpenAPI:** Certifique-se de que sua API esteja bem documentada, incluindo descrições adequadas para cada endpoint, parâmetros e modelos de dados.
