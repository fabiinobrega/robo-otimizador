#!/usr/bin/env python3.11
"""
OTIMIZAÇÃO DE PERFORMANCE E CONVERSÃO - NEXORA PRIME v11.7
Script para otimizar velocidade, carregamento e taxa de conversão
"""

import os
import gzip
import shutil
from pathlib import Path
import json

class PerformanceOptimizer:
    """Otimizador de performance do sistema"""
    
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.results = {
            "optimizations": [],
            "before": {},
            "after": {},
            "improvements": {}
        }
    
    def optimize_static_files(self):
        """Otimizar arquivos estáticos (CSS, JS)"""
        static_dir = self.root / "static"
        
        if not static_dir.exists():
            return
        
        # Minificar CSS
        css_files = list(static_dir.rglob("*.css"))
        for css_file in css_files:
            if "_min" not in css_file.name:
                self._minify_css(css_file)
        
        # Minificar JS
        js_files = list(static_dir.rglob("*.js"))
        for js_file in js_files:
            if "_min" not in js_file.name:
                self._minify_js(js_file)
        
        self.results["optimizations"].append("Arquivos estáticos otimizados")
    
    def _minify_css(self, css_file):
        """Minificar arquivo CSS"""
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remover comentários
            import re
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            # Remover espaços desnecessários
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'\s*([{}:;,])\s*', r'\1', content)
            
            # Salvar versão minificada
            min_file = css_file.parent / f"{css_file.stem}_min{css_file.suffix}"
            with open(min_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            original_size = css_file.stat().st_size
            minified_size = min_file.stat().st_size
            reduction = ((original_size - minified_size) / original_size) * 100
            
            self.results["optimizations"].append(
                f"CSS minificado: {css_file.name} ({reduction:.1f}% redução)"
            )
        except Exception as e:
            print(f"Erro ao minificar {css_file}: {e}")
    
    def _minify_js(self, js_file):
        """Minificar arquivo JS"""
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remover comentários
            import re
            content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
            # Remover espaços desnecessários
            content = re.sub(r'\s+', ' ', content)
            
            # Salvar versão minificada
            min_file = js_file.parent / f"{js_file.stem}_min{js_file.suffix}"
            with open(min_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            original_size = js_file.stat().st_size
            minified_size = min_file.stat().st_size
            reduction = ((original_size - minified_size) / original_size) * 100
            
            self.results["optimizations"].append(
                f"JS minificado: {js_file.name} ({reduction:.1f}% redução)"
            )
        except Exception as e:
            print(f"Erro ao minificar {js_file}: {e}")
    
    def create_gzip_versions(self):
        """Criar versões gzip de arquivos estáticos"""
        static_dir = self.root / "static"
        
        if not static_dir.exists():
            return
        
        # Arquivos para comprimir
        files_to_compress = []
        files_to_compress.extend(static_dir.rglob("*.css"))
        files_to_compress.extend(static_dir.rglob("*.js"))
        files_to_compress.extend(static_dir.rglob("*.json"))
        
        for file_path in files_to_compress:
            if ".gz" not in file_path.name:
                self._create_gzip(file_path)
        
        self.results["optimizations"].append("Versões gzip criadas")
    
    def _create_gzip(self, file_path):
        """Criar versão gzip de um arquivo"""
        try:
            gz_path = Path(str(file_path) + ".gz")
            
            with open(file_path, 'rb') as f_in:
                with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            original_size = file_path.stat().st_size
            compressed_size = gz_path.stat().st_size
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            self.results["optimizations"].append(
                f"Gzip criado: {file_path.name} ({reduction:.1f}% redução)"
            )
        except Exception as e:
            print(f"Erro ao criar gzip de {file_path}: {e}")
    
    def optimize_database(self):
        """Otimizar banco de dados"""
        db_file = self.root / "database.db"
        
        if not db_file.exists():
            return
        
        try:
            import sqlite3
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # VACUUM para compactar banco
            cursor.execute("VACUUM")
            
            # ANALYZE para otimizar queries
            cursor.execute("ANALYZE")
            
            conn.commit()
            conn.close()
            
            self.results["optimizations"].append("Banco de dados otimizado (VACUUM + ANALYZE)")
        except Exception as e:
            print(f"Erro ao otimizar banco: {e}")
    
    def create_conversion_optimizations(self):
        """Criar otimizações para conversão"""
        optimizations = {
            "cta_buttons": {
                "primary_color": "#6366f1",
                "hover_effect": "scale(1.05)",
                "position": "above_fold",
                "text": "Começar Agora - Grátis"
            },
            "social_proof": {
                "testimonials": True,
                "case_studies": True,
                "client_logos": True,
                "stats": ["1000+ clientes", "98% satisfação", "R$ 10M+ gerenciados"]
            },
            "urgency_triggers": {
                "limited_time_offer": True,
                "countdown_timer": True,
                "stock_indicator": True
            },
            "trust_signals": {
                "ssl_badge": True,
                "money_back_guarantee": True,
                "free_trial": True,
                "no_credit_card": True
            },
            "form_optimization": {
                "fields_count": "minimal",
                "autofill": True,
                "progress_indicator": True,
                "inline_validation": True
            }
        }
        
        # Salvar configurações
        config_file = self.root / "conversion_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(optimizations, f, indent=2, ensure_ascii=False)
        
        self.results["optimizations"].append("Configurações de conversão criadas")
    
    def generate_report(self):
        """Gerar relatório de otimizações"""
        print("=" * 100)
        print("OTIMIZAÇÃO DE PERFORMANCE E CONVERSÃO - NEXORA PRIME v11.7")
        print("=" * 100)
        print()
        
        print("✅ OTIMIZAÇÕES APLICADAS")
        print("-" * 100)
        for opt in self.results["optimizations"]:
            print(f"  ✓ {opt}")
        print()
        
        print("📊 RECOMENDAÇÕES ADICIONAIS")
        print("-" * 100)
        recommendations = [
            "Implementar cache Redis para APIs",
            "Usar CDN para arquivos estáticos",
            "Implementar lazy loading de imagens",
            "Adicionar service worker para PWA",
            "Implementar HTTP/2 Server Push",
            "Otimizar queries SQL com índices",
            "Implementar rate limiting",
            "Adicionar monitoramento de performance (New Relic, Datadog)",
            "Implementar A/B testing framework",
            "Adicionar analytics de conversão (Google Analytics, Mixpanel)"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        print()
        
        print("=" * 100)
        print("OTIMIZAÇÃO CONCLUÍDA")
        print("=" * 100)

if __name__ == "__main__":
    optimizer = PerformanceOptimizer("/home/ubuntu/robo-otimizador")
    
    print("Iniciando otimização...")
    print()
    
    optimizer.optimize_static_files()
    optimizer.create_gzip_versions()
    optimizer.optimize_database()
    optimizer.create_conversion_optimizations()
    optimizer.generate_report()
