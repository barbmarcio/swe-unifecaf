# TaskFlow - Sistema de Gerenciamento de Tarefas

**Desenvolvedor:** Marcio Costa Barbosa (RA: 190093)
**Disciplina:** Software Engineering - UNIFECAF

## Sobre o Projeto

Sistema web de gerenciamento de tarefas desenvolvido para TechFlow Solutions usando metodologias ágeis (Kanban). Permite acompanhamento de fluxo de trabalho em tempo real, priorização de tarefas críticas e monitoramento de desempenho da equipe.

## Funcionalidades

- ✅ CRUD completo de tarefas
- 📊 Quadro Kanban visual (A Fazer, Em Progresso, Concluído)
- 🎯 Sistema de prioridades (Baixa, Média, Alta, Crítica)
- 👥 Atribuição de responsáveis
- 🔍 **Sistema de Filtros** (Mudança de Escopo - Sprint 2)
- 📈 Dashboard com estatísticas em tempo real
- ✨ Interface responsiva e intuitiva

## Tecnologias

- **Backend:** Python 3.9+ com Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Testes:** Pytest (com cobertura >70%)
- **CI/CD:** GitHub Actions
- **Metodologia:** Kanban

## Estrutura do Projeto

```
taskflow/
├── src/
│   ├── app.py              # Aplicação Flask
│   ├── models.py           # Modelos de dados
│   └── templates/
│       └── index.html      # Interface web
├── tests/
│   ├── test_models.py      # Testes unitários
│   └── test_routes.py      # Testes de integração
├── docs/                   # Documentação e diagramas
├── .github/workflows/      # Pipeline CI/CD
└── requirements.txt
```

## Como Executar

### Instalação

```bash
# Clone o repositório
git clone https://github.com/barbmarcio/swe-unifecaf.git
cd swe-unifecaf

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
python src/app.py
```

Acesse: `http://localhost:5000`

## Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Verbose
pytest -v
```

## API Endpoints

- `GET /api/tasks` - Listar todas as tarefas
- `GET /api/tasks?status=<status>` - Filtrar por status
- `GET /api/tasks?priority=<priority>` - Filtrar por prioridade
- `GET /api/tasks?assignee=<nome>` - Filtrar por responsável
- `GET /api/tasks/<id>` - Obter tarefa específica
- `POST /api/tasks` - Criar nova tarefa
- `PUT /api/tasks/<id>` - Atualizar tarefa
- `DELETE /api/tasks/<id>` - Deletar tarefa

## Mudança de Escopo

**Funcionalidade Adicionada (Sprint 2):** Sistema de Filtros

Durante o desenvolvimento, identificamos a necessidade de filtrar tarefas por status, prioridade e responsável para melhorar a usabilidade em projetos com muitas tarefas.

## Metodologia Ágil

Este projeto utiliza **Kanban** para gestão de tarefas, com quadro organizado em 3 colunas:
- **A Fazer** - Tarefas planejadas
- **Em Progresso** - Tarefas em desenvolvimento
- **Concluído** - Tarefas finalizadas

## CI/CD

Pipeline automatizado com GitHub Actions que executa:
- Lint de código (flake8)
- Testes automatizados
- Verificação de cobertura (mínimo 70%)

---

**Desenvolvido como parte da disciplina de Software Engineering - UNIFECAF 2025**
