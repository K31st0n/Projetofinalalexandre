"""
Aplicação principal do Sistema de Gerenciamento Escolar Infantil
Este arquivo integra todos os módulos e configura a API REST completa
"""
from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS
import logging
from prometheus_flask_exporter import PrometheusMetrics

# Importa os módulos de cada entidade
from aluno import app as aluno_app
from professor import app as professor_app  
from turma import app as turma_app
from usuario import app as usuario_app
from atividade import app as atividade_app
from atividade_aluno import app as atividade_aluno_app
from presenca import app as presenca_app
from pagamento import app as pagamento_app

# Importa utilitários
from log_config import registrar_evento
import Util.bd as bd

# Inicialização da aplicação Flask principal
app = Flask(__name__)

# Configuração CORS para permitir requisições de diferentes origens
CORS(app)

# Configuração do Swagger para documentação completa da API
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Sistema Escolar Infantil",
        "description": "API RESTful completa para gerenciamento de escola infantil",
        "contact": {
            "name": "Equipe de Desenvolvimento",
            "email": "dev@escola.com"
        },
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {
            "name": "Alunos",
            "description": "Operações relacionadas aos alunos"
        },
        {
            "name": "Professores", 
            "description": "Operações relacionadas aos professores"
        },
        {
            "name": "Turmas",
            "description": "Operações relacionadas às turmas"
        },
        {
            "name": "Usuários",
            "description": "Operações relacionadas aos usuários do sistema"
        },
        {
            "name": "Atividades",
            "description": "Operações relacionadas às atividades pedagógicas"
        },
        {
            "name": "Presenças",
            "description": "Operações relacionadas ao controle de presença"
        },
        {
            "name": "Pagamentos",
            "description": "Operações relacionadas aos pagamentos"
        }
    ]
}

# Inicializa Swagger com configurações personalizadas
swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Configuração de métricas Prometheus para monitoramento
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Sistema Escolar Infantil', version='1.0.0')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def register_blueprints():
    """
    Registra todos os blueprints dos módulos na aplicação principal
    Cada módulo tem suas rotas específicas que são integradas aqui
    """
    try:
        # Registra as rotas de cada módulo na aplicação principal
        # Como os módulos usam Flask() individual, copiamos suas rotas
        
        # Copia rotas do módulo aluno
        for rule in aluno_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"aluno_{rule.endpoint}",
                    view_func=aluno_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
        
        # Copia rotas do módulo professor  
        for rule in professor_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"professor_{rule.endpoint}",
                    view_func=professor_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        # Copia rotas do módulo turma
        for rule in turma_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"turma_{rule.endpoint}",
                    view_func=turma_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        # Copia rotas do módulo usuario
        for rule in usuario_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"usuario_{rule.endpoint}",
                    view_func=usuario_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        # Copia rotas do módulo atividade
        for rule in atividade_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"atividade_{rule.endpoint}",
                    view_func=atividade_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        # Copia rotas do módulo atividade_aluno
        for rule in atividade_aluno_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"atividade_aluno_{rule.endpoint}",
                    view_func=atividade_aluno_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        # Copia rotas do módulo presenca
        for rule in presenca_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"presenca_{rule.endpoint}",
                    view_func=presenca_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        # Copia rotas do módulo pagamento
        for rule in pagamento_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(
                    rule.rule,
                    endpoint=f"pagamento_{rule.endpoint}",
                    view_func=pagamento_app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
                
        logging.info("Todos os módulos foram registrados com sucesso")
        
    except Exception as e:
        logging.error(f"Erro ao registrar blueprints: {e}")
        raise

@app.route('/', methods=['GET'])
def home():
    """
    Endpoint raiz da API
    Retorna informações básicas sobre o sistema
    """
    return jsonify({
        "message": "Sistema de Gerenciamento Escolar Infantil",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/swagger/",
        "endpoints": {
            "alunos": "/alunos",
            "professores": "/professores", 
            "turmas": "/turmas",
            "usuarios": "/usuarios",
            "atividades": "/atividades",
            "atividade_aluno": "/atividade_aluno",
            "presencas": "/presencas",
            "pagamentos": "/pagamentos"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde da aplicação
    Testa conectividade com banco de dados
    """
    try:
        # Testa conexão com banco de dados
        db_status = bd.test_connection()
        
        if db_status:
            registrar_evento("HEALTH_CHECK", mensagem="Sistema funcionando corretamente", sucesso=True)
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "timestamp": "2024-01-01T00:00:00Z"
            }), 200
        else:
            registrar_evento("HEALTH_CHECK", mensagem="Falha na conexão com banco", sucesso=False)
            return jsonify({
                "status": "unhealthy", 
                "database": "disconnected",
                "timestamp": "2024-01-01T00:00:00Z"
            }), 503
            
    except Exception as e:
        registrar_evento("HEALTH_CHECK", mensagem=f"Erro no health check: {e}", sucesso=False)
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """
    Handler para erros 404 - Não encontrado
    """
    return jsonify({
        "error": "Endpoint não encontrado",
        "message": "Verifique a documentação em /swagger/",
        "status_code": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handler para erros 500 - Erro interno do servidor
    """
    registrar_evento("ERROR", mensagem=f"Erro interno: {error}", sucesso=False)
    return jsonify({
        "error": "Erro interno do servidor",
        "message": "Entre em contato com o suporte",
        "status_code": 500
    }), 500

if __name__ == '__main__':
    """
    Ponto de entrada da aplicação
    Registra todos os módulos e inicia o servidor
    """
    try:
        # Registra todos os blueprints dos módulos
        register_blueprints()
        
        # Log de inicialização
        registrar_evento("STARTUP", mensagem="Sistema iniciado com sucesso", sucesso=True)
        
        # Inicia o servidor Flask
        # host='0.0.0.0' permite acesso externo
        # port=5000 é a porta padrão
        # debug=True habilita modo de desenvolvimento
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        logging.error(f"Erro ao iniciar aplicação: {e}")
        registrar_evento("STARTUP", mensagem=f"Falha ao iniciar sistema: {e}", sucesso=False)
        raise