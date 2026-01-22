"""
GEO INTELLIGENCE - Geolocalizacao Inteligente
Otimizacao geografica de campanhas com dados de mercado
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

class GeoIntelligence:
    """Sistema de geolocalizacao inteligente."""
    
    def __init__(self):
        self.name = "Geo Intelligence"
        self.version = "2.0.0"
        
        # Dados de regioes do Brasil
        self.brazil_regions = {
            "sudeste": {
                "states": ["SP", "RJ", "MG", "ES"],
                "population_share": 0.42,
                "gdp_share": 0.55,
                "digital_maturity": "high",
                "avg_cpc_multiplier": 1.2
            },
            "sul": {
                "states": ["PR", "SC", "RS"],
                "population_share": 0.14,
                "gdp_share": 0.17,
                "digital_maturity": "high",
                "avg_cpc_multiplier": 1.1
            },
            "nordeste": {
                "states": ["BA", "PE", "CE", "MA", "PB", "RN", "AL", "SE", "PI"],
                "population_share": 0.27,
                "gdp_share": 0.14,
                "digital_maturity": "medium",
                "avg_cpc_multiplier": 0.8
            },
            "centro_oeste": {
                "states": ["GO", "MT", "MS", "DF"],
                "population_share": 0.08,
                "gdp_share": 0.10,
                "digital_maturity": "medium-high",
                "avg_cpc_multiplier": 1.0
            },
            "norte": {
                "states": ["AM", "PA", "RO", "AC", "AP", "RR", "TO"],
                "population_share": 0.09,
                "gdp_share": 0.06,
                "digital_maturity": "medium-low",
                "avg_cpc_multiplier": 0.7
            }
        }
        
        # Dados de estados
        self.state_data = {
            "SP": {"name": "Sao Paulo", "population": 46000000, "capital": "Sao Paulo", "tier": 1},
            "RJ": {"name": "Rio de Janeiro", "population": 17400000, "capital": "Rio de Janeiro", "tier": 1},
            "MG": {"name": "Minas Gerais", "population": 21300000, "capital": "Belo Horizonte", "tier": 1},
            "BA": {"name": "Bahia", "population": 14900000, "capital": "Salvador", "tier": 2},
            "PR": {"name": "Parana", "population": 11500000, "capital": "Curitiba", "tier": 1},
            "RS": {"name": "Rio Grande do Sul", "population": 11400000, "capital": "Porto Alegre", "tier": 1},
            "PE": {"name": "Pernambuco", "population": 9600000, "capital": "Recife", "tier": 2},
            "CE": {"name": "Ceara", "population": 9200000, "capital": "Fortaleza", "tier": 2},
            "SC": {"name": "Santa Catarina", "population": 7300000, "capital": "Florianopolis", "tier": 1},
            "GO": {"name": "Goias", "population": 7100000, "capital": "Goiania", "tier": 2},
            "DF": {"name": "Distrito Federal", "population": 3100000, "capital": "Brasilia", "tier": 1},
            "ES": {"name": "Espirito Santo", "population": 4100000, "capital": "Vitoria", "tier": 2}
        }
        
        # Dados de cidades principais
        self.city_data = {
            "sao_paulo": {"state": "SP", "population": 12300000, "tier": 1, "ecommerce_index": 95},
            "rio_de_janeiro": {"state": "RJ", "population": 6700000, "tier": 1, "ecommerce_index": 88},
            "brasilia": {"state": "DF", "population": 3100000, "tier": 1, "ecommerce_index": 85},
            "salvador": {"state": "BA", "population": 2900000, "tier": 2, "ecommerce_index": 72},
            "fortaleza": {"state": "CE", "population": 2700000, "tier": 2, "ecommerce_index": 70},
            "belo_horizonte": {"state": "MG", "population": 2500000, "tier": 1, "ecommerce_index": 82},
            "manaus": {"state": "AM", "population": 2200000, "tier": 2, "ecommerce_index": 65},
            "curitiba": {"state": "PR", "population": 1900000, "tier": 1, "ecommerce_index": 85},
            "recife": {"state": "PE", "population": 1600000, "tier": 2, "ecommerce_index": 75},
            "porto_alegre": {"state": "RS", "population": 1500000, "tier": 1, "ecommerce_index": 83}
        }
        
        # Cache de analises
        self.analysis_cache = {}
    
    def analyze_geo_performance(self, campaign_data: Dict) -> Dict[str, Any]:
        """Analisa performance geografica de uma campanha."""
        
        geo_metrics = campaign_data.get("geo_metrics", {})
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_data.get("campaign_id"),
            "regions_analysis": {},
            "top_performers": [],
            "underperformers": [],
            "opportunities": [],
            "recommendations": []
        }
        
        # Analisar cada regiao
        for region, data in geo_metrics.items():
            spend = data.get("spend", 0)
            conversions = data.get("conversions", 0)
            revenue = data.get("revenue", 0)
            
            cpa = spend / conversions if conversions > 0 else 0
            roas = revenue / spend if spend > 0 else 0
            
            region_analysis = {
                "spend": round(spend, 2),
                "conversions": conversions,
                "revenue": round(revenue, 2),
                "cpa": round(cpa, 2),
                "roas": round(roas, 2),
                "efficiency_score": self._calculate_geo_efficiency(cpa, roas, campaign_data.get("target_cpa", cpa))
            }
            
            analysis["regions_analysis"][region] = region_analysis
            
            # Classificar performance
            if roas >= 2.5:
                analysis["top_performers"].append({"region": region, "roas": roas, "cpa": cpa})
            elif roas < 1.5:
                analysis["underperformers"].append({"region": region, "roas": roas, "cpa": cpa})
        
        # Identificar oportunidades
        analysis["opportunities"] = self._identify_geo_opportunities(analysis["regions_analysis"])
        
        # Gerar recomendacoes
        analysis["recommendations"] = self._generate_geo_recommendations(analysis)
        
        return analysis
    
    def get_geo_recommendations(self, niche: str, budget: float, objective: str = "conversions") -> Dict[str, Any]:
        """Obtem recomendacoes geograficas para um nicho."""
        
        recommendations = {
            "timestamp": datetime.now().isoformat(),
            "niche": niche,
            "budget": budget,
            "objective": objective,
            "recommended_regions": [],
            "budget_allocation": {},
            "targeting_strategy": {}
        }
        
        # Recomendacoes por nicho
        niche_geo_affinity = {
            "ecommerce": ["sudeste", "sul", "centro_oeste"],
            "infoprodutos": ["sudeste", "sul", "nordeste"],
            "servicos_locais": ["sudeste", "sul"],
            "saas": ["sudeste", "sul", "centro_oeste"],
            "dropshipping": ["sudeste", "sul", "nordeste"]
        }
        
        recommended = niche_geo_affinity.get(niche.lower(), ["sudeste", "sul"])
        
        # Calcular alocacao de orcamento
        total_weight = sum(self.brazil_regions[r]["gdp_share"] for r in recommended if r in self.brazil_regions)
        
        for region in recommended:
            if region in self.brazil_regions:
                region_data = self.brazil_regions[region]
                weight = region_data["gdp_share"] / total_weight if total_weight > 0 else 1 / len(recommended)
                allocated = budget * weight
                
                recommendations["recommended_regions"].append({
                    "region": region,
                    "states": region_data["states"],
                    "digital_maturity": region_data["digital_maturity"],
                    "expected_cpc_multiplier": region_data["avg_cpc_multiplier"]
                })
                
                recommendations["budget_allocation"][region] = {
                    "amount": round(allocated, 2),
                    "percentage": round(weight * 100, 1)
                }
        
        # Estrategia de targeting
        recommendations["targeting_strategy"] = {
            "primary_regions": recommended[:2],
            "expansion_regions": recommended[2:] if len(recommended) > 2 else [],
            "exclude_regions": [r for r in self.brazil_regions if r not in recommended],
            "city_targeting": self._get_top_cities_for_niche(niche)
        }
        
        return recommendations
    
    def optimize_geo_targeting(self, campaign_id: str, current_targeting: Dict, performance_data: Dict) -> Dict[str, Any]:
        """Otimiza targeting geografico baseado em performance."""
        
        optimizations = {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
            "current_targeting": current_targeting,
            "recommended_changes": [],
            "expected_impact": {}
        }
        
        # Analisar performance por regiao
        for region, metrics in performance_data.items():
            roas = metrics.get("roas", 0)
            spend = metrics.get("spend", 0)
            
            if roas < 1.0 and spend > 100:
                optimizations["recommended_changes"].append({
                    "action": "reduce_budget",
                    "region": region,
                    "reason": f"ROAS baixo ({roas:.2f})",
                    "suggested_reduction": "50%"
                })
            elif roas > 3.0:
                optimizations["recommended_changes"].append({
                    "action": "increase_budget",
                    "region": region,
                    "reason": f"ROAS alto ({roas:.2f})",
                    "suggested_increase": "30%"
                })
        
        # Calcular impacto esperado
        if optimizations["recommended_changes"]:
            optimizations["expected_impact"] = {
                "estimated_roas_improvement": "15-25%",
                "estimated_cpa_reduction": "10-20%",
                "confidence": "medium"
            }
        
        return optimizations
    
    def get_city_insights(self, city: str) -> Dict[str, Any]:
        """Obtem insights sobre uma cidade."""
        
        city_key = city.lower().replace(" ", "_")
        
        if city_key not in self.city_data:
            return {"error": f"Cidade '{city}' nao encontrada"}
        
        city_info = self.city_data[city_key]
        state_info = self.state_data.get(city_info["state"], {})
        
        return {
            "timestamp": datetime.now().isoformat(),
            "city": city,
            "state": city_info["state"],
            "state_name": state_info.get("name", ""),
            "population": city_info["population"],
            "tier": city_info["tier"],
            "ecommerce_index": city_info["ecommerce_index"],
            "advertising_insights": {
                "competition_level": "high" if city_info["tier"] == 1 else "medium",
                "expected_cpc": "acima da media" if city_info["tier"] == 1 else "na media",
                "audience_quality": "alta" if city_info["ecommerce_index"] > 80 else "media",
                "best_times": ["12:00-14:00", "19:00-22:00"],
                "recommended_budget_share": f"{min(30, city_info['ecommerce_index'] / 3):.0f}%"
            },
            "recommendations": self._get_city_recommendations(city_key, city_info)
        }
    
    def get_regional_benchmarks(self, region: str) -> Dict[str, Any]:
        """Obtem benchmarks regionais."""
        
        if region not in self.brazil_regions:
            return {"error": f"Regiao '{region}' nao encontrada"}
        
        region_data = self.brazil_regions[region]
        
        # Benchmarks simulados (em producao viriam de dados reais)
        benchmarks = {
            "timestamp": datetime.now().isoformat(),
            "region": region,
            "states": region_data["states"],
            "market_data": {
                "population_share": f"{region_data['population_share'] * 100:.1f}%",
                "gdp_share": f"{region_data['gdp_share'] * 100:.1f}%",
                "digital_maturity": region_data["digital_maturity"]
            },
            "advertising_benchmarks": {
                "avg_cpc": round(1.50 * region_data["avg_cpc_multiplier"], 2),
                "avg_cpm": round(15.00 * region_data["avg_cpc_multiplier"], 2),
                "avg_ctr": round(1.2 / region_data["avg_cpc_multiplier"], 2),
                "avg_conversion_rate": round(2.5 / region_data["avg_cpc_multiplier"], 2)
            },
            "competition_analysis": {
                "level": "high" if region in ["sudeste", "sul"] else "medium",
                "main_sectors": self._get_region_main_sectors(region),
                "growth_trend": "stable" if region == "sudeste" else "growing"
            }
        }
        
        return benchmarks
    
    def create_geo_strategy(self, config: Dict) -> Dict[str, Any]:
        """Cria estrategia geografica completa."""
        
        niche = config.get("niche", "ecommerce")
        budget = config.get("budget", 1000)
        objective = config.get("objective", "conversions")
        expansion_phase = config.get("expansion_phase", "initial")
        
        strategy = {
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "phases": []
        }
        
        # Fase 1: Mercados principais
        phase1 = {
            "phase": 1,
            "name": "Mercados Principais",
            "duration": "2-4 semanas",
            "budget_share": 0.60,
            "regions": ["sudeste"],
            "cities": ["sao_paulo", "rio_de_janeiro", "belo_horizonte"],
            "objective": "Validar oferta e criativos",
            "kpis": ["CPA", "ROAS", "Taxa de Conversao"]
        }
        strategy["phases"].append(phase1)
        
        # Fase 2: Expansao regional
        phase2 = {
            "phase": 2,
            "name": "Expansao Regional",
            "duration": "4-6 semanas",
            "budget_share": 0.25,
            "regions": ["sul", "centro_oeste"],
            "cities": ["curitiba", "porto_alegre", "brasilia", "goiania"],
            "objective": "Escalar para regioes similares",
            "kpis": ["CPA comparativo", "Volume de conversoes"]
        }
        strategy["phases"].append(phase2)
        
        # Fase 3: Mercados emergentes
        phase3 = {
            "phase": 3,
            "name": "Mercados Emergentes",
            "duration": "6-8 semanas",
            "budget_share": 0.15,
            "regions": ["nordeste"],
            "cities": ["salvador", "recife", "fortaleza"],
            "objective": "Testar mercados de crescimento",
            "kpis": ["Custo por lead", "Qualidade de leads"]
        }
        strategy["phases"].append(phase3)
        
        # Alocacao de orcamento
        strategy["budget_allocation"] = {
            phase["name"]: round(budget * phase["budget_share"], 2)
            for phase in strategy["phases"]
        }
        
        # Metricas de sucesso
        strategy["success_metrics"] = {
            "phase_1": {"target_roas": 2.0, "max_cpa": config.get("target_cpa", 50)},
            "phase_2": {"target_roas": 1.8, "max_cpa": config.get("target_cpa", 50) * 1.1},
            "phase_3": {"target_roas": 1.5, "max_cpa": config.get("target_cpa", 50) * 1.2}
        }
        
        return strategy
    
    def get_expansion_opportunities(self, current_regions: List[str], performance: Dict) -> Dict[str, Any]:
        """Identifica oportunidades de expansao geografica."""
        
        opportunities = {
            "timestamp": datetime.now().isoformat(),
            "current_regions": current_regions,
            "expansion_candidates": [],
            "risk_assessment": {}
        }
        
        # Identificar regioes nao exploradas
        all_regions = list(self.brazil_regions.keys())
        unexplored = [r for r in all_regions if r not in current_regions]
        
        for region in unexplored:
            region_data = self.brazil_regions[region]
            
            # Calcular score de oportunidade
            opportunity_score = (
                region_data["gdp_share"] * 40 +
                region_data["population_share"] * 30 +
                (1 if region_data["digital_maturity"] in ["high", "medium-high"] else 0.5) * 30
            )
            
            opportunities["expansion_candidates"].append({
                "region": region,
                "opportunity_score": round(opportunity_score, 1),
                "population_share": f"{region_data['population_share'] * 100:.1f}%",
                "gdp_share": f"{region_data['gdp_share'] * 100:.1f}%",
                "digital_maturity": region_data["digital_maturity"],
                "expected_cpc_multiplier": region_data["avg_cpc_multiplier"],
                "recommendation": "Alta prioridade" if opportunity_score > 20 else "Media prioridade" if opportunity_score > 10 else "Baixa prioridade"
            })
        
        # Ordenar por score
        opportunities["expansion_candidates"].sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        # Avaliacao de risco
        avg_roas = sum(p.get("roas", 0) for p in performance.values()) / len(performance) if performance else 0
        
        opportunities["risk_assessment"] = {
            "current_performance": "strong" if avg_roas > 2.5 else "moderate" if avg_roas > 1.5 else "weak",
            "expansion_readiness": "ready" if avg_roas > 2.0 else "cautious" if avg_roas > 1.5 else "not_recommended",
            "recommended_budget_for_expansion": "20-30% do orcamento atual" if avg_roas > 2.0 else "10-15%"
        }
        
        return opportunities
    
    def _calculate_geo_efficiency(self, cpa: float, roas: float, target_cpa: float) -> float:
        """Calcula eficiencia geografica."""
        cpa_score = min(100, (target_cpa / cpa) * 50) if cpa > 0 else 0
        roas_score = min(100, roas * 20)
        return round((cpa_score + roas_score) / 2, 1)
    
    def _identify_geo_opportunities(self, regions_analysis: Dict) -> List[Dict]:
        """Identifica oportunidades geograficas."""
        opportunities = []
        
        for region, analysis in regions_analysis.items():
            if analysis["efficiency_score"] > 70 and analysis["spend"] < 500:
                opportunities.append({
                    "region": region,
                    "type": "scale_opportunity",
                    "reason": "Alta eficiencia com baixo investimento",
                    "suggested_action": "Aumentar orcamento em 50%"
                })
        
        return opportunities
    
    def _generate_geo_recommendations(self, analysis: Dict) -> List[str]:
        """Gera recomendacoes geograficas."""
        recommendations = []
        
        if analysis["top_performers"]:
            top = analysis["top_performers"][0]
            recommendations.append(f"Escale investimento em {top['region']} (ROAS: {top['roas']:.2f})")
        
        if analysis["underperformers"]:
            under = analysis["underperformers"][0]
            recommendations.append(f"Reduza ou pause {under['region']} (ROAS: {under['roas']:.2f})")
        
        return recommendations
    
    def _get_top_cities_for_niche(self, niche: str) -> List[str]:
        """Obtem melhores cidades para um nicho."""
        # Ordenar por indice de ecommerce
        sorted_cities = sorted(self.city_data.items(), key=lambda x: x[1]["ecommerce_index"], reverse=True)
        return [city for city, _ in sorted_cities[:5]]
    
    def _get_city_recommendations(self, city_key: str, city_info: Dict) -> List[str]:
        """Obtem recomendacoes para uma cidade."""
        recommendations = []
        
        if city_info["tier"] == 1:
            recommendations.append("Cidade tier 1 - espere CPCs mais altos mas maior qualidade")
            recommendations.append("Foque em diferenciacao para se destacar da concorrencia")
        else:
            recommendations.append("Cidade tier 2 - oportunidade de CPCs mais baixos")
            recommendations.append("Teste diferentes abordagens de mensagem")
        
        return recommendations
    
    def _get_region_main_sectors(self, region: str) -> List[str]:
        """Obtem principais setores de uma regiao."""
        sectors = {
            "sudeste": ["Tecnologia", "Financas", "Varejo", "Industria"],
            "sul": ["Agronegocio", "Industria", "Tecnologia", "Turismo"],
            "nordeste": ["Turismo", "Comercio", "Servicos", "Agronegocio"],
            "centro_oeste": ["Agronegocio", "Governo", "Comercio", "Servicos"],
            "norte": ["Mineracao", "Agronegocio", "Comercio", "Industria"]
        }
        return sectors.get(region, ["Comercio", "Servicos"])


# Instancia global
geo_intelligence = GeoIntelligence()
