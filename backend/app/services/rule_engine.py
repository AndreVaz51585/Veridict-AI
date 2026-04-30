class RuleEngine:

    SUSPICIOUS_DOMAINS = [
    "xyz", "online", "top", "pw", "cc", "zip", "click", "link", "party",
    "gq", "run", "shop", "site", "vip", "club", "info", "pro", "biz",
    "loan", "men", "work", "date", "icu", "review",

    "best", "live", "app", "store", "website", "space", "fun",
    "monster", "today", "world", "digital", "tech", "solutions",
    "support", "help", "email", "cloud", "services",

    "tk", "ml", "ga", "cf", "gq",  

    "cam", "bar", "rest", "host", "press", "media", "agency"

    ]
    SHORTENERS = [
    "bit.ly", "tinyurl", "t.co", "is.gd", "goo.gl", "ow.ly",
    "cutt.ly", "buff.ly", "rebrand.ly",

    "rb.gy", "shorturl.at", "lnkd.in", "trib.al",
    "soo.gd", "v.gd", "qr.ae",

    "linktr.ee", "linkin.bio", "bio.link",

    "redirect", "go.", "go-link", "url", "click", "track"
    ]


    TYPOSQUATTING_TARGETS = [
    # Big Tech
    "google", "facebook", "meta", "instagram", "whatsapp",
    "apple", "microsoft", "amazon", "paypal", "netflix",
    "linkedin", "twitter", "x", "snapchat", "tiktok",
    "discord", "telegram", "github", "dropbox",

    # Finance / payments
    "visa", "mastercard", "revolut", "wise", "stripe",
    "bankofamerica", "chase", "hsbc", "santander",

    # Crypto exchanges
    "binance", "coinbase", "kraken", "okx", "bybit",

    # Portugal 
    "ctt", "financas", "autoridade tributaria", "seguranca social",
    "mbway", "multibanco", "caixadirecta", "novobanco", "bpi",
    "santanderpt", "millenniumbcp","emel"

    # E-commerce / platforms
    "aliexpress", "ebay", "shopify", "walmart", "etsy",

    # Cloud / dev tools
    "aws", "azure", "cloudflare", "digitalocean",

    # Email / productivity
    "gmail", "outlook", "office365", "teams", "zoom",

    # Gaming (muito phishing aqui)
    "steam", "epicgames", "riotgames", "playstation", "xbox"
    ]

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
                    
                if any(domain == shortener or domain.endswith(f".{shortener}") for shortener in cls.SHORTENERS):
                    score += 0.8  # VERY HIGH RISK for shorteners
                    flags.append(f"The link uses a URL shortener ({domain}). Phishers often use this to hide their true destination.")
                    
                for target in cls.TYPOSQUATTING_TARGETS:
                    # Basic check for brand name in domain, ignoring if it is the official root domain
                    if target in domain and domain not in [f"{target}.com", f"www.{target}.com", f"{target}.es", f"www.{target}.es", f"{target}.pt", f"www.{target}.pt", f"{target}.gov.pt"]:
                        score += 0.6
                        flags.append(f"Possible typosquatting: Domain '{domain}' looks like it might be impersonating '{target}'.")
                        
        # No random jitter added, to ensure reproducible deterministic testing
        final_score = min(max(score, 0.0), 1.0)
        
        return final_score, flags