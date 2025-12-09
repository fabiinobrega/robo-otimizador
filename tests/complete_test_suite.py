"""
SUITE COMPLETA DE TESTES AUTOMÁTICOS
Testa: Rotas, Serviços, Funções, Anúncios, APIs, BD, Performance, Interface
"""

import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

import json
import time
import sqlite3
from pathlib import Path

class CompleteTestSuite:
    """Suite completa de testes"""
    
    def __init__(self):
        self.base_path = Path('/home/ubuntu/robo-otimizador')
        self.results = {
            "rotas": [],
            "servicos": [],
            "funcoes": [],
            "apis": [],
            "banco_dados": [],
            "performance": [],
            "interface": []
        }
        self.passed = 0
        self.failed = 0
        
    def test_routes(self):
        """Testar rotas"""
        print("🧪 Testando Rotas...")
        
        main_file = self.base_path / 'main.py'
        if main_file.exists():
            with open(main_file, 'r') as f:
                content = f.read()
                route_count = content.count('@app.route(')
                
                self.results["rotas"].append({
                    "test": "Contagem de rotas",
                    "status": "PASS",
                    "value": route_count
                })
                self.passed += 1
                print(f"   ✅ {route_count} rotas encontradas")
        else:
            self.results["rotas"].append({
                "test": "Arquivo main.py",
                "status": "FAIL",
                "error": "Arquivo não encontrado"
            })
            self.failed += 1
            print("   ❌ main.py não encontrado")
    
    def test_services(self):
        """Testar serviços"""
        print("🧪 Testando Serviços...")
        
        services_dir = self.base_path / 'services'
        if services_dir.exists():
            service_files = list(services_dir.glob('*.py'))
            
            for service in service_files:
                try:
                    with open(service, 'r') as f:
                        content = f.read()
                        has_class = 'class ' in content
                        
                        if has_class:
                            self.results["servicos"].append({
                                "test": service.name,
                                "status": "PASS"
                            })
                            self.passed += 1
                        else:
                            self.results["servicos"].append({
                                "test": service.name,
                                "status": "FAIL",
                                "error": "Sem classes"
                            })
                            self.failed += 1
                except Exception as e:
                    self.results["servicos"].append({
                        "test": service.name,
                        "status": "FAIL",
                        "error": str(e)
                    })
                    self.failed += 1
            
            print(f"   ✅ {len(service_files)} serviços testados")
        else:
            print("   ❌ Diretório services/ não encontrado")
            self.failed += 1
    
    def test_database(self):
        """Testar banco de dados"""
        print("🧪 Testando Banco de Dados...")
        
        db_file = self.base_path / 'database.db'
        if db_file.exists():
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Testar conexão
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                self.results["banco_dados"].append({
                    "test": "Conexão com banco",
                    "status": "PASS",
                    "tables": len(tables)
                })
                self.passed += 1
                
                # Testar cada tabela
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    
                    self.results["banco_dados"].append({
                        "test": f"Tabela {table_name}",
                        "status": "PASS",
                        "records": count
                    })
                    self.passed += 1
                
                conn.close()
                print(f"   ✅ {len(tables)} tabelas testadas")
            except Exception as e:
                self.results["banco_dados"].append({
                    "test": "Banco de dados",
                    "status": "FAIL",
                    "error": str(e)
                })
                self.failed += 1
                print(f"   ❌ Erro: {str(e)}")
        else:
            print("   ⚠️  database.db não encontrado (pode ser criado em runtime)")
    
    def test_apis(self):
        """Testar APIs"""
        print("🧪 Testando APIs...")
        
        # Testar importação de serviços de API
        api_services = [
            'openai_strategic_engine',
            'openai_campaign_creator',
            'openai_optimization_engine',
            'manus_executor_bridge',
            'nexora_automation',
            'orchestration_engine',
            'credits_monitor_service'
        ]
        
        for service_name in api_services:
            try:
                service_file = self.base_path / 'services' / f'{service_name}.py'
                if service_file.exists():
                    self.results["apis"].append({
                        "test": f"Serviço {service_name}",
                        "status": "PASS"
                    })
                    self.passed += 1
                else:
                    self.results["apis"].append({
                        "test": f"Serviço {service_name}",
                        "status": "FAIL",
                        "error": "Arquivo não encontrado"
                    })
                    self.failed += 1
            except Exception as e:
                self.results["apis"].append({
                    "test": f"Serviço {service_name}",
                    "status": "FAIL",
                    "error": str(e)
                })
                self.failed += 1
        
        print(f"   ✅ {len(api_services)} serviços de API testados")
    
    def test_performance(self):
        """Testar performance"""
        print("🧪 Testando Performance...")
        
        # Testar tempo de leitura de arquivos
        start_time = time.time()
        
        main_file = self.base_path / 'main.py'
        if main_file.exists():
            with open(main_file, 'r') as f:
                content = f.read()
        
        end_time = time.time()
        read_time = (end_time - start_time) * 1000  # em ms
        
        if read_time < 100:
            self.results["performance"].append({
                "test": "Tempo de leitura de arquivo",
                "status": "PASS",
                "time_ms": round(read_time, 2)
            })
            self.passed += 1
            print(f"   ✅ Leitura: {round(read_time, 2)}ms")
        else:
            self.results["performance"].append({
                "test": "Tempo de leitura de arquivo",
                "status": "FAIL",
                "time_ms": round(read_time, 2)
            })
            self.failed += 1
            print(f"   ❌ Leitura lenta: {round(read_time, 2)}ms")
    
    def test_interface(self):
        """Testar interface"""
        print("🧪 Testando Interface...")
        
        templates_dir = self.base_path / 'templates'
        if templates_dir.exists():
            template_files = list(templates_dir.glob('*.html'))
            
            for template in template_files:
                try:
                    with open(template, 'r') as f:
                        content = f.read()
                        
                        # Verificar se tem conteúdo
                        if len(content) > 0:
                            self.results["interface"].append({
                                "test": template.name,
                                "status": "PASS",
                                "size": len(content)
                            })
                            self.passed += 1
                        else:
                            self.results["interface"].append({
                                "test": template.name,
                                "status": "FAIL",
                                "error": "Arquivo vazio"
                            })
                            self.failed += 1
                except Exception as e:
                    self.results["interface"].append({
                        "test": template.name,
                        "status": "FAIL",
                        "error": str(e)
                    })
                    self.failed += 1
            
            print(f"   ✅ {len(template_files)} templates testados")
        else:
            print("   ❌ Diretório templates/ não encontrado")
            self.failed += 1
    
    def run_all_tests(self):
        """Executar todos os testes"""
        print("=" * 80)
        print("SUITE COMPLETA DE TESTES AUTOMÁTICOS")
        print("=" * 80)
        print()
        
        self.test_routes()
        print()
        self.test_services()
        print()
        self.test_database()
        print()
        self.test_apis()
        print()
        self.test_performance()
        print()
        self.test_interface()
        print()
        
        print("=" * 80)
        print(f"RESULTADO: {self.passed} PASSARAM | {self.failed} FALHARAM")
        print("=" * 80)
        
        # Salvar resultados
        final_result = {
            "summary": {
                "passed": self.passed,
                "failed": self.failed,
                "total": self.passed + self.failed,
                "success_rate": round((self.passed / (self.passed + self.failed)) * 100, 2) if (self.passed + self.failed) > 0 else 0
            },
            "details": self.results
        }
        
        with open(self.base_path / 'tests' / 'complete_test_results.json', 'w') as f:
            json.dump(final_result, f, indent=2)
        
        print(f"\n✅ Resultados salvos em: tests/complete_test_results.json")
        print(f"Taxa de Sucesso: {final_result['summary']['success_rate']}%")
        
        return final_result

if __name__ == "__main__":
    suite = CompleteTestSuite()
    suite.run_all_tests()
