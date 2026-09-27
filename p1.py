class QueryUnderstandingLayer:
    """
    Sophisticated query analysis and decomposition engine
    """
    
    def process_query(self, user_query: str) -> QueryPlan:
        # Step 1: Intent Classification
        intent = self.classify_intent(user_query)
        # Categories: factual, analytical, comparative, procedural, conversational
        
        # Step 2: Entity Recognition & Linking
        entities = self.extract_entities(user_query)
        linked_entities = self.link_to_knowledge_graph(entities)
        
        # Step 3: Query Complexity Assessment
        complexity = self.assess_complexity(user_query)
        # simple (single-hop) | medium (multi-hop) | complex (reasoning-required)
        
        # Step 4: Query Decomposition (for complex queries)
        if complexity in ['medium', 'complex']:
            sub_queries = self.decompose_query(user_query)
            # Techniques: 
            # - ToR-Lite (lightweight semantic decomposition)
            # - LLM-based recursive decomposition
            # - Template-based decomposition for known patterns
        
        # Step 5: Query Reformulation & Expansion
        expanded_queries = self.expand_query(user_query)
        # HyDE (Hypothetical Document Embeddings)
        # Multi-query generation
        # Step-back prompting (abstract to general then specific)
        
        return QueryPlan(
            original_query=user_query,
            intent=intent,
            entities=linked_entities,
            sub_queries=sub_queries,
            reformulations=expanded_queries,
            retrieval_strategy=self.select_strategy(intent, complexity)
        )