#!/usr/bin/env python3.11
"""
MAPEAMENTO COMPLETO DO SISTEMA NEXORA PRIME
Análise profunda de rotas, serviços, arquitetura e identificação de pontos para ChatGPT e Manus
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class NexoraSystemMapper:
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.mapping = {
            "rotas": [],
            "servicos": [],
            "arquitetura": {},
            "apis": [],
            "pontos_chatgpt": [],
            "pontos_manus": []
        }
    
    def map_routes(self):
        """Mapear todas as rotas do sistema"""
        main_py = self.root / "main.py"
        
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        routes = []
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('@app.route('):
                match = re.search(r'@app\.route\(["\']([^"\']+)["\'](?:,\s*methods=\[([^\]]+)\])?', line)
                if match:
                    route_path = match.group(1)
                    methods = match.group(2) if match.group(2) else '"GET"'
                    
                    # Pegar função
                    if i < len(lines):
                        func_line = lines[i]
                        func_match = re.search(r'def\s+(\w+)', func_line)
                        func_name = func_match.group(1) if func_match else "unknown"
                    else:
                        func_name = "unknown"
                    
                    route_type = "API" if route_path.startswith("/api/") else "PAGE"
                    
                    # Classificar para ChatGPT ou Manus
                    category = self._classify_route(route_path, func_name)
                    
                    routes.append({
                        "path": route_path,
                        "methods": methods.replace('"', ''),
                        "function": func_name,
                        "type": route_type,
                        "category": category,
                        "line": i
                    })
        
        self.mapping["rotas"] = routes
        return routes
    
    def map_services(self):
        """Mapear todos os serviços"""
        services_dir = self.root / "services"
        
        services = []
        for py_file in services_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair classes e funções
            classes = re.findall(r'class\s+(\w+)', content)
            functions = re.findall(r'def\s+(\w+)', content)
            
            # Classificar serviço
            category = self._classify_service(py_file.name, content)
            
            services.append({
                "name": py_file.name,
                "path": str(py_file.relative_to(self.root)),
                "size": py_file.stat().st_size,
                "lines": len(content.split('\n')),
                "classes": classes,
                "functions_count": len(functions),
                "category": category
            })
        
        self.mapping["servicos"] = services
        return services
    
    def map_architecture(self):
        """Mapear arquitetura do sistema"""
        arch = {
            "frontend": {
                "templates": len(list((self.root / "templates").glob("*.html"))),
                "static_css": len(list((self.root / "static" / "css").glob("*.css"))),
                "static_js": len(list((self.root / "static" / "js").glob("*.js")))
            },
            "backend": {
                "main": "main.py",
                "services": len(list((self.root / "services").glob("*.py"))) - 1,
                "database": "database.db"
            },
            "integrations": {
                "google_ads": self._check_integration("google_ads"),
                "facebook_ads": self._check_integration("facebook_ads"),
                "openai": self._check_integration("openai"),
                "manus": self._check_integration("manus")
            }
        }
        
        self.mapping["arquitetura"] = arch
        return arch
    
    def identify_chatgpt_points(self):
        """Identificar pontos onde ChatGPT deve atuar"""
        chatgpt_points = [
            {
                "area": "Copywriting",
                "description": "Geração de headlines, descrições e copy de anúncios",
                "routes": [r for r in self.mapping["rotas"] if "copy" in r["path"] or "generate" in r["path"]],
                "priority": "ALTA"
            },
            {
                "area": "Estratégia de Campanhas",
                "description": "Criação de estratégias de marketing e planejamento",
                "routes": [r for r in self.mapping["rotas"] if "campaign" in r["path"] and r["type"] == "API"],
                "priority": "ALTA"
            },
            {
                "area": "Análise e Otimização",
                "description": "Análise de performance e recomendações",
                "routes": [r for r in self.mapping["rotas"] if "analyze" in r["path"] or "optimize" in r["path"]],
                "priority": "MÉDIA"
            },
            {
                "area": "Persona e Segmentação",
                "description": "Análise de público e criação de personas",
                "routes": [r for r in self.mapping["rotas"] if "segment" in r["path"] or "audience" in r["path"]],
                "priority": "MÉDIA"
            }
        ]
        
        self.mapping["pontos_chatgpt"] = chatgpt_points
        return chatgpt_points
    
    def identify_manus_points(self):
        """Identificar pontos onde Manus deve atuar"""
        manus_points = [
            {
                "area": "Execução de Campanhas",
                "description": "Aplicar campanhas no Google Ads e Facebook Ads",
                "routes": [r for r in self.mapping["rotas"] if "publish" in r["path"] or "apply" in r["path"]],
                "priority": "ALTA"
            },
            {
                "area": "Sincronização de Dados",
                "description": "Sincronizar dados entre Nexora e plataformas externas",
                "routes": [r for r in self.mapping["rotas"] if "sync" in r["path"]],
                "priority": "ALTA"
            },
            {
                "area": "Automação",
                "description": "Executar automações e rotinas",
                "routes": [r for r in self.mapping["rotas"] if "automation" in r["path"]],
                "priority": "MÉDIA"
            },
            {
                "area": "Manipulação de Estrutura",
                "description": "Criar/editar arquivos, APIs e banco de dados",
                "routes": [],
                "priority": "ALTA"
            }
        ]
        
        self.mapping["pontos_manus"] = manus_points
        return manus_points
    
    def _classify_route(self, path, func_name):
        """Classificar rota para ChatGPT ou Manus"""
        strategic_keywords = ["generate", "copy", "analyze", "recommend", "strategy", "persona"]
        execution_keywords = ["publish", "apply", "sync", "execute", "update", "create"]
        
        path_lower = path.lower()
        func_lower = func_name.lower()
        
        for keyword in strategic_keywords:
            if keyword in path_lower or keyword in func_lower:
                return "CHATGPT"
        
        for keyword in execution_keywords:
            if keyword in path_lower or keyword in func_lower:
                return "MANUS"
        
        return "NEUTRAL"
    
    def _classify_service(self, name, content):
        """Classificar serviço"""
        if "openai" in name.lower() or "gpt" in name.lower():
            return "CHATGPT"
        elif "manus" in name.lower() or "executor" in name.lower():
            return "MANUS"
        elif "ads" in name.lower() or "facebook" in name.lower() or "google" in name.lower():
            return "INTEGRATION"
        else:
            return "CORE"
    
    def _check_integration(self, integration_name):
        """Verificar se integração existe"""
        services_dir = self.root / "services"
        for py_file in services_dir.glob("*.py"):
            if integration_name in py_file.name.lower():
                return True
        return False
    
    def generate_reports(self):
        """Gerar relatórios"""
        # MAPEAMENTO_GERAL.md
        self._generate_general_mapping()
        
        # LOCALIZACAO_POTENCIAIS_CHATGPT.md
        self._generate_chatgpt_mapping()
        
        # LOCALIZACAO_POTENCIAIS_MANUS_EXECUTION.md
        self._generate_manus_mapping()
        
        # JSON completo
        output_file = self.root / "MAPEAMENTO_SISTEMA_COMPLETO.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.mapping, f, indent=2, ensure_ascii=False)
        
        print("✅ Relatórios gerados com sucesso")
    
    def _generate_general_mapping(self):
        """Gerar MAPEAMENTO_GERAL.md"""
        content = f"""# MAPEAMENTO GERAL DO SISTEMA NEXORA PRIME

