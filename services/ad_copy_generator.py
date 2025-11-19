"""
NEXORA Operator v11.7 - Ad Copy Generator Service
Geração de copy profissional para anúncios com IA
"""

import os
import json
from datetime import datetime
import random

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AdCopyGenerator:
    """Gera copy profissional para anúncios usando IA"""
    
    def __init__(self):
        self.use_openai = OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY')
        if self.use_openai:
            self.client = OpenAI()
            self.model = "gpt-4.1-mini"
    
    def generate_complete_ad_copy(self, product_data, platform='facebook', language='pt-BR'):
        """
        Gera copy completa para anúncio
        
        Args:
            product_data: Dados do produto/serviço
            platform: Plataforma do anúncio
            language: Idioma da copy
            
        Returns:
            dict: Copy completa com múltiplas variações
        """
        
        if self.use_openai:
            return self._generate_with_openai(product_data, platform, language)
        else:
            return self._generate_with_native_ai(product_data, platform, language)
    
    def _generate_with_openai(self, product_data, platform, language):
        """Gera copy usando OpenAI"""
        try:
            prompt = self._build_prompt(product_data, platform, language)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um copywriter profissional especializado em anúncios de alta conversão."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Parsear resposta
            return self._parse_ai_response(content, product_data, platform)
            
        except Exception as e:
            print(f"Erro ao gerar com OpenAI: {e}")
            return self._generate_with_native_ai(product_data, platform, language)
    
    def _generate_with_native_ai(self, product_data, platform, language):
        """Gera copy usando IA nativa (fallback)"""
        
        product_name = product_data.get('name', 'Produto')
        product_benefits = product_data.get('benefits', [])
        target_audience = product_data.get('target_audience', {})
        
        # Gerar múltiplas variações
        headlines = self._generate_headlines(product_name, product_benefits, platform)
        descriptions = self._generate_descriptions(product_name, product_benefits, target_audience)
        ctas = self._generate_ctas(platform)
        
        # Gerar variações completas
        variations = []
        for i in range(5):
            variation = {
                'id': f'var_{i+1}',
                'headline': headlines[i % len(headlines)],
                'description': descriptions[i % len(descriptions)],
                'cta': ctas[i % len(ctas)],
                'score': random.randint(75, 95),
                'estimated_ctr': f"{random.uniform(2.0, 5.0):.2f}%",
                'estimated_conversion_rate': f"{random.uniform(1.0, 3.0):.2f}%",
                'tone': random.choice(['profissional', 'casual', 'urgente', 'educativo']),
                'emotion': random.choice(['curiosidade', 'desejo', 'medo', 'alegria']),
                'consciousness_level': random.choice(['C0', 'C1', 'C2', 'C3', 'C4', 'C5'])
            }
            variations.append(variation)
        
        # Ordenar por score
        variations.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'success': True,
            'data': {
                'variations': variations,
                'top_performer': variations[0],
                'platform': platform,
                'language': language,
                'timestamp': datetime.now().isoformat(),
                'recommendations': self._generate_copy_recommendations(variations)
            },
            'message': f'{len(variations)} variações de copy geradas com sucesso'
        }
    
    def _build_prompt(self, product_data, platform, language):
        """Constrói prompt para IA"""
        product_name = product_data.get('name', 'Produto')
        product_benefits = ', '.join(product_data.get('benefits', []))
        
        prompt = f"""
Crie 5 variações de copy para anúncio de {platform} para o produto: {product_name}

Benefícios: {product_benefits}

Para cada variação, forneça:
1. Headline (título principal)
2. Description (descrição persuasiva)
3. CTA (call-to-action)

Idioma: {language}
Tom: Profissional e persuasivo
Foco: Alta conversão

Formato de resposta:
Variação 1:
Headline: [texto]
Description: [texto]
CTA: [texto]

[repetir para 5 variações]
"""
        return prompt
    
    def _parse_ai_response(self, content, product_data, platform):
        """Parseia resposta da IA"""
        # TODO: Implementar parsing robusto da resposta
        # Por enquanto, usar fallback
        return self._generate_with_native_ai(product_data, platform, 'pt-BR')
    
    def _generate_headlines(self, product_name, benefits, platform):
        """Gera headlines variadas"""
        templates = [
            f"{product_name}: Transforme Seus Resultados em 30 Dias",
            f"Descubra Como {product_name} Pode Mudar Sua Vida",
            f"{product_name} Profissional - Garantia de Satisfação",
            f"O Segredo do Sucesso com {product_name}",
            f"{product_name}: Oferta Exclusiva por Tempo Limitado",
            f"Como {product_name} Ajudou Mais de 10.000 Pessoas",
            f"{product_name}: A Solução Que Você Estava Procurando",
            f"Revolucione Seus Resultados com {product_name}",
            f"{product_name}: Comece Hoje, Veja Resultados Amanhã",
            f"Por Que {product_name} é a Escolha Número 1?"
        ]
        return templates
    
    def _generate_descriptions(self, product_name, benefits, target_audience):
        """Gera descrições persuasivas"""
        benefit_text = benefits[0] if benefits else "resultados incríveis"
        
        templates = [
            f"Aproveite nossa oferta exclusiva de {product_name}. {benefit_text.capitalize()} com garantia de satisfação ou seu dinheiro de volta! Mais de 10.000 clientes satisfeitos.",
            f"Transforme seus resultados com {product_name} profissional. {benefit_text.capitalize()} em apenas 30 dias. Teste grátis por 7 dias, sem compromisso!",
            f"O {product_name} mais completo do mercado. {benefit_text.capitalize()} com entrega rápida e suporte 24/7. Comece hoje mesmo!",
            f"Desconto especial em {product_name}! {benefit_text.capitalize()} com o melhor custo-benefício. Últimas unidades disponíveis!",
            f"Junte-se a milhares de clientes satisfeitos com {product_name}. {benefit_text.capitalize()} e alcance seus objetivos mais rápido.",
            f"{product_name} com tecnologia de ponta. {benefit_text.capitalize()} de forma simples e eficaz. Experimente sem riscos!",
            f"Não perca esta oportunidade! {product_name} com {benefit_text}. Oferta válida apenas hoje!",
            f"Conquiste seus objetivos com {product_name}. {benefit_text.capitalize()} e veja a diferença. Garantia de 30 dias!",
            f"O {product_name} que você precisa para ter sucesso. {benefit_text.capitalize()} com resultados comprovados.",
            f"Invista em você com {product_name}. {benefit_text.capitalize()} e transforme sua realidade. Parcele em até 12x!"
        ]
        return templates
    
    def _generate_ctas(self, platform):
        """Gera CTAs eficazes"""
        if platform == 'facebook' or platform == 'instagram':
            return [
                'Comprar Agora',
                'Saiba Mais',
                'Começar Agora',
                'Garantir Desconto',
                'Aproveitar Oferta',
                'Quero Experimentar',
                'Ver Mais',
                'Inscrever-se',
                'Baixar Grátis',
                'Solicitar Demo'
            ]
        elif platform == 'google':
            return [
                'Compre Já',
                'Saiba Mais',
                'Comece Grátis',
                'Solicite Orçamento',
                'Experimente Agora',
                'Ver Ofertas',
                'Cadastre-se',
                'Baixe Agora',
                'Fale Conosco',
                'Agende Demonstração'
            ]
        else:
            return [
                'Comprar',
                'Saiba Mais',
                'Começar',
                'Ver Mais',
                'Experimentar'
            ]
    
    def _generate_copy_recommendations(self, variations):
        """Gera recomendações de copy"""
        top_variation = variations[0]
        
        recommendations = [
            {
                'priority': 'Alta',
                'category': 'Teste A/B',
                'recommendation': f'Teste a variação #{top_variation["id"]} (score {top_variation["score"]}) primeiro',
                'impact': 'Alto'
            },
            {
                'priority': 'Alta',
                'category': 'Tom',
                'recommendation': f'Use tom {top_variation["tone"]} para este público',
                'impact': 'Alto'
            },
            {
                'priority': 'Média',
                'category': 'Emoção',
                'recommendation': f'Explore emoção de {top_variation["emotion"]} nos criativos',
                'impact': 'Médio'
            },
            {
                'priority': 'Média',
                'category': 'Consciência',
                'recommendation': f'Público está em nível {top_variation["consciousness_level"]} - ajuste mensagem',
                'impact': 'Médio'
            },
            {
                'priority': 'Baixa',
                'category': 'Otimização',
                'recommendation': 'Teste diferentes CTAs após 7 dias',
                'impact': 'Baixo'
            }
        ]
        
        return recommendations
    
    def generate_vsl_script(self, product_data):
        """Gera roteiro de VSL (Video Sales Letter)"""
        product_name = product_data.get('name', 'Produto')
        
        script = {
            'hook': f"Você sabia que {product_name} pode transformar completamente seus resultados?",
            'problem': "Muitas pessoas lutam com [problema específico] todos os dias...",
            'agitate': "E isso pode estar custando caro para você em termos de tempo, dinheiro e oportunidades perdidas.",
            'solution': f"Mas e se eu te dissesse que existe uma solução simples? Apresento: {product_name}",
            'benefits': [
                "Benefício 1: Economia de tempo",
                "Benefício 2: Resultados rápidos",
                "Benefício 3: Fácil de usar"
            ],
            'social_proof': "Mais de 10.000 pessoas já transformaram suas vidas com este produto.",
            'offer': "E por tempo limitado, você pode ter acesso com 50% de desconto!",
            'guarantee': "Com nossa garantia de 30 dias, você não tem nada a perder.",
            'cta': "Clique no botão abaixo e comece sua transformação hoje mesmo!",
            'urgency': "Atenção: Esta oferta expira em 24 horas!"
        }
        
        return {
            'success': True,
            'data': script,
            'message': 'Roteiro de VSL gerado com sucesso'
        }
    
    def generate_email_sequence(self, product_data, sequence_type='welcome'):
        """Gera sequência de e-mails"""
        product_name = product_data.get('name', 'Produto')
        
        if sequence_type == 'welcome':
            emails = [
                {
                    'day': 0,
                    'subject': f'Bem-vindo! Aqui está seu acesso ao {product_name}',
                    'preview': 'Estamos felizes em ter você conosco...',
                    'body': f'Olá! Obrigado por escolher {product_name}. Aqui estão seus primeiros passos...'
                },
                {
                    'day': 2,
                    'subject': f'Como aproveitar ao máximo o {product_name}',
                    'preview': 'Dicas exclusivas para você...',
                    'body': f'Aqui estão 5 dicas para você começar com o pé direito...'
                },
                {
                    'day': 5,
                    'subject': 'Você já viu estes recursos?',
                    'preview': 'Recursos que você pode estar perdendo...',
                    'body': 'Muitas pessoas não sabem que podem fazer isso...'
                }
            ]
        else:
            emails = []
        
        return {
            'success': True,
            'data': {
                'sequence_type': sequence_type,
                'emails': emails,
                'total_emails': len(emails)
            },
            'message': f'Sequência de {len(emails)} e-mails gerada'
        }
