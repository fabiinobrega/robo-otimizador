"""
A/B Testing Service
Sistema avançado para criação e análise de testes A/B
"""
import json
import random
from typing import Dict, List, Any
from datetime import datetime
from functools import wraps


def handle_errors(func):
    """Decorador para tratamento automático de erros"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Erro em {func.__name__}: {str(e)}")
            return None
    return wrapper


class ABTestingService:
    """Serviço para gerenciar testes A/B de campanhas"""
    
    def __init__(self):
        self.test_types = ['headline', 'description', 'image', 'cta', 'audience']
    
    def create_variations(self, original_content: Dict[str, Any], variation_type: str) -> List[Dict[str, Any]]:
        """Criar variações para teste A/B"""
        variations = [original_content]  # Variação A (original)
        
        if variation_type == 'headline':
            # Criar variações de título
            variations.append({
                **original_content,
                'headline': self._generate_headline_variation(original_content.get('headline', ''))
            })
            variations.append({
                **original_content,
                'headline': self._generate_headline_variation(original_content.get('headline', ''), style='urgent')
            })
        
        elif variation_type == 'description':
            # Criar variações de descrição
            variations.append({
                **original_content,
                'description': self._generate_description_variation(original_content.get('description', ''))
            })
        
        elif variation_type == 'cta':
            # Criar variações de CTA
            cta_options = [
                'Compre Agora',
                'Saiba Mais',
                'Experimente Grátis',
                'Comece Hoje',
                'Garanta o Seu',
                'Aproveite a Oferta'
            ]
            for cta in cta_options[:3]:
                variations.append({
                    **original_content,
                    'cta': cta
                })
        
        elif variation_type == 'image':
            # Sugerir diferentes estilos de imagem
            variations.append({
                **original_content,
                'image_style': 'lifestyle'
            })
            variations.append({
                **original_content,
                'image_style': 'product_focus'
            })
        
        return variations
    
    def _generate_headline_variation(self, original: str, style: str = 'benefit') -> str:
        """Gerar variação de título"""
        if style == 'urgent':
            prefixes = ['Última Chance:', 'Não Perca:', 'Oferta Limitada:', 'Hoje Apenas:']
            return f"{random.choice(prefixes)} {original}"
        elif style == 'question':
            return f"Você sabia? {original}"
        else:
            # Estilo focado em benefício
            return f"Descubra: {original}"
    
    def _generate_description_variation(self, original: str) -> str:
        """Gerar variação de descrição"""
        # Adicionar elementos de urgência ou prova social
        additions = [
            " Milhares de clientes satisfeitos!",
            " Oferta por tempo limitado.",
            " Garantia de 30 dias.",
            " Frete grátis para todo Brasil."
        ]
        return original + random.choice(additions)
    
    def analyze_test_results(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisar resultados de teste A/B"""
        variations = test_data.get('variations', [])
        
        if len(variations) < 2:
            return {'error': 'Necessário pelo menos 2 variações'}
        
        # Calcular métricas para cada variação
        results = []
        for i, variation in enumerate(variations):
            impressions = variation.get('impressions', 0)
            clicks = variation.get('clicks', 0)
            conversions = variation.get('conversions', 0)
            
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cvr = (conversions / clicks * 100) if clicks > 0 else 0
            
            results.append({
                'variation_id': i,
                'variation_name': f"Variação {chr(65 + i)}",  # A, B, C...
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'ctr': round(ctr, 2),
                'cvr': round(cvr, 2),
                'score': round(ctr * cvr, 2)
            })
        
        # Identificar vencedor
        winner = max(results, key=lambda x: x['score'])
        
        # Calcular significância estatística (simplificado)
        confidence = self._calculate_confidence(results)
        
        return {
            'results': results,
            'winner': winner,
            'confidence': confidence,
            'recommendation': self._generate_recommendation(winner, confidence),
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _calculate_confidence(self, results: List[Dict]) -> str:
        """Calcular nível de confiança estatística"""
        # Implementação simplificada
        total_impressions = sum(r['impressions'] for r in results)
        
        if total_impressions < 100:
            return 'low'
        elif total_impressions < 1000:
            return 'medium'
        else:
            return 'high'
    
    def _generate_recommendation(self, winner: Dict, confidence: str) -> str:
        """Gerar recomendação baseada nos resultados"""
        if confidence == 'high':
            return f"✅ Recomendamos usar a {winner['variation_name']} permanentemente. Ela teve {winner['score']}% melhor performance."
        elif confidence == 'medium':
            return f"⚠️ A {winner['variation_name']} está performando melhor, mas recomendamos coletar mais dados antes de decidir."
        else:
            return f"📊 Dados insuficientes. Continue o teste para obter resultados mais confiáveis."
    
    def get_test_suggestions(self, campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sugerir testes A/B para uma campanha"""
        suggestions = []
        
        # Sugerir teste de título
        suggestions.append({
            'type': 'headline',
            'priority': 'high',
            'title': 'Testar Variações de Título',
            'description': 'Títulos diferentes podem aumentar o CTR em até 50%',
            'estimated_impact': 'high'
        })
        
        # Sugerir teste de CTA
        suggestions.append({
            'type': 'cta',
            'priority': 'medium',
            'title': 'Testar Diferentes CTAs',
            'description': 'CTAs mais diretos geralmente convertem melhor',
            'estimated_impact': 'medium'
        })
        
        # Sugerir teste de imagem
        suggestions.append({
            'type': 'image',
            'priority': 'high',
            'title': 'Testar Estilos de Imagem',
            'description': 'Imagens lifestyle vs. produto podem ter resultados muito diferentes',
            'estimated_impact': 'high'
        })
        
        return suggestions
    
    def create_multivariate_test(self, elements: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Criar teste multivariado combinando múltiplos elementos"""
        # Gerar todas as combinações possíveis
        combinations = []
        
        headlines = elements.get('headlines', ['Título Padrão'])
        descriptions = elements.get('descriptions', ['Descrição Padrão'])
        ctas = elements.get('ctas', ['Saiba Mais'])
        
        for headline in headlines:
            for description in descriptions:
                for cta in ctas:
                    combinations.append({
                        'headline': headline,
                        'description': description,
                        'cta': cta
                    })
        
        return combinations[:10]  # Limitar a 10 combinações
    
    def get_winning_variations_library(self) -> List[Dict[str, Any]]:
        """Retornar biblioteca de variações vencedoras"""
        return [
            {
                'type': 'headline',
                'content': 'Transforme Seu Negócio em 30 Dias',
                'avg_ctr': 3.5,
                'tests_won': 12
            },
            {
                'type': 'headline',
                'content': 'Descubra o Segredo dos Profissionais',
                'avg_ctr': 3.2,
                'tests_won': 8
            },
            {
                'type': 'cta',
                'content': 'Comece Grátis Agora',
                'avg_cvr': 5.8,
                'tests_won': 15
            },
            {
                'type': 'cta',
                'content': 'Garantir Minha Vaga',
                'avg_cvr': 4.9,
                'tests_won': 10
            }
        ]


# Instância do serviço
ab_testing_service = ABTestingService()