## Estatísticas Gerais

- **Total de Rotas:** {len(self.mapping['rotas'])}
- **Total de Serviços:** {len(self.mapping['servicos'])}
- **Templates HTML:** {self.mapping['arquitetura']['frontend']['templates']}
- **Arquivos CSS:** {self.mapping['arquitetura']['frontend']['static_css']}
- **Arquivos JS:** {self.mapping['arquitetura']['frontend']['static_js']}

## Rotas por Tipo

| Tipo | Quantidade |
|:-----|:-----------|
| APIs | {len([r for r in self.mapping['rotas'] if r['type'] == 'API'])} |
| Páginas | {len([r for r in self.mapping['rotas'] if r['type'] == 'PAGE'])} |

## Rotas por Categoria

| Categoria | Quantidade |
|:----------|:-----------|
| ChatGPT | {len([r for r in self.mapping['rotas'] if r['category'] == 'CHATGPT'])} |
| Manus | {len([r for r in self.mapping['rotas'] if r['category'] == 'MANUS'])} |
| Neutral | {len([r for r in self.mapping['rotas'] if r['category'] == 'NEUTRAL'])} |

## Serviços por Categoria

| Categoria | Quantidade |
|:----------|:-----------|
| ChatGPT | {len([s for s in self.mapping['servicos'] if s['category'] == 'CHATGPT'])} |
| Manus | {len([s for s in self.mapping['servicos'] if s['category'] == 'MANUS'])} |
| Integration | {len([s for s in self.mapping['servicos'] if s['category'] == 'INTEGRATION'])} |
| Core | {len([s for s in self.mapping['servicos'] if s['category'] == 'CORE'])} |

