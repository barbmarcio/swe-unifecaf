"""
Testes de integração para as rotas da API
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app


@pytest.fixture
def client():
    """Cliente de teste do Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestTaskRoutes:
    """Testes das rotas de tarefas"""

    def test_get_all_tasks(self, client):
        """Teste GET /api/tasks"""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_create_task(self, client):
        """Teste POST /api/tasks"""
        task_data = {
            'title': 'Nova tarefa de teste',
            'description': 'Descrição da tarefa',
            'priority': 'alta'
        }
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Nova tarefa de teste'
        assert 'id' in data

    def test_create_task_without_title(self, client):
        """Teste POST /api/tasks sem título"""
        task_data = {'description': 'Apenas descrição'}
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_get_task_by_id(self, client):
        """Teste GET /api/tasks/<id>"""
        # Criar tarefa primeiro
        task_data = {'title': 'Tarefa para buscar'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        # Buscar tarefa
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Tarefa para buscar'

    def test_get_nonexistent_task(self, client):
        """Teste GET /api/tasks/<id> inexistente"""
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404

    def test_update_task(self, client):
        """Teste PUT /api/tasks/<id>"""
        # Criar tarefa
        task_data = {'title': 'Tarefa original'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        # Atualizar tarefa
        update_data = {'title': 'Tarefa atualizada', 'status': 'concluido'}
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Tarefa atualizada'
        assert data['status'] == 'concluido'

    def test_update_nonexistent_task(self, client):
        """Teste PUT /api/tasks/<id> inexistente"""
        update_data = {'title': 'Teste'}
        response = client.put(
            '/api/tasks/9999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_delete_task(self, client):
        """Teste DELETE /api/tasks/<id>"""
        # Criar tarefa
        task_data = {'title': 'Tarefa para deletar'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        # Deletar tarefa
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200

        # Verificar se foi deletada
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404

    def test_delete_nonexistent_task(self, client):
        """Teste DELETE /api/tasks/<id> inexistente"""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404

    def test_workflow_completo(self, client):
        """Teste workflow completo: criar, atualizar, listar, deletar"""
        # Criar
        task_data = {'title': 'Workflow Test', 'priority': 'media'}
        create_response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        task_id = json.loads(create_response.data)['id']

        # Listar
        list_response = client.get('/api/tasks')
        tasks = json.loads(list_response.data)
        assert any(t['id'] == task_id for t in tasks)

        # Atualizar
        update_response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps({'status': 'concluido'}),
            content_type='application/json'
        )
        assert update_response.status_code == 200

        # Deletar
        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 200
