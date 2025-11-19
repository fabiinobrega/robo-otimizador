"""
NEXORA Operator v11.7 - Landing Page Analyzer Service
Análise completa de landing pages com IA
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urlparse
from datetime import datetime

class LandingPageAnalyzer:
    """Analisa landing pages e extrai informações para criação de anúncios"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def analyze(self, url):
        """
        Análise completa de uma landing page
        
        Args:
            url: URL da landing page
            
        Returns:
            dict: Dados completos da análise
        """
        try:
            # Fazer crawling da página
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair informações
            analysis = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'title': self._extract_title(soup),
                'meta_description': self._extract_meta_description(soup),
                'price': self._extract_price(soup),
                'features': self._extract_features(soup),
                'benefits': self._extract_benefits(soup),
                'images': self._extract_images(soup, url),
                'cta_buttons': self._extract_ctas(soup),
                'trust_signals': self._extract_trust_signals(soup),
                'social_proof': self._extract_social_proof(soup),
                'conversion_elements': self._analyze_conversion_elements(soup),
                'hierarchy': self._analyze_hierarchy(soup),
                'keywords': self._extract_keywords(soup),
                'target_audience': self._identify_target_audience(soup),
                'estimated_performance': self._estimate_performance(soup),
                'recommendations': []
            }
            
            # Gerar recomendações
            analysis['recommendations'] = self._generate_recommendations(analysis)
            
            return {
                'success': True,
                'data': analysis,
                'message': 'Análise completa realizada com sucesso'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao analisar landing page'
            }
    
    def _extract_title(self, soup):
        """Extrai o título da página"""
        # Tentar h1 primeiro
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        # Fallback para title tag
        title = soup.find('title')
        if title:
            return title.get_text(strip=True)
        
        return "Título não encontrado"
    
    def _extract_meta_description(self, soup):
        """Extrai meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content']
        return ""
    
    def _extract_price(self, soup):
        """Extrai preço do produto"""
        # Padrões comuns de preço
        price_patterns = [
            r'R\$\s*(\d+[.,]\d{2})',
            r'\$\s*(\d+[.,]\d{2})',
            r'(\d+[.,]\d{2})\s*reais',
        ]
        
        text = soup.get_text()
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return "Preço não encontrado"
    
    def _extract_features(self, soup):
        """Extrai características do produto"""
        features = []
        
        # Procurar listas
        lists = soup.find_all(['ul', 'ol'])
        for lst in lists[:3]:  # Limitar a 3 listas
            items = lst.find_all('li')
            for item in items[:10]:  # Limitar a 10 itens por lista
                text = item.get_text(strip=True)
                if text and len(text) < 200:
                    features.append(text)
        
        return features[:15]  # Retornar no máximo 15 features
    
    def _extract_benefits(self, soup):
        """Extrai benefícios do produto"""
        benefits = []
        
        # Procurar seções de benefícios
        benefit_keywords = ['benefício', 'vantagem', 'por que', 'porque']
        
        for keyword in benefit_keywords:
            sections = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            for section in sections[:5]:
                parent = section.find_parent()
                if parent:
                    text = parent.get_text(strip=True)
                    if text and len(text) < 300:
                        benefits.append(text)
        
        return benefits[:10]
    
    def _extract_images(self, soup, base_url):
        """Extrai URLs das imagens"""
        images = []
        
        for img in soup.find_all('img')[:20]:  # Limitar a 20 imagens
            src = img.get('src') or img.get('data-src')
            if src:
                # Converter URL relativa para absoluta
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    parsed = urlparse(base_url)
                    src = f"{parsed.scheme}://{parsed.netloc}{src}"
                
                images.append({
                    'url': src,
                    'alt': img.get('alt', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', '')
                })
        
        return images
    
    def _extract_ctas(self, soup):
        """Extrai botões de CTA"""
        ctas = []
        
        # Procurar botões e links com classes comuns
        cta_elements = soup.find_all(['button', 'a'], 
                                     class_=re.compile(r'btn|button|cta', re.IGNORECASE))
        
        for element in cta_elements[:15]:
            text = element.get_text(strip=True)
            if text and len(text) < 100:
                ctas.append({
                    'text': text,
                    'href': element.get('href', ''),
                    'type': element.name
                })
        
        return ctas
    
    def _extract_trust_signals(self, soup):
        """Extrai sinais de confiança"""
        trust_signals = []
        
        trust_keywords = [
            'garantia', 'seguro', 'certificado', 'ssl', 'proteção',
            'privacidade', 'confiável', 'verificado', 'aprovado'
        ]
        
        text = soup.get_text().lower()
        for keyword in trust_keywords:
            if keyword in text:
                trust_signals.append(keyword.capitalize())
        
        return list(set(trust_signals))
    
    def _extract_social_proof(self, soup):
        """Extrai prova social"""
        social_proof = []
        
        # Procurar depoimentos, avaliações, etc.
        social_keywords = [
            'depoimento', 'avaliação', 'review', 'testemunho',
            'cliente', 'satisfeito', 'recomend'
        ]
        
        for keyword in social_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            for element in elements[:5]:
                parent = element.find_parent()
                if parent:
                    text = parent.get_text(strip=True)
                    if text and len(text) < 500:
                        social_proof.append(text)
        
        return social_proof[:10]
    
    def _analyze_conversion_elements(self, soup):
        """Analisa elementos de conversão"""
        return {
            'has_form': bool(soup.find('form')),
            'form_count': len(soup.find_all('form')),
            'button_count': len(soup.find_all('button')),
            'cta_count': len(soup.find_all(class_=re.compile(r'cta|btn', re.IGNORECASE))),
            'video_count': len(soup.find_all(['video', 'iframe'])),
            'has_chat': bool(soup.find(class_=re.compile(r'chat|whatsapp', re.IGNORECASE)))
        }
    
    def _analyze_hierarchy(self, soup):
        """Analisa hierarquia da página"""
        return {
            'h1_count': len(soup.find_all('h1')),
            'h2_count': len(soup.find_all('h2')),
            'h3_count': len(soup.find_all('h3')),
            'section_count': len(soup.find_all(['section', 'div'], class_=re.compile(r'section', re.IGNORECASE))),
            'has_header': bool(soup.find('header')),
            'has_footer': bool(soup.find('footer')),
            'has_nav': bool(soup.find('nav'))
        }
    
    def _extract_keywords(self, soup):
        """Extrai palavras-chave principais"""
        # Pegar texto completo
        text = soup.get_text().lower()
        
        # Remover stopwords básicas
        stopwords = ['o', 'a', 'de', 'da', 'do', 'para', 'com', 'em', 'e', 'que']
        
        # Extrair palavras
        words = re.findall(r'\b\w{4,}\b', text)
        
        # Contar frequência
        word_freq = {}
        for word in words:
            if word not in stopwords:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Retornar top 20
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:20]]
    
    def _identify_target_audience(self, soup):
        """Identifica público-alvo"""
        text = soup.get_text().lower()
        
        audience = {
            'gender': 'unisex',
            'age_range': 'adultos',
            'interests': [],
            'pain_points': []
        }
        
        # Detectar gênero
        if 'mulher' in text or 'feminino' in text:
            audience['gender'] = 'feminino'
        elif 'homem' in text or 'masculino' in text:
            audience['gender'] = 'masculino'
        
        # Detectar faixa etária
        if 'jovem' in text or 'adolescent' in text:
            audience['age_range'] = '18-25'
        elif 'idoso' in text or 'terceira idade' in text:
            audience['age_range'] = '60+'
        
        return audience
    
    def _estimate_performance(self, soup):
        """Estima performance da landing page"""
        # Calcular score baseado em elementos de conversão
        score = 50  # Base
        
        conversion = self._analyze_conversion_elements(soup)
        
        if conversion['has_form']:
            score += 10
        if conversion['cta_count'] > 0:
            score += 10
        if conversion['video_count'] > 0:
            score += 5
        if conversion['has_chat']:
            score += 10
        
        # Limitar a 100
        score = min(score, 100)
        
        return {
            'conversion_score': score,
            'estimated_ctr': f"{score * 0.05:.2f}%",
            'estimated_conversion_rate': f"{score * 0.02:.2f}%",
            'quality': 'Alta' if score >= 80 else 'Média' if score >= 60 else 'Baixa'
        }
    
    def _generate_recommendations(self, analysis):
        """Gera recomendações de melhoria"""
        recommendations = []
        
        if analysis['conversion_elements']['cta_count'] < 2:
            recommendations.append("Adicionar mais CTAs ao longo da página")
        
        if not analysis['conversion_elements']['has_form']:
            recommendations.append("Adicionar formulário de captura de leads")
        
        if not analysis['trust_signals']:
            recommendations.append("Adicionar sinais de confiança (garantia, certificados, etc.)")
        
        if not analysis['social_proof']:
            recommendations.append("Adicionar depoimentos e provas sociais")
        
        if analysis['conversion_elements']['video_count'] == 0:
            recommendations.append("Considerar adicionar vídeo explicativo")
        
        return recommendations
