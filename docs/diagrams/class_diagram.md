# Diagrama de Classes - TaskFlow

## Representação PlantUML

```plantuml
@startuml
skinparam classAttributeIconSize 0

class Task {
  - id: int
  - title: str
  - description: str
  - priority: str
  - status: str
  - assignee: str
  - due_date: str
  - created_at: str
  {static} - _id_counter: int
  {static} + VALID_STATUSES: List[str]
  {static} + VALID_PRIORITIES: List[str]
  __
  + __init__(title, description, priority, status, assignee, due_date)
  - _validate(): void
  + to_dict(): Dict
  + update(**kwargs): void
}

class TaskManager {
  - tasks: List[Task]
  __
  + __init__()
  + create_task(**kwargs): Task
  + get_all_tasks(): List[Task]
  + get_task_by_id(task_id: int): Task
  + update_task(task_id: int, **kwargs): Task
  + delete_task(task_id: int): bool
  + filter_tasks(status, priority, assignee): List[Task]
}

class Flask {
  + app: Application
  + route(path: str)
  + run(debug: bool, port: int)
}

class APIRoutes {
  + index(): str
  + get_tasks(): Response
  + get_task(task_id: int): Response
  + create_task(): Response
  + update_task(task_id: int): Response
  + delete_task(task_id: int): Response
}

TaskManager "1" *-- "0..*" Task : gerencia
Flask "1" -- "1" APIRoutes : expõe
APIRoutes ..> TaskManager : utiliza
Task ..> Task : valida

note right of Task::VALID_STATUSES
  Constantes de validação:
  - a_fazer
  - em_progresso
  - concluido
end note

note right of Task::VALID_PRIORITIES
  Níveis de prioridade:
  - baixa
  - media
  - alta
  - critica
end note

note bottom of TaskManager::filter_tasks
  Nova funcionalidade - Sprint 2
  Mudança de Escopo:
  Permite filtrar tarefas por
  múltiplos critérios
end note

@enduml
```

## Descrição das Classes

### Classe: Task
**Responsabilidade:** Representa uma tarefa individual no sistema

**Atributos:**
- `id` (int): Identificador único da tarefa (auto-incrementado)
- `title` (str): Título da tarefa (obrigatório)
- `description` (str): Descrição detalhada da tarefa
- `priority` (str): Nível de prioridade (baixa, media, alta, critica)
- `status` (str): Status atual (a_fazer, em_progresso, concluido)
- `assignee` (str): Nome do responsável pela tarefa
- `due_date` (str): Data de vencimento no formato YYYY-MM-DD
- `created_at` (str): Data/hora de criação (ISO format)
- `_id_counter` (static int): Contador para gerar IDs únicos
- `VALID_STATUSES` (static List): Status válidos permitidos
- `VALID_PRIORITIES` (static List): Prioridades válidas permitidas

**Métodos:**
- `__init__()`: Construtor que inicializa a tarefa e valida dados
- `_validate()`: Validação privada dos dados da tarefa
- `to_dict()`: Converte objeto para dicionário (serialização JSON)
- `update(**kwargs)`: Atualiza atributos da tarefa dinamicamente

**Regras de Negócio:**
- Título é obrigatório e não pode ser vazio
- Status deve estar na lista de status válidos
- Prioridade deve estar na lista de prioridades válidas
- ID é gerado automaticamente e não pode ser alterado

---

### Classe: TaskManager
**Responsabilidade:** Gerencia a coleção de tarefas e operações CRUD

**Atributos:**
- `tasks` (List[Task]): Lista de todas as tarefas do sistema

**Métodos:**
- `__init__()`: Inicializa gerenciador com lista vazia
- `create_task(**kwargs)`: Cria nova tarefa e adiciona à lista
- `get_all_tasks()`: Retorna todas as tarefas
- `get_task_by_id(task_id)`: Busca tarefa específica por ID
- `update_task(task_id, **kwargs)`: Atualiza tarefa existente
- `delete_task(task_id)`: Remove tarefa da lista
- `filter_tasks(status, priority, assignee)`: Filtra tarefas por critérios (Nova - Sprint 2)

**Padrões de Projeto:**
- **Repository Pattern**: Centraliza acesso aos dados de tarefas
- **Factory Method**: Método `create_task` age como factory

---

### Classe: Flask (Framework)
**Responsabilidade:** Framework web que gerencia requisições HTTP

**Funções Principais:**
- Roteamento de URLs
- Gerenciamento de requisições/respostas
- Renderização de templates
- Configuração de aplicação

---

### Classe: APIRoutes
**Responsabilidade:** Define endpoints da API REST

**Rotas Implementadas:**
- `GET /` → index(): Renderiza página principal
- `GET /api/tasks` → get_tasks(): Lista tarefas (com filtros opcionais)
- `GET /api/tasks/<id>` → get_task(): Retorna tarefa específica
- `POST /api/tasks` → create_task(): Cria nova tarefa
- `PUT /api/tasks/<id>` → update_task(): Atualiza tarefa
- `DELETE /api/tasks/<id>` → delete_task(): Remove tarefa

**Padrões de Projeto:**
- **RESTful API**: Segue princípios REST para operações CRUD
- **Controller Pattern**: Controla fluxo entre modelo e visualização

---

## Relacionamentos

### TaskManager *-- Task (Composição)
- TaskManager **possui** Tasks
- Tasks não existem sem TaskManager
- Multiplicidade: 1 TaskManager para 0..* Tasks

### APIRoutes ..> TaskManager (Dependência)
- APIRoutes **usa** TaskManager
- Dependência de uso, não de posse
- APIRoutes delega operações para TaskManager

### Flask -- APIRoutes (Associação)
- Flask **expõe** APIRoutes
- Associação bidirecional
- Flask registra rotas de APIRoutes

### Task ..> Task (Dependência Reflexiva)
- Task valida a si mesma
- Método `_validate()` verifica consistência

---

## Diagrama Simplificado (ASCII)

```
┌─────────────────┐
│   Flask App     │
└────────┬────────┘
         │ expõe
         ▼
┌─────────────────┐        usa        ┌──────────────────┐
│   APIRoutes     │◄─────────────────►│  TaskManager     │
│                 │                    │                  │
│ + index()       │                    │ + create_task()  │
│ + get_tasks()   │                    │ + get_all_tasks()│
│ + create_task() │                    │ + filter_tasks() │
└─────────────────┘                    └────────┬─────────┘
                                                │ gerencia
                                                │ 0..*
                                                ▼
                                        ┌──────────────────┐
                                        │      Task        │
                                        │                  │
                                        │ - id: int        │
                                        │ - title: str     │
                                        │ - status: str    │
                                        │ - priority: str  │
                                        └──────────────────┘
```

---

**Nota:** O diagrama reflete a arquitetura após a mudança de escopo que adicionou o método `filter_tasks()` ao TaskManager.
