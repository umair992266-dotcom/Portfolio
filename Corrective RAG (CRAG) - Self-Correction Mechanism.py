class CorrectiveRAG:
    """
    Implements CRAG: Assess retrieval quality and correct if needed
    """
    
    def assess_and_correct(self, query: str, retrieved_docs: List[Document]) -> CorrectionResult:
        # Step 1: Retrieve Relevance Score
        relevance_checker = RelevanceClassifier()
        is_relevant, confidence = relevance_checker.check(query, retrieved_docs)
        
        if confidence > 0.9 and is_relevant:
            return CorrectionResult(
                action='proceed',
                documents=retrieved_docs,
                correction_applied=False
            )
        
        elif confidence < 0.3 or not is_relevant:
            # Step 2: Knowledge Refinement - Web Search Fallback
            web_results = self.web_search(query)
            corrected_docs = self.merge_and_rerank(retrieved_docs, web_results)
            
            return CorrectionResult(
                action='corrected_with_web',
                documents=corrected_docs,
                correction_applied=True,
                fallback_used=True
            )
        
        else:  # Medium confidence - Decompose and Refine
            # Step 3: Query Decomposition & Parallel Retrieval
            sub_queries = self.decompose(query)
            all_results = []
            for sq in sub_queries:
                sq_results = self.retrieve(sq)
                all_results.extend(sq_results)
            
            # Merge, deduplicate, rerank
            refined = self.knowledge_refine(all_results, query)
            
            return CorrectionResult(
                action='decomposed_and_refined',
                documents=refined,
                correction_applied=True,
                decomposition_used=True
            )