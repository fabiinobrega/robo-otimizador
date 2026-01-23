"""
Ad Advanced Features - Funcionalidades avançadas de criação de anúncios
Implementa as funcionalidades 29, 30, 34, 37, 38 do sistema NEXORA
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class AdAdvancedFeatures:
    """Funcionalidades avançadas para criação de anúncios"""
    
    def __init__(self):
        self.optimization_history = []
        self.alignment_checks = []
        self.clarity_validations = []
        self.creative_performance = {}
        
    # ========================================
    # 29. Otimização por objetivo
    # ========================================
    def optimize_by_objective(self, ad_data: Dict, objective: str) -> Dict:
        """
        Otimiza anúncio baseado no objetivo de campanha
        Objetivos: conversao, awareness, engajamento, trafego, leads
        """
        optimization_rules = {
            'conversao': {
                'cta_style': 'urgente',
                'copy_focus': 'beneficios_diretos',
                'headline_type': 'resultado',
                'visual_emphasis': 'produto',
                'recommended_format': 'carrossel'
            },
            'awareness': {
                'cta_style': 'suave',
                'copy_focus': 'historia_marca',
                'headline_type': 'emocional',
                'visual_emphasis': 'lifestyle',
                'recommended_format': 'video'
            },
            'engajamento': {
                'cta_style': 'interativo',
                'copy_focus': 'perguntas',
                'headline_type': 'curiosidade',
                'visual_emphasis': 'pessoas',
                'recommended_format': 'imagem_unica'
            },
            'trafego': {
                'cta_style': 'claro',
                'copy_focus': 'proposta_valor',
                'headline_type': 'informativo',
                'visual_emphasis': 'destaque',
                'recommended_format': 'link_post'
            },
            'leads': {
                'cta_style': 'formulario',
                'copy_focus': 'oferta_gratuita',
                'headline_type': 'beneficio',
                'visual_emphasis': 'lead_magnet',
                'recommended_format': 'lead_form'
            }
        }
        
        rules = optimization_rules.get(objective, optimization_rules['conversao'])
        
        optimized_ad = ad_data.copy()
        optimized_ad['optimization'] = {
            'objective': objective,
            'applied_rules': rules,
            'recommendations': self._generate_objective_recommendations(objective, rules),
            'score': self._calculate_objective_alignment_score(ad_data, rules)
        }
        
        self.optimization_history.append({
            'objective': objective,
            'original_ad': ad_data,
            'optimized_ad': optimized_ad,
            'timestamp': datetime.now().isoformat()
        })
        
        return optimized_ad
    
    def _generate_objective_recommendations(self, objective: str, rules: Dict) -> List[str]:
        """Gera recomendações baseadas no objetivo"""
        recommendations = []
        
        if objective == 'conversao':
            recommendations = [
                'Use CTA com senso de urgência (ex: "Compre Agora")',
                'Destaque benefícios diretos e resultados',
                'Inclua prova social (depoimentos, números)',
                'Use cores que chamem atenção no CTA'
            ]
        elif objective == 'awareness':
            recommendations = [
                'Conte uma história envolvente sobre a marca',
                'Use vídeos de alta qualidade',
                'Foque em valores e missão da empresa',
                'Evite CTAs muito agressivos'
            ]
        elif objective == 'engajamento':
            recommendations = [
                'Faça perguntas para estimular comentários',
                'Use imagens com pessoas reais',
                'Crie conteúdo compartilhável',
                'Responda rapidamente aos comentários'
            ]
        elif objective == 'trafego':
            recommendations = [
                'Deixe claro o que o usuário encontrará no site',
                'Use preview atraente do conteúdo',
                'Otimize para cliques com headlines curiosas',
                'Garanta que a landing page seja relevante'
            ]
        elif objective == 'leads':
            recommendations = [
                'Ofereça algo de valor gratuito',
                'Minimize campos do formulário',
                'Destaque a oferta claramente',
                'Use prova social para aumentar confiança'
            ]
        
        return recommendations
    
    def _calculate_objective_alignment_score(self, ad_data: Dict, rules: Dict) -> float:
        """Calcula score de alinhamento com o objetivo"""
        score = 70.0  # Base score
        
        # Verificar elementos do anúncio
        if ad_data.get('cta'):
            score += 10
        if ad_data.get('headline'):
            score += 10
        if ad_data.get('visual'):
            score += 10
            
        return min(score, 100.0)
    
    # ========================================
    # 30. Alinhamento com página de vendas
    # ========================================
    def check_landing_page_alignment(self, ad_data: Dict, landing_page_data: Dict) -> Dict:
        """
        Verifica alinhamento entre anúncio e página de vendas
        Garante consistência de mensagem e experiência
        """
        alignment_report = {
            'is_aligned': True,
            'alignment_score': 100.0,
            'issues': [],
            'recommendations': [],
            'checks': {}
        }
        
        # 1. Verificar consistência de headline
        ad_headline = ad_data.get('headline', '').lower()
        page_headline = landing_page_data.get('headline', '').lower()
        
        headline_similarity = self._calculate_text_similarity(ad_headline, page_headline)
        alignment_report['checks']['headline_consistency'] = {
            'score': headline_similarity,
            'status': 'ok' if headline_similarity > 0.5 else 'warning'
        }
        
        if headline_similarity < 0.5:
            alignment_report['issues'].append('Headlines do anúncio e página são muito diferentes')
            alignment_report['recommendations'].append('Alinhe a headline do anúncio com a da página')
            alignment_report['alignment_score'] -= 20
        
        # 2. Verificar consistência de oferta
        ad_offer = ad_data.get('offer', '').lower()
        page_offer = landing_page_data.get('offer', '').lower()
        
        if ad_offer and page_offer:
            offer_match = ad_offer in page_offer or page_offer in ad_offer
            alignment_report['checks']['offer_consistency'] = {
                'score': 100 if offer_match else 50,
                'status': 'ok' if offer_match else 'warning'
            }
            
            if not offer_match:
                alignment_report['issues'].append('Oferta do anúncio não corresponde à da página')
                alignment_report['recommendations'].append('Garanta que a oferta seja idêntica')
                alignment_report['alignment_score'] -= 25
        
        # 3. Verificar consistência visual
        ad_colors = ad_data.get('colors', [])
        page_colors = landing_page_data.get('colors', [])
        
        if ad_colors and page_colors:
            color_match = len(set(ad_colors) & set(page_colors)) / max(len(ad_colors), 1)
            alignment_report['checks']['visual_consistency'] = {
                'score': color_match * 100,
                'status': 'ok' if color_match > 0.5 else 'warning'
            }
            
            if color_match < 0.5:
                alignment_report['issues'].append('Cores do anúncio diferem muito da página')
                alignment_report['recommendations'].append('Use paleta de cores consistente')
                alignment_report['alignment_score'] -= 15
        
        # 4. Verificar CTA consistency
        ad_cta = ad_data.get('cta', '').lower()
        page_cta = landing_page_data.get('cta', '').lower()
        
        if ad_cta and page_cta:
            cta_match = self._calculate_text_similarity(ad_cta, page_cta) > 0.6
            alignment_report['checks']['cta_consistency'] = {
                'score': 100 if cta_match else 60,
                'status': 'ok' if cta_match else 'warning'
            }
            
            if not cta_match:
                alignment_report['issues'].append('CTA do anúncio difere do CTA da página')
                alignment_report['alignment_score'] -= 10
        
        alignment_report['is_aligned'] = alignment_report['alignment_score'] >= 70
        
        self.alignment_checks.append({
            'ad_data': ad_data,
            'landing_page_data': landing_page_data,
            'report': alignment_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return alignment_report
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade entre dois textos"""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    # ========================================
    # 34. Validação de clareza
    # ========================================
    def validate_clarity(self, ad_data: Dict) -> Dict:
        """
        Valida clareza do anúncio
        Verifica se a mensagem é clara e compreensível
        """
        clarity_report = {
            'is_clear': True,
            'clarity_score': 100.0,
            'issues': [],
            'recommendations': [],
            'metrics': {}
        }
        
        headline = ad_data.get('headline', '')
        copy = ad_data.get('copy', '')
        cta = ad_data.get('cta', '')
        
        # 1. Verificar tamanho da headline
        headline_words = len(headline.split()) if headline else 0
        clarity_report['metrics']['headline_words'] = headline_words
        
        if headline_words > 10:
            clarity_report['issues'].append('Headline muito longa')
            clarity_report['recommendations'].append('Reduza headline para máximo 10 palavras')
            clarity_report['clarity_score'] -= 15
        elif headline_words < 3:
            clarity_report['issues'].append('Headline muito curta')
            clarity_report['recommendations'].append('Headline deve ter pelo menos 3 palavras')
            clarity_report['clarity_score'] -= 10
        
        # 2. Verificar complexidade do copy
        if copy:
            avg_word_length = sum(len(w) for w in copy.split()) / max(len(copy.split()), 1)
            clarity_report['metrics']['avg_word_length'] = avg_word_length
            
            if avg_word_length > 8:
                clarity_report['issues'].append('Copy usa palavras muito complexas')
                clarity_report['recommendations'].append('Use palavras mais simples e diretas')
                clarity_report['clarity_score'] -= 15
        
        # 3. Verificar CTA
        if cta:
            cta_words = len(cta.split())
            clarity_report['metrics']['cta_words'] = cta_words
            
            if cta_words > 5:
                clarity_report['issues'].append('CTA muito longo')
                clarity_report['recommendations'].append('CTA deve ter 2-4 palavras')
                clarity_report['clarity_score'] -= 10
        else:
            clarity_report['issues'].append('CTA ausente')
            clarity_report['recommendations'].append('Adicione um CTA claro')
            clarity_report['clarity_score'] -= 20
        
        # 4. Verificar uso de jargões
        jargons = ['sinergia', 'paradigma', 'disruptivo', 'escalável', 'holístico']
        text_lower = (headline + ' ' + copy).lower()
        
        found_jargons = [j for j in jargons if j in text_lower]
        if found_jargons:
            clarity_report['issues'].append(f'Uso de jargões: {", ".join(found_jargons)}')
            clarity_report['recommendations'].append('Evite jargões corporativos')
            clarity_report['clarity_score'] -= 10 * len(found_jargons)
        
        # 5. Verificar proposta de valor clara
        value_indicators = ['você', 'seu', 'sua', 'ganhe', 'economize', 'aprenda', 'descubra']
        has_value_proposition = any(ind in text_lower for ind in value_indicators)
        
        if not has_value_proposition:
            clarity_report['issues'].append('Proposta de valor não clara')
            clarity_report['recommendations'].append('Destaque o benefício para o usuário')
            clarity_report['clarity_score'] -= 15
        
        clarity_report['is_clear'] = clarity_report['clarity_score'] >= 70
        clarity_report['clarity_score'] = max(0, clarity_report['clarity_score'])
        
        self.clarity_validations.append({
            'ad_data': ad_data,
            'report': clarity_report,
            'timestamp': datetime.now().isoformat()
        })
        
        return clarity_report
    
    # ========================================
    # 37. Escala de criativos vencedores
    # ========================================
    def scale_winning_creatives(self, creatives: List[Dict], performance_threshold: float = 2.0) -> Dict:
        """
        Identifica e escala criativos vencedores
        Threshold: ROAS mínimo para considerar vencedor
        """
        scaling_report = {
            'winners': [],
            'losers': [],
            'neutral': [],
            'scaling_recommendations': [],
            'total_analyzed': len(creatives)
        }
        
        for creative in creatives:
            creative_id = creative.get('id', 'unknown')
            roas = creative.get('roas', 0)
            ctr = creative.get('ctr', 0)
            spend = creative.get('spend', 0)
            
            # Classificar criativo
            if roas >= performance_threshold and ctr >= 1.0:
                scaling_report['winners'].append({
                    'id': creative_id,
                    'roas': roas,
                    'ctr': ctr,
                    'spend': spend,
                    'scaling_factor': self._calculate_scaling_factor(roas, ctr),
                    'recommended_budget_increase': self._calculate_budget_increase(roas, spend)
                })
            elif roas < 1.0:
                scaling_report['losers'].append({
                    'id': creative_id,
                    'roas': roas,
                    'ctr': ctr,
                    'recommendation': 'pausar'
                })
            else:
                scaling_report['neutral'].append({
                    'id': creative_id,
                    'roas': roas,
                    'ctr': ctr,
                    'recommendation': 'monitorar'
                })
        
        # Gerar recomendações de escala
        if scaling_report['winners']:
            total_increase = sum(w['recommended_budget_increase'] for w in scaling_report['winners'])
            scaling_report['scaling_recommendations'] = [
                f"Escalar {len(scaling_report['winners'])} criativos vencedores",
                f"Aumento total recomendado de orçamento: R$ {total_increase:.2f}",
                "Manter monitoramento diário de performance",
                "Criar variações dos criativos vencedores"
            ]
        
        # Registrar performance
        for winner in scaling_report['winners']:
            self.creative_performance[winner['id']] = {
                'status': 'winner',
                'roas': winner['roas'],
                'last_update': datetime.now().isoformat()
            }
        
        return scaling_report
    
    def _calculate_scaling_factor(self, roas: float, ctr: float) -> float:
        """Calcula fator de escala baseado em performance"""
        base_factor = 1.0
        
        if roas >= 3.0:
            base_factor += 0.5
        if roas >= 5.0:
            base_factor += 0.5
        if ctr >= 2.0:
            base_factor += 0.3
        if ctr >= 3.0:
            base_factor += 0.2
        
        return min(base_factor, 3.0)  # Máximo 3x
    
    def _calculate_budget_increase(self, roas: float, current_spend: float) -> float:
        """Calcula aumento de orçamento recomendado"""
        if roas >= 5.0:
            return current_spend * 1.0  # Dobrar
        elif roas >= 3.0:
            return current_spend * 0.5  # +50%
        elif roas >= 2.0:
            return current_spend * 0.3  # +30%
        return current_spend * 0.2  # +20%
    
    # ========================================
    # 38. Pausa de criativos ruins
    # ========================================
    def pause_bad_creatives(self, creatives: List[Dict], min_spend: float = 50.0) -> Dict:
        """
        Identifica e pausa criativos com performance ruim
        min_spend: gasto mínimo para avaliar (evitar pausar muito cedo)
        """
        pause_report = {
            'to_pause': [],
            'to_monitor': [],
            'healthy': [],
            'total_analyzed': len(creatives),
            'potential_savings': 0
        }
        
        for creative in creatives:
            creative_id = creative.get('id', 'unknown')
            roas = creative.get('roas', 0)
            ctr = creative.get('ctr', 0)
            spend = creative.get('spend', 0)
            conversions = creative.get('conversions', 0)
            
            # Verificar se tem dados suficientes
            if spend < min_spend:
                pause_report['to_monitor'].append({
                    'id': creative_id,
                    'reason': 'Dados insuficientes',
                    'spend': spend,
                    'min_required': min_spend
                })
                continue
            
            # Critérios para pausar
            should_pause = False
            pause_reasons = []
            
            if roas < 0.5:
                should_pause = True
                pause_reasons.append(f'ROAS muito baixo ({roas:.2f})')
            
            if ctr < 0.3:
                should_pause = True
                pause_reasons.append(f'CTR muito baixo ({ctr:.2f}%)')
            
            if spend > 100 and conversions == 0:
                should_pause = True
                pause_reasons.append('Sem conversões após R$100 gastos')
            
            if should_pause:
                pause_report['to_pause'].append({
                    'id': creative_id,
                    'reasons': pause_reasons,
                    'roas': roas,
                    'ctr': ctr,
                    'spend': spend,
                    'projected_daily_waste': spend / max(creative.get('days_running', 1), 1)
                })
                pause_report['potential_savings'] += spend / max(creative.get('days_running', 1), 1)
            else:
                pause_report['healthy'].append({
                    'id': creative_id,
                    'roas': roas,
                    'ctr': ctr
                })
        
        # Atualizar registro de performance
        for bad_creative in pause_report['to_pause']:
            self.creative_performance[bad_creative['id']] = {
                'status': 'paused',
                'reasons': bad_creative['reasons'],
                'last_update': datetime.now().isoformat()
            }
        
        return pause_report
    
    def get_creative_performance_summary(self) -> Dict:
        """Retorna resumo de performance dos criativos"""
        winners = sum(1 for v in self.creative_performance.values() if v.get('status') == 'winner')
        paused = sum(1 for v in self.creative_performance.values() if v.get('status') == 'paused')
        
        return {
            'total_tracked': len(self.creative_performance),
            'winners': winners,
            'paused': paused,
            'optimization_history': len(self.optimization_history),
            'alignment_checks': len(self.alignment_checks),
            'clarity_validations': len(self.clarity_validations)
        }


# Instância global
ad_advanced_features = AdAdvancedFeatures()
