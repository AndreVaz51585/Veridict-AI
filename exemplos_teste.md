# Exemplos para Teste - Veridict AI

Abaixo estão vários exemplos de textos (URLs, emails e mensagens SMS) legítimos (seguros) e maliciosos (phishing/scam) que podes colar na tua aplicação para testar o motor de inteligência artificial e as regras.

## Links / URLs

### Corretos (Legítimos / Seguros)
- `https://www.microsoft.com/pt-pt/`
- `https://github.com/features/copilot`
- `https://www.amazon.es/`
- `https://pt.wikipedia.org/wiki/Inteligência_artificial`
- `https://www.microsoft.com/pt-pt/software-download/`
- `https://github.com/features/copilot`
- `https://www.amazon.es/gp/cart/view.html?ref_=nav_cart`
- `https://eportugal.gov.pt/`
- `https://www.mbway.pt/`

### Incorretos (Maliciosos / Phishing)
- `http://secure-login-paypal.com-update.info/login` (Usa HTTP e subdomínios estranhos)
- `http://185.15.22.1/auth/apple/` (Usa um endereço de IP direto)
- `https://www.netflxi-account-update.com/payment` (Typosquatting - nome enganador, ex: "netflxi")
- `http://bit.ly/3xY8aB` (Links encurtados sem contexto muitas vezes escondem phishing)
-  **Teste Oficial Google Safe Browsing:** `http://testsafebrowsing.appspot.com/` *(Garante 100% de rate "Dangerous")*
-  **Typosquatting (Imitação de marca):** `http://secure-login.paypal.com-update.info/login`
-  **Uso de TLDs de alto risco (.run, .online, .vip):** `https://financas-portaldasfinancas.online/reembolsos`
-  **Subdomínios enganosos:** `http://apple.com.secure-device-locate.run/auth`
-  **Encurtadores de Link (Sempre nível Suspicious/Dangerous):** `https://bit.ly/3xY8aB`
-  **Ausência de HTTPS + Endereço IP puro:** `http://185.15.22.1/auth/apple/`
-  **Google Safe Browsing Test:** `http://testsafebrowsing.appspot.com/s/malware.html` *(Ativa a label Critical/Dangerous imediata)*
-  **Typosquatting (Novo - Crypto):** `http://login-binance-secure.com` *(Imitação da marca Binance)*
-  **Typosquatting (Novo - Gaming):** `https://discord-nitro-free.online/login` *(Imitação do Discord num TLD .online)*
-  **Novas Extensões de Risco (.tk, .cam):** `http://watch-free-movies.cam/stream`
-  **Novos Encurtadores (rb.gy):** `https://rb.gy/x82bA` *(Ativa a flag de VERY HIGH RISK para encurtadores)*
-  **Ausência de DNS/IP puro:** `http://185.15.22.1/auth/apple/`


---

## Emails

### Corretos (Legítimos / Seguros)

**Assunto:** Confirmação da sua encomenda #12345
**Corpo:**
Olá Pedro,
A sua encomenda foi processada com sucesso. Poderá acompanhar o envio através do site oficial da transportadora usando o código PT123456789.
Se tiver alguma dúvida, aceda à sua área de cliente em https://www.amazon.es.
Obrigado por comprar connosco!



**Confirmação de Encomenda (Worten/Fnac)**
> Olá Pedro,
> A sua encomenda #827361 foi processada com sucesso e entregue à transportadora. Acompanhe o estado do envio usando o código PT881928373 na sua área de cliente em https://www.worten.pt/. Obrigado pela sua preferência!


**Serviço Público (Portal das Finanças Real)**
> Autoridade Tributária e Aduaneira: Informamos que a sua declaração de IRS foi liquidada com sucesso. Pode consultar a respetiva demonstração de liquidação através do portal oficial: https://portaldasfinancas.gov.pt.



**Serviço Público (SNS 24)**
> Caro utente, relembramos que tem uma teleconsulta agendada para 20-05-2026 às 10h30. Poderá aceder através da sua App SNS24 ou no portal oficial https://www.sns24.gov.pt. Para cancelar, ligue 808 24 24 24.

