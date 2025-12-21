#!/usr/bin/env python3
"""Script de teste para verificar se a aplicação carrega corretamente"""

try:
    from main import app
    print("App carregado com sucesso!")
    print("\nRotas de pagamento:")
    for r in app.url_map.iter_rules():
        if 'payment' in r.rule or 'wallet' in r.rule or 'webhook' in r.rule:
            print(f"  {r.methods} {r.rule}")
    print("\nTeste concluido com sucesso!")
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()
