class ContextAssemblyLayer:
    """
    Advanced context window management and prompt engineering
    """
    
    def assemble_context(
        self, 
        query: str, 
        retrieved_docs: List[Document],
        graph_context: GraphContext,
        max_tokens: int = 8000
    ) -> AssembledPrompt:
        
        # Strategy 1: Lost-in-the-Middle Prevention
        ordered_docs = self.reorder_for_optimal_positioning(retrieved_docs)
        # Most important at BEGINNING and END of context
        
        # Strategy 2: Compressed Context (for long documents)
        if self.estimate_tokens(ordered_docs) > max_tokens:
            compressed = self.compress_context(ordered_docs, query)
            # Use LLMLingua or selective summarization
        else:
            compressed = ordered_docs
        
        # Strategy 3: Structured Context Formatting
        formatted_context = self.format_with_structure(
            documents=compressed,
            graph_data=graph_context,
            format_template='hierarchical'  # or 'linear', 'tabular'
        )
        
        # Strategy 4: Dynamic Prompt Construction
        prompt = self.build_adaptive_prompt(
            user_query=query,
            context=formatted_context,
            intent=query_intent,
            few_shot_examples=self.select_examples(query_intent),
            instructions=self.get_domain_instructions()
        )
        
        return AssembledPrompt(
            system_prompt=prompt.system,
            user_prompt=prompt.user,
            context_window_usage=self.calculate_usage(formatted_context),
            metadata={
                'num_documents': len(compressed),
                'compression_ratio': len(ordered_docs) / len(compressed),
                'graph_entities': len(graph_context.entities)
            }
        )