### Incorretos (Maliciosos / Phishing)xx

**Assunto:** URGENTE: A sua conta bancária foi bloqueada!
**Corpo:**
Caro(a) Cliente,
Detectamos atividades suspeitas na sua conta bancária. Para evitar o bloqueio permanente, por favor confirme a sua identidade e os seus dados de acesso imediatamente clicando no link abaixo:
http://banco-seguranca-online-2024.com/loginpt/
Se não agir dentro de 24 horas, perderá o acesso definitivo aos fundos da sua conta.
Os melhores cumprimentos,
O Departamento de Segurança


**Typosquatting Financeiro (Novo - Revolut)**
> SECURITY ALERT: Revolut Account Restricted!
> We noticed an unauthorized login attempt from a new device (IP: 192.168.1.1). Your funds have been frozen. To unlock your account and prevent permanent suspension, verify your identity immediately:
> https://revolut-security-auth.help/unlock

**Phishing Empresarial (Novo - Office 365)**
> Action Required: Password Expiration
> Dear employee, your Office365 password will expire in exactly 2 hours. Please update your information immediately using the link below to avoid losing access to your company emails.
> http://cutt.ly/admin-it-update-password



**Netflix** 
 URGENTE: A sua conta Netflix vai ser suspensa amanhã!
> Caro cliente, o seu último pagamento falhou devido a informações desatualizadas. Para evitar a suspensão imediata da sua conta nas próximas 12 horas, clique em "Atualizar Informações" no link abaixo:
> http://netflix-update-billing.pw/pt/

**Typosquatting Bancário (Millennium / Santander)**
> ALERTA DE SEGURANÇA: Nova tentativa de login detetada.
> Ocorreu um login não autorizado na sua conta através de um novo dispositivo (iPhone 14). Se não foi você, tem de cancelar a operação urgentemente para não perder os seus fundos.
> Clique aqui para validação de segurança:
> https://www.millenniumbcp-seguranca.top/act-cancel

---

## Mensagens de Texto (SMS / WhatsApp)

### Corretas (Legítimas / Seguras)
- "CTT Expresso: A sua encomenda 003L456789123 está em distribuição e será entregue hoje entre as 14h e as 18h."
- "MB WAY: O seu codigo para confirmacao e 459123. Valido por 15 min. Nao partilhe com ninguem."
- "A consulta no Centro de Saude de Lisboa foi agendada para 20-05-2026 as 10:30. Para cancelar ligue SNS24."

### Incorretas (Maliciosas / Smishing)
- "CTT: A sua encomenda foi retida na alfandega. Falta pagar as taxas aduaneiras (1.99€). Pague agora pelo link para libertar a encomenda: http://ctt-taxas-alfandega.com/pay"
- "AT: Autoridade Tributaria informa: Tem um reembolso de imposto pendente no valor de 245,50 EUR. Confirme os seus dados bancarios aqui imediatamente: http://portaldasfinancas-pt.online/reembolsos"
- "Olá Pai, o meu telemóvel partiu-se e estou a usar este número provisório. Podes mandar-me uma mensagem no WhatsApp para este número? É muito urgente, preciso que faças um pagamento por mim."

**Fraude "Olá Pai/Mãe" (WhatsApp)**
> Olá pai, o meu telemóvel avariou e estou a usar este número provisório. Podes mandar-me uma mensagem no WhatsApp para este número? É muito urgente, preciso que me pagues uma fatura importante senão pago multa.

**Fraude das Finanças (AT / Reembolso)**
> AT Informa: Tem um reembolso de imposto a seu favor no valor de 325,50 EUR referente ao IRS. Para receber de imediato confirme o seu IBAN no portal: http://portaldasfinancas.gov.pt-reembolso.online/

**Fraude da Alfândega / CTT**
> CTT: A sua encomenda ficou retida na alfandega devido a taxas aduaneiras nao pagas (2.15 EUR). Efetue o pagamento imediato para libertar o envio ou o mesmo sera devolvido ao remetente: http://ctt-alfandega-pagamentos.run/pay


---

