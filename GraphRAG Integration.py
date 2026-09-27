class GraphRetrievalLayer:
    """
    Knowledge graph-enhanced retrieval for relational reasoning
    """
    
    def retrieve(self, query_entities: List[Entity]) -> GraphContext:
        # Local Retrieval: Direct entity neighborhood
        local_context = self.traverse_graph(
            start_nodes=query_entities,
            depth=2,  # 2-hop neighbors
            relation_types=['related_to', 'part_of', 'causes']
        )
        
        # Global Retrieval: Community detection for broad topics
        global_context = self.detect_communities(
            seed_entities=query_entities,
            algorithm='leiden',  # or louvain
            summary_level='medium'  # community summaries
        )
        
        # Multi-Hop Reasoning Paths
        reasoning_paths = self.find_paths(
            source=query_entities[0],
            target=query_entities[-1],
            max_hops=3,
            path_scoring='relevance_weighted'
        )
        
        return GraphContext(
            local=local_context,
            global=global_context,
            paths=reasoning_paths,
            structured_facts=self.extract_triples(local_context)
        )