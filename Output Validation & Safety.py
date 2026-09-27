class OutputValidator:
    """
    Ensures generated responses are accurate, safe, and grounded
    """
    
    def validate(self, response: str, context: List[Document]) -> ValidationResult:
        checks = {}
        
        # 1. Groundedness Check (Hallucination Detection)
        checks['groundedness'] = self.verify_claims_against_sources(response, context)
        
        # 2. Factuality Verification
        checks['factuality'] = self.fact_check(response)
        
        # 3. Safety & Policy Compliance
        checks['safety'] = self.safety_check(response)
        # PII detection, hate speech, harmful content
        
        # 4. Coherence & Fluency
        checks['coherence'] = self.assess_coherence(response)
        
        # 5. Completeness (did we answer the question?)
        checks['completeness'] = self.check_completeness(response, original_query)
        
        # Aggregate Score
        overall_score = np.mean([check.score for check in checks.values()])
        
        return ValidationResult(
            is_valid=overall_score > 0.8,
            confidence=overall_score,
            individual_checks=checks,
            issues=[k for k,v in checks.items() if v.score < 0.7]
        )