# Veridict-AI


Veridict AI — System Design & Product Definition

Visão Geral

Veridict AI é uma aplicação de cibersegurança baseada em inteligência artificial que analisa mensagens, emails e links com o objetivo de detetar potenciais ameaças como phishing, engenharia social e conteúdos maliciosos.

A aplicação fornece ao utilizador:
	•	Uma avaliação de risco quantitativa (score)
	•	Uma classificação clara (Seguro, Suspeito, Perigoso)
	•	Uma explicação em linguagem natural
	•	Recomendações acionáveis

O sistema foi concebido com uma abordagem privacy-first, sem necessidade de armazenamento persistente numa fase inicial, e com uma arquitetura modular e escalável.

⸻

Objetivo Principal

Permitir que qualquer utilizador — especialmente não técnico — consiga:
	•	Validar rapidamente uma mensagem ou link
	•	Compreender o risco associado
	•	Tomar decisões informadas antes de clicar ou responder

⸻

Abordagem Técnica (Core Concept)

O Veridict AI utiliza um modelo híbrido de decisão, combinando:
	1.	Análise baseada em regras (determinística)
	2.	Verificação de reputação (dados externos)
	3.	Análise contextual com LLM (AI)
	4.	Sistema de scoring unificado

O ponto crítico do sistema é que a AI não decide sozinha.
Ela recebe contexto estruturado e contribui para o veredicto final, que é calculado de forma ponderada.

⸻

Pipeline de Análise

User Input (text/email/link)
↓
Feature Extraction
↓
Rule Engine → Score parcial
↓
Reputation Service → Score parcial
↓
AI Engine (Ollama) → Score + explicação
↓
Risk Scorer → Score final agregado
↓
Response Builder → Output estruturado

⸻

Componentes do Sistema

1. Feature Extraction Layer

Responsável por transformar input bruto em dados estruturados.

Extrai:
	•	URLs
	•	Domínios
	•	Palavras-chave suspeitas
	•	Estrutura textual (urgência, tom, etc.)
	•	Metadados de email (quando aplicável)

⸻

2. Rule Engine

Sistema determinístico baseado em heurísticas.

Exemplos:
	•	Uso de palavras como “urgente”, “ganhou”, “clique agora”
	•	URLs encurtadas
	•	Domínios semelhantes a marcas legítimas (typosquatting)
	•	Links excessivamente longos ou ofuscados

Output:

{
“rule_score”: 0.0 - 1.0,
“flags”: […]
}

⸻

3. Reputation Service

Avalia a confiabilidade de entidades externas.

Fatores:
	•	Idade do domínio (WHOIS)
	•	Presença em listas negras
	•	Histórico conhecido

Nota: inicialmente pode ser simulado ou simplificado.

⸻

4. AI Engine (LLM via Ollama)

A AI não recebe apenas texto — recebe contexto enriquecido.

Input para o modelo:
	•	Texto original
	•	URLs extraídas
	•	Resultados do rule engine
	•	Dados de reputação
	•	(Opcional) contexto RAG

Output esperado:

{
“ai_score”: 0.0 - 1.0,
“classification”: “safe | suspicious | dangerous”,
“explanation”: “…”,
“confidence”: 0.0 - 1.0
}

A AI atua como analista contextual, não como decisor absoluto.

⸻

5. Risk Scoring Engine (Crítico)

Combina todas as fontes de forma ponderada:

final_score = (
0.4 * rule_score +
0.2 * reputation_score +
0.4 * ai_score
)

Classificação baseada no score:

0.0 – 0.3 → Seguro
0.3 – 0.7 → Suspeito
0.7 – 1.0 → Perigoso

Isto garante consistência e reduz erros da AI.

⸻

6. Response Builder

Transforma o resultado técnico em algo utilizável:

{
“risk_score”: 0.78,
“risk_level”: “Perigoso”,
“explanation”: “O domínio foi criado recentemente e contém sinais de phishing…”,
“recommendation”: “Não clicar no link e evitar fornecer dados pessoais”
}

⸻

RAG (Retrieval-Augmented Generation)

Para melhorar a qualidade da AI, o sistema pode incorporar um módulo RAG.

Dados utilizados:
	•	Exemplos reais de phishing
	•	Padrões conhecidos
	•	Casos de engenharia social

Funcionamento:
	1.	Input é convertido em embedding
	2.	Pesquisa em base vetorial (FAISS ou Chroma)
	3.	Contexto relevante é injetado no prompt

Resultado:
	•	AI mais precisa
	•	Explicações mais realistas

⸻

Arquitetura do Backend

Backend desenvolvido em FastAPI, organizado de forma modular:
	•	API Layer → endpoints
	•	Service Layer → lógica de negócio
	•	Analysis Engine → pipeline de deteção
	•	AI Layer → interação com LLM
	•	Scoring Layer → decisão final

⸻

Frontend

Desenvolvido com React e Vite.

Formato:
	•	Progressive Web App (PWA)

Objetivo:
	•	Interface simples
	•	Input direto (colar mensagem)
	•	Output visual claro (cores + explicação)

⸻

Persistência de Dados

Fase inicial:
	•	Sem base de dados (privacy-first)

Fase futura:
	•	Histórico de análises
	•	Feedback do utilizador
	•	Aprendizagem contínua

⸻

Considerações de Segurança
	•	Sanitização de inputs
	•	Rate limiting
	•	Não armazenamento de dados sensíveis
	•	Logs anonimizados

⸻

Roadmap

MVP:
	•	Input texto
	•	Rule engine
	•	AI via Ollama
	•	Score final

Fase 2:
	•	Reputation APIs
	•	RAG
	•	Melhor scoring

Fase 3:
	•	Base de dados
	•	Contas de utilizador
	•	Extensão de browser

⸻

Diferencial do Veridict AI

O que distingue esta aplicação:
	•	Abordagem híbrida (regras + AI + scoring)
	•	AI contextualizada (não isolada)
	•	Explicações claras e úteis
	•	Arquitetura modular e escalável
	•	Foco em utilizadores não técnicos

⸻

Conclusão

Veridict AI não é apenas um classificador de phishing — é um sistema de decisão assistida que combina engenharia de software, cibersegurança e inteligência artificial.

O foco não está apenas em detetar ameaças, mas em explicar o risco de forma compreensível, permitindo ao utilizador agir com confiança.
