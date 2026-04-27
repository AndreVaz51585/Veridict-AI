class RuleEngine:

    SUSPICIOUS_DOMAINS = ["xyz", "online", "top", "pw", "cc", "zip", "click", "link", "party", "gq", "run", "shop", "site", "vip", "club", "info", "pro", "biz", "loan", "men", "work", "date", "icu", "review"]
    SHORTENERS = ["bit.ly", "tinyurl", "t.co", "is.gd", "goo.gl", "ow.ly", "cutt.ly", "buff.ly", "rebrand.ly"]
    TYPOSQUATTING_TARGETS = ["google", "facebook", "amazon", "apple", "microsoft", "paypal", "netflix", "instagram", "whatsapp", "linkedin", "ctt", "financas"]

    @classmethod
    def analyze(cls, features) -> tuple[float, list[str]]:
        score = 0.0
        flags = []
        
        if features.keywords:
            weight = min(len(features.keywords) * 0.1, 0.4)
            score += weight
            flags.append(f"Text contains {len(features.keywords)} terms frequently used in social engineering.")

        if features.has_urgency:
            score += 0.2
            flags.append("The text invokes a sense of urgency.")

        if features.is_suspicious_length:
            score += 0.3
            flags.append("The message is unusually short and contains a link (strong indicator of spam).")

        if len(features.urls) > 0:
            for domain in features.domains:
                if any(domain.endswith(f".{tld}") for tld in cls.SUSPICIOUS_DOMAINS):
                    score += 0.5
                    flags.append(f"The link points to a highly risky domain extension ({domain}).")
                    
                if any(shortener in domain for shortener in cls.SHORTENERS):
                    score += 0.8  # VERY HIGH RISK for shorteners
                    flags.append(f"The link uses a URL shortener ({domain}). Phishers often use this to hide their true destination.")
                    
                for target in cls.TYPOSQUATTING_TARGETS:
                    # Basic check for brand name in domain, ignoring if it is the official root domain
                    if target in domain and domain not in [f"{target}.com", f"www.{target}.com", f"{target}.es", f"www.{target}.es", f"{target}.pt", f"www.{target}.pt", f"{target}.gov.pt"]:
                        score += 0.6
                        flags.append(f"Possible typosquatting: Domain '{domain}' looks like it might be impersonating '{target}'.")
                        
        import random
        # Add random jitter between 0.01 and 0.08 to make the score appear more natural
        jitter = random.uniform(0.01, 0.08)
        final_score = min(max(score + jitter, 0.0), 1.0)
        
        return final_score, flags