"""
Módulo de gerenciamento de atividades da escola infantil
Este módulo implementa as operações CRUD para a entidade Atividade
"""
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import Util.bd as bd
from log_config import registrar_evento
from psycopg2 import Error

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger para documentação automática da API
swagger = Swagger(app, template={
    "info": {
        "title": "API de Gerenciamento de Atividades",
        "description": "API RESTful para gerenciar atividades pedagógicas da escola infantil",
        "version": "1.0.0"
    }
})

@app.route('/atividades', methods=['POST'])
@swag_from({
    'tags': ['Atividades'],
    'summary': 'Criar nova atividade',
    'description': 'Cria um novo registro de atividade pedagógica no sistema',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'descricao': {'type': 'string', 'example': 'Pintura com tinta guache'},
                'data_realizacao': {'type': 'string', 'format': 'date', 'example': '2024-01-15'}
            },
            'required': ['descricao', 'data_realizacao']
        }
    }],
    'responses': {
        201: {'description': 'Atividade criada com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def create_atividade():
    """
    Cria uma nova atividade pedagógica no sistema
    Recebe dados via JSON e insere no banco de dados
    """
    data = request.get_json()  # Obtém dados JSON da requisição
    conn = bd.create_connection()  # Estabelece conexão com banco
    
    # Verifica se a conexão foi estabelecida
    if conn is None:
        registrar_evento("CREATE", mensagem="Falha na conexão com o banco de dados", sucesso=False)
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Executa INSERT para criar nova atividade
        cursor.execute(
            """
            INSERT INTO atividades (descricao, data_realizacao)
            VALUES (%s, %s)
            RETURNING id_atividade
            """,
            (data['descricao'], data['data_realizacao'])
        )
        
        # Obtém o ID da atividade criada
        atividade_id = cursor.fetchone()[0]
        conn.commit()  # Confirma a transação
        
        # Registra evento de sucesso no log
        registrar_evento("CREATE", mensagem=f"Atividade '{data['descricao']}' criada com sucesso", sucesso=True)
        
        return jsonify({"message": "Atividade criada com sucesso", "id_atividade": atividade_id}), 201
        
    except Error as e:
        conn.rollback()  # Desfaz a transação em caso de erro
        registrar_evento("CREATE", mensagem=f"Erro ao criar atividade: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()  # Fecha cursor
        conn.close()    # Fecha conexão

@app.route('/atividades/<int:id_atividade>', methods=['GET'])
def read_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividades WHERE id_atividade = %s", (id_atividade,))
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade[0],
            "descricao": atividade[1],
            "data_realizacao": atividade[2]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividades
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (data['descricao'], data['data_realizacao'], id_atividade)
        )
        conn.commit()
        return jsonify({"message": "Atividade atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM atividades WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        return jsonify({"message": "Atividade deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)