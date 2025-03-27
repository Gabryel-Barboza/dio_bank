# Propósito

Um projeto de API para simular transações bancárias, criado com o propósito de desenvolver os conhecimentos sobre FastAPI e outros relacionados.

O mesmo projeto está sendo desenvolvido com outros frameworks, veja as branches disponíveis.

## Funcionalidades

O objetivo deste desafio é desenvolver uma API com as seguintes funcionalidades:

- [] **Cadastro de Transações**: Permita o cadastro de transações bancárias, como depósitos e saques.
- [] **Exibição de Extrato**: Implemente um endpoint para exibir o extrato de uma conta, mostrando todas \* as transações realizadas.
- [] **Autenticação com JWT**: Utilize JWT (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.

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
- [] Alterar modelos com os tipos de dados apropriados para campos específicos
- [] ? Unificar rotas de user Put e Patch ?
- [x] Alterar modelos adicionando relacionamentos
- [x] Criar schemas das rotas de User para refletir as entradas e saídas, com apenas os parâmetros necessários em cada rota
- [x] Implementar campo de senha em usuários e controlador de autenticação e login
- [] Implementar verificação de username e senha no db para auth
- [] Criar decorador de autenticação necessária para rotas
- [x] Implementar rotas para manipular contas de usuário
- [x] Criar exceptions para criação de contas com usuários inexistentes e para limite de contas excedido
- [] Criar exceptions para integridade do banco de dados
- [] Implementar camada para transação a partir do controlador de Account
- [] Implementar métodos de saque e depósito no controlador de Account
- [] Implementar decorador para criar log de transação
- [] Implementar identificação global com UUID e identificação local com ID
- [] Criar handler principal para exceptions comuns
- [] Aprimorar conformidade com OpenAPI 3
- [] Criar bateria de testes com Pytest
- [] Criar módulo de configurações para .env
- [] Implementar migrações com Alembic
- [] Refatorar código para deploy:

  - [] Padronizar estrutura do projeto com pacotes
  - [] Instalar dependências adicionais para PostgreSQL
  - [] Testar projeto em contêiner com PostgreSQL

- [] Criar mais tipos de transação/operação
- [] Implementar restrições para as operações de saque e depósito
- [] Criar front-end
- [] Integrar front-end com a API
