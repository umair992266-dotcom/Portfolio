class RerankingRefinementLayer:
    """
    Multi-model reranking with self-correction capabilities
    """
    
    def __init__(self):
        self.bi_encoder = BiEncoderModel('ms-marco-MiniLM-L-6-v2')
        self.cross_encoder = CrossEncoderModel('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.llm_judge = LLMAsJudge(model='gpt-4o-mini')
        
    def rerank(self, query: str, candidates: List[Document]) -> List[Document]:
        # Stage 1: Fast Bi-Encoder Scoring
        scored = [
            (doc, self.bi_encoder.score(query, doc))
            for doc in candidates
        ]
        top_20 = sorted(scored, key=lambda x: x[1], reverse=True)[:20]
        
        # Stage 2: Precise Cross-Encoder Reranking
        cross_scored = [
            (doc, self.cross_encoder.score(query, doc.text))
            for doc, _ in top_20
        ]
        top_10 = sorted(cross_scored, key=lambda x: x[1], reverse=True)[:10]
        
        # Stage 3: LLM-Based Relevance Judgment (for top critical docs)
        final_scores = []
        for doc, score in top_10:
            relevance = self.llm_judge.evaluate_relevance(query, doc)
            final_scores.append((doc, score * 0.7 + relevance * 0.3))
        
        return [doc for doc, _ in sorted(final_scores, key=lambda x: x[1], reverse=True)[:5]]