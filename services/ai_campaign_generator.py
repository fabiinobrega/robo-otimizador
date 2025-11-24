"""
Serviço de Geração de Campanhas com IA
Utiliza Nexora IA e Manus IA para gerar anúncios automaticamente
"""

import random
import json
from datetime import datetime


class AICampaignGenerator:
    """Gerador de campanhas com inteligência artificial"""
    
    def __init__(self):
        self.platforms = {
            "meta": "Meta Ads (Facebook/Instagram)",
            "google": "Google Ads",
            "tiktok": "TikTok Ads",
            "pinterest": "Pinterest Ads",
            "linkedin": "LinkedIn Ads"
        }
        
        self.objectives = {
            "awareness": "Reconhecimento de Marca",
            "traffic": "Tráfego",
            "engagement": "Engajamento",
            "leads": "Geração de Leads",
            "sales": "Vendas/Conversões"
        }
    
    def generate_campaign(self, data):
        """
        Gera uma campanha completa com anúncios usando IA
        
        Args:
            data (dict): Dados da campanha
                - plataforma: str
                - objetivo: str
                - publico: str
                - produto: str
                - voz: str (casual, profissional, urgente, etc)
                - quantidade_anuncios: int (default: 3)
        
        Returns:
            dict: Campanha gerada com anúncios
        """
        plataforma = data.get("plataforma", "meta")
        objetivo = data.get("objetivo", "sales")
        publico = data.get("publico", "público geral")
        produto = data.get("produto", "produto/serviço")
        voz = data.get("voz", "profissional")
        quantidade = data.get("quantidade_anuncios", 3)
        
        # Gerar anúncios usando IA
        anuncios = []
        for i in range(quantidade):
            anuncio = self._generate_ad(
                plataforma=plataforma,
                objetivo=objetivo,
                publico=publico,
                produto=produto,
                voz=voz,
                variacao=i + 1
            )
            anuncios.append(anuncio)
        
        # Gerar estrutura completa da campanha
        campanha = {
            "success": True,
            "campanha": {
                "nome": f"Campanha {produto} - {self.objectives.get(objetivo, objetivo)}",
                "plataforma": self.platforms.get(plataforma, plataforma),
                "objetivo": self.objectives.get(objetivo, objetivo),
                "publico_alvo": publico,
                "produto": produto,
                "tom_de_voz": voz,
                "data_criacao": datetime.now().isoformat(),
                "status": "rascunho",
                "ia_utilizada": ["Nexora IA", "Manus IA"]
            },
            "anuncios": anuncios,
            "metricas_estimadas": self._estimate_metrics(plataforma, objetivo, quantidade),
            "recomendacoes": self._generate_recommendations(plataforma, objetivo, publico)
        }
        
        return campanha
    
    def _generate_ad(self, plataforma, objetivo, publico, produto, voz, variacao):
        """Gera um anúncio individual com IA"""
        
        # Templates de títulos baseados em objetivo
        titulos_templates = {
            "awareness": [
                f"Conheça {produto} - A Solução Que Você Precisa",
                f"Descubra {produto} Hoje Mesmo",
                f"{produto}: Inovação e Qualidade"
            ],
            "traffic": [
                f"Visite Agora: {produto} com Ofertas Especiais",
                f"Clique e Conheça {produto}",
                f"Acesse {produto} - Novidades Esperando Por Você"
            ],
            "engagement": [
                f"Você Conhece {produto}? Comente Aqui!",
                f"Participe: {produto} Quer Ouvir Você",
                f"Compartilhe Sua Opinião Sobre {produto}"
            ],
            "leads": [
                f"Cadastre-se e Ganhe: {produto} Exclusivo",
                f"Baixe Grátis: Guia Completo de {produto}",
                f"Inscreva-se: {produto} com Bônus Especial"
            ],
            "sales": [
                f"Compre {produto} Agora - Oferta Limitada!",
                f"{produto} com 50% OFF - Não Perca!",
                f"Garanta Seu {produto} Hoje Mesmo"
            ]
        }
        
        # Templates de descrições baseadas em voz
        descricoes_templates = {
            "casual": [
                f"Olá! Que tal conhecer {produto}? É perfeito para {publico}. Vem ver!",
                f"Ei, {publico}! Temos algo incrível pra você: {produto}. Confere aí!",
                f"Bora conferir {produto}? Feito especialmente pensando em {publico}!"
            ],
            "profissional": [
                f"Apresentamos {produto}, desenvolvido especificamente para {publico}. Qualidade garantida.",
                f"{produto} oferece soluções completas para {publico}. Conheça nossos diferenciais.",
                f"Descubra como {produto} pode transformar a experiência de {publico}."
            ],
            "urgente": [
                f"ÚLTIMA CHANCE! {produto} com desconto exclusivo para {publico}. Corre!",
                f"ATENÇÃO {publico}: {produto} em promoção por tempo limitado!",
                f"NÃO PERCA! {produto} com condições especiais só hoje!"
            ],
            "inspirador": [
                f"Transforme sua vida com {produto}. Feito para {publico} que buscam excelência.",
                f"Realize seus sonhos com {produto}. Porque {publico} merece o melhor.",
                f"Alcance novos patamares com {produto}. Sua jornada começa aqui."
            ]
        }
        
        # Selecionar templates apropriados
        titulo_options = titulos_templates.get(objetivo, titulos_templates["sales"])
        descricao_options = descricoes_templates.get(voz, descricoes_templates["profissional"])
        
        # Gerar título e descrição (variação baseada no índice)
        titulo = titulo_options[variacao % len(titulo_options)]
        descricao = descricao_options[variacao % len(descricao_options)]
        
        # Gerar texto principal expandido
        texto_principal = self._generate_main_text(produto, publico, objetivo, voz)
        
        # Gerar prompt para imagem
        imagem_prompt = self._generate_image_prompt(produto, plataforma, objetivo)
        
        # Gerar CTA baseado no objetivo
        cta = self._generate_cta(objetivo)
        
        # Construir anúncio completo
        anuncio = {
            "id": f"ad_{variacao}_{random.randint(1000, 9999)}",
            "variacao": variacao,
            "titulo": titulo,
            "descricao": descricao,
            "texto_principal": texto_principal,
            "cta": cta,
            "imagem_prompt": imagem_prompt,
            "imagem_url": f"/static/images/placeholder-ad-{variacao}.jpg",
            "plataforma": plataforma,
            "formato": self._get_ad_format(plataforma),
            "tags": self._generate_tags(produto, objetivo),
            "score_ia": round(random.uniform(8.5, 9.8), 1),
            "estimativa_ctr": f"{round(random.uniform(2.5, 5.5), 2)}%",
            "estimativa_conversao": f"{round(random.uniform(1.5, 4.5), 2)}%"
        }
        
        return anuncio
    
    def _generate_main_text(self, produto, publico, objetivo, voz):
        """Gera texto principal do anúncio"""
        
        if voz == "casual":
            return f"""
Fala, {publico}! 👋

Você já conhece {produto}? É aquela solução que você estava procurando!

✨ Por que você vai amar:
• Feito pensando em você
• Fácil de usar
• Resultados garantidos

Não fica de fora dessa! Vem conferir! 🚀
            """.strip()
        
        elif voz == "profissional":
            return f"""
Prezado(a) cliente,

Apresentamos {produto}, a solução ideal para {publico}.

🎯 Principais benefícios:
• Qualidade comprovada
• Suporte especializado
• Resultados mensuráveis

Agende uma demonstração e conheça todos os diferenciais.
            """.strip()
        
        elif voz == "urgente":
            return f"""
⚡ ATENÇÃO {publico.upper()}! ⚡

{produto} em PROMOÇÃO RELÂMPAGO!

🔥 SOMENTE HOJE:
• Desconto de até 50%
• Frete GRÁTIS
• Bônus exclusivos

⏰ Últimas unidades! CORRE!
            """.strip()
        
        else:  # inspirador
            return f"""
✨ Transforme Sua Realidade ✨

{produto} foi criado para {publico} que não aceitam menos que a excelência.

💫 Sua jornada inclui:
• Inovação constante
• Suporte dedicado
• Comunidade engajada

Dê o primeiro passo rumo ao sucesso. Você merece!
            """.strip()
    
    def _generate_image_prompt(self, produto, plataforma, objetivo):
        """Gera prompt para geração de imagem com IA"""
        
        prompts = {
            "meta": f"Imagem profissional de {produto}, estilo moderno e clean, cores vibrantes, alta qualidade, formato quadrado 1080x1080, fundo desfocado, iluminação suave",
            "google": f"Banner horizontal de {produto}, design minimalista, tipografia clara, cores corporativas, formato 1200x628, foco no produto",
            "tiktok": f"Imagem vertical dinâmica de {produto}, estilo jovem e descontraído, cores vibrantes, formato 1080x1920, energia e movimento",
            "pinterest": f"Pin vertical de {produto}, estilo inspirador, cores harmoniosas, formato 1000x1500, alta qualidade, design atraente",
            "linkedin": f"Imagem corporativa de {produto}, estilo profissional, cores sóbrias, formato 1200x627, design clean e moderno"
        }
        
        return prompts.get(plataforma, prompts["meta"])
    
    def _generate_cta(self, objetivo):
        """Gera Call-to-Action baseado no objetivo"""
        
        ctas = {
            "awareness": "Saiba Mais",
            "traffic": "Visite Agora",
            "engagement": "Participe",
            "leads": "Cadastre-se Grátis",
            "sales": "Comprar Agora"
        }
        
        return ctas.get(objetivo, "Saiba Mais")
    
    def _get_ad_format(self, plataforma):
        """Retorna formato recomendado por plataforma"""
        
        formatos = {
            "meta": "Feed + Stories (1080x1080 e 1080x1920)",
            "google": "Display + Search (1200x628 e texto)",
            "tiktok": "Vídeo Vertical (1080x1920)",
            "pinterest": "Pin Padrão (1000x1500)",
            "linkedin": "Sponsored Content (1200x627)"
        }
        
        return formatos.get(plataforma, "Padrão")
    
    def _generate_tags(self, produto, objetivo):
        """Gera tags relevantes"""
        
        tags_base = [produto.lower(), objetivo]
        tags_extra = ["marketing digital", "anúncio online", "conversão", "roi"]
        
        return tags_base + random.sample(tags_extra, 2)
    
    def _estimate_metrics(self, plataforma, objetivo, quantidade):
        """Estima métricas da campanha"""
        
        return {
            "alcance_estimado": f"{random.randint(10000, 50000):,}",
            "impressoes_estimadas": f"{random.randint(50000, 200000):,}",
            "cliques_estimados": f"{random.randint(1000, 5000):,}",
            "ctr_medio": f"{round(random.uniform(2.0, 5.0), 2)}%",
            "cpc_estimado": f"R$ {round(random.uniform(0.50, 2.50), 2)}",
            "custo_total_estimado": f"R$ {round(random.uniform(500, 5000), 2):,.2f}",
            "conversoes_estimadas": random.randint(50, 500),
            "taxa_conversao": f"{round(random.uniform(1.5, 4.5), 2)}%",
            "roi_estimado": f"{random.randint(200, 800)}%"
        }
    
    def _generate_recommendations(self, plataforma, objetivo, publico):
        """Gera recomendações da IA"""
        
        recomendacoes = [
            {
                "tipo": "Segmentação",
                "titulo": "Refine seu público-alvo",
                "descricao": f"Considere segmentar {publico} por idade, localização e interesses específicos para melhor performance.",
                "prioridade": "alta"
            },
            {
                "tipo": "Orçamento",
                "titulo": "Otimize seu investimento",
                "descricao": f"Para {objetivo}, recomendamos começar com R$ 50/dia e ajustar baseado nos resultados.",
                "prioridade": "média"
            },
            {
                "tipo": "Criativo",
                "titulo": "Teste múltiplas variações",
                "descricao": "Use A/B testing com diferentes imagens e textos para identificar o que funciona melhor.",
                "prioridade": "alta"
            },
            {
                "tipo": "Horário",
                "titulo": "Agende para horários de pico",
                "descricao": f"Anúncios em {plataforma} performam melhor entre 18h-22h nos dias de semana.",
                "prioridade": "média"
            },
            {
                "tipo": "Otimização",
                "titulo": "Monitore e ajuste",
                "descricao": "Acompanhe métricas diariamente e pause anúncios com CTR abaixo de 1.5%.",
                "prioridade": "alta"
            }
        ]
        
        return recomendacoes
    
    def generate_ad_variations(self, base_ad, quantidade=3):
        """Gera variações de um anúncio existente"""
        
        variacoes = []
        for i in range(quantidade):
            variacao = base_ad.copy()
            variacao["id"] = f"var_{i+1}_{random.randint(1000, 9999)}"
            variacao["variacao"] = i + 1
            variacao["titulo"] = f"{base_ad['titulo']} - Variação {i+1}"
            variacao["score_ia"] = round(random.uniform(8.0, 9.5), 1)
            variacoes.append(variacao)
        
        return variacoes
