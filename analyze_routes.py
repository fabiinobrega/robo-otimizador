#!/usr/bin/env python3
"""
Script para analisar páginas HTML e rotas Flask
Identifica páginas sem rotas correspondentes
"""

import os
import re
from pathlib import Path

# Listar todas as páginas HTML
templates_dir = Path("templates")
html_files = []

for file in templates_dir.rglob("*.html"):
    if "components" not in str(file):  # Ignorar componentes
        html_files.append(str(file))

print("=" * 80)
print("PÁGINAS HTML ENCONTRADAS (excluindo components)")
print("=" * 80)
for f in sorted(html_files):
    print(f"  {f}")
print(f"\nTotal: {len(html_files)} páginas\n")

# Extrair rotas do main.py
with open("main.py", "r", encoding="utf-8") as f:
    main_content = f.read()

# Encontrar todas as rotas
route_pattern = r'@app\.route\(["\']([^"\']+)["\']'
routes = re.findall(route_pattern, main_content)

# Filtrar apenas rotas de páginas (não APIs)
page_routes = [r for r in routes if not r.startswith("/api") and not r.startswith("/webhooks")]

print("=" * 80)
print("ROTAS DE PÁGINAS EXISTENTES")
print("=" * 80)
for route in sorted(set(page_routes)):
    print(f"  {route}")
print(f"\nTotal: {len(set(page_routes))} rotas\n")

# Mapear páginas HTML para rotas esperadas
html_to_route = {}
for html_file in html_files:
    # Extrair nome do arquivo sem extensão
    filename = Path(html_file).stem
    
    # Converter para formato de rota
    if filename == "index":
        expected_route = "/"
    else:
        # Converter underscores para hífens
        route_name = filename.replace("_", "-")
        expected_route = f"/{route_name}"
    
    html_to_route[html_file] = expected_route

# Identificar páginas sem rotas
missing_routes = []
for html_file, expected_route in sorted(html_to_route.items()):
    if expected_route not in page_routes:
        missing_routes.append((html_file, expected_route))

print("=" * 80)
print("PÁGINAS SEM ROTAS CORRESPONDENTES")
print("=" * 80)
if missing_routes:
    for html_file, expected_route in missing_routes:
        print(f"  {html_file}")
        print(f"    → Rota esperada: {expected_route}")
        print()
    print(f"Total: {len(missing_routes)} páginas sem rotas\n")
else:
    print("  ✅ Todas as páginas têm rotas correspondentes!\n")

# Gerar código Flask para rotas faltantes
if missing_routes:
    print("=" * 80)
    print("CÓDIGO FLASK PARA ADICIONAR AO main.py")
    print("=" * 80)
    print()
    
    for html_file, expected_route in missing_routes:
        # Gerar nome da função
        func_name = Path(html_file).stem
        
        # Template do código
        code = f'''@app.route("{expected_route}")
def {func_name}():
    return render_template("{html_file}")

'''
        print(code)
