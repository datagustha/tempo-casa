"""
SERVIÇO DE ENVIO DE E-MAILS
============================
Responsável por enviar e-mails de comemoração (1 mês, 6 meses, aniversário de admissão).
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# ================================================================
# CONFIGURAÇÕES DO GMAIL
# ================================================================

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Caminho para os templates HTML
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


# ================================================================
# FUNÇÃO AUXILIAR: Carregar template HTML
# ================================================================

def _carregar_template(tipo: str, nome: str, login: str, imagem: str, anos: int = None):
    """
    Carrega o template HTML e substitui os placeholders.
    
    Args:
        tipo: '1mes', '6meses', ou 'aniversario'
        nome: Nome do operador
        login: Login do operador
        imagem: URL da imagem do operador
        anos: Número de anos (apenas para tipo 'aniversario')
    
    Returns:
        str: HTML com placeholders substituídos
    """
    if tipo == "1mes":
        template_path = TEMPLATES_DIR / "email_1mes.html"
    elif tipo == "6meses":
        template_path = TEMPLATES_DIR / "email_6meses.html"
    else:  # aniversario
        template_path = TEMPLATES_DIR / "email_aniversario.html"
    
    # Ler o arquivo HTML
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Substituir placeholders
    html = html.replace("{{NOME}}", nome)
    html = html.replace("{{LOGIN}}", login)
    html = html.replace("{{IMAGEM}}", imagem if imagem else "")
    
    if tipo == "aniversario" and anos:
        html = html.replace("{{ANOS}}", str(anos))
    
    return html


# ================================================================
# FUNÇÃO 1: Enviar e-mail de comemoração
# ================================================================

def enviar_comemoracao_email(destinatario: str, nome: str, login: str, mensagem: str, imagem: str = None):
    """
    Envia um e-mail de comemoração para o operador usando template HTML.
    
    Args:
        destinatario: E-mail do operador (ex: roseli@gmail.com)
        nome: Nome completo do operador (ex: ROSELI BATISTA DOS SANTOS)
        login: Login do operador (ex: 2552ROSELI)
        mensagem: Mensagem de comemoração (ex: "🎉 1 mês de casa! 🎉")
        imagem: URL da imagem do operador (opcional)
    
    Returns:
        bool: True se enviou, False se falhou
    """
    
    # Define o tipo e assunto baseado na mensagem
    if "1 mês" in mensagem:
        tipo = "1mes"
        assunto = "🎉 1 mês de casa! - Parabéns!"
    elif "6 meses" in mensagem:
        tipo = "6meses"
        assunto = "🎉 6 meses de casa! - Parabéns!"
    elif "ano(s)" in mensagem:
        tipo = "aniversario"
        # Extrair o número de anos da mensagem (ex: "🎉 3 ano(s) de casa! 🎉")
        import re
        anos_match = re.search(r'(\d+)', mensagem)
        anos = int(anos_match.group(1)) if anos_match else 0
        assunto = f"🎉 {anos} anos de casa! - Parabéns!"
    else:
        tipo = "1mes"
        assunto = "🎉 Parabéns! - Tempo de Casa"
        anos = None
    
    # Carregar o template HTML
    html = _carregar_template(tipo, nome, login, imagem, anos if tipo == "aniversario" else None)
    
    try:
        # 1. Criar a mensagem
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        # 2. Versão em texto simples (fallback)
        texto_plain = f"""
Olá {nome} (login: {login})!

{mensagem}

Agradecemos pela sua dedicação e comprometimento com nosso time!

Continue com o ótimo trabalho!

---

Dashboard - Sistema de Gestão
"""
        msg.attach(MIMEText(texto_plain, 'plain', 'utf-8'))
        
        # 3. Versão em HTML
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        
        # 4. Conectar ao servidor do Gmail e enviar
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)
        server.quit()
        
        print(f"  ✅ E-mail enviado para {nome} ({destinatario})")
        return True
        
    except Exception as e:
        print(f"  ❌ Falha ao enviar e-mail para {nome}: {str(e)}")
        return False


# ================================================================
# FUNÇÃO 2: Testar configuração de e-mail
# ================================================================

def enviar_email_teste(destinatario: str):
    """
    Envia um e-mail de teste para verificar se a configuração está correta.
    
    Args:
        destinatario: Seu e-mail para testar
    
    Returns:
        bool: True se enviou, False se falhou
    """
    assunto = "🧪 Teste de Configuração - Dashboard"
    corpo_html = """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
        <h2 style="color: #7d3d96;">🧪 Teste de Configuração</h2>
        <p>Sua configuração de e-mail está funcionando corretamente!</p>
        <p>Agora você pode enviar e-mails de comemoração para os operadores.</p>
        <hr>
        <p style="color: #777; font-size: 12px;">Dashboard - Sistema de Gestão</p>
    </body>
    </html>
    """
    texto_plain = "Teste de Configuração - Dashboard\n\nSua configuração está funcionando!"
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(texto_plain, 'plain', 'utf-8'))
        msg.attach(MIMEText(corpo_html, 'html', 'utf-8'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ E-mail de teste enviado para {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Falha no e-mail de teste: {str(e)}")
        return False