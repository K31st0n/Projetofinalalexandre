#!/usr/bin/env python3
"""
Script de inicialização do Sistema de Gerenciamento Escolar Infantil
Este script verifica dependências e inicia a aplicação de forma segura
"""
import sys
import os
import subprocess
import time
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_dependencies():
    """
    Verifica se todas as dependências estão instaladas
    """
    try:
        import flask
        import psycopg2
        import flasgger
        import prometheus_flask_exporter
        logging.info("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        logging.error(f"❌ Dependência faltando: {e}")
        logging.info("Execute: pip install -r requeriments.txt")
        return False

def check_database_connection():
    """
    Verifica conectividade com o banco de dados
    """
    try:
        import Util.bd as bd
        if bd.test_connection():
            logging.info("✅ Conexão com banco de dados OK")
            return True
        else:
            logging.warning("⚠️  Não foi possível conectar ao banco")
            logging.info("Certifique-se que o PostgreSQL está rodando")
            return False
    except Exception as e:
        logging.error(f"❌ Erro ao testar banco: {e}")
        return False

def create_directories():
    """
    Cria diretórios necessários se não existirem
    """
    directories = ['logs', 'Util']
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logging.info(f"📁 Diretório criado: {directory}")

def start_application():
    """
    Inicia a aplicação Flask
    """
    try:
        logging.info("🚀 Iniciando Sistema de Gerenciamento Escolar...")
        
        # Importa e executa a aplicação principal
        from app import app
        
        logging.info("📊 Swagger disponível em: http://localhost:5000/swagger/")
        logging.info("🏥 Health check em: http://localhost:5000/health")
        logging.info("📈 Métricas em: http://localhost:5000/metrics")
        
        # Inicia o servidor
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Evita reinicialização dupla
        )
        
    except Exception as e:
        logging.error(f"❌ Erro ao iniciar aplicação: {e}")
        sys.exit(1)

def main():
    """
    Função principal do script de inicialização
    """
    print("=" * 60)
    print("🏫 SISTEMA DE GERENCIAMENTO ESCOLAR INFANTIL")
    print("=" * 60)
    
    # Verifica se está no diretório correto
    if not Path('app.py').exists():
        logging.error("❌ Execute este script no diretório do projeto")
        sys.exit(1)
    
    # Cria diretórios necessários
    create_directories()
    
    # Verifica dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Verifica banco de dados (opcional)
    check_database_connection()
    
    # Inicia aplicação
    start_application()

if __name__ == "__main__":
    main()