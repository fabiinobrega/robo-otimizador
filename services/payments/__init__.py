"""
Services de Pagamentos - NEXORA PRIME
Serviços para processamento de pagamentos, créditos e integrações
"""

# Imports seguros com fallback
try:
    from .stripe_payment_service import StripePaymentService
except ImportError:
    StripePaymentService = None

try:
    from .stripe_webhook_handler import StripeWebhookHandler
except ImportError:
    StripeWebhookHandler = None

try:
    from .credit_wallet_service import CreditWalletService
except ImportError:
    CreditWalletService = None

try:
    from .facebook_ads_funding_service import FacebookAdsFundingService
except ImportError:
    FacebookAdsFundingService = None

try:
    from .google_ads_funding_service import GoogleAdsFundingService
except ImportError:
    GoogleAdsFundingService = None

try:
    from .payment_security_blocks import PaymentSecurityBlocks
except ImportError:
    PaymentSecurityBlocks = None

try:
    from .payment_audit_log import PaymentAuditLog
except ImportError:
    PaymentAuditLog = None

try:
    from .manus_payment_commands import ManusPaymentCommands
except ImportError:
    ManusPaymentCommands = None

__all__ = [
    'StripePaymentService',
    'StripeWebhookHandler',
    'CreditWalletService',
    'FacebookAdsFundingService',
    'GoogleAdsFundingService',
    'PaymentSecurityBlocks',
    'PaymentAuditLog',
    'ManusPaymentCommands'
]
