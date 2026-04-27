import asyncio
from typing import List, Tuple
from app.models.schemas import ExtractedFeatures
import whois
import socket
from datetime import datetime, timezone

# Cache for DNS and WHOIS checks { domain: { "dns": bool, "age": int, "timestamp": datetime } }
DOMAIN_CACHE = {}
# Known safe domains to skip expensive WHOIS lookups
WELL_KNOWN_DOMAINS = {"google.com", "microsoft.com", "apple.com", "amazon.com", "facebook.com", "netflix.com", "paypal.com", "github.com", "linkedin.com", "twitter.com"}

class ReputationService:
    @staticmethod
    async def check_domain_age(domain: str) -> int:
        if domain in WELL_KNOWN_DOMAINS:
            return 9999 # Safe value
            
        loop = asyncio.get_event_loop()
        try:
            w = await loop.run_in_executor(None, whois.whois, domain)
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
        except Exception:
            return -1
            
    @staticmethod
    async def check_dns_resolution(domain: str) -> bool:
        if domain in WELL_KNOWN_DOMAINS:
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
        
        if not features.domains:
            return score, flags
            
        for domain in features.domains:
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
            if age_days != -1:
                if age_days < 30:
                    score += 0.8
                    flags.append(f"Domain '{domain}' is very recent ({age_days} days old), high risk of being a temporary phishing domain.")
                elif age_days < 180:
                    score += 0.3
                    flags.append(f"Domain '{domain}' was created relatively recently ({age_days} days old).")
            else:
                score += 0.2
                flags.append(f"Could not verify creation date for domain '{domain}'.")
                
        final_score = min(max(score, 0.0), 1.0)
        return final_score, flags
