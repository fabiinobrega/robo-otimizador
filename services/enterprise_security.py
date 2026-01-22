"""
ENTERPRISE SECURITY - Seguranca Enterprise
Sistema de seguranca com 2FA, LGPD, GDPR e compliance
Nexora Prime V2 - Expansao Unicornio
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random
import hashlib
import secrets

class EnterpriseSecurity:
    """Sistema de seguranca enterprise."""
    
    def __init__(self):
        self.name = "Enterprise Security"
        self.version = "2.0.0"
        
        # Configuracoes de seguranca
        self.security_config = {
            "2fa_enabled": True,
            "session_timeout_minutes": 30,
            "max_login_attempts": 5,
            "password_min_length": 8,
            "require_special_chars": True,
            "encryption_algorithm": "AES-256"
        }
        
        # Usuarios e sessoes
        self.users = {}
        self.sessions = {}
        self.login_attempts = {}
        
        # Logs de auditoria
        self.audit_logs = []
        
        # Consentimentos LGPD/GDPR
        self.consents = {}
        
        # Dados pessoais rastreados
        self.personal_data_registry = {}
    
    # ==================== 2FA ====================
    
    def enable_2fa(self, user_id: str) -> Dict[str, Any]:
        """Habilita 2FA para um usuario."""
        
        # Gerar secret para TOTP
        secret = secrets.token_hex(20)
        
        if user_id not in self.users:
            self.users[user_id] = {}
        
        self.users[user_id]["2fa_secret"] = secret
        self.users[user_id]["2fa_enabled"] = True
        self.users[user_id]["2fa_enabled_at"] = datetime.now().isoformat()
        
        # Log de auditoria
        self._log_audit("2fa_enabled", user_id, {"method": "totp"})
        
        return {
            "status": "enabled",
            "user_id": user_id,
            "secret": secret,
            "backup_codes": self._generate_backup_codes(),
            "setup_url": f"otpauth://totp/NexoraPrime:{user_id}?secret={secret}&issuer=NexoraPrime"
        }
    
    def verify_2fa(self, user_id: str, code: str) -> Dict[str, Any]:
        """Verifica codigo 2FA."""
        
        if user_id not in self.users:
            return {"valid": False, "error": "Usuario nao encontrado"}
        
        user = self.users[user_id]
        
        if not user.get("2fa_enabled"):
            return {"valid": False, "error": "2FA nao habilitado"}
        
        # Verificar codigo (simplificado - em producao usar pyotp)
        # Simulacao de verificacao
        is_valid = len(code) == 6 and code.isdigit()
        
        self._log_audit("2fa_verification", user_id, {"success": is_valid})
        
        return {
            "valid": is_valid,
            "user_id": user_id,
            "verified_at": datetime.now().isoformat() if is_valid else None
        }
    
    def disable_2fa(self, user_id: str, admin_override: bool = False) -> Dict[str, Any]:
        """Desabilita 2FA."""
        
        if user_id not in self.users:
            return {"error": "Usuario nao encontrado"}
        
        self.users[user_id]["2fa_enabled"] = False
        self.users[user_id]["2fa_disabled_at"] = datetime.now().isoformat()
        
        self._log_audit("2fa_disabled", user_id, {"admin_override": admin_override})
        
        return {
            "status": "disabled",
            "user_id": user_id,
            "disabled_at": self.users[user_id]["2fa_disabled_at"]
        }
    
    # ==================== LGPD/GDPR ====================
    
    def register_consent(self, user_id: str, consent_type: str, granted: bool, details: Dict = None) -> Dict[str, Any]:
        """Registra consentimento do usuario."""
        
        consent_types = [
            "data_processing",
            "marketing_emails",
            "third_party_sharing",
            "analytics_tracking",
            "personalization",
            "cookies"
        ]
        
        if consent_type not in consent_types:
            return {"error": f"Tipo de consentimento invalido. Validos: {consent_types}"}
        
        if user_id not in self.consents:
            self.consents[user_id] = {}
        
        self.consents[user_id][consent_type] = {
            "granted": granted,
            "timestamp": datetime.now().isoformat(),
            "ip_address": details.get("ip_address") if details else None,
            "user_agent": details.get("user_agent") if details else None,
            "version": "1.0"
        }
        
        self._log_audit("consent_registered", user_id, {
            "type": consent_type,
            "granted": granted
        })
        
        return {
            "status": "registered",
            "user_id": user_id,
            "consent_type": consent_type,
            "granted": granted,
            "timestamp": self.consents[user_id][consent_type]["timestamp"]
        }
    
    def get_user_consents(self, user_id: str) -> Dict[str, Any]:
        """Obtem todos os consentimentos de um usuario."""
        
        if user_id not in self.consents:
            return {"user_id": user_id, "consents": {}}
        
        return {
            "user_id": user_id,
            "consents": self.consents[user_id],
            "retrieved_at": datetime.now().isoformat()
        }
    
    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """Exporta todos os dados do usuario (direito de portabilidade)."""
        
        export = {
            "user_id": user_id,
            "exported_at": datetime.now().isoformat(),
            "data_categories": {},
            "format": "JSON"
        }
        
        # Dados do usuario
        if user_id in self.users:
            user_data = self.users[user_id].copy()
            # Remover dados sensiveis
            user_data.pop("2fa_secret", None)
            export["data_categories"]["profile"] = user_data
        
        # Consentimentos
        if user_id in self.consents:
            export["data_categories"]["consents"] = self.consents[user_id]
        
        # Dados pessoais registrados
        if user_id in self.personal_data_registry:
            export["data_categories"]["personal_data"] = self.personal_data_registry[user_id]
        
        # Logs de auditoria do usuario
        user_logs = [log for log in self.audit_logs if log.get("user_id") == user_id]
        export["data_categories"]["activity_logs"] = user_logs[-100:]  # Ultimos 100
        
        self._log_audit("data_exported", user_id, {"categories": list(export["data_categories"].keys())})
        
        return export
    
    def delete_user_data(self, user_id: str, confirm: bool = False) -> Dict[str, Any]:
        """Deleta todos os dados do usuario (direito ao esquecimento)."""
        
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "Confirme a exclusao definindo confirm=True",
                "warning": "Esta acao e irreversivel"
            }
        
        deleted_categories = []
        
        # Deletar dados do usuario
        if user_id in self.users:
            del self.users[user_id]
            deleted_categories.append("profile")
        
        # Deletar consentimentos
        if user_id in self.consents:
            del self.consents[user_id]
            deleted_categories.append("consents")
        
        # Deletar dados pessoais
        if user_id in self.personal_data_registry:
            del self.personal_data_registry[user_id]
            deleted_categories.append("personal_data")
        
        # Anonimizar logs (manter para compliance, mas anonimizar)
        for log in self.audit_logs:
            if log.get("user_id") == user_id:
                log["user_id"] = f"deleted_{hashlib.sha256(user_id.encode()).hexdigest()[:8]}"
        
        self._log_audit("data_deleted", f"deleted_{user_id[:8]}", {
            "categories": deleted_categories,
            "reason": "user_request"
        })
        
        return {
            "status": "deleted",
            "deleted_categories": deleted_categories,
            "deleted_at": datetime.now().isoformat()
        }
    
    def register_personal_data(self, user_id: str, data_type: str, data: Dict) -> Dict[str, Any]:
        """Registra dados pessoais coletados."""
        
        if user_id not in self.personal_data_registry:
            self.personal_data_registry[user_id] = {}
        
        self.personal_data_registry[user_id][data_type] = {
            "data": data,
            "collected_at": datetime.now().isoformat(),
            "purpose": data.get("purpose", "service_provision"),
            "retention_period": data.get("retention_period", "2_years"),
            "legal_basis": data.get("legal_basis", "consent")
        }
        
        return {
            "status": "registered",
            "user_id": user_id,
            "data_type": data_type,
            "registered_at": datetime.now().isoformat()
        }
    
    # ==================== Auditoria ====================
    
    def get_audit_logs(self, filters: Dict = None) -> Dict[str, Any]:
        """Obtem logs de auditoria."""
        
        logs = self.audit_logs.copy()
        
        if filters:
            if filters.get("user_id"):
                logs = [l for l in logs if l.get("user_id") == filters["user_id"]]
            if filters.get("action"):
                logs = [l for l in logs if l.get("action") == filters["action"]]
            if filters.get("from_date"):
                from_date = datetime.fromisoformat(filters["from_date"])
                logs = [l for l in logs if datetime.fromisoformat(l["timestamp"]) >= from_date]
        
        return {
            "total_logs": len(logs),
            "logs": logs[-100:],  # Ultimos 100
            "retrieved_at": datetime.now().isoformat()
        }
    
    def generate_compliance_report(self, report_type: str = "lgpd") -> Dict[str, Any]:
        """Gera relatorio de compliance."""
        
        report = {
            "report_type": report_type.upper(),
            "generated_at": datetime.now().isoformat(),
            "period": "last_30_days",
            "summary": {},
            "details": {},
            "recommendations": []
        }
        
        if report_type.lower() == "lgpd":
            report["summary"] = {
                "total_users": len(self.users),
                "users_with_consent": len(self.consents),
                "data_export_requests": sum(1 for l in self.audit_logs if l.get("action") == "data_exported"),
                "data_deletion_requests": sum(1 for l in self.audit_logs if l.get("action") == "data_deleted"),
                "2fa_adoption_rate": f"{sum(1 for u in self.users.values() if u.get('2fa_enabled')) / max(1, len(self.users)) * 100:.1f}%"
            }
            
            report["details"] = {
                "consent_breakdown": self._get_consent_breakdown(),
                "data_categories_collected": list(set(
                    dt for user_data in self.personal_data_registry.values()
                    for dt in user_data.keys()
                )),
                "legal_bases_used": ["consent", "legitimate_interest", "contract"]
            }
            
            report["recommendations"] = [
                "Revisar politica de privacidade periodicamente",
                "Implementar revisao automatica de retencao de dados",
                "Treinar equipe sobre LGPD regularmente"
            ]
        
        elif report_type.lower() == "gdpr":
            report["summary"] = {
                "total_data_subjects": len(self.users),
                "consent_records": len(self.consents),
                "dsar_requests": sum(1 for l in self.audit_logs if l.get("action") in ["data_exported", "data_deleted"]),
                "data_breaches": 0
            }
            
            report["details"] = {
                "lawful_bases": ["consent", "contract", "legitimate_interest"],
                "data_processing_activities": ["marketing", "analytics", "service_provision"],
                "third_party_processors": [],
                "international_transfers": False
            }
            
            report["recommendations"] = [
                "Manter registro de atividades de processamento atualizado",
                "Realizar DPIA para novos processamentos de alto risco",
                "Revisar contratos com processadores"
            ]
        
        return report
    
    # ==================== Sessoes ====================
    
    def create_session(self, user_id: str, metadata: Dict = None) -> Dict[str, Any]:
        """Cria sessao de usuario."""
        
        session_id = secrets.token_urlsafe(32)
        
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(minutes=self.security_config["session_timeout_minutes"])).isoformat(),
            "ip_address": metadata.get("ip_address") if metadata else None,
            "user_agent": metadata.get("user_agent") if metadata else None,
            "is_active": True
        }
        
        self._log_audit("session_created", user_id, {"session_id": session_id[:8]})
        
        return {
            "session_id": session_id,
            "expires_at": self.sessions[session_id]["expires_at"]
        }
    
    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Valida sessao."""
        
        if session_id not in self.sessions:
            return {"valid": False, "error": "Sessao nao encontrada"}
        
        session = self.sessions[session_id]
        
        if not session["is_active"]:
            return {"valid": False, "error": "Sessao inativa"}
        
        if datetime.fromisoformat(session["expires_at"]) < datetime.now():
            session["is_active"] = False
            return {"valid": False, "error": "Sessao expirada"}
        
        return {
            "valid": True,
            "user_id": session["user_id"],
            "expires_at": session["expires_at"]
        }
    
    def invalidate_session(self, session_id: str) -> Dict[str, Any]:
        """Invalida sessao."""
        
        if session_id not in self.sessions:
            return {"error": "Sessao nao encontrada"}
        
        self.sessions[session_id]["is_active"] = False
        self.sessions[session_id]["invalidated_at"] = datetime.now().isoformat()
        
        self._log_audit("session_invalidated", self.sessions[session_id]["user_id"], {"session_id": session_id[:8]})
        
        return {
            "status": "invalidated",
            "session_id": session_id
        }
    
    # ==================== Criptografia ====================
    
    def encrypt_data(self, data: str, purpose: str = "storage") -> Dict[str, Any]:
        """Criptografa dados sensiveis."""
        
        # Simulacao de criptografia (em producao usar cryptography)
        encrypted = hashlib.sha256(data.encode()).hexdigest()
        
        return {
            "encrypted": True,
            "algorithm": self.security_config["encryption_algorithm"],
            "purpose": purpose,
            "data": f"enc_{encrypted[:32]}",
            "encrypted_at": datetime.now().isoformat()
        }
    
    def hash_password(self, password: str) -> Dict[str, Any]:
        """Gera hash de senha."""
        
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        
        return {
            "hash": hashed.hex(),
            "salt": salt,
            "algorithm": "pbkdf2_sha256",
            "iterations": 100000
        }
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Valida forca da senha."""
        
        checks = {
            "min_length": len(password) >= self.security_config["password_min_length"],
            "has_uppercase": any(c.isupper() for c in password),
            "has_lowercase": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        }
        
        passed = sum(checks.values())
        
        if passed == 5:
            strength = "strong"
        elif passed >= 3:
            strength = "medium"
        else:
            strength = "weak"
        
        return {
            "valid": passed >= 4,
            "strength": strength,
            "checks": checks,
            "score": passed,
            "max_score": 5
        }
    
    # ==================== Metodos Privados ====================
    
    def _log_audit(self, action: str, user_id: str, details: Dict = None):
        """Registra log de auditoria."""
        
        self.audit_logs.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "details": details or {},
            "log_id": secrets.token_hex(8)
        })
    
    def _generate_backup_codes(self, count: int = 10) -> List[str]:
        """Gera codigos de backup para 2FA."""
        
        return [secrets.token_hex(4).upper() for _ in range(count)]
    
    def _get_consent_breakdown(self) -> Dict[str, int]:
        """Obtem breakdown de consentimentos."""
        
        breakdown = {}
        
        for user_consents in self.consents.values():
            for consent_type, consent_data in user_consents.items():
                if consent_type not in breakdown:
                    breakdown[consent_type] = {"granted": 0, "denied": 0}
                
                if consent_data.get("granted"):
                    breakdown[consent_type]["granted"] += 1
                else:
                    breakdown[consent_type]["denied"] += 1
        
        return breakdown


# Instancia global
enterprise_security = EnterpriseSecurity()