## Integrações Existentes

| Integração | Status |
|:-----------|:-------|
| Google Ads | {'✅' if self.mapping['arquitetura']['integrations']['google_ads'] else '❌'} |
| Facebook Ads | {'✅' if self.mapping['arquitetura']['integrations']['facebook_ads'] else '❌'} |
| OpenAI | {'✅' if self.mapping['arquitetura']['integrations']['openai'] else '❌'} |
| Manus | {'✅' if self.mapping['arquitetura']['integrations']['manus'] else '❌'} |
"""
        
        output_file = self.root / "MAPEAMENTO_GERAL.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_chatgpt_mapping(self):
        """Gerar LOCALIZACAO_POTENCIAIS_CHATGPT.md"""
        content = """# LOCALIZAÇÃO DE POTENCIAIS CHATGPT

## Áreas Estratégicas para ChatGPT

"""
        for point in self.mapping["pontos_chatgpt"]:
            content += f"""### {point['area']} (Prioridade: {point['priority']})

**Descrição:** {point['description']}

**Rotas Relacionadas:** {len(point['routes'])}

"""
            for route in point['routes'][:5]:
                content += f"- `{route['methods']} {route['path']}` → `{route['function']}()`\n"
            
            content += "\n"
        
        output_file = self.root / "LOCALIZACAO_POTENCIAIS_CHATGPT.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_manus_mapping(self):
        """Gerar LOCALIZACAO_POTENCIAIS_MANUS_EXECUTION.md"""
        content = """# LOCALIZAÇÃO DE POTENCIAIS MANUS EXECUTION

## Áreas de Execução para Manus

"""
        for point in self.mapping["pontos_manus"]:
            content += f"""### {point['area']} (Prioridade: {point['priority']})

**Descrição:** {point['description']}

**Rotas Relacionadas:** {len(point['routes'])}

"""
            for route in point['routes'][:5]:
                content += f"- `{route['methods']} {route['path']}` → `{route['function']}()`\n"
            
            content += "\n"
        
        output_file = self.root / "LOCALIZACAO_POTENCIAIS_MANUS_EXECUTION.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    print("=" * 100)
    print("MAPEAMENTO COMPLETO DO SISTEMA NEXORA PRIME")
    print("=" * 100)
    print()
    
    mapper = NexoraSystemMapper("/home/ubuntu/robo-otimizador")
    
    print("📍 Mapeando rotas...")
    routes = mapper.map_routes()
    print(f"   ✓ {len(routes)} rotas mapeadas")
    
    print("⚙️  Mapeando serviços...")
    services = mapper.map_services()
    print(f"   ✓ {len(services)} serviços mapeados")
    
    print("🏗️  Mapeando arquitetura...")
    arch = mapper.map_architecture()
    print(f"   ✓ Arquitetura mapeada")
    
    print("🧠 Identificando pontos ChatGPT...")
    chatgpt_points = mapper.identify_chatgpt_points()
    print(f"   ✓ {len(chatgpt_points)} áreas identificadas")
    
    print("⚙️  Identificando pontos Manus...")
    manus_points = mapper.identify_manus_points()
    print(f"   ✓ {len(manus_points)} áreas identificadas")
    
    print("📄 Gerando relatórios...")
    mapper.generate_reports()
    
    print()
    print("=" * 100)
    print("MAPEAMENTO CONCLUÍDO")
    print("=" * 100)
