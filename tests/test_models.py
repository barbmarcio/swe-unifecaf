"""
Testes unitários para os modelos
"""

import pytest
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models import Task, TaskManager


class TestTask:
    """Testes para o modelo Task"""

    def test_create_task_with_required_fields(self):
        """Teste criação de tarefa com campos obrigatórios"""
        task = Task(title="Minha tarefa")

        assert task.title == "Minha tarefa"
        assert task.id > 0
        assert task.status == "a_fazer"
        assert task.priority == "media"

    def test_create_task_with_all_fields(self):
        """Teste criação de tarefa com todos os campos"""
        task = Task(
            title="Implementar login",
            description="Adicionar autenticação",
            priority="alta",
            status="em_progresso",
            assignee="João",
            due_date="2025-01-15"
        )

        assert task.title == "Implementar login"
        assert task.description == "Adicionar autenticação"
        assert task.priority == "alta"
        assert task.status == "em_progresso"
        assert task.assignee == "João"
        assert task.due_date == "2025-01-15"

    def test_task_requires_title(self):
        """Teste validação de título obrigatório"""
        with pytest.raises(ValueError, match="Título é obrigatório"):
            Task(title="")

    def test_task_invalid_status(self):
        """Teste validação de status inválido"""
        with pytest.raises(ValueError, match="Status inválido"):
            Task(title="Teste", status="invalido")

    def test_task_invalid_priority(self):
        """Teste validação de prioridade inválida"""
        with pytest.raises(ValueError, match="Prioridade inválida"):
            Task(title="Teste", priority="invalido")

    def test_task_to_dict(self):
        """Teste conversão de tarefa para dicionário"""
        task = Task(title="Teste", description="Descrição")
        data = task.to_dict()

        assert data['title'] == "Teste"
        assert data['description'] == "Descrição"
        assert 'id' in data
        assert 'created_at' in data

    def test_task_update(self):
        """Teste atualização de tarefa"""
        task = Task(title="Original")
        task.update(title="Atualizado", priority="alta")

        assert task.title == "Atualizado"
        assert task.priority == "alta"


class TestTaskManager:
    """Testes para o TaskManager"""

    def setup_method(self):
        """Executado antes de cada teste"""
        self.manager = TaskManager()

    def test_create_task(self):
        """Teste criação de tarefa via manager"""
        task = self.manager.create_task(title="Nova tarefa")

        assert task.title == "Nova tarefa"
        assert len(self.manager.tasks) == 1

    def test_get_all_tasks(self):
        """Teste obter todas as tarefas"""
        self.manager.create_task(title="Tarefa 1")
        self.manager.create_task(title="Tarefa 2")

        tasks = self.manager.get_all_tasks()
        assert len(tasks) == 2

    def test_get_task_by_id(self):
        """Teste buscar tarefa por ID"""
        task = self.manager.create_task(title="Teste")
        found = self.manager.get_task_by_id(task.id)

        assert found is not None
        assert found.title == "Teste"

    def test_get_task_by_invalid_id(self):
        """Teste buscar tarefa com ID inválido"""
        found = self.manager.get_task_by_id(9999)
        assert found is None

    def test_update_task(self):
        """Teste atualizar tarefa via manager"""
        task = self.manager.create_task(title="Original")
        updated = self.manager.update_task(task.id, title="Atualizado")

        assert updated is not None
        assert updated.title == "Atualizado"

    def test_update_nonexistent_task(self):
        """Teste atualizar tarefa inexistente"""
        updated = self.manager.update_task(9999, title="Test")
        assert updated is None

    def test_delete_task(self):
        """Teste deletar tarefa"""
        task = self.manager.create_task(title="Deletar")
        result = self.manager.delete_task(task.id)

        assert result is True
        assert len(self.manager.tasks) == 0

    def test_delete_nonexistent_task(self):
        """Teste deletar tarefa inexistente"""
        result = self.manager.delete_task(9999)
        assert result is False
