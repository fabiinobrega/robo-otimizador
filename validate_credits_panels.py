"""
VALIDAÇÃO DOS PAINÉIS DE CRÉDITO
Testa OpenAI, Manus, widget, cores, tempo real, erros e alertas
"""

import sys
sys.path.insert(0, '/home/ubuntu/robo-otimizador')

import json
import os
from datetime import datetime
from services.credits_monitor_service import CreditsMonitorService

class CreditsPanelValidator:
    """Validador dos painéis de crédito"""
    
    def __init__(self):
        self.monitor = CreditsMonitorService()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "passed": 0,
            "failed": 0
        }
        
    def test_openai_status(self):
        """Testar status da OpenAI"""
        print("🧪 Testando status OpenAI...")
        
        try:
            status = self.monitor.get_openai_credits()
            
            # Verificar campos obrigatórios
            required_fields = ['success', 'status', 'message', 'color', 'balance']
            missing_fields = [f for f in required_fields if f not in status]
            
            if missing_fields:
                self.results["tests"].append({
                    "name": "OpenAI Status - Campos obrigatórios",
                    "status": "FAIL",
                    "error": f"Campos faltando: {missing_fields}"
                })
                self.results["failed"] += 1
                print(f"   ❌ Campos faltando: {missing_fields}")
            else:
                self.results["tests"].append({
                    "name": "OpenAI Status - Campos obrigatórios",
                    "status": "PASS",
                    "data": status
                })
                self.results["passed"] += 1
                print(f"   ✅ Todos os campos presentes")
                
            # Verificar cores válidas
            valid_colors = ['green', 'yellow', 'red', 'gray']
            if status.get('color') not in valid_colors:
                self.results["tests"].append({
                    "name": "OpenAI Status - Cor válida",
                    "status": "FAIL",
                    "error": f"Cor inválida: {status.get('color')}"
                })
                self.results["failed"] += 1
                print(f"   ❌ Cor inválida: {status.get('color')}")
            else:
                self.results["tests"].append({
                    "name": "OpenAI Status - Cor válida",
                    "status": "PASS",
                    "color": status.get('color')
                })
                self.results["passed"] += 1
                print(f"   ✅ Cor válida: {status.get('color')}")
                
        except Exception as e:
            self.results["tests"].append({
                "name": "OpenAI Status - Execução",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
            print(f"   ❌ Erro: {str(e)}")
    
    def test_manus_status(self):
        """Testar status do Manus"""
        print("🧪 Testando status Manus...")
        
        try:
            status = self.monitor.get_manus_credits()
            
            # Verificar campos obrigatórios
            required_fields = ['success', 'status', 'message', 'color', 'credits']
            missing_fields = [f for f in required_fields if f not in status]
            
            if missing_fields:
                self.results["tests"].append({
                    "name": "Manus Status - Campos obrigatórios",
                    "status": "FAIL",
                    "error": f"Campos faltando: {missing_fields}"
                })
                self.results["failed"] += 1
                print(f"   ❌ Campos faltando: {missing_fields}")
            else:
                self.results["tests"].append({
                    "name": "Manus Status - Campos obrigatórios",
                    "status": "PASS",
                    "data": status
                })
                self.results["passed"] += 1
                print(f"   ✅ Todos os campos presentes")
                
            # Verificar cores válidas
            valid_colors = ['green', 'yellow', 'red', 'gray']
            if status.get('color') not in valid_colors:
                self.results["tests"].append({
                    "name": "Manus Status - Cor válida",
                    "status": "FAIL",
                    "error": f"Cor inválida: {status.get('color')}"
                })
                self.results["failed"] += 1
                print(f"   ❌ Cor inválida: {status.get('color')}")
            else:
                self.results["tests"].append({
                    "name": "Manus Status - Cor válida",
                    "status": "PASS",
                    "color": status.get('color')
                })
                self.results["passed"] += 1
                print(f"   ✅ Cor válida: {status.get('color')}")
                
        except Exception as e:
            self.results["tests"].append({
                "name": "Manus Status - Execução",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
            print(f"   ❌ Erro: {str(e)}")
    
    def test_all_credits_status(self):
        """Testar status geral"""
        print("🧪 Testando status geral...")
        
        try:
            status = self.monitor.get_all_credits_status()
            
            # Verificar estrutura
            required_fields = ['success', 'overall_status', 'overall_color', 'overall_message', 'openai', 'manus']
            missing_fields = [f for f in required_fields if f not in status]
            
            if missing_fields:
                self.results["tests"].append({
                    "name": "Status Geral - Estrutura",
                    "status": "FAIL",
                    "error": f"Campos faltando: {missing_fields}"
                })
                self.results["failed"] += 1
                print(f"   ❌ Campos faltando: {missing_fields}")
            else:
                self.results["tests"].append({
                    "name": "Status Geral - Estrutura",
                    "status": "PASS"
                })
                self.results["passed"] += 1
                print(f"   ✅ Estrutura correta")
                
        except Exception as e:
            self.results["tests"].append({
                "name": "Status Geral - Execução",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
            print(f"   ❌ Erro: {str(e)}")
    
    def test_error_simulation(self):
        """Simular erros e validar respostas"""
        print("🧪 Testando simulação de erros...")
        
        # Simular API key inválida temporariamente
        original_key = os.getenv('OPENAI_API_KEY')
        os.environ['OPENAI_API_KEY'] = 'invalid_key_test'
        
        try:
            monitor_test = CreditsMonitorService()
            status = monitor_test.get_openai_credits()
            
            # Deve retornar erro amigável
            if 'error' in status.get('status', '') or not status.get('success'):
                self.results["tests"].append({
                    "name": "Simulação de Erro - API Key Inválida",
                    "status": "PASS",
                    "message": "Erro tratado corretamente"
                })
                self.results["passed"] += 1
                print(f"   ✅ Erro tratado corretamente")
            else:
                self.results["tests"].append({
                    "name": "Simulação de Erro - API Key Inválida",
                    "status": "FAIL",
                    "error": "Erro não foi detectado"
                })
                self.results["failed"] += 1
                print(f"   ❌ Erro não foi detectado")
                
        except Exception as e:
            self.results["tests"].append({
                "name": "Simulação de Erro - Execução",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
            print(f"   ❌ Erro: {str(e)}")
        finally:
            # Restaurar chave original
            if original_key:
                os.environ['OPENAI_API_KEY'] = original_key
    
    def run_validation(self):
        """Executar validação completa"""
        print("=" * 80)
        print("VALIDAÇÃO DOS PAINÉIS DE CRÉDITO")
        print("=" * 80)
        print()
        
        self.test_openai_status()
        print()
        self.test_manus_status()
        print()
        self.test_all_credits_status()
        print()
        self.test_error_simulation()
        print()
        
        print("=" * 80)
        print(f"RESULTADO: {self.results['passed']} PASSARAM | {self.results['failed']} FALHARAM")
        print("=" * 80)
        
        # Salvar resultados
        with open('/tmp/nexora_validation_output/credits_status.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Resultados salvos em: /tmp/nexora_validation_output/credits_status.json")
        
        # Também salvar status atual
        current_status = self.monitor.get_all_credits_status()
        with open('/tmp/nexora_validation_output/credits_current_status.json', 'w') as f:
            json.dump(current_status, f, indent=2)
        
        print(f"✅ Status atual salvo em: /tmp/nexora_validation_output/credits_current_status.json")
        
        return self.results

if __name__ == "__main__":
    validator = CreditsPanelValidator()
    validator.run_validation()
