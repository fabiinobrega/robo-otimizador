from functools import wraps
"""
Serviço de Inteligência de Produtos e Vendas
Análise e recomendações baseadas em dados de produtos
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random


class ProductIntelligenceService:
    """Serviço de inteligência para produtos e vendas"""
    

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


    def __init__(self, db_path='database.db'):
        self.db_path = db_path
    
    # ===== ANÁLISE DE PRODUTOS =====
    
    def analyze_product(self, product_data: Dict) -> Dict[str, Any]:
        """
        Analisa um produto e gera insights
        
        Args:
            product_data: Dados do produto
            
        Returns:
            dict: Análise e insights
        """
        product_name = product_data.get('name', 'Produto')
        category = product_data.get('category', 'Geral')
        price = product_data.get('price', 0)
        description = product_data.get('description', '')
        
        insights = []
        recommendations = []
        score = 0
        
        # Análise de preço
        if price > 0:
            if price < 50:
                insights.append('Produto de baixo ticket')
                recommendations.append('Considerar upsell ou cross-sell')
                score += 20
            elif price < 200:
                insights.append('Produto de ticket médio')
                score += 30
            else:
                insights.append('Produto de alto ticket')
                recommendations.append('Focar em qualidade e benefícios')
                score += 25
        
        # Análise de descrição
        if len(description) > 100:
            insights.append('Descrição detalhada')
            score += 20
        else:
            recommendations.append('Expandir descrição do produto')
            score += 10
        
        # Análise de categoria
        high_demand_categories = ['Eletrônicos', 'Moda', 'Beleza', 'Saúde']
        if category in high_demand_categories:
            insights.append(f'Categoria de alta demanda: {category}')
            score += 30
        
        # Gerar recomendações de marketing
        marketing_recommendations = self._generate_marketing_recommendations(
            product_name, category, price
        )
        
        return {
            'success': True,
            'product_name': product_name,
            'category': category,
            'price': price,
            'score': score,
            'insights': insights,
            'recommendations': recommendations,
            'marketing_recommendations': marketing_recommendations,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _generate_marketing_recommendations(
        self,
        product_name: str,
        category: str,
        price: float
    ) -> List[Dict]:
        """Gera recomendações de marketing"""
        
        recommendations = []
        
        # Recomendações de canais
        if price < 100:
            recommendations.append({
                'type': 'channel',
                'title': 'Facebook e Instagram',
                'description': 'Ideal para produtos de baixo/médio ticket',
                'priority': 'high'
            })
        else:
            recommendations.append({
                'type': 'channel',
                'title': 'Google Ads e LinkedIn',
                'description': 'Melhor para produtos de alto ticket',
                'priority': 'high'
            })
        
        # Recomendações de conteúdo
        recommendations.append({
            'type': 'content',
            'title': 'Vídeos demonstrativos',
            'description': f'Criar vídeos mostrando {product_name} em uso',
            'priority': 'medium'
        })
        
        recommendations.append({
            'type': 'content',
            'title': 'Depoimentos de clientes',
            'description': 'Coletar e promover avaliações positivas',
            'priority': 'medium'
        })
        
        # Recomendações de estratégia
        if price > 200:
            recommendations.append({
                'type': 'strategy',
                'title': 'Remarketing agressivo',
                'description': 'Produtos de alto ticket precisam de múltiplos touchpoints',
                'priority': 'high'
            })
        
        return recommendations
    
    # ===== ANÁLISE DE VENDAS =====
    
    def analyze_sales_data(self, period_days: int = 30) -> Dict[str, Any]:
        """
        Analisa dados de vendas
        
        Args:
            period_days: Período em dias para análise
            
        Returns:
            dict: Análise de vendas
        """
        # Dados simulados para demonstração
        sales_data = {
            'total_revenue': random.uniform(10000, 50000),
            'total_orders': random.randint(50, 200),
            'average_order_value': 0,
            'conversion_rate': random.uniform(1.5, 5.0),
            'top_products': [
                {'name': 'Produto A', 'revenue': random.uniform(2000, 8000), 'units': random.randint(20, 100)},
                {'name': 'Produto B', 'revenue': random.uniform(1500, 6000), 'units': random.randint(15, 80)},
                {'name': 'Produto C', 'revenue': random.uniform(1000, 4000), 'units': random.randint(10, 60)}
            ],
            'sales_by_channel': {
                'Facebook Ads': random.uniform(3000, 15000),
                'Google Ads': random.uniform(2500, 12000),
                'Instagram': random.uniform(2000, 10000),
                'Orgânico': random.uniform(1500, 8000)
            }
        }
        
        # Calcular AOV
        sales_data['average_order_value'] = (
            sales_data['total_revenue'] / sales_data['total_orders']
            if sales_data['total_orders'] > 0 else 0
        )
        
        # Gerar insights
        insights = []
        recommendations = []
        
        if sales_data['conversion_rate'] < 2.0:
            insights.append('Taxa de conversão abaixo da média')
            recommendations.append('Otimizar landing pages e checkout')
        elif sales_data['conversion_rate'] > 4.0:
            insights.append('Taxa de conversão excelente')
            recommendations.append('Aumentar investimento em tráfego')
        
        if sales_data['average_order_value'] < 100:
            insights.append('Ticket médio baixo')
            recommendations.append('Implementar estratégias de upsell')
        elif sales_data['average_order_value'] > 300:
            insights.append('Ticket médio alto')
            recommendations.append('Focar em retenção de clientes')
        
        # Identificar melhor canal
        best_channel = max(sales_data['sales_by_channel'].items(), key=lambda x: x[1])
        insights.append(f'Melhor canal: {best_channel[0]} (R$ {best_channel[1]:.2f})')
        recommendations.append(f'Aumentar investimento em {best_channel[0]}')
        
        return {
            'success': True,
            'period_days': period_days,
            'sales_data': sales_data,
            'insights': insights,
            'recommendations': recommendations,
            'analyzed_at': datetime.now().isoformat()
        }
    
    # ===== PREVISÃO DE VENDAS =====
    
    def forecast_sales(self, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Prevê vendas futuras
        
        Args:
            days_ahead: Dias para prever
            
        Returns:
            dict: Previsão de vendas
        """
        # Análise histórica (simulada)
        historical_avg = random.uniform(500, 2000)
        growth_rate = random.uniform(0.05, 0.20)  # 5-20% de crescimento
        
        # Calcular previsão
        forecasted_revenue = historical_avg * days_ahead * (1 + growth_rate)
        forecasted_orders = int(forecasted_revenue / 150)  # AOV médio de R$ 150
        
        # Gerar previsão diária
        daily_forecast = []
        for day in range(1, min(days_ahead + 1, 8)):  # Limitar a 7 dias para visualização
            daily_revenue = historical_avg * (1 + growth_rate * (day / days_ahead))
            daily_forecast.append({
                'day': day,
                'date': (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d'),
                'forecasted_revenue': round(daily_revenue, 2),
                'forecasted_orders': int(daily_revenue / 150)
            })
        
        # Gerar insights
        insights = []
        if growth_rate > 0.15:
            insights.append('Crescimento acelerado previsto')
        elif growth_rate > 0.10:
            insights.append('Crescimento saudável previsto')
        else:
            insights.append('Crescimento moderado previsto')
        
        return {
            'success': True,
            'days_ahead': days_ahead,
            'forecasted_revenue': round(forecasted_revenue, 2),
            'forecasted_orders': forecasted_orders,
            'growth_rate': round(growth_rate * 100, 1),
            'daily_forecast': daily_forecast,
            'insights': insights,
            'generated_at': datetime.now().isoformat()
        }
    
    # ===== RECOMENDAÇÕES DE PRODUTOS =====
    
    def recommend_products_for_campaign(
        self,
        campaign_objective: str,
        budget: float
    ) -> Dict[str, Any]:
        """
        Recomenda produtos para uma campanha
        
        Args:
            campaign_objective: Objetivo da campanha
            budget: Orçamento disponível
            
        Returns:
            dict: Produtos recomendados
        """
        # Produtos simulados
        all_products = [
            {
                'id': 1,
                'name': 'Produto Premium A',
                'category': 'Eletrônicos',
                'price': 299.90,
                'margin': 0.35,
                'conversion_rate': 3.5,
                'score': 0
            },
            {
                'id': 2,
                'name': 'Produto Best-Seller B',
                'category': 'Moda',
                'price': 89.90,
                'margin': 0.45,
                'conversion_rate': 5.2,
                'score': 0
            },
            {
                'id': 3,
                'name': 'Produto Novo C',
                'category': 'Beleza',
                'price': 149.90,
                'margin': 0.40,
                'conversion_rate': 2.8,
                'score': 0
            },
            {
                'id': 4,
                'name': 'Produto Promocional D',
                'category': 'Casa',
                'price': 49.90,
                'margin': 0.25,
                'conversion_rate': 6.5,
                'score': 0
            }
        ]
        
        # Calcular score baseado no objetivo
        for product in all_products:
            score = 0
            
            if campaign_objective == 'conversions':
                # Priorizar conversão
                score += product['conversion_rate'] * 15
                score += product['margin'] * 50
            elif campaign_objective == 'revenue':
                # Priorizar receita
                score += product['price'] / 10
                score += product['margin'] * 40
            elif campaign_objective == 'awareness':
                # Priorizar produtos populares
                score += product['conversion_rate'] * 10
                score += (300 - product['price']) / 10  # Produtos mais baratos
            else:
                # Score balanceado
                score += product['conversion_rate'] * 10
                score += product['margin'] * 30
                score += product['price'] / 20
            
            product['score'] = round(score, 1)
        
        # Ordenar por score
        all_products.sort(key=lambda x: x['score'], reverse=True)
        
        # Selecionar top produtos que cabem no orçamento
        recommended = []
        estimated_cpa = 30  # CPA estimado
        
        for product in all_products[:3]:
            estimated_conversions = (budget / estimated_cpa) * (product['conversion_rate'] / 100)
            estimated_revenue = estimated_conversions * product['price']
            estimated_profit = estimated_revenue * product['margin'] - budget
            
            recommended.append({
                **product,
                'estimated_conversions': round(estimated_conversions, 1),
                'estimated_revenue': round(estimated_revenue, 2),
                'estimated_profit': round(estimated_profit, 2),
                'roi': round((estimated_profit / budget) * 100, 1) if budget > 0 else 0
            })
        
        return {
            'success': True,
            'campaign_objective': campaign_objective,
            'budget': budget,
            'recommended_products': recommended,
            'total_estimated_revenue': sum(p['estimated_revenue'] for p in recommended),
            'total_estimated_profit': sum(p['estimated_profit'] for p in recommended),
            'generated_at': datetime.now().isoformat()
        }
    
    # ===== ANÁLISE DE CONCORRÊNCIA =====
    
    def analyze_competitor_products(self, product_name: str) -> Dict[str, Any]:
        """
        Analisa produtos concorrentes
        
        Args:
            product_name: Nome do produto
            
        Returns:
            dict: Análise de concorrência
        """
        # Dados simulados de concorrentes
        competitors = [
            {
                'name': 'Concorrente A',
                'price': random.uniform(80, 150),
                'rating': random.uniform(3.5, 5.0),
                'reviews': random.randint(50, 500),
                'features': random.randint(5, 15)
            },
            {
                'name': 'Concorrente B',
                'price': random.uniform(90, 180),
                'rating': random.uniform(3.8, 4.9),
                'reviews': random.randint(100, 800),
                'features': random.randint(6, 18)
            },
            {
                'name': 'Concorrente C',
                'price': random.uniform(70, 140),
                'rating': random.uniform(3.2, 4.7),
                'reviews': random.randint(30, 400),
                'features': random.randint(4, 12)
            }
        ]
        
        # Calcular médias
        avg_price = sum(c['price'] for c in competitors) / len(competitors)
        avg_rating = sum(c['rating'] for c in competitors) / len(competitors)
        avg_reviews = sum(c['reviews'] for c in competitors) / len(competitors)
        
        # Gerar insights
        insights = []
        recommendations = []
        
        insights.append(f'Preço médio do mercado: R$ {avg_price:.2f}')
        insights.append(f'Avaliação média: {avg_rating:.1f} estrelas')
        insights.append(f'Média de avaliações: {int(avg_reviews)} reviews')
        
        recommendations.append('Monitorar preços dos concorrentes semanalmente')
        recommendations.append('Coletar mais avaliações de clientes')
        recommendations.append('Destacar diferenciais competitivos')
        
        return {
            'success': True,
            'product_name': product_name,
            'competitors': competitors,
            'market_averages': {
                'price': round(avg_price, 2),
                'rating': round(avg_rating, 1),
                'reviews': int(avg_reviews)
            },
            'insights': insights,
            'recommendations': recommendations,
            'analyzed_at': datetime.now().isoformat()
        }
    
    # ===== RELATÓRIO COMPLETO =====
    
    def generate_intelligence_report(self) -> Dict[str, Any]:
        """Gera relatório completo de inteligência"""
        
        sales_analysis = self.analyze_sales_data(30)
        sales_forecast = self.forecast_sales(30)
        
        return {
            'success': True,
            'sales_analysis': sales_analysis,
            'sales_forecast': sales_forecast,
            'summary': {
                'current_revenue': sales_analysis['sales_data']['total_revenue'],
                'forecasted_revenue': sales_forecast['forecasted_revenue'],
                'growth_rate': sales_forecast['growth_rate'],
                'top_recommendations': [
                    sales_analysis['recommendations'][0] if sales_analysis['recommendations'] else 'N/A',
                    'Focar em produtos de alta margem',
                    'Expandir canais de vendas'
                ]
            },
            'generated_at': datetime.now().isoformat()
        }


# Instância global
product_intelligence = ProductIntelligenceService()
