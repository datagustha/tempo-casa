"""
SERVIÇO DE ENVIO DE E-MAILS
============================
Responsável por enviar e-mails de comemoração:
- Tempo de casa (1 mês, 6 meses, anos de empresa)
- Aniversário pessoal (com template email_niver.html)
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
# FUNÇÃO: Enviar e-mail de ANIVERSÁRIO (email_niver.html)
# ================================================================

def enviar_aniversario(destinatario: str, nome: str, login: str = None, imagem: str = None):
    """
    Envia e-mail de aniversário.
    """
    
    template_path = TEMPLATES_DIR / "email_niver.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"  ❌ Template não encontrado: {template_path}")
        return False
    
    # Substitui o nome
    html = html.replace("{{NOME}}", nome)
    
    # Substitui a foto
    if imagem and imagem.strip():
        html = html.replace("{{IMAGEM}}", imagem)
    else:
        # Placeholder se não tiver foto
        html = html.replace("{{IMAGEM}}", "https://i.ibb.co/placeholder.png")
    
    assunto = f"🎂 Feliz Aniversário, {nome.split()[0]}! - SiM Facilita"
    
    texto_plain = f"""
{nome}

Que este novo ciclo seja de muitas conquistas.
Aproveite cada momento deste día.

Feliz Aniversário!

Agradecemos pela sua dedicação e comprometimento!

Atenciosamente,
Equipe SiM Facilita
"""
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        msg.attach(MIMEText(texto_plain, 'plain', 'utf-8'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)
        server.quit()
        
        print(f"  ✅ Cartão de aniversário enviado para {nome}")
        return True
        
    except Exception as e:
        print(f"  ❌ Falha ao enviar: {str(e)}")
        return False

# ================================================================
# FUNÇÃO: Enviar e-mail de TEMPO DE CASA (1 mês, 6 meses, anos)
# ================================================================

def enviar_tempo_casa(destinatario: str, nome: str, login: str, mensagem: str, imagem: str = None):
    """
    Envia e-mail comemorativo de tempo de casa.
    
    Args:
        destinatario: E-mail do operador
        nome: Nome completo
        login: Login do operador
        mensagem: Mensagem de comemoração (ex: "🎉 1 mês de casa! 🎉")
        imagem: URL da imagem do operador (opcional)
    
    Returns:
        bool: True se enviou, False se falhou
    """
    
    # Define qual template usar baseado na mensagem
    if "1 mês" in mensagem:
        template_path = TEMPLATES_DIR / "email_1mes.html"
        assunto = "🎉 1 mês de casa! - Parabéns!"
    elif "6 meses" in mensagem:
        template_path = TEMPLATES_DIR / "email_6meses.html"
        assunto = "🎉 6 meses de casa! - Parabéns!"
    elif "ano" in mensagem:
        template_path = TEMPLATES_DIR / "email_aniversario_empresa.html"
        assunto = f"🎉 {mensagem} - Parabéns!"
    else:
        print(f"  ⚠️ Tipo de comemoração não identificado para {nome}")
        return False
    
    # Ler o template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"  ❌ Template não encontrado: {template_path}")
        return False
    
    # Substituir placeholders
    html = html.replace("{{NOME}}", nome)
    html = html.replace("{{LOGIN}}", login)
    html = html.replace("{{IMAGEM}}", imagem if imagem else "")
    
    # Versão em texto simples
    texto_plain = f"""
Olá {nome} (login: {login})!

{mensagem}

Agradecemos pela sua dedicação e comprometimento com nosso time!

Continue com o ótimo trabalho!

---

Dashboard - Sistema de Gestão | SiM Facilita
"""
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = destinatario
        msg['Subject'] = assunto
        
        msg.attach(MIMEText(texto_plain, 'plain', 'utf-8'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)
        server.quit()
        
        print(f"  ✅ E-mail de tempo de casa enviado para {nome} ({destinatario})")
        return True
        
    except Exception as e:
        print(f"  ❌ Falha ao enviar e-mail para {nome}: {str(e)}")
        return False


# ================================================================
# FUNÇÃO DE TESTE
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
        <p>✅ Envio de aniversário (email_niver.html)</p>
        <p>✅ Envio de tempo de casa</p>
        <hr>
        <p style="color: #777; font-size: 12px;">Dashboard - SiM Facilita</p>
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


# ================================================================
# EXEMPLO DE COMO USAR NO MAIN
# ================================================================