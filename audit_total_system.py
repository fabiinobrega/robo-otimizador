"""
AUDITORIA TOTAL DO SISTEMA NEXORA PRIME
Audita: Backend, Frontend, APIs, BD, Integrações, Webhooks
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

class TotalSystemAudit:
    def __init__(self):
        self.base_path = Path('/home/ubuntu/robo-otimizador')
        self.errors = []
        self.warnings = []
        self.info = []
        
    def audit_backend(self):
        """Auditar backend Python"""
        print("🔍 Auditando Backend...")
        
        # Verificar main.py
        main_file = self.base_path / 'main.py'
        if main_file.exists():
            try:
                with open(main_file, 'r') as f:
                    content = f.read()
                    
                # Verificar imports
                if 'from flask import' not in content:
                    self.errors.append("main.py: Flask não importado corretamente")
                else:
                    self.info.append("main.py: Flask importado ✓")
                    
                # Contar rotas
                route_count = content.count('@app.route(')
                self.info.append(f"main.py: {route_count} rotas definidas")
                
            except Exception as e:
                self.errors.append(f"main.py: Erro ao ler - {str(e)}")
        else:
            self.errors.append("main.py: Arquivo não encontrado")
            
        # Verificar serviços
        services_dir = self.base_path / 'services'
        if services_dir.exists():
            service_files = list(services_dir.glob('*.py'))
            self.info.append(f"Services: {len(service_files)} arquivos encontrados")
            
            for service in service_files:
                try:
                    with open(service, 'r') as f:
                        content = f.read()
                        if 'class ' in content:
                            self.info.append(f"{service.name}: Contém classes ✓")
                except Exception as e:
                    self.errors.append(f"{service.name}: Erro ao ler - {str(e)}")
        else:
            self.errors.append("services/: Diretório não encontrado")
            
    def audit_frontend(self):
        """Auditar frontend (templates e static)"""
        print("🔍 Auditando Frontend...")
        
        # Verificar templates
        templates_dir = self.base_path / 'templates'
        if templates_dir.exists():
            template_files = list(templates_dir.glob('*.html'))
            self.info.append(f"Templates: {len(template_files)} arquivos encontrados")
            
            for template in template_files:
                try:
                    with open(template, 'r') as f:
                        content = f.read()
                        if '<!DOCTYPE html>' not in content and '<html' not in content:
                            self.warnings.append(f"{template.name}: Pode não ser HTML válido")
                except Exception as e:
                    self.errors.append(f"{template.name}: Erro ao ler - {str(e)}")
        else:
            self.errors.append("templates/: Diretório não encontrado")
            
        # Verificar static
        static_dir = self.base_path / 'static'
        if static_dir.exists():
            css_files = list((static_dir / 'css').glob('*.css')) if (static_dir / 'css').exists() else []
            js_files = list((static_dir / 'js').glob('*.js')) if (static_dir / 'js').exists() else []
            
            self.info.append(f"Static CSS: {len(css_files)} arquivos")
            self.info.append(f"Static JS: {len(js_files)} arquivos")
        else:
            self.errors.append("static/: Diretório não encontrado")
            
    def audit_database(self):
        """Auditar banco de dados"""
        print("🔍 Auditando Banco de Dados...")
        
        db_file = self.base_path / 'database.db'
        if db_file.exists():
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Listar tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                self.info.append(f"Database: {len(tables)} tabelas encontradas")
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    self.info.append(f"  - {table_name}: {count} registros")
                    
                conn.close()
            except Exception as e:
                self.errors.append(f"Database: Erro ao conectar - {str(e)}")
        else:
            self.warnings.append("database.db: Arquivo não encontrado (pode ser criado em runtime)")
            
    def audit_apis(self):
        """Auditar APIs e endpoints"""
        print("🔍 Auditando APIs...")
        
        main_file = self.base_path / 'main.py'
        if main_file.exists():
            try:
                with open(main_file, 'r') as f:
                    content = f.read()
                    
                # Contar endpoints por tipo
                get_count = content.count("methods=['GET']")
                post_count = content.count("methods=['POST']")
                put_count = content.count("methods=['PUT']")
                delete_count = content.count("methods=['DELETE']")
                
                self.info.append(f"APIs GET: {get_count}")
                self.info.append(f"APIs POST: {post_count}")
                self.info.append(f"APIs PUT: {put_count}")
                self.info.append(f"APIs DELETE: {delete_count}")
                
            except Exception as e:
                self.errors.append(f"APIs: Erro ao analisar - {str(e)}")
                
    def audit_integrations(self):
        """Auditar integrações externas"""
        print("🔍 Auditando Integrações...")
        
        env_file = self.base_path / '.env'
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    
                # Verificar credenciais
                if 'OPENAI_API_KEY' in content:
                    self.info.append("OpenAI: API Key configurada ✓")
                else:
                    self.warnings.append("OpenAI: API Key não configurada")
                    
                if 'GOOGLE_ADS' in content:
                    self.info.append("Google Ads: Credenciais configuradas ✓")
                else:
                    self.warnings.append("Google Ads: Credenciais não configuradas")
                    
                if 'FACEBOOK' in content:
                    self.info.append("Facebook Ads: Credenciais configuradas ✓")
                else:
                    self.warnings.append("Facebook Ads: Credenciais não configuradas")
                    
            except Exception as e:
                self.errors.append(f".env: Erro ao ler - {str(e)}")
        else:
            self.errors.append(".env: Arquivo não encontrado")
            
    def run_audit(self):
        """Executar auditoria completa"""
        print("=" * 80)
        print("AUDITORIA TOTAL DO SISTEMA NEXORA PRIME")
        print("=" * 80)
        print()
        
        self.audit_backend()
        self.audit_frontend()
        self.audit_database()
        self.audit_apis()
        self.audit_integrations()
        
        print()
        print("=" * 80)
        print("RESULTADO DA AUDITORIA")
        print("=" * 80)
        print(f"✅ Informações: {len(self.info)}")
        print(f"⚠️  Avisos: {len(self.warnings)}")
        print(f"❌ Erros: {len(self.errors)}")
        print()
        
        if self.errors:
            print("ERROS ENCONTRADOS:")
            for error in self.errors:
                print(f"  ❌ {error}")
            print()
            
        if self.warnings:
            print("AVISOS:")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
            print()
            
        # Salvar resultado
        result = {
            "info": self.info,
            "warnings": self.warnings,
            "errors": self.errors,
            "summary": {
                "total_info": len(self.info),
                "total_warnings": len(self.warnings),
                "total_errors": len(self.errors)
            }
        }
        
        with open(self.base_path / 'AUDIT_RESULT.json', 'w') as f:
            json.dump(result, f, indent=2)
            
        print("✅ Resultado salvo em: AUDIT_RESULT.json")
        
        return result

if __name__ == "__main__":
    auditor = TotalSystemAudit()
    auditor.run_audit()
