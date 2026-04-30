import asyncio
from typing import List, Tuple
from app.models.schemas import ExtractedFeatures
import whois
import socket
import requests
import os
from datetime import datetime, timezone

import urllib.parse
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DOMAIN_CACHE = {}

WELL_KNOWN_DOMAINS = {
    "google.com", "microsoft.com", "apple.com", "amazon.com",
    "amazon.es", "amazon.co.uk", "amazon.de",
    "facebook.com", "meta.com",
    "instagram.com", "whatsapp.com",
    "netflix.com",
    "paypal.com",
    "github.com",
    "linkedin.com",
    "x.com", "twitter.com",
    "snapchat.com",
    "tiktok.com",
    "discord.com",
    "telegram.org",
    "dropbox.com",

    "aws.amazon.com",
    "azure.com",
    "cloudflare.com",
    "digitalocean.com",
    "fastly.com",

    "visa.com",
    "mastercard.com",
    "stripe.com",
    "wise.com",
    "revolut.com",
    "bankofamerica.com",
    "chase.com",
    "hsbc.com",
    "santander.pt",
    "millenniumbcp.pt",
    "bportugal.pt",

    "ctt.pt",
    "financas.gov.pt",
    "seg-social.pt",
    "portaldasfinancas.gov.pt",
    "ama.gov.pt",
    "dgs.pt",

    "aliexpress.com",
    "ebay.com",
    "etsy.com",
    "shopify.com",
    "walmart.com",

    "steamcommunity.com",
    "steampowered.com",
    "epicgames.com",
    "riotgames.com",
    "playstation.com",
    "xbox.com",

    "gmail.com",
    "outlook.com",
    "office.com",
    "live.com",
    "teams.microsoft.com",
    "zoom.us",

    "dhl.com",
    "ups.com",
    "fedex.com",
    "gls-group.com",
    "ctt.pt"
}


class ReputationService:
    @staticmethod
    def _query_google_safe_browsing_v4(urls: List[str], api_key: str) -> dict:
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "client": {
                "clientId": "veridict-ai",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": u} for u in urls]
            }
        }
        
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json() # This will contain "matches" if any threats are found, or be empty if the URLs are not in the cache of known threats.
        return {}

    @classmethod
    async def check_safe_browsing(cls, urls: List[str]) -> List[str]:
        api_key = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "")

        print(f"[DEBUG] Google API Key loaded: {bool(api_key)}, URLs recebidos: {urls}")

        if not api_key or not urls:
            return []
        
        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, cls._query_google_safe_browsing_v4, urls, api_key)
            
            if "matches" in data and data["matches"]:
                malicious_identified = [match.get("threat", {}).get("url") for match in data["matches"] if match.get("threat", {}).get("url")]
                print(f"[*] Google Safe Browsing API successfully queried for {len(urls)} URL(s). Threats found: {len(malicious_identified)}")
                return list(set(malicious_identified))
            else:
                print(f"[*] Google Safe Browsing V4 verified {len(urls)} URL(s): Secure URL(s) (0 Threats, not listed in cache/DB).")
                return []
                    
        except Exception as e:
            print(f"Google Safe Browsing V4 validation failed: {str(e)}")
            
        return []

    @staticmethod
    def is_well_known_domain(domain: str) -> bool:
        if domain in WELL_KNOWN_DOMAINS:
            return True
            # this is a basic heuristic to catch government and educational institutions, which are almost universally safe and often have WHOIS privacy or other red herrings that could inflate their risk score unnecessarily. We want to ensure these are treated as safe without needing to rely on potentially unreliable WHOIS data.
        if domain.endswith(".gov.pt") or domain.endswith(".gov") or domain.endswith(".edu"):
            return True
        return False

    @classmethod
    async def check_domain_age(cls, domain: str) -> int:
        
        if cls.is_well_known_domain(domain):
            return 9999 # Safe value
            
        loop = asyncio.get_event_loop()
        try:
            w = await loop.run_in_executor(None, whois.whois, domain)
            
            # Se o domínio constar como não reconhecido / não registado, devolvemos -2
            if w.text and any(nf in w.text.upper() for nf in ["NO MATCH", "NOT FOUND", "NO ENTRIES FOUND", "UNREGISTERED"]):
                return -2
                
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if creation_date:
                now = datetime.now()
                if creation_date.tzinfo:
                    now = datetime.now(timezone.utc)
                age_days = (now - creation_date).days
                return age_days
            return -1
        except Exception as e:
            if "PywhoisError" in str(type(e)) or "No match" in str(e):
                return -2 # Domínio explicitamente não encontrado na bd de WHOIS
            return -1 # Timeout, Rate Limit, ou bloqueio de porta
            
    @classmethod
    async def check_dns_resolution(cls, domain: str) -> bool:
        if cls.is_well_known_domain(domain):
            return True
            
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, socket.gethostbyname, domain)
            return True
        except socket.error:
            return False

    @classmethod
    async def analyze(cls, features: ExtractedFeatures) -> Tuple[float, List[str]]:
        score = 0.0
        flags = []
        
        if not features.domains and not features.urls:
            return score, flags
            
        #Check Full URLs against Google Safe Browsing API first
        if features.urls:
            malicious_urls = await cls.check_safe_browsing(features.urls)
            
            if not malicious_urls:
                flags.append("Google Safe Browsing DB: No threats found in the current cache for the URL(s). The link may be safe or too recent.")
                
            for m_url in malicious_urls:
                score += 1.0 # Instant maximum risk via Google Safe Browsing
                flags.append(f"Critical Warning: Google Safe Browsing strongly flagged the URL with Threats (Malware/Phishing): {m_url}")
                
        # Extract checks for Individual Domains
        for raw_domain in features.domains:
            # Força remoção de 'www.' caso algo tenha escapado ao extractor
            domain = raw_domain[4:] if raw_domain.startswith('www.') else raw_domain

            # Check Cache
            cached = DOMAIN_CACHE.get(domain)
            if cached:
                resolves = cached["dns"]
                age_days = cached["age"]
            else:
                # Run checks concurrently
                resolves, age_days = await asyncio.gather(
                    cls.check_dns_resolution(domain),
                    cls.check_domain_age(domain)
                )
                DOMAIN_CACHE[domain] = {"dns": resolves, "age": age_days, "timestamp": datetime.now()}

            # Check DNS
            if not resolves:
                score += 0.5
                flags.append(f"Domain '{domain}' does not resolve to an IP address.")
                continue

            # Check Age
            if age_days == -2:
                score += 0.5
                flags.append(f"Domain '{domain}' is completely unregistered or missing from WHOIS databases. This is highly suspicious.")
            elif age_days != -1:
                if age_days < 30:
                    score += 0.8
                    flags.append(f"Domain '{domain}' is very recent ({age_days} days old), high risk of being a temporary phishing domain.")
                elif age_days < 180:
                    score += 0.3
                    flags.append(f"Domain '{domain}' was created relatively recently ({age_days} days old).")
                elif cls.is_well_known_domain(domain):
                    flags.append(f"Domain '{domain}' is a highly reputable, universally known organization (or government entity).")
                else:
                    flags.append(f"Domain '{domain}' is established ({age_days} days old) and therefore safer.")
            else:
                flags.append(f"Could not verify exact creation date for domain '{domain}' (WHOIS shielded/timeout), but no recent registration concerns found.")

        final_score = min(max(score, 0.0), 1.0)
        return final_score, flags
