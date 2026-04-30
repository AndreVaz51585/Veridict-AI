import re # regular expressions for URL extraction, used to identify patterns in text, such as URLs or specific keywords.
from urllib.parse import urlparse
from app.models.schemas import ExtractedFeatures

class FeatureExtractor:

    SUSPICIOUS_KEYWORDS = [
        # Urgency / common phishing phrases
    "urgent", "click here", "won", "congratulations", "suspended account",
    "validation expires", "password", "update your information", "immediate cancellation",
    "verify your account", "action required", "login attempt", "invoice attached",
    "unauthorized login", "security alert",

    # Sense of urgency
    "immediate action required",
    "act now",
    "final notice",
    "last warning",
    "account will be closed",
    "account locked",
    "account permanently suspended",
    "service interruption",
    "your access will be restricted",
    "deadline today",
    "within 24 hours",
    "within 48 hours",

    # Account security
    "confirm identity",
    "re-authenticate",
    "session expired",
    "new login detected",
    "suspicious activity detected",
    "unusual activity",
    "security breach",
    "data breach",
    "compromised account",
    "reset your password",

    # Financial / payment
    "payment failed",
    "payment declined",
    "refund available",
    "tax refund",
    "invoice overdue",
    "outstanding payment",
    "billing issue",
    "update billing information",
    "credit card expired",
    "verify payment method",
    "tax refund available",
    "irs refund",
    "tax authority",
    "social security",
    "customs notice",
    "government alert",
    "legal notice",
    "court summons",

    # Prizes / rewards
    "you have been selected",
    "claim your prize",
    "free gift",
    "exclusive offer",
    "limited offer",
    "you won a prize",
    "lottery winner",
    "reward points",

    # Delivery / Shipping
    "delivery failed",
    "package on hold",
    "shipment delayed",
    "confirm delivery address",
    "customs fee required",
    "your order is waiting",
    "track your package",

    # Uncommon requests
    "trusted contact",
    "from your friend",
    "shared document",
    "view this file",
    "important document",
    "confidential",
    "private message",
    "download now",
    "open attachment",
    "enable content",
    "view document",
    "secure document",
    "protected file",
]
    
    # the static method is used to define a method that belongs to the class rather than an instance of the class. It can be called on the class itself without needing to create an instance. In this case, it is used for utility functions that do not require access to instance-specific data.
    # indepent function, that does not rely on instance state.
    @staticmethod
    def extract_urls(text: str) -> list[str]:

        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return url_pattern.findall(text)


    @staticmethod
    def extract_domain(url: str) -> str:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove trailing dots (e.g. from end of sentence: "amazon.es.")
            domain = domain.rstrip('.')
            # Strip 'www.' so that WHOIS lookups and the Well-Known domain cache perfectly matches the root domain
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return ""

    @staticmethod
    def check_keywords(text: str, keywords: list[str]) -> list[str]:
        text_lower = text.lower()
        found = [kw for kw in keywords if kw in text_lower]
        return found
        
    # its classmethod because it needs to access the class variable SUSPICIOUS_KEYWORDS, and it is a utility function that processes text to extract features. It does not rely on instance-specific data, but it does need access to the class-level keywords list.    
    @classmethod
    def process_text(cls, text: str, input_type: str = "text") -> ExtractedFeatures:
        urls = cls.extract_urls(text)
        
        if input_type == "link" and not urls:
            url_to_add = text.strip()
            if not url_to_add.startswith("http"):
                url_to_add = "http://" + url_to_add
            urls.append(url_to_add)
            
        domains = [cls.extract_domain(url) for url in urls if cls.extract_domain(url)]
        
        if input_type == "link":
             return ExtractedFeatures(
                 urls=urls,
                 domains=domains,
                 keywords=[],
                 has_urgency=False,
                 is_suspicious_length=False
             )
             
        found_keywords = cls.check_keywords(text, cls.SUSPICIOUS_KEYWORDS)
        
        return ExtractedFeatures(
            urls=urls,
            domains=domains,
            keywords=found_keywords,
            has_urgency="urgent" in [k.lower() for k in found_keywords] or "immediate" in text.lower(),
            is_suspicious_length=len(text) < 10 and len(urls) > 0 # Short messages with links are often suspicious, especially in phishing attempts.
        )
