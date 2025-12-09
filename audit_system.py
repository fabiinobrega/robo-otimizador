#!/usr/bin/env python3.11
"""
AUDITORIA TOTAL SEMI-FORENSE - NEXORA PRIME v11.7
Varredura completa de todos os componentes do sistema
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class SystemAuditor:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.results = {
            "rotas": [],
            "templates": [],
            "services": [],
            "static_files": [],
            "apis": [],
            "problemas": [],
            "estatisticas": {}
        }
    
    def audit_routes(self):
        """Auditar todas as rotas em main.py"""
        main_py = self.root / "main.py"
        if not main_py.exists():
            self.results["problemas"].append("CRÍTICO: main.py não encontrado")
            return
        
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        routes = []
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('@app.route('):
                # Extrair rota
                match = re.search(r'@app\.route\(["\']([^"\']+)["\']', line)
                if match:
                    route_path = match.group(1)
                    # Pegar próxima linha (função)
                    if i < len(lines):
                        func_line = lines[i]
                        func_match = re.search(r'def\s+(\w+)', func_line)
                        func_name = func_match.group(1) if func_match else "unknown"
                    else:
                        func_name = "unknown"
                    
                    routes.append({
                        "path": route_path,
                        "function": func_name,
                        "line": i,
                        "type": "API" if route_path.startswith("/api/") else "PAGE"
                    })
        
        self.results["rotas"] = routes
        self.results["estatisticas"]["total_rotas"] = len(routes)
        self.results["estatisticas"]["rotas_api"] = len([r for r in routes if r["type"] == "API"])
        self.results["estatisticas"]["rotas_page"] = len([r for r in routes if r["type"] == "PAGE"])
    
    def audit_templates(self):
        """Auditar todos os templates HTML"""
        templates_dir = self.root / "templates"
        if not templates_dir.exists():
            self.results["problemas"].append("CRÍTICO: diretório templates/ não encontrado")
            return
        
        templates = []
        for html_file in templates_dir.rglob("*.html"):
            rel_path = html_file.relative_to(self.root)
            
            # Verificar sintaxe básica Jinja2
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            # Verificar tags Jinja2 não fechadas
            open_tags = content.count('{%')
            close_tags = content.count('%}')
            if open_tags != close_tags:
                issues.append(f"Tags Jinja2 desbalanceadas: {open_tags} aberturas, {close_tags} fechamentos")
            
            # Verificar variáveis não fechadas
            open_vars = content.count('{{')
            close_vars = content.count('}}')
            if open_vars != close_vars:
                issues.append(f"Variáveis Jinja2 desbalanceadas: {open_vars} aberturas, {close_vars} fechamentos")
            
            templates.append({
                "path": str(rel_path),
                "size": html_file.stat().st_size,
                "lines": len(content.split('\n')),
                "issues": issues
            })
        
        self.results["templates"] = templates
        self.results["estatisticas"]["total_templates"] = len(templates)
        self.results["estatisticas"]["templates_com_problemas"] = len([t for t in templates if t["issues"]])
    
    def audit_services(self):
        """Auditar todos os serviços Python"""
        services_dir = self.root / "services"
        if not services_dir.exists():
            self.results["problemas"].append("AVISO: diretório services/ não encontrado")
            return
        
        services = []
        for py_file in services_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            
            rel_path = py_file.relative_to(self.root)
            
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair classes
            classes = re.findall(r'class\s+(\w+)', content)
            
            # Extrair funções
            functions = re.findall(r'def\s+(\w+)', content)
            
            services.append({
                "path": str(rel_path),
                "size": py_file.stat().st_size,
                "lines": len(content.split('\n')),
                "classes": classes,
                "functions": len(functions)
            })
        
        self.results["services"] = services
        self.results["estatisticas"]["total_services"] = len(services)
    
    def audit_static_files(self):
        """Auditar arquivos estáticos (CSS, JS)"""
        static_dir = self.root / "static"
        if not static_dir.exists():
            self.results["problemas"].append("AVISO: diretório static/ não encontrado")
            return
        
        static_files = {"css": [], "js": [], "outros": []}
        
        for file_path in static_dir.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.root)
                file_info = {
                    "path": str(rel_path),
                    "size": file_path.stat().st_size
                }
                
                if file_path.suffix == ".css":
                    static_files["css"].append(file_info)
                elif file_path.suffix == ".js":
                    static_files["js"].append(file_info)
                else:
                    static_files["outros"].append(file_info)
        
        self.results["static_files"] = static_files
        self.results["estatisticas"]["total_css"] = len(static_files["css"])
        self.results["estatisticas"]["total_js"] = len(static_files["js"])
    
    def check_integrations(self):
        """Verificar status das integrações"""
        integrations = {}
        
        # Verificar Google Ads
        google_service = self.root / "services" / "google_ads_service_complete.py"
        integrations["google_ads"] = {
            "service_exists": google_service.exists(),
            "size": google_service.stat().st_size if google_service.exists() else 0
        }
        
        # Verificar Facebook Ads
        facebook_service = self.root / "services" / "facebook_ads_service_complete.py"
        integrations["facebook_ads"] = {
            "service_exists": facebook_service.exists(),
            "size": facebook_service.stat().st_size if facebook_service.exists() else 0
        }
        
        # Verificar Sales System
        sales_service = self.root / "services" / "sales_system.py"
        integrations["sales_system"] = {
            "service_exists": sales_service.exists(),
            "size": sales_service.stat().st_size if sales_service.exists() else 0
        }
        
        self.results["integrations"] = integrations
    
    def check_database(self):
        """Verificar banco de dados"""
        db_file = self.root / "database.db"
        self.results["database"] = {
            "exists": db_file.exists(),
            "size": db_file.stat().st_size if db_file.exists() else 0
        }
    
    def generate_report(self):
        """Gerar relatório completo"""
        print("=" * 100)
        print("AUDITORIA TOTAL SEMI-FORENSE - NEXORA PRIME v11.7")
        print("=" * 100)
        print()
        
        print("📊 ESTATÍSTICAS GERAIS")
        print("-" * 100)
        for key, value in self.results["estatisticas"].items():
            print(f"  {key}: {value}")
        print()
        
        print("🔍 ROTAS MAPEADAS")
        print("-" * 100)
        print(f"  Total de rotas: {len(self.results['rotas'])}")
        print(f"  APIs: {len([r for r in self.results['rotas'] if r['type'] == 'API'])}")
        print(f"  Páginas: {len([r for r in self.results['rotas'] if r['type'] == 'PAGE'])}")
        print()
        
        print("📄 TEMPLATES")
        print("-" * 100)
        print(f"  Total: {len(self.results['templates'])}")
        print(f"  Com problemas: {len([t for t in self.results['templates'] if t['issues']])}")
        if self.results["templates"]:
            problematic = [t for t in self.results["templates"] if t["issues"]]
            if problematic:
                print("\n  Templates com problemas:")
                for t in problematic[:10]:
                    print(f"    - {t['path']}")
                    for issue in t["issues"]:
                        print(f"      ⚠️ {issue}")
        print()
        
        print("⚙️ SERVIÇOS")
        print("-" * 100)
        print(f"  Total: {len(self.results['services'])}")
        if self.results["services"]:
            print("\n  Top 10 maiores serviços:")
            sorted_services = sorted(self.results["services"], key=lambda x: x["size"], reverse=True)
            for s in sorted_services[:10]:
                print(f"    - {s['path']}: {s['size']} bytes, {s['lines']} linhas, {len(s['classes'])} classes")
        print()
        
        print("🎨 ARQUIVOS ESTÁTICOS")
        print("-" * 100)
        print(f"  CSS: {len(self.results['static_files']['css'])}")
        print(f"  JS: {len(self.results['static_files']['js'])}")
        print(f"  Outros: {len(self.results['static_files']['outros'])}")
        print()
        
        print("🔌 INTEGRAÇÕES")
        print("-" * 100)
        for name, info in self.results["integrations"].items():
            status = "✅" if info["service_exists"] else "❌"
            print(f"  {status} {name}: {info['size']} bytes")
        print()
        
        print("💾 BANCO DE DADOS")
        print("-" * 100)
        db_status = "✅" if self.results["database"]["exists"] else "❌"
        print(f"  {db_status} database.db: {self.results['database']['size']} bytes")
        print()
        
        if self.results["problemas"]:
            print("⚠️ PROBLEMAS CRÍTICOS")
            print("-" * 100)
            for problema in self.results["problemas"]:
                print(f"  ❌ {problema}")
            print()
        
        print("=" * 100)
        print("AUDITORIA CONCLUÍDA")
        print("=" * 100)
        
        # Salvar JSON
        output_file = self.root / "AUDITORIA_COMPLETA.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório JSON salvo em: {output_file}")

if __name__ == "__main__":
    auditor = SystemAuditor("/home/ubuntu/robo-otimizador")
    auditor.audit_routes()
    auditor.audit_templates()
    auditor.audit_services()
    auditor.audit_static_files()
    auditor.check_integrations()
    auditor.check_database()
    auditor.generate_report()
