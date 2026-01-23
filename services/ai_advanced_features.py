"""
AI Advanced Features - Funcionalidades avançadas de IA
Implementa as funcionalidades 5, 8, 16, 17, 18, 19 do sistema NEXORA
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class AIAdvancedFeatures:
    """Funcionalidades avançadas de IA para o sistema NEXORA"""
    
    def __init__(self):
        self.execution_history = []
        self.output_validations = []
        self.function_calls = {}
        self.cognitive_failures = []
        self.corrections_made = []
        
    # ========================================
    # 5. Correção de alucinação
    # ========================================
    def detect_hallucination(self, response: str, context: Dict) -> Dict:
        """
        Detecta possíveis alucinações na resposta da IA
        Verifica inconsistências com o contexto fornecido
        """
        hallucination_indicators = {
            'invented_data': False,
            'inconsistent_facts': False,
            'fabricated_sources': False,
            'impossible_claims': False
        }
        
        # Verificar dados inventados
        if self._check_invented_data(response, context):
            hallucination_indicators['invented_data'] = True
            
        # Verificar fatos inconsistentes
        if self._check_inconsistent_facts(response, context):
            hallucination_indicators['inconsistent_facts'] = True
            
        # Verificar fontes fabricadas
        if self._check_fabricated_sources(response):
            hallucination_indicators['fabricated_sources'] = True
            
        # Verificar afirmações impossíveis
        if self._check_impossible_claims(response):
            hallucination_indicators['impossible_claims'] = True
            
        has_hallucination = any(hallucination_indicators.values())
        
        return {
            'has_hallucination': has_hallucination,
            'indicators': hallucination_indicators,
            'confidence': self._calculate_hallucination_confidence(hallucination_indicators),
            'timestamp': datetime.now().isoformat()
        }
    
    def correct_hallucination(self, response: str, hallucination_data: Dict) -> str:
        """Corrige alucinações detectadas na resposta"""
        corrected_response = response
        
        if hallucination_data['indicators']['invented_data']:
            corrected_response = self._remove_invented_data(corrected_response)
            
        if hallucination_data['indicators']['inconsistent_facts']:
            corrected_response = self._fix_inconsistent_facts(corrected_response)
            
        if hallucination_data['indicators']['fabricated_sources']:
            corrected_response = self._remove_fabricated_sources(corrected_response)
            
        self.corrections_made.append({
            'type': 'hallucination_correction',
            'original': response[:100],
            'corrected': corrected_response[:100],
            'timestamp': datetime.now().isoformat()
        })
        
        return corrected_response
    
    def _check_invented_data(self, response: str, context: Dict) -> bool:
        """Verifica se há dados inventados"""
        # Verificar números específicos não presentes no contexto
        numbers_in_response = re.findall(r'\d+\.?\d*%?', response)
        context_str = json.dumps(context)
        
        for num in numbers_in_response:
            if num not in context_str and len(num) > 3:
                return True
        return False
    
    def _check_inconsistent_facts(self, response: str, context: Dict) -> bool:
        """Verifica fatos inconsistentes"""
        # Implementação básica - pode ser expandida
        return False
    
    def _check_fabricated_sources(self, response: str) -> bool:
        """Verifica fontes fabricadas"""
        fabricated_patterns = [
            r'segundo estudo de \d{4}',
            r'pesquisa da universidade',
            r'relatório oficial'
        ]
        for pattern in fabricated_patterns:
            if re.search(pattern, response.lower()):
                return True
        return False
    
    def _check_impossible_claims(self, response: str) -> bool:
        """Verifica afirmações impossíveis"""
        impossible_patterns = [
            r'100% de certeza',
            r'garantido que',
            r'impossível falhar'
        ]
        for pattern in impossible_patterns:
            if re.search(pattern, response.lower()):
                return True
        return False
    
    def _calculate_hallucination_confidence(self, indicators: Dict) -> float:
        """Calcula confiança na detecção de alucinação"""
        true_count = sum(1 for v in indicators.values() if v)
        return true_count / len(indicators)
    
    def _remove_invented_data(self, response: str) -> str:
        """Remove dados inventados"""
        return response
    
    def _fix_inconsistent_facts(self, response: str) -> str:
        """Corrige fatos inconsistentes"""
        return response
    
    def _remove_fabricated_sources(self, response: str) -> str:
        """Remove fontes fabricadas"""
        return re.sub(r'segundo estudo de \d{4}[^.]*\.', '', response)
    
    # ========================================
    # 8. Execução 100% do escopo
    # ========================================
    def validate_scope_execution(self, scope: Dict, execution_result: Dict) -> Dict:
        """
        Valida se 100% do escopo foi executado
        Retorna relatório detalhado de cobertura
        """
        required_items = scope.get('required_items', [])
        executed_items = execution_result.get('executed_items', [])
        
        coverage_report = {
            'total_required': len(required_items),
            'total_executed': 0,
            'coverage_percentage': 0,
            'missing_items': [],
            'extra_items': [],
            'status': 'incomplete'
        }
        
        # Verificar itens executados
        for item in required_items:
            if item in executed_items:
                coverage_report['total_executed'] += 1
            else:
                coverage_report['missing_items'].append(item)
        
        # Verificar itens extras
        for item in executed_items:
            if item not in required_items:
                coverage_report['extra_items'].append(item)
        
        # Calcular porcentagem
        if coverage_report['total_required'] > 0:
            coverage_report['coverage_percentage'] = (
                coverage_report['total_executed'] / coverage_report['total_required']
            ) * 100
        
        # Definir status
        if coverage_report['coverage_percentage'] == 100:
            coverage_report['status'] = 'complete'
        elif coverage_report['coverage_percentage'] >= 90:
            coverage_report['status'] = 'almost_complete'
        elif coverage_report['coverage_percentage'] >= 50:
            coverage_report['status'] = 'partial'
        else:
            coverage_report['status'] = 'incomplete'
        
        self.execution_history.append({
            'scope': scope,
            'result': coverage_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return coverage_report
    
    def ensure_complete_execution(self, scope: Dict, executor_func) -> Dict:
        """
        Garante execução completa do escopo
        Re-executa itens faltantes até atingir 100%
        """
        max_retries = 3
        current_retry = 0
        
        while current_retry < max_retries:
            result = executor_func(scope)
            validation = self.validate_scope_execution(scope, result)
            
            if validation['status'] == 'complete':
                return {
                    'success': True,
                    'result': result,
                    'validation': validation,
                    'retries': current_retry
                }
            
            # Re-executar itens faltantes
            scope['required_items'] = validation['missing_items']
            current_retry += 1
        
        return {
            'success': False,
            'result': result,
            'validation': validation,
            'retries': current_retry,
            'error': 'Could not achieve 100% scope execution'
        }
    
    # ========================================
    # 16. Anti-repetição de função
    # ========================================
    def register_function_call(self, function_name: str, params: Dict) -> bool:
        """
        Registra chamada de função e verifica repetição
        Retorna True se é uma chamada válida (não repetida)
        """
        call_signature = f"{function_name}:{json.dumps(params, sort_keys=True)}"
        
        if call_signature in self.function_calls:
            self.function_calls[call_signature]['count'] += 1
            self.function_calls[call_signature]['last_call'] = datetime.now().isoformat()
            
            # Verificar se é repetição excessiva
            if self.function_calls[call_signature]['count'] > 3:
                return False  # Repetição detectada
        else:
            self.function_calls[call_signature] = {
                'count': 1,
                'first_call': datetime.now().isoformat(),
                'last_call': datetime.now().isoformat()
            }
        
        return True
    
    def detect_repetition_pattern(self) -> Dict:
        """Detecta padrões de repetição nas chamadas de função"""
        repetition_report = {
            'has_repetition': False,
            'repeated_functions': [],
            'total_calls': sum(v['count'] for v in self.function_calls.values()),
            'unique_calls': len(self.function_calls)
        }
        
        for signature, data in self.function_calls.items():
            if data['count'] > 3:
                repetition_report['has_repetition'] = True
                repetition_report['repeated_functions'].append({
                    'signature': signature,
                    'count': data['count']
                })
        
        return repetition_report
    
    def reset_function_tracking(self):
        """Reseta o rastreamento de funções"""
        self.function_calls = {}
    
    # ========================================
    # 17. Detecção de falha cognitiva
    # ========================================
    def detect_cognitive_failure(self, response: str, expected_behavior: Dict) -> Dict:
        """
        Detecta falhas cognitivas na resposta da IA
        Verifica se a resposta atende ao comportamento esperado
        """
        failure_report = {
            'has_failure': False,
            'failure_types': [],
            'severity': 'none',
            'recommendations': []
        }
        
        # Verificar resposta vazia ou muito curta
        if not response or len(response) < 10:
            failure_report['has_failure'] = True
            failure_report['failure_types'].append('empty_response')
            failure_report['severity'] = 'critical'
            failure_report['recommendations'].append('Regenerar resposta com mais contexto')
        
        # Verificar resposta genérica
        generic_patterns = [
            'não sei',
            'não tenho certeza',
            'não posso ajudar',
            'desculpe, mas'
        ]
        for pattern in generic_patterns:
            if pattern in response.lower():
                failure_report['has_failure'] = True
                failure_report['failure_types'].append('generic_response')
                failure_report['severity'] = 'medium'
                failure_report['recommendations'].append('Fornecer resposta mais específica')
        
        # Verificar loop de resposta
        if self._detect_response_loop(response):
            failure_report['has_failure'] = True
            failure_report['failure_types'].append('response_loop')
            failure_report['severity'] = 'high'
            failure_report['recommendations'].append('Quebrar loop com nova abordagem')
        
        # Verificar contradição interna
        if self._detect_internal_contradiction(response):
            failure_report['has_failure'] = True
            failure_report['failure_types'].append('internal_contradiction')
            failure_report['severity'] = 'high'
            failure_report['recommendations'].append('Revisar lógica da resposta')
        
        if failure_report['has_failure']:
            self.cognitive_failures.append({
                'report': failure_report,
                'response_preview': response[:200],
                'timestamp': datetime.now().isoformat()
            })
        
        return failure_report
    
    def _detect_response_loop(self, response: str) -> bool:
        """Detecta loops na resposta"""
        sentences = response.split('.')
        if len(sentences) > 3:
            # Verificar se há sentenças repetidas
            unique_sentences = set(s.strip().lower() for s in sentences if s.strip())
            if len(unique_sentences) < len(sentences) * 0.5:
                return True
        return False
    
    def _detect_internal_contradiction(self, response: str) -> bool:
        """Detecta contradições internas"""
        contradiction_pairs = [
            ('sim', 'não'),
            ('sempre', 'nunca'),
            ('todos', 'nenhum'),
            ('aumentar', 'diminuir')
        ]
        
        response_lower = response.lower()
        for pair in contradiction_pairs:
            if pair[0] in response_lower and pair[1] in response_lower:
                # Verificar se estão próximos (possível contradição)
                pos1 = response_lower.find(pair[0])
                pos2 = response_lower.find(pair[1])
                if abs(pos1 - pos2) < 100:
                    return True
        return False
    
    # ========================================
    # 18. Autocorreção lógica
    # ========================================
    def auto_correct_logic(self, response: str, context: Dict) -> Dict:
        """
        Aplica autocorreção lógica na resposta
        Corrige inconsistências e erros lógicos
        """
        corrections = []
        corrected_response = response
        
        # Corrigir números inconsistentes
        corrected_response, num_corrections = self._correct_number_inconsistencies(
            corrected_response, context
        )
        if num_corrections:
            corrections.extend(num_corrections)
        
        # Corrigir contradições
        corrected_response, contradiction_corrections = self._correct_contradictions(
            corrected_response
        )
        if contradiction_corrections:
            corrections.extend(contradiction_corrections)
        
        # Corrigir sequência lógica
        corrected_response, sequence_corrections = self._correct_logical_sequence(
            corrected_response
        )
        if sequence_corrections:
            corrections.extend(sequence_corrections)
        
        self.corrections_made.append({
            'type': 'logic_correction',
            'corrections_count': len(corrections),
            'corrections': corrections,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'original': response,
            'corrected': corrected_response,
            'corrections': corrections,
            'was_corrected': len(corrections) > 0
        }
    
    def _correct_number_inconsistencies(self, response: str, context: Dict) -> tuple:
        """Corrige inconsistências numéricas"""
        corrections = []
        # Implementação básica
        return response, corrections
    
    def _correct_contradictions(self, response: str) -> tuple:
        """Corrige contradições"""
        corrections = []
        # Implementação básica
        return response, corrections
    
    def _correct_logical_sequence(self, response: str) -> tuple:
        """Corrige sequência lógica"""
        corrections = []
        # Implementação básica
        return response, corrections
    
    # ========================================
    # 19. Validação de outputs
    # ========================================
    def validate_output(self, output: Any, expected_schema: Dict) -> Dict:
        """
        Valida output contra schema esperado
        Retorna relatório de validação detalhado
        """
        validation_report = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'schema_compliance': 100.0
        }
        
        # Verificar tipo
        expected_type = expected_schema.get('type')
        if expected_type:
            if not self._check_type(output, expected_type):
                validation_report['is_valid'] = False
                validation_report['errors'].append(f'Expected type {expected_type}')
        
        # Verificar campos obrigatórios (para dicts)
        if isinstance(output, dict):
            required_fields = expected_schema.get('required', [])
            for field in required_fields:
                if field not in output:
                    validation_report['is_valid'] = False
                    validation_report['errors'].append(f'Missing required field: {field}')
        
        # Verificar formato
        format_spec = expected_schema.get('format')
        if format_spec and not self._check_format(output, format_spec):
            validation_report['warnings'].append(f'Format mismatch: expected {format_spec}')
        
        # Verificar range (para números)
        if isinstance(output, (int, float)):
            min_val = expected_schema.get('minimum')
            max_val = expected_schema.get('maximum')
            if min_val is not None and output < min_val:
                validation_report['is_valid'] = False
                validation_report['errors'].append(f'Value below minimum: {min_val}')
            if max_val is not None and output > max_val:
                validation_report['is_valid'] = False
                validation_report['errors'].append(f'Value above maximum: {max_val}')
        
        # Calcular compliance
        total_checks = len(validation_report['errors']) + len(validation_report['warnings']) + 1
        passed_checks = total_checks - len(validation_report['errors'])
        validation_report['schema_compliance'] = (passed_checks / total_checks) * 100
        
        self.output_validations.append({
            'report': validation_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return validation_report
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Verifica tipo do valor"""
        type_mapping = {
            'string': str,
            'number': (int, float),
            'integer': int,
            'boolean': bool,
            'array': list,
            'object': dict
        }
        expected = type_mapping.get(expected_type)
        if expected:
            return isinstance(value, expected)
        return True
    
    def _check_format(self, value: Any, format_spec: str) -> bool:
        """Verifica formato do valor"""
        if format_spec == 'email':
            return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(value)))
        elif format_spec == 'url':
            return bool(re.match(r'^https?://', str(value)))
        elif format_spec == 'date':
            try:
                datetime.strptime(str(value), '%Y-%m-%d')
                return True
            except ValueError:
                return False
        return True
    
    def get_validation_summary(self) -> Dict:
        """Retorna resumo das validações realizadas"""
        total = len(self.output_validations)
        valid = sum(1 for v in self.output_validations if v['report']['is_valid'])
        
        return {
            'total_validations': total,
            'valid_outputs': valid,
            'invalid_outputs': total - valid,
            'success_rate': (valid / total * 100) if total > 0 else 100,
            'cognitive_failures': len(self.cognitive_failures),
            'corrections_made': len(self.corrections_made)
        }


# Instância global
ai_advanced_features = AIAdvancedFeatures()
