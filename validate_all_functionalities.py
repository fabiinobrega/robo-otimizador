"""
VALIDAÇÃO DE TODAS AS FUNCIONALIDADES
Testa: Rotas, APIs, Interfaces, Banco de Dados, Templates
"""

import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

import json
import sqlite3
from pathlib import Path
from datetime import datetime

class AllFunctionalitiesValidator:
    """Validador de todas as funcionalidades"""
    
    def __init__(self):
        self.base_path = Path('/home/ubuntu/robo-otimizador')
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "categories": {
                "rotas": {"tests": [], "passed": 0, "failed": 0},
                "apis": {"tests": [], "passed": 0, "failed": 0},
                "banco_dados": {"tests": [], "passed": 0, "failed": 0},
                "templates": {"tests": [], "passed": 0, "failed": 0},
                "servicos": {"tests": [], "passed": 0, "failed": 0}
            }
        }
        
    def test_routes(self):
        """Testar rotas"""
        print("🧪 Testando Rotas...")
        cat = self.results["categories"]["rotas"]
        
        main_file = self.base_path / 'main.py'
        if main_file.exists():
            try:
                with open(main_file, 'r') as f:
                    content = f.read()
                    
                # Contar rotas
                route_count = content.count('@app.route(')
                
                cat["tests"].append({
                    "name": "Contagem de rotas",
                    "status": "PASS",
                    "count": route_count
                })
                cat["passed"] += 1
                print(f"   ✅ {route_count} rotas encontradas")
                
                # Verificar rotas críticas
                critical_routes = [
                    '/api/credits/status',
                    '/api/openai/generate-campaign',
                    '/api/manus/apply-campaign',
                    '/api/orchestration/create-deploy-campaign',
                    '/credits-dashboard',
                    '/ai-dashboard'
                ]
                
                for route in critical_routes:
                    if f"'{route}'" in content or f'"{route}"' in content:
                        cat["tests"].append({
                            "name": f"Rota crítica: {route}",
                            "status": "PASS"
                        })
                        cat["passed"] += 1
                        print(f"   ✅ {route}")
                    else:
                        cat["tests"].append({
                            "name": f"Rota crítica: {route}",
                            "status": "FAIL",
                            "error": "Rota não encontrada"
                        })
                        cat["failed"] += 1
                        print(f"   ❌ {route} não encontrada")
                        
            except Exception as e:
                cat["tests"].append({
                    "name": "Leitura de rotas",
                    "status": "FAIL",
                    "error": str(e)
                })
                cat["failed"] += 1
                print(f"   ❌ Erro: {str(e)}")
        else:
            cat["tests"].append({
                "name": "Arquivo main.py",
                "status": "FAIL",
                "error": "Arquivo não encontrado"
            })
            cat["failed"] += 1
            print("   ❌ main.py não encontrado")
    
    def test_apis(self):
        """Testar APIs"""
        print("🧪 Testando APIs...")
        cat = self.results["categories"]["apis"]
        
        # Verificar serviços de API
        api_services = {
            'openai_strategic_engine.py': 'OpenAI Strategic Engine',
            'openai_campaign_creator.py': 'OpenAI Campaign Creator',
            'openai_optimization_engine.py': 'OpenAI Optimization Engine',
            'manus_executor_bridge.py': 'Manus Executor Bridge',
            'nexora_automation.py': 'Nexora Automation',
            'orchestration_engine.py': 'Orchestration Engine',
            'credits_monitor_service.py': 'Credits Monitor'
        }
        
        services_dir = self.base_path / 'services'
        for filename, name in api_services.items():
            service_file = services_dir / filename
            if service_file.exists():
                try:
                    with open(service_file, 'r') as f:
                        content = f.read()
                        if 'class ' in content:
                            cat["tests"].append({
                                "name": name,
                                "status": "PASS",
                                "file": filename
                            })
                            cat["passed"] += 1
                            print(f"   ✅ {name}")
                        else:
                            cat["tests"].append({
                                "name": name,
                                "status": "FAIL",
                                "error": "Sem classes definidas",
                                "file": filename
                            })
                            cat["failed"] += 1
                            print(f"   ❌ {name} - sem classes")
                except Exception as e:
                    cat["tests"].append({
                        "name": name,
                        "status": "FAIL",
                        "error": str(e),
                        "file": filename
                    })
                    cat["failed"] += 1
                    print(f"   ❌ {name} - erro: {str(e)}")
            else:
                cat["tests"].append({
                    "name": name,
                    "status": "FAIL",
                    "error": "Arquivo não encontrado",
                    "file": filename
                })
                cat["failed"] += 1
                print(f"   ❌ {name} - arquivo não encontrado")
    
    def test_database(self):
        """Testar banco de dados"""
        print("🧪 Testando Banco de Dados...")
        cat = self.results["categories"]["banco_dados"]
        
        db_file = self.base_path / 'database.db'
        if db_file.exists():
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Testar conexão
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                cat["tests"].append({
                    "name": "Conexão com banco",
                    "status": "PASS",
                    "tables_count": len(tables)
                })
                cat["passed"] += 1
                print(f"   ✅ Conexão OK - {len(tables)} tabelas")
                
                # Testar integridade de cada tabela
                for table in tables:
                    table_name = table[0]
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        
                        cat["tests"].append({
                            "name": f"Tabela {table_name}",
                            "status": "PASS",
                            "records": count
                        })
                        cat["passed"] += 1
                        print(f"   ✅ {table_name}: {count} registros")
                    except Exception as e:
                        cat["tests"].append({
                            "name": f"Tabela {table_name}",
                            "status": "FAIL",
                            "error": str(e)
                        })
                        cat["failed"] += 1
                        print(f"   ❌ {table_name}: {str(e)}")
                
                conn.close()
            except Exception as e:
                cat["tests"].append({
                    "name": "Banco de dados",
                    "status": "FAIL",
                    "error": str(e)
                })
                cat["failed"] += 1
                print(f"   ❌ Erro: {str(e)}")
        else:
            cat["tests"].append({
                "name": "Arquivo database.db",
                "status": "WARNING",
                "message": "Arquivo não encontrado (pode ser criado em runtime)"
            })
            print("   ⚠️  database.db não encontrado")
    
    def test_templates(self):
        """Testar templates"""
        print("🧪 Testando Templates...")
        cat = self.results["categories"]["templates"]
        
        templates_dir = self.base_path / 'templates'
        if templates_dir.exists():
            template_files = list(templates_dir.glob('*.html'))
            
            # Templates críticos
            critical_templates = [
                'credits_dashboard.html',
                'ai_dashboard.html',
                'dashboard.html',
                'create_campaign.html'
            ]
            
            for template_name in critical_templates:
                template_file = templates_dir / template_name
                if template_file.exists():
                    try:
                        with open(template_file, 'r') as f:
                            content = f.read()
                            if len(content) > 0:
                                cat["tests"].append({
                                    "name": template_name,
                                    "status": "PASS",
                                    "size": len(content)
                                })
                                cat["passed"] += 1
                                print(f"   ✅ {template_name}")
                            else:
                                cat["tests"].append({
                                    "name": template_name,
                                    "status": "FAIL",
                                    "error": "Arquivo vazio"
                                })
                                cat["failed"] += 1
                                print(f"   ❌ {template_name} - vazio")
                    except Exception as e:
                        cat["tests"].append({
                            "name": template_name,
                            "status": "FAIL",
                            "error": str(e)
                        })
                        cat["failed"] += 1
                        print(f"   ❌ {template_name} - erro: {str(e)}")
                else:
                    cat["tests"].append({
                        "name": template_name,
                        "status": "FAIL",
                        "error": "Arquivo não encontrado"
                    })
                    cat["failed"] += 1
                    print(f"   ❌ {template_name} - não encontrado")
            
            # Contar todos os templates
            cat["tests"].append({
                "name": "Total de templates",
                "status": "INFO",
                "count": len(template_files)
            })
            print(f"   ℹ️  Total: {len(template_files)} templates")
        else:
            cat["tests"].append({
                "name": "Diretório templates",
                "status": "FAIL",
                "error": "Diretório não encontrado"
            })
            cat["failed"] += 1
            print("   ❌ Diretório templates/ não encontrado")
    
    def test_services(self):
        """Testar serviços"""
        print("🧪 Testando Serviços...")
        cat = self.results["categories"]["servicos"]
        
        services_dir = self.base_path / 'services'
        if services_dir.exists():
            service_files = list(services_dir.glob('*.py'))
            
            for service_file in service_files:
                try:
                    with open(service_file, 'r') as f:
                        content = f.read()
                        
                    # Verificar sintaxe Python
                    compile(content, service_file.name, 'exec')
                    
                    cat["tests"].append({
                        "name": service_file.name,
                        "status": "PASS"
                    })
                    cat["passed"] += 1
                    
                except SyntaxError as e:
                    cat["tests"].append({
                        "name": service_file.name,
                        "status": "FAIL",
                        "error": f"Erro de sintaxe: {str(e)}"
                    })
                    cat["failed"] += 1
                    print(f"   ❌ {service_file.name} - erro de sintaxe")
                except Exception as e:
                    cat["tests"].append({
                        "name": service_file.name,
                        "status": "FAIL",
                        "error": str(e)
                    })
                    cat["failed"] += 1
                    print(f"   ❌ {service_file.name} - erro: {str(e)}")
            
            print(f"   ✅ {cat['passed']}/{len(service_files)} serviços válidos")
        else:
            cat["tests"].append({
                "name": "Diretório services",
                "status": "FAIL",
                "error": "Diretório não encontrado"
            })
            cat["failed"] += 1
            print("   ❌ Diretório services/ não encontrado")
    
    def run_validation(self):
        """Executar validação completa"""
        print("=" * 80)
        print("VALIDAÇÃO DE TODAS AS FUNCIONALIDADES")
        print("=" * 80)
        print()
        
        self.test_routes()
        print()
        self.test_apis()
        print()
        self.test_database()
        print()
        self.test_templates()
        print()
        self.test_services()
        print()
        
        # Calcular totais
        total_passed = sum(cat["passed"] for cat in self.results["categories"].values())
        total_failed = sum(cat["failed"] for cat in self.results["categories"].values())
        
        print("=" * 80)
        print(f"RESULTADO: {total_passed} PASSARAM | {total_failed} FALHARAM")
        print("=" * 80)
        
        # Salvar resultados
        with open('/tmp/nexora_validation_output/test_results/all_functionalities.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Resultados salvos em: /tmp/nexora_validation_output/test_results/all_functionalities.json")
        
        return self.results

if __name__ == "__main__":
    validator = AllFunctionalitiesValidator()
    validator.run_validation()
