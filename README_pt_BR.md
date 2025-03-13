# Air Travel Management System

## 📌 Explicação do Projeto

### Visão Geral
Sistema de gerenciamento de viagens aérias desenvolvido para administrar voos, reservas, passageiros e usuários. Oferece uma interface intuitiva com funcionalidades para administradores e usuários comuns, incluindo cadastro de voos, acompanhamento de reservas e geração de relatórios básicos.

### Objetivos
- Automatizar o gerenciamento de operações aéreas.
- Fornecer uma plataforma centralizada para reservas e controle de voos.
- Permitir a distinção de níveis de acesso (admin e usuário).

### Funcionalidades Implementadas
- **Autenticação de Usuários**: Login com níveis de acesso (admin/user).
- **Gerenciamento de Voos**:
  - Adicionar/editar/excluir voos (apenas admin).
  - Visualizar status de voos (agendado, em rota, finalizado).
- **Dashboard**: Estatísticas de voos, reservas e destinos.
- **Reservas**: Interface básica para futura implementação.
- **Relatórios**: Seção em desenvolvimento para análise de dados.

---

## 🛠️ Manual de Instalação

### Pré-requisitos
- Python 3.10 ou superior
- XAMPP (para banco de dados MySQL local)
- Bibliotecas Python: 
  ```bash
  pip install customtkinter pywinstyles mysql-connector-python pytz

```markdown
# Air Travel Management System

## 📌 Explicação do Projeto

### Visão Geral
Sistema de gerenciamento de viagens aérias desenvolvido para administrar voos, reservas, passageiros e usuários. Oferece uma interface intuitiva com funcionalidades para administradores e usuários comuns, incluindo cadastro de voos, acompanhamento de reservas e geração de relatórios básicos.

### Objetivos
- Automatizar o gerenciamento de operações aéreas.
- Fornecer uma plataforma centralizada para reservas e controle de voos.
- Permitir a distinção de níveis de acesso (admin e usuário).

### Funcionalidades Implementadas
- **Autenticação de Usuários**: Login com níveis de acesso (admin/user).
- **Gerenciamento de Voos**:
  - Adicionar/editar/excluir voos (apenas admin).
  - Visualizar status de voos (agendado, em rota, finalizado).
- **Dashboard**: Estatísticas de voos, reservas e destinos.
- **Reservas**: Interface básica para futura implementação.
- **Relatórios**: Seção em desenvolvimento para análise de dados.

---

## 🛠️ Manual de Instalação

### Pré-requisitos
- Python 3.10 ou superior
- XAMPP (para banco de dados MySQL local)
- Bibliotecas Python: 
  ```bash
  pip install customtkinter pywinstyles mysql-connector-python pytz
  ```

### Passo a Passo
1. **Configurar Banco de Dados**:
   - Inicie o Apache e MySQL via XAMPP.
   - Acesse `http://localhost/phpmyadmin`.
   - Crie um banco de dados chamado `air_travel_management`.
   - Importe o arquivo `air_travel_management.sql` (via aba "Importar").

2. **Configurar Ambiente Python**:
   - Clone o repositório:
     ```bash
     git clone https://github.com/seu-usuario/air_travel_management.git
     ```
   - Navegue até a pasta do projeto:
     ```bash
     cd air_travel_management
     ```

3. **Executar o Sistema**:
   ```bash
   python main.py
   ```

---

## 📖 Manual de Uso

### Login
- **Admin Padrão**:
  - Usuário: `admin`
  - Senha: `123` (senha hash no código, altere no banco de dados para produção).
- **Usuários Comuns**: Podem se registrar via botão "Registrar".

### Navegação
- **Dashboard**:
  - Visualiza estatísticas rápidas e próximos voos.
- **Voos** (Admin apenas):
  - Adicione novos voos com detalhes como origem, destino e horário.
  - Edite ou exclua voos clicando em `✏️` ou `🗑️` na tabela.
- **Reservas** (Em desenvolvimento):
  - Interface placeholder para futuras funcionalidades.
- **Configurações**:
  - Ajuste o tema (claro/escuro) e outras preferências.

---

## ⚙️ Manual de Configuração

### Banco de Dados
- Altere as credenciais em `main.py` (linha 68):
  ```python
  connection = mysql.connector.connect(
      host="localhost",
      user="root",       # Altere se necessário
      password="",       # Adicione a senha do seu MySQL
      database="air_travel_management"
  )
  ```

### Tema da Interface
- Modifique o tema em `main.py` (linhas 18-19):
  ```python
  ctk.set_appearance_mode("dark")  # Opções: "System", "Dark", "Light"
  ctk.set_default_color_theme("blue")  # Opções: "blue", "green", "dark-blue"
  ```

---

## 👤 Créditos

### Desenvolvedor
- **Vítor Luciano Cardoso Noe**  
  Projeto desenvolvido individualmente para fins acadêmicos.

### Referências
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)

---

**Nota**: Este projeto é uma versão simplificada. Para uso em produção, recomenda-se adicionar validações de dados, criptografia robusta para senhas e testes adicionais.
``` 

### Arquivos do Repositório
- `air_travel_management.sql`: Estrutura do banco de dados.
- `main.py`: Código-fonte da aplicação.
- `README.md`: Documentação do projeto (este arquivo).

### Instruções Adicionais
1. Certifique-se de que o MySQL está ativo via XAMPP antes de executar `main.py`.
2. Para resetar senhas ou adicionar admins, edite diretamente a tabela `users` no phpMyAdmin.
3. A senha do admin padrão (`123`) está hasheada como `240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9`. Troque-a no banco de dados para maior segurança.
