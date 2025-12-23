"""
Modelos de dados do TaskFlow
"""

from datetime import datetime
from typing import Optional, List, Dict


class Task:
    """Representa uma tarefa no sistema"""

    _id_counter = 1
    VALID_STATUSES = ['a_fazer', 'em_progresso', 'concluido']
    VALID_PRIORITIES = ['baixa', 'media', 'alta', 'critica']

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "media",
        status: str = "a_fazer",
        assignee: str = "",
        due_date: Optional[str] = None
    ):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.status = status.lower()
        self.assignee = assignee
        self.due_date = due_date
        self.created_at = datetime.now().isoformat()

        self._validate()

    def _validate(self):
        """Valida os dados da tarefa"""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Título é obrigatório")

        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Status inválido")

        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida")

    def to_dict(self) -> Dict:
        """Converte tarefa para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'assignee': self.assignee,
            'due_date': self.due_date,
            'created_at': self.created_at
        }

    def update(self, **kwargs):
        """Atualiza atributos da tarefa"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self._validate()


class TaskManager:
    """Gerenciador de tarefas"""

    def __init__(self):
        self.tasks: List[Task] = []

    def create_task(self, **kwargs) -> Task:
        """Cria nova tarefa"""
        task = Task(**kwargs)
        self.tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retorna todas as tarefas"""
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Busca tarefa por ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Atualiza tarefa existente"""
        task = self.get_task_by_id(task_id)
        if task:
            task.update(**kwargs)
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """Remove tarefa"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def filter_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee: Optional[str] = None
    ) -> List[Task]:
        """
        Filtra tarefas por critérios
        Mudança de Escopo - Sprint 2
        """
        filtered = self.tasks

        if status:
            filtered = [t for t in filtered if t.status == status.lower()]

        if priority:
            filtered = [t for t in filtered if t.priority == priority.lower()]

        if assignee:
            filtered = [
                t for t in filtered
                if assignee.lower() in t.assignee.lower()
            ]

        return filtered
