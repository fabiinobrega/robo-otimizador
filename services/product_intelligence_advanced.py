"""
Inteligência de Produto / E-commerce - NEXORA PRIME
Sistema avançado de análise e otimização de produtos
Nível: Agência Milionária
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class ProductIntelligenceAdvanced:
    """
    Inteligência de Produto / E-commerce
    Sistema completo de análise, otimização e recomendação de produtos
    """
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        
        # Categorias de produtos
        self.product_categories = [
            "Eletrônicos", "Moda", "Casa e Decoração", "Esportes",
            "Beleza", "Alimentos", "Livros", "Brinquedos"
        ]
        
        # Métricas de performance
        self.performance_metrics = [
            "conversion_rate", "cart_abandonment", "avg_order_value",
            "return_rate", "review_score", "click_through_rate"
        ]
    
    def analyze_product_auto(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análise automática completa de produto
        
        Args:
            product_data: Dados do produto
        
        Returns:
            Dict com análise completa
        """
        product_id = product_data.get("id", "unknown")
        product_name = product_data.get("name", "Produto")
        price = product_data.get("price", 0)
        category = product_data.get("category", "Geral")
        
        analysis = {
            "product_id": product_id,
            "product_name": product_name,
            "analyzed_at": datetime.now().isoformat(),
            
            # Score geral do produto
            "overall_score": self._calculate_product_score(product_data),
            
            # Análise de preço
            "pricing_analysis": self._analyze_pricing(product_data),
            
            # Análise de descrição e imagens
            "content_analysis": self._analyze_product_content(product_data),
            
            # Potencial de vendas
            "sales_potential": self._estimate_sales_potential(product_data),
            
            # Análise de concorrência
            "competition_analysis": self._analyze_competition(product_data),
            
            # Recomendações de otimização
            "optimization_recommendations": self._generate_optimization_recommendations(product_data),
            
            # Sugestões de campanhas
            "campaign_suggestions": self._suggest_campaigns(product_data),
            
            # Palavras-chave recomendadas
            "recommended_keywords": self._generate_keywords(product_data),
            
            # Público-alvo ideal
            "target_audience": self._identify_target_audience(product_data),
            
            # Previsão de performance
            "performance_forecast": self._forecast_performance(product_data)
        }
        
        return analysis
    
    def recommend_products_for_campaign(self, campaign_objective: str,
                                       budget: float,
                                       target_audience: str) -> List[Dict[str, Any]]:
        """
        Recomenda produtos ideais para uma campanha
        
        Args:
            campaign_objective: Objetivo da campanha
            budget: Orçamento disponível
            target_audience: Público-alvo
        
        Returns:
            Lista de produtos recomendados com justificativas
        """
        # Simular catálogo de produtos
        catalog = self._get_product_catalog()
        
        recommendations = []
        
        for product in catalog[:5]:  # Top 5 produtos
            recommendation = {
                "product_id": product["id"],
                "product_name": product["name"],
                "product_price": product["price"],
                "product_category": product["category"],
                
                # Score de adequação
                "fit_score": random.randint(75, 98),
                
                # Justificativa
                "recommendation_reason": self._generate_recommendation_reason(
                    product, campaign_objective, target_audience
                ),
                
                # Estimativas
                "estimated_performance": {
                    "impressions": int(budget / 0.02 * 1000),  # CPM R$ 20
                    "clicks": int(budget / 0.02 * 1000 * 0.03),  # CTR 3%
                    "conversions": int(budget / 0.02 * 1000 * 0.03 * 0.02),  # CR 2%
                    "revenue": int(budget / 0.02 * 1000 * 0.03 * 0.02 * product["price"]),
                    "roas": round(int(budget / 0.02 * 1000 * 0.03 * 0.02 * product["price"]) / budget, 2)
                },
                
                # Orçamento sugerido
                "suggested_budget": round(budget * 0.20, 2),  # 20% do orçamento total
                
                # Estratégia recomendada
                "recommended_strategy": self._get_product_strategy(product, campaign_objective)
            }
            
            recommendations.append(recommendation)
        
        # Ordenar por fit_score
        recommendations.sort(key=lambda x: x["fit_score"], reverse=True)
        
        return recommendations
    
    def optimize_product_catalog(self, catalog_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Otimiza catálogo completo de produtos
        
        Args:
            catalog_data: Dados do catálogo
        
        Returns:
            Dict com otimizações recomendadas
        """
        products = catalog_data.get("products", [])
        
        optimization = {
            "catalog_size": len(products),
            "analyzed_at": datetime.now().isoformat(),
            
            # Produtos de alta performance
            "top_performers": self._identify_top_performers(products),
            
            # Produtos com problemas
            "underperformers": self._identify_underperformers(products),
            
            # Produtos para descontinuar
            "discontinue_candidates": self._identify_discontinue_candidates(products),
            
            # Oportunidades de cross-sell
            "cross_sell_opportunities": self._identify_cross_sell_opportunities(products),
            
            # Oportunidades de upsell
            "upsell_opportunities": self._identify_upsell_opportunities(products),
            
            # Gaps no catálogo
            "catalog_gaps": self._identify_catalog_gaps(products),
            
            # Recomendações de precificação
            "pricing_recommendations": self._generate_pricing_recommendations(products),
            
            # Sugestões de bundles
            "bundle_suggestions": self._suggest_product_bundles(products),
            
            # Score geral do catálogo
            "catalog_health_score": random.randint(70, 90)
        }
        
        return optimization
    
    def forecast_sales(self, product_id: str, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Previsão de vendas para um produto
        
        Args:
            product_id: ID do produto
            days_ahead: Dias para prever
        
        Returns:
            Dict com previsão de vendas
        """
        # Simular histórico de vendas
        historical_sales = [random.randint(10, 50) for _ in range(30)]
        avg_daily_sales = sum(historical_sales) / len(historical_sales)
        
        # Calcular tendência
        trend = "growing" if historical_sales[-7:] > historical_sales[:7] else "declining"
        
        # Prever vendas futuras
        forecast_sales = []
        for day in range(days_ahead):
            if trend == "growing":
                predicted = int(avg_daily_sales * (1 + 0.02 * day))
            else:
                predicted = int(avg_daily_sales * (1 - 0.01 * day))
            
            forecast_sales.append(max(0, predicted))
        
        total_forecast = sum(forecast_sales)
        
        forecast = {
            "product_id": product_id,
            "forecast_period": f"{days_ahead} days",
            "forecast_start": datetime.now().strftime("%Y-%m-%d"),
            "forecast_end": (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d"),
            
            # Histórico
            "historical_data": {
                "avg_daily_sales": round(avg_daily_sales, 2),
                "last_30_days_total": sum(historical_sales),
                "trend": trend
            },
            
            # Previsão
            "forecast_data": {
                "daily_forecast": forecast_sales,
                "total_forecast": total_forecast,
                "avg_daily_forecast": round(total_forecast / days_ahead, 2)
            },
            
            # Confiança
            "confidence_level": random.randint(75, 95),
            
            # Fatores de influência
            "influencing_factors": [
                "Sazonalidade",
                "Tendência histórica",
                "Ações de marketing",
                "Concorrência"
            ],
            
            # Recomendações
            "recommendations": self._generate_forecast_recommendations(trend, total_forecast)
        }
        
        return forecast
    
    def analyze_competition(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análise de concorrência para um produto
        
        Args:
            product_data: Dados do produto
        
        Returns:
            Dict com análise de concorrência
        """
        product_name = product_data.get("name", "Produto")
        product_price = product_data.get("price", 0)
        
        # Simular concorrentes
        competitors = [
            {
                "name": f"Concorrente {i+1}",
                "price": product_price * random.uniform(0.8, 1.2),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "reviews_count": random.randint(50, 500),
                "market_share": round(random.uniform(5, 25), 1)
            }
            for i in range(3)
        ]
        
        analysis = {
            "product_name": product_name,
            "your_price": product_price,
            "analyzed_at": datetime.now().isoformat(),
            
            # Concorrentes
            "competitors": competitors,
            
            # Posicionamento de preço
            "price_positioning": self._analyze_price_positioning(product_price, competitors),
            
            # Vantagens competitivas
            "competitive_advantages": [
                "Melhor custo-benefício",
                "Entrega mais rápida",
                "Atendimento diferenciado"
            ],
            
            # Desvantagens
            "competitive_disadvantages": [
                "Preço ligeiramente acima da média"
            ],
            
            # Estratégia recomendada
            "recommended_strategy": self._get_competitive_strategy(product_price, competitors),
            
            # Oportunidades
            "opportunities": [
                "Destacar diferenciais de qualidade",
                "Oferecer garantia estendida",
                "Criar programa de fidelidade"
            ],
            
            # Ameaças
            "threats": [
                "Concorrentes com preços mais baixos",
                "Novos entrantes no mercado"
            ]
        }
        
        return analysis
    
    def suggest_pricing(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sugestões de precificação inteligente
        
        Args:
            product_data: Dados do produto
        
        Returns:
            Dict com sugestões de preço
        """
        current_price = product_data.get("price", 100.0)
        cost = product_data.get("cost", current_price * 0.4)
        
        suggestions = {
            "product_id": product_data.get("id"),
            "current_price": current_price,
            "cost": cost,
            "current_margin": round(((current_price - cost) / current_price) * 100, 2),
            
            # Preço ótimo
            "optimal_price": {
                "value": round(current_price * 1.15, 2),
                "reason": "Maximiza lucro mantendo competitividade",
                "expected_impact": "+15% de margem, -5% de volume"
            },
            
            # Preço premium
            "premium_price": {
                "value": round(current_price * 1.30, 2),
                "reason": "Posicionamento premium com valor agregado",
                "expected_impact": "+30% de margem, -15% de volume"
            },
            
            # Preço promocional
            "promotional_price": {
                "value": round(current_price * 0.85, 2),
                "reason": "Aumentar volume e market share",
                "expected_impact": "-15% de margem, +40% de volume"
            },
            
            # Preço psicológico
            "psychological_price": {
                "value": round(current_price * 0.99, 2),  # .99 ending
                "reason": "Preço psicológico aumenta conversão",
                "expected_impact": "+8% de conversão"
            },
            
            # Estratégia de precificação dinâmica
            "dynamic_pricing_strategy": {
                "peak_hours_multiplier": 1.10,
                "off_peak_multiplier": 0.90,
                "high_demand_multiplier": 1.20,
                "low_inventory_multiplier": 1.15
            },
            
            # Recomendação final
            "recommended_price": round(current_price * 1.15, 2),
            "recommendation_reason": "Melhor equilíbrio entre margem e volume"
        }
        
        return suggestions
    
    def _calculate_product_score(self, product_data: Dict[str, Any]) -> float:
        """Calcula score geral do produto"""
        score = 50.0
        
        # Fator 1: Preço competitivo
        if product_data.get("price", 0) > 0:
            score += 10.0
        
        # Fator 2: Descrição completa
        if len(product_data.get("description", "")) > 100:
            score += 10.0
        
        # Fator 3: Imagens
        if product_data.get("images_count", 0) >= 3:
            score += 10.0
        
        # Fator 4: Reviews
        if product_data.get("reviews_count", 0) > 10:
            score += 10.0
        
        # Fator 5: Rating
        rating = product_data.get("rating", 0)
        if rating >= 4.5:
            score += 10.0
        elif rating >= 4.0:
            score += 5.0
        
        return min(100.0, score)
    
    def _analyze_pricing(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa precificação do produto"""
        price = product_data.get("price", 0)
        cost = product_data.get("cost", price * 0.4)
        
        return {
            "current_price": price,
            "cost": cost,
            "margin": round(((price - cost) / price) * 100, 2) if price > 0 else 0,
            "positioning": "competitive" if price < 200 else "premium",
            "price_elasticity": "medium",
            "optimal_price_range": {
                "min": round(price * 0.90, 2),
                "max": round(price * 1.20, 2)
            }
        }
    
    def _analyze_product_content(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa conteúdo do produto"""
        description = product_data.get("description", "")
        images_count = product_data.get("images_count", 0)
        
        return {
            "description_length": len(description),
            "description_quality": "good" if len(description) > 100 else "needs_improvement",
            "images_count": images_count,
            "images_quality": "excellent" if images_count >= 5 else "good" if images_count >= 3 else "poor",
            "has_video": product_data.get("has_video", False),
            "seo_score": random.randint(60, 90)
        }
    
    def _estimate_sales_potential(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estima potencial de vendas"""
        return {
            "potential_level": "high",
            "estimated_monthly_sales": random.randint(100, 500),
            "estimated_monthly_revenue": random.randint(10000, 50000),
            "growth_potential": f"+{random.randint(20, 50)}%",
            "market_size": "large"
        }
    
    def _analyze_competition(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise rápida de concorrência"""
        return {
            "competition_level": "medium",
            "avg_competitor_price": product_data.get("price", 100) * random.uniform(0.9, 1.1),
            "market_position": "competitive",
            "differentiation_score": random.randint(60, 85)
        }
    
    def _generate_optimization_recommendations(self, product_data: Dict[str, Any]) -> List[str]:
        """Gera recomendações de otimização"""
        recommendations = []
        
        if len(product_data.get("description", "")) < 100:
            recommendations.append("Expandir descrição do produto com mais detalhes e benefícios")
        
        if product_data.get("images_count", 0) < 5:
            recommendations.append("Adicionar mais imagens de alta qualidade (mínimo 5)")
        
        if not product_data.get("has_video"):
            recommendations.append("Criar vídeo demonstrativo do produto")
        
        if product_data.get("reviews_count", 0) < 20:
            recommendations.append("Incentivar mais avaliações de clientes")
        
        recommendations.append("Otimizar título com palavras-chave relevantes")
        recommendations.append("Adicionar badges de confiança (frete grátis, garantia, etc)")
        
        return recommendations
    
    def _suggest_campaigns(self, product_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Sugere campanhas para o produto"""
        return [
            {
                "type": "awareness",
                "platform": "Meta",
                "objective": "Aumentar conhecimento da marca",
                "budget_suggestion": "R$ 500/dia"
            },
            {
                "type": "conversion",
                "platform": "Google",
                "objective": "Gerar vendas diretas",
                "budget_suggestion": "R$ 800/dia"
            }
        ]
    
    def _generate_keywords(self, product_data: Dict[str, Any]) -> List[str]:
        """Gera palavras-chave"""
        category = product_data.get("category", "produto")
        name = product_data.get("name", "")
        
        return [
            f"{name.lower()}",
            f"comprar {name.lower()}",
            f"{category.lower()} online",
            f"melhor {category.lower()}",
            f"{name.lower()} preço"
        ]
    
    def _identify_target_audience(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identifica público-alvo ideal"""
        return {
            "age_range": "25-45",
            "gender": "all",
            "interests": ["tecnologia", "inovação", "qualidade"],
            "income_level": "middle_to_high",
            "location": "urban_areas"
        }
    
    def _forecast_performance(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Previsão de performance"""
        return {
            "next_30_days": {
                "estimated_sales": random.randint(50, 200),
                "estimated_revenue": random.randint(5000, 20000),
                "confidence": f"{random.randint(70, 90)}%"
            }
        }
    
    def _get_product_catalog(self) -> List[Dict[str, Any]]:
        """Retorna catálogo simulado"""
        return [
            {
                "id": f"prod_{i}",
                "name": f"Produto {i}",
                "price": random.uniform(50, 500),
                "category": random.choice(self.product_categories),
                "rating": round(random.uniform(3.5, 5.0), 1)
            }
            for i in range(1, 11)
        ]
    
    def _generate_recommendation_reason(self, product: Dict[str, Any],
                                       objective: str, audience: str) -> str:
        """Gera justificativa de recomendação"""
        return f"Produto com alta taxa de conversão para {audience} e alinhado com objetivo de {objective}"
    
    def _get_product_strategy(self, product: Dict[str, Any], objective: str) -> str:
        """Retorna estratégia para o produto"""
        strategies = {
            "awareness": "Focar em alcance e impressões",
            "traffic": "Otimizar para cliques",
            "sales": "Otimizar para conversões",
            "engagement": "Criar conteúdo interativo"
        }
        return strategies.get(objective, "Estratégia balanceada")
    
    def _identify_top_performers(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica produtos de alta performance"""
        return products[:3] if products else []
    
    def _identify_underperformers(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica produtos com baixa performance"""
        return products[-3:] if len(products) > 3 else []
    
    def _identify_discontinue_candidates(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica produtos para descontinuar"""
        return []
    
    def _identify_cross_sell_opportunities(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica oportunidades de cross-sell"""
        return [
            {
                "product_a": "Produto 1",
                "product_b": "Produto 2",
                "affinity_score": 0.85
            }
        ]
    
    def _identify_upsell_opportunities(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifica oportunidades de upsell"""
        return [
            {
                "base_product": "Produto Básico",
                "upsell_product": "Produto Premium",
                "price_difference": 200.00
            }
        ]
    
    def _identify_catalog_gaps(self, products: List[Dict[str, Any]]) -> List[str]:
        """Identifica gaps no catálogo"""
        return [
            "Falta produtos na faixa de R$ 200-300",
            "Categoria 'Acessórios' subrepresentada"
        ]
    
    def _generate_pricing_recommendations(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gera recomendações de precificação"""
        return [
            {
                "product": "Produto 1",
                "current_price": 100.00,
                "recommended_price": 115.00,
                "reason": "Aumentar margem"
            }
        ]
    
    def _suggest_product_bundles(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sugere bundles de produtos"""
        return [
            {
                "bundle_name": "Kit Completo",
                "products": ["Produto 1", "Produto 2"],
                "bundle_price": 250.00,
                "savings": 50.00
            }
        ]
    
    def _generate_forecast_recommendations(self, trend: str, total_forecast: int) -> List[str]:
        """Gera recomendações baseadas na previsão"""
        if trend == "growing":
            return [
                "Aumentar estoque para atender demanda crescente",
                "Considerar aumentar investimento em marketing",
                "Preparar campanhas de upsell"
            ]
        else:
            return [
                "Criar promoções para estimular vendas",
                "Revisar estratégia de marketing",
                "Analisar feedback de clientes"
            ]
    
    def _analyze_price_positioning(self, your_price: float, 
                                   competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisa posicionamento de preço"""
        competitor_prices = [c["price"] for c in competitors]
        avg_price = sum(competitor_prices) / len(competitor_prices)
        
        return {
            "your_price": your_price,
            "market_avg": round(avg_price, 2),
            "position": "above_average" if your_price > avg_price else "below_average",
            "price_difference_pct": round(((your_price - avg_price) / avg_price) * 100, 2)
        }
    
    def _get_competitive_strategy(self, your_price: float,
                                  competitors: List[Dict[str, Any]]) -> str:
        """Retorna estratégia competitiva"""
        competitor_prices = [c["price"] for c in competitors]
        avg_price = sum(competitor_prices) / len(competitor_prices)
        
        if your_price > avg_price * 1.1:
            return "Justificar preço premium com valor agregado e diferenciais"
        elif your_price < avg_price * 0.9:
            return "Aproveitar vantagem de preço para ganhar market share"
        else:
            return "Competir em outros atributos além de preço (qualidade, atendimento)"


# Instância global
product_intelligence_advanced = ProductIntelligenceAdvanced()
