"""
Services Package
Módulo de serviços do NEXORA PRIME
"""

class ServicesPackage:
    """Classe para o pacote de serviços"""
    
    def __init__(self):
        """Inicializar pacote"""
        self.name = "NEXORA PRIME Services"
        self.version = "12.0"
    
    def get_info(self):
        """Obter informações do pacote"""
        return {
            "name": self.name,
            "version": self.version,
            "status": "active"
        }
