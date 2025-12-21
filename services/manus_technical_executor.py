"""
Manus Technical Executor - Executor Técnico
Manus EXECUTA tudo que OpenAI pensou
Cria campanhas, anúncios, pixel do Facebook, configura eventos
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ManusTechnicalExecutor:
    """
    Executor técnico que EXECUTA tudo que OpenAI pensou
    Não pensa - apenas executa com precisão
    """
    
    def __init__(self):
        self.execution_log = []
    
    def execute_complete_campaign(self, strategy, copy, total_budget, duration_days, platform='facebook'):
        """
        Executa campanha completa baseada na estratégia do OpenAI
        
        Args:
            strategy (dict): Estratégia criada pelo OpenAI
            copy (dict): Copy criado pelo OpenAI
            total_budget (float): Orçamento total
            duration_days (int): Duração em dias
            platform (str): Plataforma
            
        Returns:
            dict: Resultado da execução
        """
        from datetime import datetime, timedelta
        
        # Calcular orçamento diário e datas
        daily_budget = total_budget / duration_days
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        try:
            execution_steps = []
            
            # PASSO 1: Criar/Verificar Pixel do Facebook
            if platform == 'facebook':
                pixel_result = self.create_facebook_pixel_if_not_exists()
                execution_steps.append(pixel_result)
            
            # PASSO 2: Criar campanha
            campaign_result = self.create_campaign(strategy, daily_budget, start_date, end_date, platform)
            execution_steps.append(campaign_result)
            
            # PASSO 3: Criar conjunto de anúncios
            adset_result = self.create_ad_set(campaign_result['campaign_id'], strategy, daily_budget, start_date, end_date)
            execution_steps.append(adset_result)
            
            # PASSO 4: Criar anúncios (3 variações)
            ads_results = self.create_ads(adset_result['adset_id'], copy)
            execution_steps.extend(ads_results)
            
            # PASSO 5: Aplicar orçamento
            budget_result = self.apply_budget(campaign_result['campaign_id'], budget)
            execution_steps.append(budget_result)
            
            # PASSO 6: Publicar
            publish_result = self.publish_campaign(campaign_result['campaign_id'])
            execution_steps.append(publish_result)
            
            # Log completo
            self._log_execution({
                'timestamp': datetime.now().isoformat(),
                'platform': platform,
                'steps': execution_steps,
                'status': 'completed'
            })
            
            return {
                'status': 'success',
                'message': 'Campanha executada com sucesso',
                'campaign_id': campaign_result['campaign_id'],
                'ads_created': len(ads_results),
                'execution_steps': execution_steps
            }
            
        except Exception as e:
            logger.error(f"Erro na execução: {e}")
            self._log_execution({
                'timestamp': datetime.now().isoformat(),
                'platform': platform,
                'error': str(e),
                'status': 'failed'
            })
            raise
    
    def create_facebook_pixel_if_not_exists(self):
        """
        Cria pixel do Facebook automaticamente se não existir
        Configura eventos padrão
        """
        try:
            # Verificar se pixel já existe
            existing_pixel = self._check_existing_pixel()
            
            if existing_pixel:
                logger.info(f"Pixel já existe: {existing_pixel['id']}")
                return {
                    'step': 'pixel_verification',
                    'action': 'existing_pixel_found',
                    'pixel_id': existing_pixel['id'],
                    'status': 'ok'
                }
            
            # Criar novo pixel
            pixel_id = self._create_new_pixel()
            
            # Configurar eventos padrão
            events_configured = self._configure_standard_events(pixel_id)
            
            return {
                'step': 'pixel_creation',
                'action': 'new_pixel_created',
                'pixel_id': pixel_id,
                'events': events_configured,
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar pixel: {e}")
            return {
                'step': 'pixel_creation',
                'action': 'error',
                'error': str(e),
                'status': 'failed'
            }
    
    def _check_existing_pixel(self):
        """Verifica se pixel já existe"""
        # TODO: Integração real com Facebook API
        # Por enquanto, retorna None (não existe)
        return None
    
    def _create_new_pixel(self):
        """Cria novo pixel do Facebook"""
        # TODO: Integração real com Facebook API
        # Por enquanto, retorna ID simulado
        pixel_id = f"pixel_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"Pixel criado: {pixel_id}")
        return pixel_id
    
    def _configure_standard_events(self, pixel_id):
        """
        Configura eventos padrão do pixel:
        - ViewContent
        - AddToCart
        - InitiateCheckout
        - Purchase
        """
        standard_events = [
            'ViewContent',
            'AddToCart',
            'InitiateCheckout',
            'Purchase'
        ]
        
        configured_events = []
        
        for event in standard_events:
            # TODO: Configuração real via API
            configured_events.append({
                'event_name': event,
                'pixel_id': pixel_id,
                'status': 'configured'
            })
            logger.info(f"Evento configurado: {event}")
        
        return configured_events
    
    def create_campaign(self, strategy, daily_budget, start_date, end_date, platform):
        """Cria campanha na plataforma com duração definida"""
        try:
            campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            campaign_data = {
                'id': campaign_id,
                'name': f"Campanha {strategy.get('product', 'Produto')}",
                'objective': strategy.get('objective', 'CONVERSIONS'),
                'daily_budget': int(daily_budget * 100),  # Em centavos para Facebook
                'start_time': start_date.isoformat(),
                'end_time': end_date.isoformat(),
                'platform': platform,
                'status': 'created'
            }
            
            # TODO: Criação real via API
            logger.info(f"Campanha criada: {campaign_id}")
            
            return {
                'step': 'campaign_creation',
                'campaign_id': campaign_id,
                'data': campaign_data,
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar campanha: {e}")
            raise
    
    def create_ad_set(self, campaign_id, strategy, daily_budget, start_date, end_date):
        """Cria conjunto de anúncios com duração definida"""
        try:
            adset_id = f"adset_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            adset_data = {
                'id': adset_id,
                'campaign_id': campaign_id,
                'name': 'Conjunto Principal',
                'daily_budget': int(daily_budget * 100),  # Em centavos
                'start_time': start_date.isoformat(),
                'end_time': end_date.isoformat(),
                'status': 'created'
            }
            
            # TODO: Criação real via API
            logger.info(f"Conjunto criado: {adset_id}")
            
            return {
                'step': 'adset_creation',
                'adset_id': adset_id,
                'data': adset_data,
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar conjunto: {e}")
            raise
    
    def create_ads(self, adset_id, copy):
        """Cria anúncios (3 variações de teste A/B)"""
        try:
            ads_created = []
            
            headlines = copy.get('headlines', ['Headline padrão'])
            ctas = copy.get('ctas', ['Saiba Mais'])
            
            # Criar 3 variações
            for i in range(min(3, len(headlines))):
                ad_id = f"ad_{i+1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                ad_data = {
                    'id': ad_id,
                    'adset_id': adset_id,
                    'name': f'Variação {chr(65+i)}',  # A, B, C
                    'headline': headlines[i] if i < len(headlines) else headlines[0],
                    'cta': ctas[i] if i < len(ctas) else ctas[0],
                    'body': copy.get('full_copy', ''),
                    'status': 'created'
                }
                
                # TODO: Criação real via API
                logger.info(f"Anúncio criado: {ad_id}")
                
                ads_created.append({
                    'step': f'ad_creation_{i+1}',
                    'ad_id': ad_id,
                    'data': ad_data,
                    'status': 'created'
                })
            
            return ads_created
            
        except Exception as e:
            logger.error(f"Erro ao criar anúncios: {e}")
            raise
    
    def apply_budget(self, campaign_id, budget):
        """Aplica orçamento corretamente"""
        try:
            # TODO: Aplicação real via API
            logger.info(f"Orçamento aplicado: R$ {budget:.2f}")
            
            return {
                'step': 'budget_application',
                'campaign_id': campaign_id,
                'budget': budget,
                'status': 'applied'
            }
            
        except Exception as e:
            logger.error(f"Erro ao aplicar orçamento: {e}")
            raise
    
    def publish_campaign(self, campaign_id):
        """Publica campanha"""
        try:
            # TODO: Publicação real via API
            logger.info(f"Campanha publicada: {campaign_id}")
            
            return {
                'step': 'campaign_publication',
                'campaign_id': campaign_id,
                'status': 'published',
                'published_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao publicar campanha: {e}")
            raise
    
    def _log_execution(self, log_entry):
        """Registra log de execução"""
        self.execution_log.append(log_entry)
        
        try:
            os.makedirs('logs/manus_execution', exist_ok=True)
            
            log_file = 'logs/manus_execution/execution.jsonl'
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            logger.error(f"Erro ao salvar log: {e}")
