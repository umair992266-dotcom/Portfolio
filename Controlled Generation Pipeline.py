class GenerationLayer:
    """
    LLM invocation with output control and validation
    """
    
    def generate(
        self, 
        assembled_prompt: AssembledPrompt,
        config: GenerationConfig
    ) -> GeneratedResponse:
        
        # Model Selection (based on complexity/cost)
        model = self.select_model(
            complexity=config.query_complexity,
            latency_requirement=config.max_latency,
            budget_constraint=config.cost_budget
        )
        # Options: GPT-4o (quality), Claude 3.5 (reasoning), 
        #          Llama 3.1 (cost-effective), Mixtral (balanced)
        
        # Invoke with Parameters
        raw_response = model.generate(
            prompt=assembled_prompt,
            temperature=config.temperature,  # 0.0-0.7 for factual, 0.7-1.0 for creative
            top_p=config.top_p,
            max_tokens=config.max_output_tokens,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
            stop_sequences=config.stop_sequences
        )
        
        # Post-Processing Pipeline
        processed = self.post_process(raw_response)
        
        # Output Validation
        validation_result = self.validate_output(processed, assembled_prompt.context)
        
        if not validation_result.is_valid:
            # Retry with adjusted parameters or different strategy
            return self.handle_validation_failure(validation_result)
        
        return GeneratedResponse(
            content=processed.content,
            citations=processed.citations,
            confidence_score=validation_result.confidence,
            tokens_used=processed.token_count,
            model_used=model.name,
            latency=processed.latency
        )