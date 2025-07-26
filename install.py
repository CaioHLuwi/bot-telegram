#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Automatizada - Bot Kyoko
Este script automatiza a instalação e configuração inicial do bot.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Exibir cabeçalho do instalador"""
    print("\n" + "="*60)
    print("🤖 INSTALADOR AUTOMÁTICO - BOT KYOKO")
    print("="*60)
    print("Este script irá configurar automaticamente o Bot Kyoko")
    print("Certifique-se de ter Python 3.9+ instalado")
    print("="*60 + "\n")

def check_python_version():
    """Verificar versão do Python"""
    print("🔍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("⚠️  É necessário Python 3.9 ou superior")
        print("📥 Baixe em: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_pip():
    """Verificar se pip está disponível"""
    print("🔍 Verificando pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip - OK")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip não encontrado")
        print("📥 Instale pip: python -m ensurepip --upgrade")
        return False

def create_virtual_environment():
    """Criar ambiente virtual"""
    print("🔧 Criando ambiente virtual...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("⚠️  Ambiente virtual já existe")
        response = input("Deseja recriar? (s/N): ").lower()
        if response == 's':
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("✅ Usando ambiente virtual existente")
            return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False

def get_pip_executable():
    """Obter caminho do pip no ambiente virtual"""
    system = platform.system()
    if system == "Windows":
        return Path("venv") / "Scripts" / "pip.exe"
    else:
        return Path("venv") / "bin" / "pip"

def install_dependencies():
    """Instalar dependências"""
    print("📦 Instalando dependências...")
    
    pip_path = get_pip_executable()
    
    if not pip_path.exists():
        print(f"❌ pip não encontrado em: {pip_path}")
        return False
    
    try:
        # Atualizar pip
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                      check=True)
        
        # Instalar dependências
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], 
                      check=True)
        
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_requirements_file():
    """Verificar se arquivo requirements.txt existe"""
    if not Path("requirements.txt").exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    return True

def setup_env_file():
    """Configurar arquivo .env"""
    print("⚙️  Configurando arquivo .env...")
    
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  Arquivo .env já existe")
        response = input("Deseja reconfigurar? (s/N): ").lower()
        if response != 's':
            print("✅ Mantendo configuração existente")
            return True
    
    print("\n📝 Configuração do Bot:")
    print("Para obter o token:")
    print("1. Acesse @BotFather no Telegram")
    print("2. Digite /newbot")
    print("3. Nome: Kyoko uwu")
    print("4. Username: kyoko_pack_bot (ou outro disponível)")
    print("5. Copie o token fornecido\n")
    
    bot_token = input("🔑 Digite o token do bot: ").strip()
    
    if not bot_token:
        print("❌ Token não pode estar vazio")
        return False
    
    # Validar formato básico do token
    if ":" not in bot_token or len(bot_token) < 40:
        print("⚠️  Token parece inválido (formato: 123456789:ABC...)")
        response = input("Continuar mesmo assim? (s/N): ").lower()
        if response != 's':
            return False
    
    env_content = f"""# Token do Bot do Telegram
# Obtenha seu token em: https://t.me/BotFather
BOT_TOKEN={bot_token}

# Configurações do Pushin Pay
PUSHIN_PAY_TOKEN=39884|DKt79CdRINdHafadVS01KwEHsF6vi8GwAoW273Meea17b5d5

