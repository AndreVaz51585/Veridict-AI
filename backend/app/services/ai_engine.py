from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document
import json
import os

OLLAMA_MODEL = "llama3"

class AIEngine:
    def __init__(self):
        # Start core LLM and Embedder dependencies
        self.llm = Ollama(model=OLLAMA_MODEL)
        self.embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
        
        # Load Chroma Vector Store 
        self.persist_directory = "./chroma_db"
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
            
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def retrieve_related_context(self, text: str) -> str:
        """Retrieves past analyses from the vector store."""
        try:
            results = self.vector_store.similarity_search(text, k=3)
            # If we don't have results yet, just return empty
            if not results:
                 return ""
                 
            # Format the output from the metadata stored
            history_text = "\n".join([
                f"- Past Similar Message: {res.page_content}\n  AI Result: {res.metadata.get('explanation', 'Known phishing pattern.')} (Class: {res.metadata.get('classification', 'malicious')})" 
                for res in results
            ])
            return history_text
            
        except Exception as e:
            print("Failed to retrieve context from ChromaDB:", e)
            return ""

    def save_to_memory(self, text: str, result: dict):
        """Saves a processed message to the local ChromaDB vector store."""
        try:
            # We don't want to pollute DB with completely clean things.
            # Optional: just save suspicious or dangerous ones.
            if result.get("ai_score", 0.0) > 0.35:
                doc = Document(
                    page_content=text,
                    metadata={
                        "ai_score": result.get("ai_score", 0.0),
                        "classification": result.get("classification", "suspicious"),
                        "explanation": result.get("explanation", "")
                    }
                )
                self.vector_store.add_documents([doc])
        except Exception as e:
            print("Failed to save to ChromaDB:", e)

            
    def generate_context(self, text: str, rule_flags: list, rep_flags: list, past_context: str) -> str:
        
        prompt = f"""
You are Veridict AI, a cybersecurity expert assistant analyzing messages to protect users from phishing and social engineering.
Your task is to analyze ONLY the current user's message and the findings from our rule engine and reputation service.

CURRENT MESSAGE FOR ANALYSIS: "{text}"

Findings from Rule Engine:
{', '.join(rule_flags) if rule_flags else "No immediate structural red flags found."}

Findings from Reputation Service:
{', '.join(rep_flags) if rep_flags else "No URL/domain reputation warnings."}
"""
        if past_context:
            prompt += f"""
---
CONTEXT MATTERS (Do NOT mix these topics into the explanation for the current message):
Below are historical instances of SIMILAR phrasing or links we caught in the past. 
Use this ONLY to recognize patterns or determine if the CURRENT message matches a known phishing vector.
{past_context}
---
"""

        prompt += """
Analyze the tone, context, findings, and overall urgency of the CURRENT MESSAGE. 
Pay special attention to domains that do not resolve, use shorteners (like bit.ly), or are very recent, as these are massive red flags for phishing. Give a high penalty for typosquatting.

Return only a valid JSON with the following structure:
{
  "ai_score": float (between 0.0 for completely safe to 1.0 for extremely dangerous. Be assertive: if DNS fails or shortener used suspiciously, score > 0.80),
  "classification": string ("safe", "suspicious", or "dangerous"),
  "explanation": "A short, assertive list of 2-3 bullet points explaining the risk. Do not write a paragraph.",
  "recommendation": "A short, actionable piece of advice (e.g. 'Do not click the link.', 'Verify via official app.', etc)",
  "confidence": float (between 0.0 to 1.0)
}

Make sure your explanation is clear, highly relevant ONLY to the CURRENT MESSAGE, and outputs only valid JSON. 
"""
        return prompt
    def analyze(self, text: str, rule_flags: list, rep_flags: list) -> dict:
        
        # Query ChromaDB specifically for this text
        past_context = self.retrieve_related_context(text)
        
        prompt = self.generate_context(text, rule_flags, rep_flags, past_context)
        response = self.llm.invoke(prompt)
        
        try:
            # Safely parse JSON output
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                # Save the new finding to Memory if it's considered malicious
                self.save_to_memory(text, parsed)
                
                return parsed
            else:
                raise ValueError("JSON not found in LLM output")
        except Exception as e:
            print("Failed to parse LLaMA output:", response)
            return {
                "ai_score": 0.5,
                "classification": "suspicious",
                "explanation": "The AI model returned an ambiguous response. Please rely on rule and reputation scores.",
                "confidence": 0.0,
                "recommendation": "Be cautious and verify the sender."
            }
