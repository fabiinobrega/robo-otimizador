"""
Competitor Spy Engine - Motor de Espionagem de Concorrência
Analisa anúncios concorrentes ANTES de gerar campanhas
"""

import os
import json
import logging
from datetime import datetime
from openai import OpenAI

logger = logging.getLogger(__name__)


class CompetitorSpyEngine:
    """
    Motor de espionagem que analisa concorrentes antes de criar anúncios
    """
    
    def __init__(self):
        self.client = OpenAI()
    
    def analyze_competitors(self, product, niche, platform='facebook'):
        """
        Analisa concorrentes e gera relatório interno
        
        Args:
            product (str): Produto/serviço a ser anunciado
            niche (str): Nicho de mercado
            platform (str): Plataforma (facebook, google, etc)
            
        Returns:
            dict: Relatório de espionagem
        """
        try:
            # Gerar análise com OpenAI
            analysis = self._generate_spy_analysis(product, niche, platform)
            
            # Estruturar relatório
            report = {
                'timestamp': datetime.now().isoformat(),
                'product': product,
                'niche': niche,
                'platform': platform,
                'analysis': analysis,
                'recommendations': self._extract_recommendations(analysis)
            }
            
            # Salvar relatório
            self._save_report(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Erro na espionagem de concorrência: {e}")
            raise
    
    def _generate_spy_analysis(self, product, niche, platform):
        """
        Gera análise de concorrência usando OpenAI
        """
        prompt = f"""
Você é um especialista em análise competitiva de anúncios digitais.

Analise a concorrência para o seguinte produto/serviço:
- Produto: {product}
- Nicho: {niche}
- Plataforma: {platform}

Forneça uma análise DETALHADA sobre:

1. HEADLINES COMUNS:
   - Quais headlines os concorrentes usam?
   - Quais padrões se repetem?
   - Quais são mais eficazes?

2. CRIATIVOS VISUAIS:
   - Que tipo de imagens/vídeos usam?
   - Cores predominantes
   - Estilo (profissional, casual, moderno, etc)

3. PROMESSAS E BENEFÍCIOS:
   - Quais promessas fazem?
   - Quais benefícios destacam?
   - Quais são mais convincentes?

4. OFERTAS:
   - Que tipo de ofertas apresentam?
   - Descontos, brindes, garantias?
   - Urgência e escassez?

5. CALL-TO-ACTION (CTA):
   - Quais CTAs usam?
   - Quais são mais diretos?
   - Quais geram mais ação?

6. FREQUÊNCIA E TIMING:
   - Com que frequência anunciam?
   - Horários preferenciais?
   - Sazonalidade?

7. O QUE FUNCIONA:
   - Padrões de sucesso identificados
   - Elementos que se repetem em anúncios de alta performance

8. O QUE NÃO REPETIR:
   - Erros comuns
   - Abordagens saturadas
   - Promessas exageradas

9. OPORTUNIDADES DE DIFERENCIAÇÃO:
   - Lacunas no mercado
   - Ângulos não explorados
   - Formas de se destacar

Seja específico, prático e baseado em dados reais do mercado brasileiro.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise competitiva de anúncios digitais com 10 anos de experiência."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro ao gerar análise com OpenAI: {e}")
            # Retornar análise genérica em caso de erro
            return self._get_generic_analysis(product, niche)
    
    def _extract_recommendations(self, analysis):
        """
        Extrai recomendações práticas da análise
        """
        try:
            prompt = f"""
Com base nesta análise de concorrência:

{analysis}

Extraia as 5 PRINCIPAIS RECOMENDAÇÕES PRÁTICAS para criar anúncios que se destaquem.

Formato:
1. [Recomendação específica e acionável]
2. [Recomendação específica e acionável]
...

Seja direto e prático.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um consultor de marketing digital focado em resultados."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            recommendations_text = response.choices[0].message.content
            
            # Converter em lista
            recommendations = [
                line.strip() 
                for line in recommendations_text.split('\n') 
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erro ao extrair recomendações: {e}")
            return [
                "Foque em benefícios claros e mensuráveis",
                "Use prova social (depoimentos, números)",
                "Crie senso de urgência genuíno",
                "Diferencie-se com uma proposta única",
                "Teste múltiplas variações de copy"
            ]
    
    def _save_report(self, report):
        """
        Salva relatório de espionagem
        """
        try:
            os.makedirs('reports/competitor_spy', exist_ok=True)
            
            filename = f"reports/competitor_spy/spy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Relatório de espionagem salvo: {filename}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {e}")
    
    def _get_generic_analysis(self, product, niche):
        """
        Retorna análise genérica em caso de erro
        """
        return f"""
ANÁLISE GENÉRICA DE CONCORRÊNCIA

Produto: {product}
Nicho: {niche}

1. HEADLINES COMUNS:
- Foco em benefícios principais
- Uso de números e dados
- Perguntas que geram curiosidade

2. CRIATIVOS:
- Imagens de alta qualidade
- Cores vibrantes
- Foco no produto/resultado

3. PROMESSAS:
- Resultados rápidos
- Garantia de satisfação
- Diferencial competitivo

4. OFERTAS:
- Descontos por tempo limitado
- Bônus exclusivos
- Garantia de devolução

5. CTA:
- "Compre Agora"
- "Saiba Mais"
- "Garanta o Seu"

6. OPORTUNIDADES:
- Humanizar a comunicação
- Mostrar casos reais
- Criar conexão emocional
"""
    
    def get_spy_summary(self, report):
        """
        Gera resumo executivo do relatório
        """
        return {
            'product': report['product'],
            'niche': report['niche'],
            'platform': report['platform'],
            'key_insights': report['recommendations'][:3],
            'analyzed_at': report['timestamp']
        }
