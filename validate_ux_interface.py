"""
VALIDAÇÃO DE UX E INTERFACE
Smoke tests, responsividade e acessibilidade
"""

import json
from pathlib import Path
from datetime import datetime
import re

class UXInterfaceValidator:
    """Validador de UX e Interface"""
    
    def __init__(self):
        self.base_path = Path('/home/ubuntu/robo-otimizador')
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "categories": {
                "smoke_tests": {"tests": [], "passed": 0, "failed": 0},
                "responsiveness": {"tests": [], "passed": 0, "failed": 0},
                "accessibility": {"tests": [], "passed": 0, "failed": 0},
                "css_quality": {"tests": [], "passed": 0, "failed": 0}
            }
        }
        
    def smoke_test_critical_pages(self):
        """Smoke test de páginas críticas"""
        print("🧪 Smoke Tests - Páginas Críticas...")
        cat = self.results["categories"]["smoke_tests"]
        
        critical_pages = [
            'dashboard.html',
            'create_campaign.html',
            'campaigns.html',
            'credits_dashboard.html',
            'ai_dashboard.html',
            'settings.html'
        ]
        
        templates_dir = self.base_path / 'templates'
        
        for page in critical_pages:
            page_file = templates_dir / page
            if page_file.exists():
                try:
                    with open(page_file, 'r') as f:
                        content = f.read()
                    
                    # Verificações básicas
                    checks = {
                        "has_content": len(content) > 100,
                        "has_html_tag": '<html' in content.lower() or '<!doctype' in content.lower(),
                        "has_body_tag": '<body' in content.lower(),
                        "has_title": '<title' in content.lower(),
                        "no_syntax_errors": '{{' in content or '{%' in content  # Jinja2
                    }
                    
                    if all(checks.values()):
                        cat["tests"].append({
                            "name": page,
                            "status": "PASS",
                            "size": len(content)
                        })
                        cat["passed"] += 1
                        print(f"   ✅ {page}")
                    else:
                        failed_checks = [k for k, v in checks.items() if not v]
                        cat["tests"].append({
                            "name": page,
                            "status": "FAIL",
                            "failed_checks": failed_checks
                        })
                        cat["failed"] += 1
                        print(f"   ❌ {page} - {failed_checks}")
                        
                except Exception as e:
                    cat["tests"].append({
                        "name": page,
                        "status": "FAIL",
                        "error": str(e)
                    })
                    cat["failed"] += 1
                    print(f"   ❌ {page} - erro: {str(e)}")
            else:
                cat["tests"].append({
                    "name": page,
                    "status": "FAIL",
                    "error": "Arquivo não encontrado"
                })
                cat["failed"] += 1
                print(f"   ❌ {page} - não encontrado")
    
    def test_responsiveness(self):
        """Testar responsividade"""
        print("🧪 Testando Responsividade...")
        cat = self.results["categories"]["responsiveness"]
        
        css_files = list((self.base_path / 'static' / 'css').glob('*.css'))
        
        responsive_indicators = [
            '@media',
            'max-width',
            'min-width',
            'flex',
            'grid',
            'responsive'
        ]
        
        for css_file in css_files:
            try:
                with open(css_file, 'r') as f:
                    content = f.read().lower()
                
                found_indicators = [ind for ind in responsive_indicators if ind in content]
                
                if len(found_indicators) >= 3:
                    cat["tests"].append({
                        "name": css_file.name,
                        "status": "PASS",
                        "indicators": found_indicators
                    })
                    cat["passed"] += 1
                    print(f"   ✅ {css_file.name} - {len(found_indicators)} indicadores")
                else:
                    cat["tests"].append({
                        "name": css_file.name,
                        "status": "WARNING",
                        "indicators": found_indicators,
                        "note": "Poucos indicadores de responsividade"
                    })
                    print(f"   ⚠️  {css_file.name} - apenas {len(found_indicators)} indicadores")
                    
            except Exception as e:
                cat["tests"].append({
                    "name": css_file.name,
                    "status": "FAIL",
                    "error": str(e)
                })
                cat["failed"] += 1
                print(f"   ❌ {css_file.name} - erro: {str(e)}")
    
    def test_accessibility(self):
        """Testar acessibilidade"""
        print("🧪 Testando Acessibilidade...")
        cat = self.results["categories"]["accessibility"]
        
        templates_dir = self.base_path / 'templates'
        template_files = list(templates_dir.glob('*.html'))
        
        accessibility_features = {
            'alt_attributes': r'alt=',
            'aria_labels': r'aria-label',
            'semantic_html': r'<(header|nav|main|footer|article|section)',
            'form_labels': r'<label',
            'skip_links': r'skip'
        }
        
        sample_templates = template_files[:10]  # Testar amostra
        
        for template_file in sample_templates:
            try:
                with open(template_file, 'r') as f:
                    content = f.read()
                
                found_features = {}
                for feature, pattern in accessibility_features.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    found_features[feature] = len(matches)
                
                total_features = sum(1 for count in found_features.values() if count > 0)
                
                if total_features >= 2:
                    cat["tests"].append({
                        "name": template_file.name,
                        "status": "PASS",
                        "features": found_features
                    })
                    cat["passed"] += 1
                    print(f"   ✅ {template_file.name} - {total_features} features")
                else:
                    cat["tests"].append({
                        "name": template_file.name,
                        "status": "WARNING",
                        "features": found_features,
                        "note": "Poucas features de acessibilidade"
                    })
                    print(f"   ⚠️  {template_file.name} - apenas {total_features} features")
                    
            except Exception as e:
                cat["tests"].append({
                    "name": template_file.name,
                    "status": "FAIL",
                    "error": str(e)
                })
                cat["failed"] += 1
                print(f"   ❌ {template_file.name} - erro: {str(e)}")
    
    def test_css_quality(self):
        """Testar qualidade do CSS"""
        print("🧪 Testando Qualidade do CSS...")
        cat = self.results["categories"]["css_quality"]
        
        css_dir = self.base_path / 'static' / 'css'
        if not css_dir.exists():
            print("   ⚠️  Diretório CSS não encontrado")
            return
        
        css_files = list(css_dir.glob('*.css'))
        
        for css_file in css_files:
            try:
                with open(css_file, 'r') as f:
                    content = f.read()
                
                # Métricas de qualidade
                metrics = {
                    "size_kb": len(content) / 1024,
                    "has_comments": '/*' in content,
                    "has_variables": '--' in content or ':root' in content,
                    "has_media_queries": '@media' in content,
                    "organized": '/*' in content and len(content.split('/*')) > 3
                }
                
                quality_score = sum([
                    metrics["has_comments"],
                    metrics["has_variables"],
                    metrics["has_media_queries"],
                    metrics["organized"]
                ])
                
                if quality_score >= 3:
                    cat["tests"].append({
                        "name": css_file.name,
                        "status": "PASS",
                        "metrics": metrics,
                        "quality_score": f"{quality_score}/4"
                    })
                    cat["passed"] += 1
                    print(f"   ✅ {css_file.name} - score {quality_score}/4")
                else:
                    cat["tests"].append({
                        "name": css_file.name,
                        "status": "WARNING",
                        "metrics": metrics,
                        "quality_score": f"{quality_score}/4"
                    })
                    print(f"   ⚠️  {css_file.name} - score {quality_score}/4")
                    
            except Exception as e:
                cat["tests"].append({
                    "name": css_file.name,
                    "status": "FAIL",
                    "error": str(e)
                })
                cat["failed"] += 1
                print(f"   ❌ {css_file.name} - erro: {str(e)}")
    
    def run_validation(self):
        """Executar validação completa"""
        print("=" * 80)
        print("VALIDAÇÃO DE UX E INTERFACE")
        print("=" * 80)
        print()
        
        self.smoke_test_critical_pages()
        print()
        self.test_responsiveness()
        print()
        self.test_accessibility()
        print()
        self.test_css_quality()
        print()
        
        # Calcular totais
        total_passed = sum(cat["passed"] for cat in self.results["categories"].values())
        total_failed = sum(cat["failed"] for cat in self.results["categories"].values())
        
        print("=" * 80)
        print(f"RESULTADO: {total_passed} PASSARAM | {total_failed} FALHARAM")
        print("=" * 80)
        
        # Salvar resultados
        with open('/tmp/nexora_validation_output/ux_interface_validation.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Resultados salvos em: /tmp/nexora_validation_output/ux_interface_validation.json")
        
        return self.results

if __name__ == "__main__":
    validator = UXInterfaceValidator()
    validator.run_validation()
