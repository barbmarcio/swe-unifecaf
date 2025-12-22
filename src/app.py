"""
Aplicação principal do TaskFlow
Sistema de gerenciamento de tarefas
"""

from flask import Flask, request, jsonify, render_template
from models import TaskManager

app = Flask(__name__)
task_manager = TaskManager()


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Lista todas as tarefas"""
    tasks = task_manager.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obt uma tarefa específica"""
    task = task_manager.get_task_by_id(task_id)
    if task:
        return jsonify(task.to_dict())
    return jsonify({'error': 'Tarefa não encontrada'}), 404


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Cria nova tarefa"""
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Título é obrigatório'}), 400

    try:
        task = task_manager.create_task(**data)
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualiza tarefa existente"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    try:
        task = task_manager.update_task(task_id, **data)
        if task:
            return jsonify(task.to_dict())
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deleta tarefa"""
    if task_manager.delete_task(task_id):
        return jsonify({'message': 'Tarefa deletada com sucesso'})
    return jsonify({'error': 'Tarefa não encontrada'}), 404


if __name__ == '__main__':
    # Criar algumas tarefas de exemplo
    task_manager.create_task(
        title="Configurar ambiente de desenvolvimento",
        description="Instalar Python, Flask e dependências",
        priority="alta",
        status="concluido",
        assignee="Marcio Barbosa"
    )
    task_manager.create_task(
        title="Implementar modelos de dados",
        description="Criar classes Task e TaskManager",
        priority="alta",
        status="concluido",
        assignee="Marcio Barbosa"
    )
    task_manager.create_task(
        title="Criar API REST",
        description="Implementar endpoints CRUD",
        priority="alta",
        status="em_progresso",
        assignee="Marcio Barbosa"
    )

    app.run(debug=True, port=5000)
