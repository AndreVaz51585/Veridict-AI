# Exemplos para Teste - Veridict AI

Abaixo estão vários exemplos de textos (URLs, emails e mensagens SMS) legítimos (seguros) e maliciosos (phishing/scam) que podes colar na tua aplicação para testar o motor de inteligência artificial e as regras.

## 🔗 Links / URLs

### ✅ Corretos (Legítimos / Seguros)
- `https://www.microsoft.com/pt-pt/`
- `https://github.com/features/copilot`
- `https://www.amazon.es/`
- `https://pt.wikipedia.org/wiki/Inteligência_artificial`

### ❌ Incorretos (Maliciosos / Phishing)
- `http://secure-login-paypal.com-update.info/login` (Usa HTTP e subdomínios estranhos)
- `http://185.15.22.1/auth/apple/` (Usa um endereço de IP direto)
- `https://www.netflxi-account-update.com/payment` (Typosquatting - nome enganador, ex: "netflxi")
- `http://bit.ly/3xY8aB` (Links encurtados sem contexto muitas vezes escondem phishing)

---

## 📧 Emails

### ✅ Corretos (Legítimos / Seguros)

**Assunto:** Confirmação da sua encomenda #12345
**Corpo:**
Olá André,
A sua encomenda foi processada com sucesso. Poderá acompanhar o envio através do site oficial da transportadora usando o código PT123456789.
Se tiver alguma dúvida, aceda à sua área de cliente em https://www.amazon.es.
Obrigado por comprar connosco!

### ❌ Incorretos (Maliciosos / Phishing)xx

**Assunto:** URGENTE: A sua conta bancária foi bloqueada!
**Corpo:**
Caro(a) Cliente,
Detectamos atividades suspeitas na sua conta bancária. Para evitar o bloqueio permanente, por favor confirme a sua identidade e os seus dados de acesso imediatamente clicando no link abaixo:
http://banco-seguranca-online-2024.com/loginpt/
Se não agir dentro de 24 horas, perderá o acesso definitivo aos fundos da sua conta.
Os melhores cumprimentos,
O Departamento de Segurança

---

## 💬 Mensagens de Texto (SMS / WhatsApp)

### ✅ Corretas (Legítimas / Seguras)
- "CTT Expresso: A sua encomenda 003L456789123 está em distribuição e será entregue hoje entre as 14h e as 18h."
- "MB WAY: O seu codigo para confirmacao e 459123. Valido por 15 min. Nao partilhe com ninguem."
- "A consulta no Centro de Saude de Lisboa foi agendada para 20-05-2026 as 10:30. Para cancelar ligue SNS24."

### ❌ Incorretas (Maliciosas / Smishing)
- "CTT: A sua encomenda foi retida na alfandega. Falta pagar as taxas aduaneiras (1.99€). Pague agora pelo link para libertar a encomenda: http://ctt-taxas-alfandega.com/pay"
- "AT: Autoridade Tributaria informa: Tem um reembolso de imposto pendente no valor de 245,50 EUR. Confirme os seus dados bancarios aqui imediatamente: http://portaldasfinancas-pt.online/reembolsos"
- "Olá Pai, o meu telemóvel partiu-se e estou a usar este número provisório. Podes mandar-me uma mensagem no WhatsApp para este número? É muito urgente, preciso que faças um pagamento por mim."
