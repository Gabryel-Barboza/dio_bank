# Propósito

Um projeto de API para simular transações bancárias, criado com o propósito de desenvolver os conhecimentos sobre FastAPI e outros relacionados.

O mesmo projeto está sendo desenvolvido com outros frameworks, veja as branches disponíveis.

## Funcionalidades

O objetivo deste desafio é desenvolver uma API com as seguintes funcionalidades:

- [x] **Cadastro de Transações**: Permita o cadastro de transações bancárias, como depósitos e saques.
- [x] **Exibição de Extrato**: Implemente um endpoint para exibir o extrato de uma conta, mostrando todas \* as transações realizadas.
- [x] **Autenticação com JWT**: Utilize JWT (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.

## Requisitos do Desafio

Para a realização deste desafio, você deve atender aos seguintes requisitos técnicos:

- **FastAPI:** Utilize FastAPI como framework para criar sua API. Aproveite os recursos assíncronos do framework para lidar com operações de I/O de forma eficiente.
- **Modelagem de Dados:** Crie modelos de dados adequados para representar contas correntes e transações. Garanta que as transações estão relacionadas a uma conta corrente, e que contas possam ter múltiplas transações.
- **Validação das operações:** Não permita depósitos e saques com valores negativos, valide se o usuário possui saldo para realizar o saque.
- **Segurança:** Implemente autenticação usando JWT para proteger os endpoints que necessitam de acesso autenticado.
- **Documentação com OpenAPI:** Certifique-se de que sua API esteja bem documentada, incluindo descrições adequadas para cada endpoint, parâmetros e modelos de dados.

## Checklist de Afazeres

- [x] Criar modelagem inicial da API
- [x] Criar arquitetura base MVC
- [x] Instalar dependências de FastAPI Standard
- [x] Inicializar servidor FastAPI
- [x] Criar controladores
- [x] Criar modelos
- [x] Criar serviços para os controladores
- [x] Adicionar modelo para transações
- [x] Refatorar camadas para modularizar código
- [x] Criar exception de registro não encontrado para controladores
- [x] Alterar modelos com os tipos de dados apropriados para campos específicos
- [x] Alterar modelos adicionando relacionamentos
- [x] Criar schemas das rotas de User para refletir as entradas e saídas, com apenas os parâmetros necessários em cada rota
- [x] Implementar campo de senha em usuários e controlador de autenticação e login
- [x] Implementar verificação de username e senha no db para auth
- [x] Criar método de autenticação necessária para rotas
- [x] Implementar rotas para manipular contas de usuário
- [x] Criar exceptions para criação de contas com usuários inexistentes e para limite de contas excedido
- [x] Criar exceptions para integridade do banco de dados
- [x] Implementar camada para transação a partir do controlador de Account
- [x] Implementar métodos de saque e depósito no controlador de Account
- [x] Implementar decorador para criar log de transação
- [x] Implementar identificação global com UUID e identificação local com ID
- [x] Alterar modelo de transações para procurar somente por ID dentro de uma conta
- [x] Implementar offset e limit em read accounts e read transactions
- [x] Criar handler principal para exceptions comuns
- [x] Criar middleware para separar exceptions do main
- [x] Impedir erros por valores negativos nos respectivos métodos de busca por int (Query params são tratados já)
- [] Criar alguma limitação para a quantidade de transações retornadas
- [x] Tratar usuário para ser sem espaços ou caixa alta e senha sem espaços
- [] Aprimorar conformidade com OpenAPI 3
- [] Documentar projeto corretamente
- [] Criar bateria de testes com Pytest

  - [x] Testes para a funcionalidade esperada do controlador
  - [] Testes para falhas do controlador
  - [x] Atualizar testes para versão nova
  - [] Criar fixtures para recuperar ids de usuários e contas criadas
  - [] Usar fixtures dentro de parametrize com pytest lazyfixture

- [x] Criar módulo de configurações para .env
- [x] Implementar migrações com Alembic
- [] Refatorar código para deploy:

  - [] Padronizar estrutura do projeto com pacotes
  - [] Instalar dependências adicionais para PostgreSQL
  - [] Implementar CORS
  - [] Testar projeto em contêiner com PostgreSQL

- [] Criar mais tipos de transação/operação
- [] Implementar restrições para as operações de saque e depósito
- [] Criar front-end
- [] Integrar front-end com a API
