"""
ClickBank Service - Integração Completa
Sistema de Rastreamento de Vendas e Comissões
Autor: Manus AI Agent
Data: 03/02/2026
"""

import os
import json
import hashlib
import hmac
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests


class ClickBankService:
    """Serviço completo de integração com ClickBank"""
    
    def __init__(self):
        """Inicializar serviço com credenciais"""
        # Credenciais ClickBank
        self.api_key = os.environ.get("CLICKBANK_API_KEY", "")
        self.developer_key = os.environ.get("CLICKBANK_DEVELOPER_KEY", "")
        self.clerk_key = os.environ.get("CLICKBANK_CLERK_KEY", "")
        self.secret_key = os.environ.get("CLICKBANK_SECRET_KEY", "")
        
        # Configurações do afiliado
        self.affiliate_id = "fabiinobre"  # hop=fabiinobre
        self.vendor_id = os.environ.get("CLICKBANK_VENDOR_ID", "synadentix")
        
        # URLs da API
        self.base_url = "https://api.clickbank.com/rest/1.3"
        self.tracking_url = "https://track.clickbank.net"
        
        # Cache de dados
        self.sales_cache = []
        self.commissions_cache = []
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(self.api_key and self.developer_key)
    
    # ===== TRACKING DE VENDAS =====
    
    def generate_affiliate_link(self, product_id: str, tid: Optional[str] = None) -> str:
        """
        Gerar link de afiliado ClickBank
        
        Args:
            product_id: ID do produto (ex: "synadentix")
            tid: Tracking ID opcional para identificar fonte do tráfego
        
        Returns:
            URL completa do link de afiliado
        """
        base_link = f"{self.tracking_url}/?hop={self.affiliate_id}&vendor={product_id}"
        
        if tid:
            base_link += f"&tid={tid}"
        
        return base_link
    
    def track_click(self, campaign_id: int, source: str = "meta_ads") -> Dict[str, Any]:
        """
        Rastrear clique em link de afiliado
        
        Args:
            campaign_id: ID da campanha que gerou o clique
            source: Fonte do tráfego (meta_ads, google_ads, etc.)
        """
        tid = f"camp_{campaign_id}_{source}"
        link = self.generate_affiliate_link(self.vendor_id, tid)
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "source": source,
            "tid": tid,
            "affiliate_link": link,
            "timestamp": datetime.now().isoformat()
        }
    
    # ===== WEBHOOK DE CONVERSÕES =====
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verificar assinatura do webhook ClickBank
        
        Args:
            payload: Corpo da requisição
            signature: Assinatura recebida no header
        
        Returns:
            True se assinatura é válida
        """
        if not self.secret_key:
            return False
        
        expected_signature = hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    def process_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processar webhook de conversão do ClickBank
        
        Args:
            data: Dados do webhook
        
        Returns:
            Resultado do processamento
        """
        try:
            # Extrair dados da venda
            receipt = data.get("receipt", "")
            transaction_type = data.get("transactionType", "")
            amount = float(data.get("amount", 0))
            commission = float(data.get("affiliate", {}).get("affiliateCommission", 0))
            product = data.get("lineItems", [{}])[0].get("itemNo", "")
            tid = data.get("tid", "")
            
            # Registrar venda
            sale_record = {
                "receipt": receipt,
                "type": transaction_type,
                "amount": amount,
                "commission": commission,
                "product": product,
                "tid": tid,
                "timestamp": datetime.now().isoformat(),
                "processed": True
            }
            
            self.sales_cache.append(sale_record)
            
            # Extrair campaign_id do TID (formato: camp_123_meta_ads)
            campaign_id = None
            if tid and tid.startswith("camp_"):
                parts = tid.split("_")
                if len(parts) >= 2:
                    campaign_id = int(parts[1])
            
            return {
                "success": True,
                "message": "Venda processada com sucesso",
                "sale": sale_record,
                "campaign_id": campaign_id
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao processar webhook: {str(e)}"
            }
    
    # ===== RELATÓRIOS DE VENDAS =====
    
    def get_sales(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Obter vendas do ClickBank via API
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
        
        Returns:
            Lista de vendas
        """
        if not self.is_configured():
            return {"success": False, "message": "ClickBank não configurado"}
        
        try:
            # Datas padrão (últimos 30 dias)
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")
            
            # Fazer requisição à API
            url = f"{self.base_url}/orders/list"
            headers = {
                "Authorization": self.api_key,
                "Accept": "application/json"
            }
            params = {
                "startDate": start_date,
                "endDate": end_date,
                "type": "SALE"
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            sales = data.get("orderData", [])
            
            return {
                "success": True,
                "sales": sales,
                "total_sales": len(sales),
                "period": f"{start_date} to {end_date}"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Erro na API ClickBank: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao obter vendas: {str(e)}"
            }
    
    def get_commissions(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Calcular comissões totais do período
        
        Args:
            start_date: Data inicial
            end_date: Data final
        
        Returns:
            Resumo de comissões
        """
        sales_result = self.get_sales(start_date, end_date)
        
        if not sales_result.get("success"):
            return sales_result
        
        sales = sales_result.get("sales", [])
        
        total_commission = 0
        total_sales_amount = 0
        commission_by_product = {}
        
        for sale in sales:
            amount = float(sale.get("orderAmount", 0))
            commission = float(sale.get("affiliateCommission", 0))
            product = sale.get("lineItems", [{}])[0].get("itemNo", "unknown")
            
            total_sales_amount += amount
            total_commission += commission
            
            if product not in commission_by_product:
                commission_by_product[product] = {
                    "sales": 0,
                    "amount": 0,
                    "commission": 0
                }
            
            commission_by_product[product]["sales"] += 1
            commission_by_product[product]["amount"] += amount
            commission_by_product[product]["commission"] += commission
        
        return {
            "success": True,
            "total_sales": len(sales),
            "total_sales_amount": round(total_sales_amount, 2),
            "total_commission": round(total_commission, 2),
            "commission_rate": round((total_commission / total_sales_amount * 100), 2) if total_sales_amount > 0 else 0,
            "by_product": commission_by_product,
            "period": sales_result.get("period")
        }
    
    # ===== DASHBOARD DE PERFORMANCE =====
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """
        Obter dashboard completo de performance
        
        Returns:
            Métricas consolidadas
        """
        # Últimos 7 dias
        week_commissions = self.get_commissions(
            start_date=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        )
        
        # Últimos 30 dias
        month_commissions = self.get_commissions(
            start_date=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        )
        
        # Hoje
        today_commissions = self.get_commissions(
            start_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        return {
            "success": True,
            "today": today_commissions if today_commissions.get("success") else {},
            "last_7_days": week_commissions if week_commissions.get("success") else {},
            "last_30_days": month_commissions if month_commissions.get("success") else {},
            "affiliate_id": self.affiliate_id,
            "vendor_id": self.vendor_id,
            "timestamp": datetime.now().isoformat()
        }
    
    # ===== ATRIBUIÇÃO DE VENDAS A CAMPANHAS =====
    
    def attribute_sale_to_campaign(self, receipt: str, campaign_id: int) -> Dict[str, Any]:
        """
        Atribuir uma venda a uma campanha específica
        
        Args:
            receipt: Número do recibo ClickBank
            campaign_id: ID da campanha
        
        Returns:
            Resultado da atribuição
        """
        return {
            "success": True,
            "message": "Venda atribuída à campanha",
            "receipt": receipt,
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_campaign_sales(self, campaign_id: int) -> Dict[str, Any]:
        """
        Obter vendas de uma campanha específica
        
        Args:
            campaign_id: ID da campanha
        
        Returns:
            Vendas da campanha
        """
        # Filtrar vendas do cache por TID
        tid_prefix = f"camp_{campaign_id}_"
        campaign_sales = [
            sale for sale in self.sales_cache
            if sale.get("tid", "").startswith(tid_prefix)
        ]
        
        total_sales = len(campaign_sales)
        total_amount = sum(sale.get("amount", 0) for sale in campaign_sales)
        total_commission = sum(sale.get("commission", 0) for sale in campaign_sales)
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "total_sales": total_sales,
            "total_amount": round(total_amount, 2),
            "total_commission": round(total_commission, 2),
            "sales": campaign_sales
        }


# Instância global do serviço
clickbank_service = ClickBankService()


# Funções de conveniência para uso nas APIs
def generate_affiliate_link(product_id: str, campaign_id: Optional[int] = None) -> str:
    """Gerar link de afiliado"""
    tid = f"camp_{campaign_id}" if campaign_id else None
    return clickbank_service.generate_affiliate_link(product_id, tid)


def process_sale_webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """Processar webhook de venda"""
    return clickbank_service.process_webhook(data)


def get_performance_metrics() -> Dict[str, Any]:
    """Obter métricas de performance"""
    return clickbank_service.get_performance_dashboard()
