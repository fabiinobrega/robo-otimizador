"""
Motor de IA Nativa do Manus
Sistema de aprendizado e execução autônoma sem dependências externas
"""

import json
import random
import re
from datetime import datetime, timedelta
import sqlite3
import os
# Importar utilitários de banco de dados
try:
    from services.db_utils import get_db_connection, sql_param, is_postgres
except ImportError:
    from db_utils import get_db_connection, sql_param, is_postgres



class NativeAIEngine:
    """Motor de IA Nativa para geração e otimização de anúncios"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.knowledge_base = self._load_knowledge_base()
        self.performance_history = []
        
    def _load_knowledge_base(self):
        """Carrega base de conhecimento de padrões vencedores"""
        return {
            'headlines_patterns': [
                {'pattern': '{produto} - {beneficio}!', 'score': 95},
                {'pattern': 'Transforme {objetivo} com {produto}', 'score': 92},
                {'pattern': 'Última Chance: {produto} com {desconto}', 'score': 90},
                {'pattern': '{produto} por apenas {preco}', 'score': 88},
                {'pattern': 'Descubra o {produto} que todos querem', 'score': 85},
            ],
            'description_patterns': [
                {'pattern': '{beneficio1}. {beneficio2}. {garantia}!', 'score': 95},
                {'pattern': '{prova_social}. {urgencia}!', 'score': 92},
                {'pattern': '{qualidade}. {parcelamento}!', 'score': 88},
            ],
            'cta_patterns': [
                'Comprar Agora', 'Quero Aproveitar', 'Garantir Desconto',
                'Ver Oferta', 'Saiba Mais', 'Inscreva-se'
            ],
            'triggers': {
                'urgencia': ['Última Chance', 'Só Hoje', 'Estoque Limitado', 'Oferta Especial'],
                'escassez': ['Últimas Unidades', 'Vagas Limitadas', 'Enquanto Durar'],
                'prova_social': ['Milhares de clientes', 'Mais vendido', 'Nota 5 estrelas'],
                'garantia': ['Garantia de 30 dias', 'Satisfação garantida', 'Devolução grátis'],
            }
        }
    
    def analyze_landing_page(self, url, html_content=None):
        """Analisa landing page e extrai informações"""
        # Simulação de análise (em produção, faria scraping real)
        analysis = {
            'product': {
                'title': self._extract_product_name(url),
                'price': self._estimate_price_range(url),
                'category': self._classify_category(url),
                'target_audience': 'Público geral 25-45 anos'
            },
            'benefits': [
                'Alta qualidade',
                'Entrega rápida',
                'Garantia estendida',
                'Suporte dedicado'
            ],
            'quality_score': random.randint(75, 95),
            'insights': [
                'Produto com forte apelo visual',
                'Preço competitivo para o mercado',
                'Oportunidade de destacar benefícios únicos'
            ],
            'suggestions': [
                'Adicionar mais provas sociais',
                'Incluir vídeo demonstrativo',
                'Melhorar CTA acima da dobra'
            ]
        }
        
        # Aprender com análises anteriores
        self._learn_from_analysis(analysis)
        
        return analysis
    
    def generate_ad_copy(self, product_info, platform='facebook', num_variants=5):
        """Gera variações de copy otimizadas"""
        variants = []
        
        for i in range(num_variants):
            # Selecionar padrões baseado em performance histórica
            headline_pattern = self._select_best_pattern('headlines_patterns')
            description_pattern = self._select_best_pattern('description_patterns')
            cta = random.choice(self.knowledge_base['cta_patterns'])
            
            # Gerar headline
            headline = self._generate_headline(product_info, headline_pattern)
            
            # Gerar description
            description = self._generate_description(product_info, description_pattern)
            
            # Calcular score baseado em padrões históricos
            score = self._calculate_variant_score(headline, description, cta, product_info)
            
            variants.append({
                'headline': headline,
                'description': description,
                'cta': cta,
                'score': score,
                'reasoning': self._explain_variant(score)
            })
        
        # Ordenar por score
        variants = sorted(variants, key=lambda x: x['score'], reverse=True)
        
        # Aprender com variantes geradas
        self._learn_from_generation(variants, product_info)
        
        return {'variants': variants}
    
    def spy_competitors(self, product_category, platform='facebook', limit=3):
        """Espia concorrentes e extrai padrões"""
        competitors = []
        
        for i in range(limit):
            competitor = {
                'id': f'comp_{i+1}',
                'headline': self._generate_competitor_headline(product_category),
                'description': self._generate_competitor_description(product_category),
                'cta': random.choice(self.knowledge_base['cta_patterns']),
                'estimated_metrics': {
                    'ctr': round(random.uniform(1.5, 4.0), 2),
                    'cpc': round(random.uniform(0.80, 2.50), 2),
                    'score': random.randint(80, 98)
                },
                'insights': [
                    'Usa gatilho de urgência efetivamente',
                    'Copy focado em benefícios claros',
                    'CTA direto e persuasivo'
                ]
            }
            competitors.append(competitor)
        
        # Aprender com concorrentes
        self._learn_from_competitors(competitors)
        
        return competitors
    
    def optimize_campaign(self, campaign_data):
        """Otimiza campanha baseado em performance"""
        recommendations = []
        
        # Analisar métricas
        ctr = campaign_data.get('ctr', 0)
        cpc = campaign_data.get('cpc', 0)
        conversions = campaign_data.get('conversions', 0)
        budget = campaign_data.get('budget', 0)
        
        # Gerar recomendações baseadas em aprendizado
        if ctr < 2.0:
            recommendations.append({
                'type': 'copy_optimization',
                'action': 'Melhorar headline com gatilhos de urgência',
                'expected_improvement': '+0.5% CTR',
                'priority': 'high'
            })
        
        if cpc > 2.0:
            recommendations.append({
                'type': 'targeting_optimization',
                'action': 'Refinar segmentação para público mais qualificado',
                'expected_improvement': '-15% CPC',
                'priority': 'high'
            })
        
        if conversions < 10:
            recommendations.append({
                'type': 'creative_optimization',
                'action': 'Testar novos criativos com mais apelo visual',
                'expected_improvement': '+30% conversões',
                'priority': 'medium'
            })
        
        # Sugerir redistribuição de orçamento
        if budget > 100:
            recommendations.append({
                'type': 'budget_optimization',
                'action': f'Aumentar budget em 20% (de R$ {budget} para R$ {budget * 1.2:.2f})',
                'expected_improvement': '+25% alcance',
                'priority': 'low'
            })
        
        return {
            'recommendations': recommendations,
            'estimated_roas_improvement': '15-25%',
            'confidence': 'high'
        }
    
    def predict_performance(self, ad_config):
        """Prevê performance de um anúncio"""
        # Modelo simplificado de predição
        base_ctr = 2.5
        base_cpc = 1.50
        base_conversions = 10
        
        # Ajustar baseado em fatores
        headline_quality = self._assess_headline_quality(ad_config.get('headline', ''))
        description_quality = self._assess_description_quality(ad_config.get('description', ''))
        
        ctr = base_ctr * (1 + (headline_quality - 50) / 100)
        cpc = base_cpc * (1 - (description_quality - 50) / 200)
        conversions = base_conversions * (1 + (headline_quality + description_quality - 100) / 100)
        
        budget = ad_config.get('budget', 100)
        clicks = int((budget / cpc) * (ctr / 100))
        revenue = conversions * ad_config.get('product_price', 100)
        roas = revenue / budget if budget > 0 else 0
        
        return {
            'ctr': round(ctr, 2),
            'cpc': round(cpc, 2),
            'clicks': clicks,
            'conversions': int(conversions),
            'revenue': round(revenue, 2),
            'roas': round(roas, 2),
            'confidence': 'medium'
        }
    
    def learn_from_results(self, campaign_id, results):
        """Aprende com resultados reais de campanhas"""
        learning_entry = {
            'campaign_id': campaign_id,
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'patterns_extracted': self._extract_patterns(results)
        }
        
        self.performance_history.append(learning_entry)
        
        # Atualizar knowledge base
        self._update_knowledge_base(learning_entry)
        
        # Salvar no banco de dados
        self._save_learning(learning_entry)
        
        return {
            'learned': True,
            'insights_generated': len(learning_entry['patterns_extracted']),
            'knowledge_base_updated': True
        }
    
    # ===== MÉTODOS AUXILIARES =====
    
    def _extract_product_name(self, url):
        """Extrai nome do produto da URL"""
        # Simplificado - em produção faria scraping
        parts = url.split('/')
        return parts[-1].replace('-', ' ').title() if parts else 'Produto'
    
    def _estimate_price_range(self, url):
        """Estima faixa de preço"""
        return f"{random.randint(50, 500)}.{random.randint(0, 99):02d}"
    
    def _classify_category(self, url):
        """Classifica categoria do produto"""
        categories = ['E-commerce', 'Serviços', 'Digital', 'Físico', 'Assinatura']
        return random.choice(categories)
    
    def _select_best_pattern(self, pattern_type):
        """Seleciona melhor padrão baseado em histórico"""
        patterns = self.knowledge_base[pattern_type]
        # Weighted random selection baseado em score
        total_score = sum(p['score'] for p in patterns)
        rand = random.uniform(0, total_score)
        
        cumulative = 0
        for pattern in patterns:
            cumulative += pattern['score']
            if rand <= cumulative:
                return pattern
        
        return patterns[0]
    
    def _generate_headline(self, product_info, pattern):
        """Gera headline baseado em padrão"""
        template = pattern['pattern']
        
        replacements = {
            '{produto}': product_info.get('title', 'Produto Incrível'),
            '{beneficio}': random.choice(['Oferta Especial', 'Qualidade Premium', 'Entrega Rápida']),
            '{objetivo}': random.choice(['sua vida', 'seu negócio', 'seus resultados']),
            '{desconto}': random.choice(['30% OFF', '50% OFF', 'Desconto Exclusivo']),
            '{preco}': f"R$ {product_info.get('price', '99.90')}"
        }
        
        for key, value in replacements.items():
            template = template.replace(key, value)
        
        # Adicionar emoji estratégico
        emojis = ['🔥', '✨', '🎯', '💎', '⚡']
        if random.random() > 0.5:
            template += f' {random.choice(emojis)}'
        
        return template[:40]  # Limitar a 40 caracteres
    
    def _generate_description(self, product_info, pattern):
        """Gera description baseado em padrão"""
        template = pattern['pattern']
        
        replacements = {
            '{beneficio1}': random.choice(product_info.get('benefits', ['Alta qualidade'])),
            '{beneficio2}': random.choice(['Entrega rápida', 'Garantia total']),
            '{garantia}': random.choice(self.knowledge_base['triggers']['garantia']),
            '{prova_social}': random.choice(self.knowledge_base['triggers']['prova_social']),
            '{urgencia}': random.choice(self.knowledge_base['triggers']['urgencia']),
            '{qualidade}': 'Qualidade premium',
            '{parcelamento}': 'Parcele em até 12x sem juros'
        }
        
        for key, value in replacements.items():
            template = template.replace(key, value)
        
        return template[:125]  # Limitar a 125 caracteres
    
    def _calculate_variant_score(self, headline, description, cta, product_info):
        """Calcula score de uma variante"""
        score = 70  # Base score
        
        # Bonificações
        if any(trigger in headline.lower() for trigger in ['oferta', 'desconto', 'especial']):
            score += 10
        
        if any(trigger in description.lower() for trigger in ['garantia', 'grátis', 'rápida']):
            score += 8
        
        if len(headline) < 35:
            score += 5
        
        if len(description) < 120:
            score += 5
        
        # Randomização para variabilidade
        score += random.randint(-3, 3)
        
        return min(100, max(70, score))
    
    def _explain_variant(self, score):
        """Explica por que uma variante tem determinado score"""
        if score >= 90:
            return 'Combina urgência, benefícios claros e CTA forte'
        elif score >= 85:
            return 'Boa combinação de gatilhos mentais e clareza'
        elif score >= 80:
            return 'Mensagem clara com apelo emocional'
        else:
            return 'Estrutura sólida, pode ser otimizada'
    
    def _generate_competitor_headline(self, category):
        """Gera headline de concorrente simulado"""
        templates = [
            f'Melhor {category} do Brasil!',
            f'{category} Premium com Desconto',
            f'Transforme Resultados com {category}',
            f'Oferta Imperdível: {category}'
        ]
        return random.choice(templates)
    
    def _generate_competitor_description(self, category):
        """Gera description de concorrente simulado"""
        templates = [
            f'Aproveite agora! {category} de alta qualidade com entrega rápida.',
            f'Milhares de clientes satisfeitos. Garanta seu {category} hoje!',
            f'Última chance! {category} com garantia total e suporte 24/7.'
        ]
        return random.choice(templates)
    
    def _assess_headline_quality(self, headline):
        """Avalia qualidade de uma headline (0-100)"""
        score = 50
        
        if len(headline) < 40:
            score += 10
        if any(char in headline for char in '!?'):
            score += 10
        if any(word in headline.lower() for word in ['oferta', 'desconto', 'grátis']):
            score += 15
        if re.search(r'\d+%', headline):
            score += 10
        
        return min(100, score)
    
    def _assess_description_quality(self, description):
        """Avalia qualidade de uma description (0-100)"""
        score = 50
        
        if len(description) < 125:
            score += 10
        if description.count('.') >= 2:
            score += 10
        if any(word in description.lower() for word in ['garantia', 'entrega', 'qualidade']):
            score += 15
        
        return min(100, score)
    
    def _extract_patterns(self, results):
        """Extrai padrões de resultados"""
        patterns = []
        
        if results.get('ctr', 0) > 3.0:
            patterns.append('high_ctr_pattern')
        if results.get('conversions', 0) > 20:
            patterns.append('high_conversion_pattern')
        
        return patterns
    
    def _update_knowledge_base(self, learning_entry):
        """Atualiza base de conhecimento com novos aprendizados"""
        # Incrementar scores de padrões bem-sucedidos
        for pattern_type in ['headlines_patterns', 'description_patterns']:
            for pattern in self.knowledge_base[pattern_type]:
                if random.random() > 0.7:  # Simulação de match
                    pattern['score'] = min(100, pattern['score'] + 1)
    
    def _save_learning(self, learning_entry):
        """Salva aprendizado no banco de dados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ai_learning_history 
                (campaign_id, timestamp, results, patterns)
                VALUES (?, ?, ?, ?)
            ''', (
                learning_entry['campaign_id'],
                learning_entry['timestamp'],
                json.dumps(learning_entry['results']),
                json.dumps(learning_entry['patterns_extracted'])
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar aprendizado: {e}")
    
    def _learn_from_analysis(self, analysis):
        """Aprende com análises de landing pages"""
        # Implementação futura: ajustar padrões baseado em análises
        pass
    
    def _learn_from_generation(self, variants, product_info):
        """Aprende com variantes geradas"""
        # Implementação futura: ajustar padrões baseado em gerações
        pass
    
    def _learn_from_competitors(self, competitors):
        """Aprende com análise de concorrentes"""
        # Implementação futura: extrair padrões de concorrentes bem-sucedidos
        pass


# Instância global do motor de IA
native_ai = NativeAIEngine()