# Link do conteúdo
CONTEUDO_LINK=https://kyokoleticia.site/conteudo
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Arquivo .env configurado")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def check_media_folder():
    """Verificar pasta de mídias"""
    print("📁 Verificando pasta de mídias...")
    
    fotos_path = Path("fotos")
    if not fotos_path.exists():
        fotos_path.mkdir()
        print("✅ Pasta fotos/ criada")
    
    # Verificar arquivos necessários
    required_files = ["1.jpg", "2.jpg", "4.jpg", "1.mp4"]
    missing_files = []
    
    for file in required_files:
        if not (fotos_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  Arquivos de mídia faltando: {', '.join(missing_files)}")
        print("📝 Adicione os arquivos na pasta fotos/ antes de usar o bot")
    else:
        print("✅ Todos os arquivos de mídia encontrados")
    
    # Verificar foto do bot
    if (fotos_path / "bot-foot.png").exists():
        print("✅ Foto do perfil do bot encontrada")
    else:
        print("⚠️  Foto do perfil (bot-foot.png) não encontrada")
    
    return True

def test_bot_connection():
    """Testar conexão com o bot"""
    print("🔗 Testando conexão com o bot...")
    
    try:
        # Importar e testar
        python_path = get_python_executable()
        result = subprocess.run(
            [str(python_path), "setup_bot.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Bot conectado com sucesso")
            return True
        else:
            print(f"❌ Erro na conexão: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout na conexão - verifique sua internet")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar bot: {e}")
        return False

def get_python_executable():
    """Obter caminho do Python no ambiente virtual"""
    system = platform.system()
    if system == "Windows":
        return Path("venv") / "Scripts" / "python.exe"
    else:
        return Path("venv") / "bin" / "python"

def create_start_script():
    """Criar script de inicialização"""
    print("📝 Criando script de inicialização...")
    
    system = platform.system()
    python_path = get_python_executable()
    
    if system == "Windows":
        script_content = f"""@echo off
echo Iniciando Bot Kyoko...
cd /d "%~dp0"
"{python_path}" bot.py
pause
"""
        script_name = "start_bot.bat"
    else:
        script_content = f"""#!/bin/bash
echo "Iniciando Bot Kyoko..."
cd "$(dirname "$0")"
"{python_path}" bot.py
"""
        script_name = "start_bot.sh"
    
    try:
        with open(script_name, "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # Dar permissão de execução no Linux/macOS
        if system != "Windows":
            os.chmod(script_name, 0o755)
        
        print(f"✅ Script criado: {script_name}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar script: {e}")
        return False

def print_final_instructions():
    """Exibir instruções finais"""
    system = platform.system()
    script_name = "start_bot.bat" if system == "Windows" else "start_bot.sh"
    
    print("\n" + "="*60)
    print("🎉 INSTALAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("\n1. 📁 Adicione os arquivos de mídia na pasta fotos/:")
    print("   - 1.jpg (primeira foto)")
    print("   - 2.jpg (segunda foto)")
    print("   - 4.jpg (foto de despedida)")
    print("   - 1.mp4 (vídeo)")
    print("   - audio.mp3 (áudio - opcional)")
    
    print("\n2. 🚀 Para iniciar o bot:")
    if system == "Windows":
        print(f"   - Clique duas vezes em: {script_name}")
        print("   - Ou execute: python bot.py")
    else:
        print(f"   - Execute: ./{script_name}")
        print("   - Ou execute: python bot.py")
    
    print("\n3. 📱 Teste no Telegram:")
    print("   - Procure seu bot pelo username")
    print("   - Envie /start para testar")
    
    print("\n4. 📚 Documentação:")
    print("   - README.md - Guia básico")
    print("   - Docs/documentacao_tecnica.md - Documentação completa")
    print("   - Docs/guia_instalacao.md - Guia detalhado")
    
    print("\n⚠️  Lembre-se:")
    print("   - Mantenha o token do bot seguro")
    print("   - Adicione as mídias antes de usar")
    print("   - Verifique os logs em caso de erro")
    
    print("\n" + "="*60)
    print("✨ Bot Kyoko pronto para uso!")
    print("="*60 + "\n")

def main():
    """Função principal do instalador"""
    print_header()
    
    # Verificações iniciais
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    if not check_requirements_file():
        return False
    
    # Instalação
    steps = [
        ("Criar ambiente virtual", create_virtual_environment),
        ("Instalar dependências", install_dependencies),
        ("Configurar .env", setup_env_file),
        ("Verificar mídias", check_media_folder),
        ("Testar conexão", test_bot_connection),
        ("Criar script de inicialização", create_start_script)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"\n❌ Falha na etapa: {step_name}")
            print("🔧 Verifique os erros acima e tente novamente")
            return False
    
    print_final_instructions()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro inesperado: {e}")
        print("🔧 Tente executar a instalação manual")
        sys.exit(1)