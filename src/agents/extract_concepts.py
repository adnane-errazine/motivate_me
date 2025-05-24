from src.agents.orchestrator import WorkflowState


async def _extract_significant_concepts_node(
    self, state: WorkflowState
) -> WorkflowState:
    """Extract only significant mathematical/scientific concepts, filtering out basic elements"""
    try:
        logger.info("Extracting significant concepts from lecture material")

        # Prepare the prompt - focus on major concepts only
        system_prompt = """You are an expert at identifying significant mathematical, scientific, and engineering concepts from academic material. 

IMPORTANT: Only extract major concepts, theorems, phenomena, and advanced mathematical/scientific principles. 
DO NOT extract basic elements like:
- Individual numbers, variables, or symbols
- Basic operations (+, -, ×, ÷)
- Simple geometric shapes
- Elementary concepts

DO extract significant concepts like:
- Named theorems (Fourier Transform, Laplace Transform, etc.)
- Mathematical phenomena (Resonance, Interference, etc.)  
- Advanced techniques (Convolution, Optimization, etc.)
- Scientific principles (Wave mechanics, Quantum effects, etc.)
- Engineering methods (Signal processing, Control theory, etc.)

For each significant concept, provide:
1. Name: The official name of the theorem/concept/phenomenon
2. Type: (theorem, principle, method, phenomenon, etc.)
3. Domain: (mathematics, physics, engineering, computer science, etc.)
4. Significance: Why this concept is important and powerful
5. Mathematical_basis: Core mathematical foundation
6. Confidence: Your confidence this is correctly identified (0.0-1.0)

Return a JSON array with only the most significant 2-4 concepts. Quality over quantity."""

        # Encode image
        image_data = self._encode_image(state["image_path"])

        # Prepare user message
        user_content = f"""Analyze this lecture material for significant mathematical/scientific concepts.

Additional context: {state['text_input']}
User background: {json.dumps(state['user_metadata'])}

Focus on identifying major theorems, principles, or phenomena that have real-world applications."""

        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(
                role="user",
                content=[
                    {"type": "text", "text": user_content},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                    },
                ],
            ),
        ]

        response = await self.mistral_client.chat(
            model=config.MISTRAL_MODEL,
            messages=messages,
            max_tokens=1500,
            temperature=0.2,  # Lower temperature for more focused extraction
        )

        # Parse response
        concepts_text = response.choices[0].message.content
        try:
            concepts = json.loads(concepts_text)
            if not isinstance(concepts, list):
                concepts = [concepts]
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from text
            import re

            json_match = re.search(r"\[.*\]", concepts_text, re.DOTALL)
            if json_match:
                concepts = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse concepts JSON")

        # Filter by confidence and limit to most significant
        significant_concepts = [
            c
            for c in concepts
            if c.get("confidence", 0) >= 0.7  # Higher threshold for significance
        ][
            :4
        ]  # Max 4 significant concepts

        state["significant_concepts"] = significant_concepts
        logger.info(
            f"Extracted {len(significant_concepts)} significant concepts: {[c['name'] for c in significant_concepts]}"
        )

    except Exception as e:
        logger.error(f"Error extracting significant concepts: {e}")
        state["error"] = str(e)

    return state
