from pydantic import BaseModel, Field
from typing import List, Optional

# The field is used to provide additional metadata for the model fields, such as descriptions, default values, and validation constraints. Very useful for API documentation and ensuring that the data adheres to specific rules.
# The BaseModel is the base class for creating data models in Pydantic, which provides data validation and parsing capabilities. By inheriting from BaseModel, you can define your own data models with specific fields and validation rules.

class AnalysisRequest(BaseModel):
    content: str = Field(..., description="The raw text, message body, email body, or URL to be analyzed")

class ExtractedFeatures(BaseModel):
    urls: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    has_urgency: bool = False
    is_suspicious_length: bool = False


# ge stands for greater or equal, and le stands for less or equal.

class RuleEngineResult(BaseModel):
    rule_score: float = Field(ge=0.0, le=1.0) 
    flags: List[str] = Field(default_factory=list)

class ReputationResult(BaseModel):
    reputation_score: float = Field(ge=0.0, le=1.0)
    reputation_flags: List[str] = Field(default_factory=list)

class AnalysisResponse(BaseModel):
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: str = Field(..., description="Secure, Suspicious, or Dangerous")
    explanation: str
    recommendation: str
    extracted_features: Optional[ExtractedFeatures] = None
    rule_result: Optional[RuleEngineResult] = None
