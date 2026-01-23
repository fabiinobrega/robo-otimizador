# services/legal_governance_automation.py
"""
NEXORA PRIME - Camada Legal / Governança Automática
Compliance por região e políticas de plataforma
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class LegalGovernanceAutomation:
    """Sistema de governança legal e compliance automático."""
    
    def __init__(self):
        self.regional_policies = {
            "GDPR": {
                "applies_to": ["EU", "EEA"],
                "rules": ["consent_required", "data_anonymization", "right_to_erasure"],
                "penalties": "Até 4% do faturamento global"
            },
            "LGPD": {
                "applies_to": ["BR"],
                "rules": ["consent_required", "legitimate_interest", "data_portability"],
                "penalties": "Até 2% do faturamento, limitado a R$50M"
            },
            "CCPA": {
                "applies_to": ["US-CA"],
                "rules": ["right_to_opt_out", "right_to_know", "right_to_delete"],
                "penalties": "Até $7.500 por violação intencional"
            },
            "COPPA": {
                "applies_to": ["US"],
                "rules": ["parental_consent_under_13", "no_behavioral_targeting_children"],
                "penalties": "Até $50.000 por violação"
            }
        }
        self.platform_policies = {
            "meta": {
                "prohibited_content": ["tobacco", "weapons", "adult_content", "misleading_claims"],
                "restricted_content": ["alcohol", "gambling", "cryptocurrency", "political"],
                "special_categories": ["credit", "employment", "housing", "social_issues"]
            },
            "google": {
                "prohibited_content": ["counterfeit", "dangerous_products", "dishonest_behavior"],
                "restricted_content": ["alcohol", "gambling", "healthcare", "financial"],
                "special_categories": ["personalized_advertising", "sensitive_categories"]
            }
        }
        self.compliance_checks = []
        self.violations = []
    
    def check_compliance(self, campaign_context: Dict) -> Dict:
        """Verifica a conformidade da campanha com todas as políticas aplicáveis."""
        region = campaign_context.get("region", "BR")
        platform = campaign_context.get("platform", "meta")
        content_type = campaign_context.get("content_type", "general")
        
        issues = []
        warnings = []
        
        # Verificar políticas regionais
        for policy_name, policy in self.regional_policies.items():
            if region in policy["applies_to"]:
                for rule in policy["rules"]:
                    if not self._is_rule_compliant(rule, campaign_context):
                        issues.append({
                            "policy": policy_name,
                            "rule": rule,
                            "severity": "critical",
                            "message": f"Não conformidade com {policy_name}: {rule}"
                        })
        
        # Verificar políticas de plataforma
        platform_policy = self.platform_policies.get(platform, {})
        
        if content_type in platform_policy.get("prohibited_content", []):
            issues.append({
                "policy": f"{platform}_policy",
                "rule": "prohibited_content",
                "severity": "critical",
                "message": f"Conteúdo proibido na plataforma {platform}: {content_type}"
            })
        
        if content_type in platform_policy.get("restricted_content", []):
            warnings.append({
                "policy": f"{platform}_policy",
                "rule": "restricted_content",
                "severity": "warning",
                "message": f"Conteúdo restrito na plataforma {platform}: {content_type}. Requer aprovação especial."
            })
        
        if content_type in platform_policy.get("special_categories", []):
            warnings.append({
                "policy": f"{platform}_policy",
                "rule": "special_category",
                "severity": "info",
                "message": f"Categoria especial detectada: {content_type}. Segmentação limitada."
            })
        
        # Registrar verificação
        check_record = {
            "campaign_context": campaign_context,
            "issues": issues,
            "warnings": warnings,
            "checked_at": datetime.now().isoformat(),
            "compliant": len(issues) == 0
        }
        self.compliance_checks.append(check_record)
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "recommendations": self._generate_compliance_recommendations(issues, warnings)
        }
    
    def _is_rule_compliant(self, rule: str, context: Dict) -> bool:
        """Verifica se uma regra específica está sendo cumprida."""
        if rule == "consent_required":
            return context.get("has_consent", False)
        if rule == "data_anonymization":
            return context.get("is_anonymized", False)
        if rule == "legitimate_interest":
            return context.get("has_legitimate_interest", False)
        if rule == "right_to_opt_out":
            return context.get("opt_out_available", False)
        if rule == "parental_consent_under_13":
            return not context.get("targets_children", False) or context.get("has_parental_consent", False)
        return True
    
    def _generate_compliance_recommendations(self, issues: List[Dict], warnings: List[Dict]) -> List[str]:
        """Gera recomendações para resolver problemas de compliance."""
        recommendations = []
        
        for issue in issues:
            if "consent_required" in issue.get("rule", ""):
                recommendations.append("Implemente mecanismo de consentimento explícito antes da coleta de dados")
            if "data_anonymization" in issue.get("rule", ""):
                recommendations.append("Anonimize dados pessoais antes do processamento")
            if "prohibited_content" in issue.get("rule", ""):
                recommendations.append("Revise o conteúdo da campanha para remover elementos proibidos")
        
        for warning in warnings:
            if "restricted_content" in warning.get("rule", ""):
                recommendations.append("Solicite aprovação especial para conteúdo restrito")
            if "special_category" in warning.get("rule", ""):
                recommendations.append("Ajuste a segmentação para categorias especiais")
        
        return recommendations
    
    def get_applicable_policies(self, region: str, platform: str) -> Dict:
        """Retorna as políticas aplicáveis para uma região e plataforma."""
        applicable = {
            "regional_policies": [],
            "platform_policies": {}
        }
        
        for policy_name, policy in self.regional_policies.items():
            if region in policy["applies_to"]:
                applicable["regional_policies"].append({
                    "name": policy_name,
                    "rules": policy["rules"],
                    "penalties": policy["penalties"]
                })
        
        if platform in self.platform_policies:
            applicable["platform_policies"] = self.platform_policies[platform]
        
        return applicable
    
    def report_violation(self, violation: Dict) -> Dict:
        """Registra uma violação de compliance."""
        violation_record = {
            **violation,
            "reported_at": datetime.now().isoformat(),
            "status": "open"
        }
        self.violations.append(violation_record)
        return violation_record
    
    def get_compliance_report(self) -> Dict:
        """Gera relatório de compliance."""
        return {
            "total_checks": len(self.compliance_checks),
            "compliant_checks": len([c for c in self.compliance_checks if c["compliant"]]),
            "non_compliant_checks": len([c for c in self.compliance_checks if not c["compliant"]]),
            "open_violations": len([v for v in self.violations if v["status"] == "open"]),
            "recent_checks": self.compliance_checks[-10:] if self.compliance_checks else []
        }
    
    def get_system_status(self) -> Dict:
        """Retorna o status do sistema de governança legal."""
        return {
            "regional_policies_count": len(self.regional_policies),
            "platform_policies_count": len(self.platform_policies),
            "total_compliance_checks": len(self.compliance_checks),
            "total_violations": len(self.violations)
        }


legal_governance = LegalGovernanceAutomation()
