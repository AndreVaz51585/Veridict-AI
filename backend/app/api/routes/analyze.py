from fastapi import APIRouter
from app.models.schemas import AnalysisRequest, AnalysisResponse, ExtractedFeatures, RuleEngineResult
from app.services.extractor import FeatureExtractor
from app.services.rule_engine import RuleEngine
from app.services.reputation import ReputationService
from app.services.ai_engine import AIEngine
from typing import Optional

router = APIRouter()
ai_engine = AIEngine()

@router.post("/analyze", response_model=AnalysisResponse, description="Primary analysis endpoint")
async def analyze_content(request: AnalysisRequest):

    extracted_features = FeatureExtractor.process_text(request.content)
    
    score, flags = RuleEngine.analyze(extracted_features)
    rule_result = RuleEngineResult(rule_score=score, flags=flags)
    
    rep_score, rep_flags = await ReputationService.analyze(extracted_features)
    
    ai_response = ai_engine.analyze(request.content, flags, rep_flags)
    ai_score = ai_response.get("ai_score", 0.0)
    ai_recommendation = ai_response.get("recommendation", "Exercise caution.")

    has_critical_risk = any("does not resolve" in flag for flag in rep_flags) or any("very recent" in flag for flag in rep_flags)
    if has_critical_risk:
        rep_score = 1.0
    
    final_score = (0.35 * rule_result.rule_score) + (0.35 * rep_score) + (0.30 * ai_score)
    if has_critical_risk:
        final_score = max(final_score, 0.90)

    final_score = min(max(final_score, 0.0), 1.0)
    
    risk_level = "Secure"
    if final_score >= 0.7:
        risk_level = "Dangerous"
    elif final_score >= 0.35:
        risk_level = "Suspicious"
        
    explanation = f"AI Explanation: {ai_response.get('explanation', '')}"
    if rule_result.flags:
        explanation += f" | Rules triggered: {', '.join(rule_result.flags)}"
    if rep_flags:
        explanation += f" | Reputation warnings: {', '.join(rep_flags)}"
        
    recommendation = ai_recommendation if risk_level != "Secure" else "Looks to be in compliance. Validate cautiously."
    
    return AnalysisResponse(
        risk_score=final_score,
        risk_level=risk_level,
        explanation=explanation,
        recommendation=recommendation,
        extracted_features=extracted_features,
        rule_result=rule_result
    )

