"""
UX & Scale Features - Funcionalidades de UX e Escala
Implementa as funcionalidades 47, 48, 85 do sistema NEXORA
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class UXScaleFeatures:
    """Funcionalidades de UX e Escala para o sistema NEXORA"""
    
    def __init__(self):
        self.coherence_checks = []
        self.friction_analyses = []
        self.scale_simulations = []
        
    # ========================================
    # 47. Coerência anúncio → página
    # ========================================
    def check_ad_page_coherence(self, ad_data: Dict, page_data: Dict) -> Dict:
        """
        Verifica coerência completa entre anúncio e página
        Analisa mensagem, visual, promessa e experiência
        """
        coherence_report = {
            'is_coherent': True,
            'coherence_score': 100.0,
            'dimensions': {},
            'issues': [],
            'recommendations': []
        }
        
        # 1. Coerência de Mensagem
        message_score = self._check_message_coherence(ad_data, page_data)
        coherence_report['dimensions']['message'] = {
            'score': message_score,
            'status': 'ok' if message_score >= 70 else 'warning'
        }
        if message_score < 70:
            coherence_report['issues'].append('Mensagem do anúncio não reflete na página')
            coherence_report['recommendations'].append('Alinhe a mensagem principal do anúncio com a headline da página')
        
        # 2. Coerência Visual
        visual_score = self._check_visual_coherence(ad_data, page_data)
        coherence_report['dimensions']['visual'] = {
            'score': visual_score,
            'status': 'ok' if visual_score >= 70 else 'warning'
        }
        if visual_score < 70:
            coherence_report['issues'].append('Identidade visual inconsistente')
            coherence_report['recommendations'].append('Use mesma paleta de cores e estilo visual')
        
        # 3. Coerência de Promessa
        promise_score = self._check_promise_coherence(ad_data, page_data)
        coherence_report['dimensions']['promise'] = {
            'score': promise_score,
            'status': 'ok' if promise_score >= 70 else 'warning'
        }
        if promise_score < 70:
            coherence_report['issues'].append('Promessa do anúncio não é cumprida na página')
            coherence_report['recommendations'].append('Garanta que a oferta do anúncio esteja claramente visível na página')
        
        # 4. Coerência de Experiência
        experience_score = self._check_experience_coherence(ad_data, page_data)
        coherence_report['dimensions']['experience'] = {
            'score': experience_score,
            'status': 'ok' if experience_score >= 70 else 'warning'
        }
        if experience_score < 70:
            coherence_report['issues'].append('Experiência do usuário é inconsistente')
            coherence_report['recommendations'].append('Otimize a jornada do clique até a conversão')
        
        # Calcular score final
        scores = [d['score'] for d in coherence_report['dimensions'].values()]
        coherence_report['coherence_score'] = sum(scores) / len(scores) if scores else 0
        coherence_report['is_coherent'] = coherence_report['coherence_score'] >= 70
        
        self.coherence_checks.append({
            'ad_data': ad_data,
            'page_data': page_data,
            'report': coherence_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return coherence_report
    
    def _check_message_coherence(self, ad_data: Dict, page_data: Dict) -> float:
        """Verifica coerência de mensagem"""
        ad_headline = ad_data.get('headline', '').lower()
        page_headline = page_data.get('headline', '').lower()
        ad_copy = ad_data.get('copy', '').lower()
        page_copy = page_data.get('main_copy', '').lower()
        
        score = 50.0  # Base
        
        # Verificar palavras-chave em comum
        ad_words = set(ad_headline.split() + ad_copy.split())
        page_words = set(page_headline.split() + page_copy.split())
        
        common_words = ad_words & page_words
        if len(common_words) > 5:
            score += 30
        elif len(common_words) > 2:
            score += 15
        
        # Verificar tom similar
        if self._detect_tone(ad_headline) == self._detect_tone(page_headline):
            score += 20
        
        return min(score, 100)
    
    def _check_visual_coherence(self, ad_data: Dict, page_data: Dict) -> float:
        """Verifica coerência visual"""
        score = 60.0  # Base
        
        ad_colors = set(ad_data.get('colors', []))
        page_colors = set(page_data.get('colors', []))
        
        if ad_colors and page_colors:
            common_colors = ad_colors & page_colors
            if len(common_colors) >= 2:
                score += 25
            elif len(common_colors) >= 1:
                score += 15
        
        # Verificar estilo
        if ad_data.get('style') == page_data.get('style'):
            score += 15
        
        return min(score, 100)
    
    def _check_promise_coherence(self, ad_data: Dict, page_data: Dict) -> float:
        """Verifica coerência de promessa"""
        score = 50.0  # Base
        
        ad_offer = ad_data.get('offer', '').lower()
        page_offers = page_data.get('offers', [])
        
        if ad_offer:
            for offer in page_offers:
                if ad_offer in offer.lower() or offer.lower() in ad_offer:
                    score += 40
                    break
        
        # Verificar preço consistente
        ad_price = ad_data.get('price')
        page_price = page_data.get('price')
        
        if ad_price and page_price and ad_price == page_price:
            score += 10
        
        return min(score, 100)
    
    def _check_experience_coherence(self, ad_data: Dict, page_data: Dict) -> float:
        """Verifica coerência de experiência"""
        score = 60.0  # Base
        
        # Verificar CTA consistente
        ad_cta = ad_data.get('cta', '').lower()
        page_cta = page_data.get('primary_cta', '').lower()
        
        if ad_cta and page_cta:
            if ad_cta in page_cta or page_cta in ad_cta:
                score += 25
        
        # Verificar tempo de carregamento
        page_load_time = page_data.get('load_time', 5)
        if page_load_time < 3:
            score += 15
        elif page_load_time > 5:
            score -= 20
        
        return max(min(score, 100), 0)
    
    def _detect_tone(self, text: str) -> str:
        """Detecta tom do texto"""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ['urgente', 'agora', 'última', 'limitado']):
            return 'urgente'
        elif any(w in text_lower for w in ['descubra', 'aprenda', 'conheça']):
            return 'educativo'
        elif any(w in text_lower for w in ['grátis', 'oferta', 'desconto']):
            return 'promocional'
        else:
            return 'neutro'
    
    # ========================================
    # 48. UX sem fricção
    # ========================================
    def analyze_friction(self, page_data: Dict, user_flow: List[Dict]) -> Dict:
        """
        Analisa pontos de fricção na experiência do usuário
        Identifica e sugere correções para melhorar conversão
        """
        friction_report = {
            'friction_score': 0,  # 0 = sem fricção, 100 = muita fricção
            'friction_points': [],
            'recommendations': [],
            'estimated_conversion_impact': 0
        }
        
        # 1. Analisar tempo de carregamento
        load_time = page_data.get('load_time', 3)
        if load_time > 3:
            friction_report['friction_points'].append({
                'type': 'load_time',
                'severity': 'high' if load_time > 5 else 'medium',
                'description': f'Página leva {load_time}s para carregar',
                'impact': -15 if load_time > 5 else -8
            })
            friction_report['friction_score'] += 20 if load_time > 5 else 10
        
        # 2. Analisar formulários
        form_fields = page_data.get('form_fields', 0)
        if form_fields > 5:
            friction_report['friction_points'].append({
                'type': 'form_complexity',
                'severity': 'high' if form_fields > 8 else 'medium',
                'description': f'Formulário com {form_fields} campos',
                'impact': -20 if form_fields > 8 else -10
            })
            friction_report['friction_score'] += 25 if form_fields > 8 else 15
        
        # 3. Analisar etapas do checkout
        checkout_steps = page_data.get('checkout_steps', 1)
        if checkout_steps > 2:
            friction_report['friction_points'].append({
                'type': 'checkout_steps',
                'severity': 'medium',
                'description': f'Checkout com {checkout_steps} etapas',
                'impact': -5 * (checkout_steps - 2)
            })
            friction_report['friction_score'] += 10 * (checkout_steps - 2)
        
        # 4. Analisar distrações
        distractions = page_data.get('distractions', [])
        if distractions:
            friction_report['friction_points'].append({
                'type': 'distractions',
                'severity': 'low',
                'description': f'{len(distractions)} elementos distrativos',
                'impact': -3 * len(distractions)
            })
            friction_report['friction_score'] += 5 * len(distractions)
        
        # 5. Analisar fluxo do usuário
        for step in user_flow:
            if step.get('drop_off_rate', 0) > 30:
                friction_report['friction_points'].append({
                    'type': 'high_drop_off',
                    'severity': 'high',
                    'description': f"Alta taxa de abandono em '{step.get('name', 'etapa')}'",
                    'impact': -step.get('drop_off_rate', 0) / 5
                })
                friction_report['friction_score'] += 15
        
        # 6. Analisar mobile experience
        if not page_data.get('mobile_optimized', True):
            friction_report['friction_points'].append({
                'type': 'mobile_issues',
                'severity': 'high',
                'description': 'Página não otimizada para mobile',
                'impact': -25
            })
            friction_report['friction_score'] += 30
        
        # Gerar recomendações
        friction_report['recommendations'] = self._generate_friction_recommendations(
            friction_report['friction_points']
        )
        
        # Calcular impacto estimado na conversão
        friction_report['estimated_conversion_impact'] = sum(
            fp.get('impact', 0) for fp in friction_report['friction_points']
        )
        
        # Normalizar score
        friction_report['friction_score'] = min(friction_report['friction_score'], 100)
        
        self.friction_analyses.append({
            'page_data': page_data,
            'report': friction_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return friction_report
    
    def _generate_friction_recommendations(self, friction_points: List[Dict]) -> List[str]:
        """Gera recomendações para reduzir fricção"""
        recommendations = []
        
        for fp in friction_points:
            if fp['type'] == 'load_time':
                recommendations.append('Otimize imagens e use lazy loading')
                recommendations.append('Implemente cache e CDN')
            elif fp['type'] == 'form_complexity':
                recommendations.append('Reduza campos do formulário para o mínimo necessário')
                recommendations.append('Use preenchimento automático quando possível')
            elif fp['type'] == 'checkout_steps':
                recommendations.append('Considere checkout em uma única página')
                recommendations.append('Adicione barra de progresso')
            elif fp['type'] == 'distractions':
                recommendations.append('Remova elementos que não contribuem para conversão')
                recommendations.append('Simplifique o design da página')
            elif fp['type'] == 'high_drop_off':
                recommendations.append('Analise e otimize a etapa com alta taxa de abandono')
                recommendations.append('Adicione elementos de confiança (selos, depoimentos)')
            elif fp['type'] == 'mobile_issues':
                recommendations.append('Implemente design responsivo')
                recommendations.append('Teste em múltiplos dispositivos móveis')
        
        return list(set(recommendations))  # Remove duplicatas
    
    # ========================================
    # 85. Modo Escala Bilionária
    # ========================================
    def simulate_billion_scale(self, campaign_data: Dict, target_scale: str = '1B') -> Dict:
        """
        Simula escala bilionária para campanhas
        Analisa capacidade de escalar para alto volume
        """
        scale_multipliers = {
            '10M': 10,
            '100M': 100,
            '500M': 500,
            '1B': 1000,
            '10B': 10000
        }
        
        multiplier = scale_multipliers.get(target_scale, 1000)
        current_spend = campaign_data.get('daily_spend', 1000)
        current_conversions = campaign_data.get('daily_conversions', 100)
        current_roas = campaign_data.get('roas', 2.0)
        
        simulation_report = {
            'target_scale': target_scale,
            'current_metrics': {
                'daily_spend': current_spend,
                'daily_conversions': current_conversions,
                'roas': current_roas
            },
            'projected_metrics': {},
            'scalability_score': 0,
            'bottlenecks': [],
            'requirements': [],
            'risk_factors': [],
            'timeline_estimate': ''
        }
        
        # Projetar métricas em escala
        projected_spend = current_spend * multiplier
        
        # Aplicar degradação de performance em escala (realista)
        roas_degradation = 1 - (0.1 * (multiplier / 100))  # 10% degradação por 100x
        roas_degradation = max(roas_degradation, 0.5)  # Mínimo 50% do ROAS original
        
        projected_roas = current_roas * roas_degradation
        projected_conversions = current_conversions * multiplier * roas_degradation
        projected_revenue = projected_spend * projected_roas
        
        simulation_report['projected_metrics'] = {
            'daily_spend': projected_spend,
            'daily_conversions': projected_conversions,
            'projected_roas': projected_roas,
            'projected_daily_revenue': projected_revenue,
            'roas_degradation': f'{(1 - roas_degradation) * 100:.1f}%'
        }
        
        # Identificar gargalos
        bottlenecks = []
        
        # 1. Gargalo de audiência
        audience_size = campaign_data.get('audience_size', 1000000)
        required_audience = projected_conversions * 1000  # Estimativa
        
        if required_audience > audience_size:
            bottlenecks.append({
                'type': 'audience',
                'description': 'Audiência insuficiente para escala',
                'current': audience_size,
                'required': required_audience,
                'severity': 'critical'
            })
        
        # 2. Gargalo de criativos
        creative_count = campaign_data.get('active_creatives', 5)
        required_creatives = max(20, multiplier / 10)
        
        if creative_count < required_creatives:
            bottlenecks.append({
                'type': 'creatives',
                'description': 'Poucos criativos para escala',
                'current': creative_count,
                'required': int(required_creatives),
                'severity': 'high'
            })
        
        # 3. Gargalo de orçamento
        if projected_spend > campaign_data.get('max_budget', float('inf')):
            bottlenecks.append({
                'type': 'budget',
                'description': 'Orçamento máximo insuficiente',
                'current': campaign_data.get('max_budget', 0),
                'required': projected_spend,
                'severity': 'critical'
            })
        
        # 4. Gargalo de infraestrutura
        if projected_conversions > 10000:
            bottlenecks.append({
                'type': 'infrastructure',
                'description': 'Infraestrutura pode não suportar volume',
                'current': 'Verificar capacidade',
                'required': f'{projected_conversions:.0f} conversões/dia',
                'severity': 'medium'
            })
        
        simulation_report['bottlenecks'] = bottlenecks
        
        # Calcular score de escalabilidade
        critical_bottlenecks = sum(1 for b in bottlenecks if b['severity'] == 'critical')
        high_bottlenecks = sum(1 for b in bottlenecks if b['severity'] == 'high')
        
        scalability_score = 100 - (critical_bottlenecks * 30) - (high_bottlenecks * 15)
        simulation_report['scalability_score'] = max(0, scalability_score)
        
        # Gerar requisitos
        simulation_report['requirements'] = [
            f"Orçamento diário de R$ {projected_spend:,.2f}",
            f"Mínimo de {int(required_creatives)} criativos ativos",
            f"Audiência de pelo menos {required_audience:,.0f} pessoas",
            "Infraestrutura de alta disponibilidade",
            "Equipe dedicada de monitoramento",
            "Sistema de alerta em tempo real"
        ]
        
        # Fatores de risco
        simulation_report['risk_factors'] = [
            f"Degradação de ROAS estimada em {(1 - roas_degradation) * 100:.1f}%",
            "Saturação de audiência em mercados menores",
            "Aumento de CPM devido à competição",
            "Necessidade de diversificação de canais",
            "Risco de fadiga criativa"
        ]
        
        # Estimativa de timeline
        if scalability_score >= 80:
            simulation_report['timeline_estimate'] = '3-6 meses para atingir escala'
        elif scalability_score >= 50:
            simulation_report['timeline_estimate'] = '6-12 meses com otimizações necessárias'
        else:
            simulation_report['timeline_estimate'] = '12+ meses - requer mudanças significativas'
        
        self.scale_simulations.append({
            'campaign_data': campaign_data,
            'report': simulation_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return simulation_report
    
    def get_scale_readiness_certification(self, campaign_data: Dict) -> Dict:
        """
        Certifica prontidão para escala
        Retorna certificação com nível e recomendações
        """
        simulation = self.simulate_billion_scale(campaign_data, '100M')
        
        certification = {
            'certified': simulation['scalability_score'] >= 70,
            'level': '',
            'score': simulation['scalability_score'],
            'bottlenecks_count': len(simulation['bottlenecks']),
            'certification_date': datetime.now().isoformat(),
            'valid_until': '',
            'recommendations': []
        }
        
        if simulation['scalability_score'] >= 90:
            certification['level'] = 'PLATINUM - Pronto para Escala Bilionária'
        elif simulation['scalability_score'] >= 80:
            certification['level'] = 'GOLD - Pronto para Escala de 100M+'
        elif simulation['scalability_score'] >= 70:
            certification['level'] = 'SILVER - Pronto para Escala de 10M+'
        elif simulation['scalability_score'] >= 50:
            certification['level'] = 'BRONZE - Escala limitada, melhorias necessárias'
        else:
            certification['level'] = 'NÃO CERTIFICADO - Requer otimizações significativas'
        
        # Recomendações baseadas em gargalos
        for bottleneck in simulation['bottlenecks']:
            if bottleneck['type'] == 'audience':
                certification['recommendations'].append('Expandir audiências com lookalikes')
            elif bottleneck['type'] == 'creatives':
                certification['recommendations'].append('Criar mais variações de criativos')
            elif bottleneck['type'] == 'budget':
                certification['recommendations'].append('Aumentar limite de orçamento')
            elif bottleneck['type'] == 'infrastructure':
                certification['recommendations'].append('Escalar infraestrutura de backend')
        
        return certification
    
    def get_summary(self) -> Dict:
        """Retorna resumo das análises realizadas"""
        return {
            'coherence_checks': len(self.coherence_checks),
            'friction_analyses': len(self.friction_analyses),
            'scale_simulations': len(self.scale_simulations),
            'avg_coherence_score': sum(
                c['report']['coherence_score'] for c in self.coherence_checks
            ) / max(len(self.coherence_checks), 1),
            'avg_friction_score': sum(
                f['report']['friction_score'] for f in self.friction_analyses
            ) / max(len(self.friction_analyses), 1)
        }


# Instância global
ux_scale_features = UXScaleFeatures()
