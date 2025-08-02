#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste para Backend PIX + ZapVoice

Este script testa todas as funcionalidades do backend:
1. Health check
2. Criação de PIX
3. Consulta de status
4. Simulação de webhook
5. Teste ZapVoice (se configurado)

Uso:
    python test_backend.py
"""

import requests
import json
import time
import uuid
from datetime import datetime

# Configurações
BASE_URL = 'http://localhost:5000'
TEST_TIMEOUT = 30

class BackendTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name, success, message, data=None):
        """Registra resultado de um teste"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if data and not success:
            print(f"   Dados: {json.dumps(data, indent=2)}")
    
    def test_health_check(self):
        """Testa endpoint de saúde"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Health Check",
                    True,
                    f"Servidor funcionando. Status: {data.get('status')}",
                    data
                )
                return True
            else:
                self.log_test(
                    "Health Check",
                    False,
                    f"Status HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Health Check",
                False,
                f"Erro de conexão: {str(e)}"
            )
            return False
    
    def test_criar_pix(self):
        """Testa criação de PIX"""
        try:
            payload = {
                'valor': 19.90,
                'nome_cliente': 'Cliente Teste',
                'descricao': 'Pack Premium - Teste Automatizado',
                'cliente_info': {
                    'phone': '11999999999',
                    'email': 'teste@exemplo.com'
                },
                'produto_info': {
                    'name': 'Pack Premium',
                    'type': 'pack_premium'
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/pix/criar",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('qr_code'):
                    self.log_test(
                        "Criar PIX",
                        True,
                        f"PIX criado. ID: {data.get('pedido_id')}",
                        {
                            'pedido_id': data.get('pedido_id'),
                            'pix_id': data.get('pix_id'),
                            'valor': data.get('valor')
                        }
                    )
                    return data.get('pedido_id')
                else:
                    self.log_test(
                        "Criar PIX",
                        False,
                        "Resposta inválida",
                        data
                    )
                    return None
            else:
                self.log_test(
                    "Criar PIX",
                    False,
                    f"Status HTTP {response.status_code}",
                    response.text
                )
                return None
                
        except Exception as e:
            self.log_test(
                "Criar PIX",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    def test_consultar_status(self, pedido_id):
        """Testa consulta de status"""
        if not pedido_id:
            self.log_test(
                "Consultar Status",
                False,
                "Pedido ID não fornecido"
            )
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/pix/status/{pedido_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.log_test(
                        "Consultar Status",
                        True,
                        f"Status: {data.get('status')}",
                        data
                    )
                    return True
                else:
                    self.log_test(
                        "Consultar Status",
                        False,
                        "Resposta inválida",
                        data
                    )
                    return False
            else:
                self.log_test(
                    "Consultar Status",
                    False,
                    f"Status HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Consultar Status",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_webhook_simulation(self, pedido_id):
        """Simula webhook de pagamento"""
        if not pedido_id:
            self.log_test(
                "Webhook Simulation",
                False,
                "Pedido ID não fornecido"
            )
            return False
        
        try:
            # Simular webhook de pagamento aprovado
            webhook_payload = {
                'id': f'pix_{uuid.uuid4()}',
                'status': 'paid',
                'external_id': pedido_id,
                'amount': 19.90,
                'paid_at': datetime.now().isoformat(),
                'payer_name': 'Cliente Teste',
                'description': 'Pack Premium - Teste Automatizado'
            }
            
            response = self.session.post(
                f"{self.base_url}/webhook/pushinpay",
                json=webhook_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.log_test(
                        "Webhook Simulation",
                        True,
                        "Webhook processado com sucesso",
                        webhook_payload
                    )
                    return True
                else:
                    self.log_test(
                        "Webhook Simulation",
                        False,
                        "Webhook rejeitado",
                        data
                    )
                    return False
            else:
                self.log_test(
                    "Webhook Simulation",
                    False,
                    f"Status HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Webhook Simulation",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_zapvoice_integration(self):
        """Testa integração ZapVoice"""
        try:
            test_payload = {
                'pedido_id': f'test_{uuid.uuid4()}'
            }
            
            response = self.session.post(
                f"{self.base_url}/zapvoice/test",
                json=test_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.log_test(
                        "ZapVoice Integration",
                        True,
                        "Integração ZapVoice funcionando",
                        data
                    )
                    return True
                else:
                    self.log_test(
                        "ZapVoice Integration",
                        False,
                        "Erro na integração ZapVoice",
                        data
                    )
                    return False
            elif response.status_code == 400:
                # ZapVoice não configurado é esperado
                self.log_test(
                    "ZapVoice Integration",
                    True,
                    "ZapVoice não configurado (esperado)"
                )
                return True
            else:
                self.log_test(
                    "ZapVoice Integration",
                    False,
                    f"Status HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "ZapVoice Integration",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_listar_pedidos(self):
        """Testa listagem de pedidos"""
        try:
            response = self.session.get(
                f"{self.base_url}/pedidos",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    total = data.get('total', 0)
                    self.log_test(
                        "Listar Pedidos",
                        True,
                        f"Encontrados {total} pedidos",
                        {'total': total}
                    )
                    return True
                else:
                    self.log_test(
                        "Listar Pedidos",
                        False,
                        "Resposta inválida",
                        data
                    )
                    return False
            else:
                self.log_test(
                    "Listar Pedidos",
                    False,
                    f"Status HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Listar Pedidos",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes do Backend PIX + ZapVoice")
        print(f"📍 URL Base: {self.base_url}")
        print("=" * 60)
        
        # 1. Health Check
        if not self.test_health_check():
            print("\n❌ Servidor não está respondendo. Verifique se está rodando.")
            return False
        
        # 2. Criar PIX
        pedido_id = self.test_criar_pix()
        
        # 3. Consultar Status
        self.test_consultar_status(pedido_id)
        
        # 4. Simular Webhook
        self.test_webhook_simulation(pedido_id)
        
        # 5. Verificar status após webhook
        time.sleep(1)  # Aguardar processamento
        self.test_consultar_status(pedido_id)
        
        # 6. Testar ZapVoice
        self.test_zapvoice_integration()
        
        # 7. Listar Pedidos
        self.test_listar_pedidos()
        
        # Resumo
        self.print_summary()
        
        return True
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"✅ Testes Aprovados: {passed_tests}")
        print(f"❌ Testes Falharam: {failed_tests}")
        print(f"📈 Taxa de Sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ TESTES QUE FALHARAM:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['message']}")
        
        print("\n" + "=" * 60)
        
        if failed_tests == 0:
            print("🎉 TODOS OS TESTES PASSARAM! Backend está funcionando perfeitamente.")
        else:
            print("⚠️  Alguns testes falharam. Verifique a configuração do backend.")
        
        print("=" * 60)

def main():
    """Função principal"""
    print("🔧 Backend PIX + ZapVoice - Script de Teste")
    print("Versão: 1.0")
    print("Data:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print()
    
    # Verificar se servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Servidor não está respondendo corretamente (Status: {response.status_code})")
            print("💡 Certifique-se de que o backend está rodando em http://localhost:5000")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor")
        print("💡 Certifique-se de que o backend está rodando:")
        print("   python backend_pix_zapvoice.py")
        return
    except Exception as e:
        print(f"❌ Erro ao verificar servidor: {e}")
        return
    
    # Executar testes
    tester = BackendTester(BASE_URL)
    tester.run_all_tests()
    
    # Salvar relatório
    try:
        with open('test_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'base_url': BASE_URL,
                'results': tester.test_results
            }, f, indent=2, ensure_ascii=False)
        print("\n💾 Relatório salvo em: test_report.json")
    except Exception as e:
        print(f"\n⚠️  Erro ao salvar relatório: {e}")

if __name__ == '__main__':
    main()