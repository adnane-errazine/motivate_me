# -*- coding: utf-8 -*-
"""Agent to generate a personalized learning roadmap for understanding an application
agent_roadmap.py
"""

import json


from src.config import config

from mistralai import Mistral

from src.data_models import WorkflowState

import logging

logger = logging.getLogger(__name__)


class AgentRoadmap:
    def __init__(self):
        self.mistral_client = Mistral(api_key=config.MISTRAL_API_KEY)

    async def generate_roadmap(
        self, state: WorkflowState, str_application_name: str
    ) -> WorkflowState:
        """Generate a personalized learning roadmap based on the user's interests and goals"""
        try:
            logger.info("Generating personalized learning roadmap")

            # Prepare the prompt for generating the roadmap
            system_prompt = """
            You are an AI assistant tasked with generating a focused, three-phase learning roadmap to help a learner understand or build a specific real-world application.

            Your goal is to deconstruct the technical foundation of the target application (provided in the user message) and generate a progressive roadmap that equips a learner with the essential knowledge to comprehend and potentially implement it.

            Your output MUST be a single, valid JSON object. Do not include any explanations, markdown, or text before or after the JSON. The object must match this structure exactly:

            {
            "title": "string (a concise, relevant title for the roadmap, ideally referencing the application)",
            "description_1": [  // Phase 1: Foundational concepts
                ["string (concept/topic name)", "string (estimated time to learn, e.g., '5 hours')", "string (brief description of what the concept is and why it's useful)"],
                ...
            ],
            "description_2": [  // Phase 2: Intermediate concepts
                ["string (concept/topic name)", "string (estimated time to learn)", "string (brief description)"],
                ...
            ],
            "description_3": [  // Phase 3: Advanced or specialized concepts
                ["string (concept/topic name)", "string (estimated time to learn)", "string (brief description)"],
                ...
            ]
            }

            Instructions:

            - Each of the "description_X" fields must contain a list of 1–4 items.
            - Each item must be a list with exactly 3 strings: [concept name, estimated learning time, brief description].
            - Concepts must follow a logical progression:
            - **description_1**: Beginner-level foundations needed to explore the application.
            - **description_2**: Intermediate ideas that build on Phase 1 and relate directly to how the application works internally.
            - **description_3**: Advanced techniques or specialized knowledge needed for deeper understanding or real-world implementation.
            - If relevant concepts are provided, place them in the appropriate phase and describe them clearly.
            - Ensure all concepts are *directly relevant* to the target application — avoid unrelated or overly generic topics.
            - You may optionally tailor the content using the user's background, if provided — but the roadmap must still be driven by the application.
            """

            user_metadata = state.get("user_metadata", {})
            relevant_concepts = state.get("relevant_concepts", [])

            user_message_content = f"""
            You are an AI tutor generating a focused learning roadmap to help someone understand and potentially build the following application:

            **Target Application**: {str_application_name}

            Your objective is to break down this application into the core technical concepts and principles it relies on, and then organize those into a structured, three-phase learning roadmap:
            - **description_1**: Foundational knowledge (absolute basics needed to get started)
            - **description_2**: Intermediate concepts (used within the application or required to understand how it works internally)
            - **description_3**: Advanced or specialized topics (deeper mechanics, optimization, or real-world implementation challenges)

            Use this structure to ensure a natural progression in learning difficulty. Each concept must include:
            1. The concept name
            2. An estimated time to learn it (e.g., "10 hours", "3 days")
            3. A brief description of what the concept is and how it helps in understanding the application

            Also, incorporate the following **relevant technical concepts** associated with this application, placing them in the appropriate phase:
            {", ".join([c["name"] for c in relevant_concepts]) if relevant_concepts else "None specified"}

            Only include technical and scientific concepts that are essential to understanding how the application works — avoid general productivity tips, soft skills, or unrelated tangents.

            You may optionally tailor the content using the user's background, if available:

            - Interests: {user_metadata.get("interests", "Not specified")}
            - Career Goals: {user_metadata.get("career_goals", "Not specified")}
            - Education Level: {user_metadata.get("education_level", "Not specified")}
            - Background: {user_metadata.get("background", "Not specified")}
            - Hobbies: {user_metadata.get("hobbies", "Not specified")}

            **Final output must be a single JSON object** matching this structure:
            
            "title": "...",
            "description_1": [ [concept, time, brief_description], ... ],
            "description_2": [ [concept, time, brief_description], ... ],
            "description_3": [ [concept, time, brief_description], ... ]
            

            This roadmap should clearly show how a learner can go from beginner to capable of understanding and analyzing the core technologies behind **{str_application_name}**.
            """

            # Prepare messages for Mistral chat
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message_content},
            ]

            # Call Mistral API to generate the roadmap
            response = self.mistral_client.chat.complete(
                model=config.MISTRAL_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
            )

            # Parse the response to extract the roadmap
            try:
                raw_response = response.choices[0].message.content
                roadmap = json.loads(raw_response)
                if not isinstance(roadmap, dict):
                    raise ValueError("Response is not a valid JSON object")
            except json.JSONDecodeError:
                import re

                # Fallback parsing if JSON is not directly parsable
                json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
                if json_match:
                    roadmap = json.loads(json_match.group())
                else:
                    logger.error("Could not parse roadmap JSON")
                    raise ValueError("Response does not contain valid JSON")

            roadmap["application"] = str_application_name
            # Update the state with the generated roadmap
            state["roadmap"] = roadmap

            return state

        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            raise e


if __name__ == "__main__":
    import asyncio

    # Example usage
    state = WorkflowState(
        uuid="example-uuid",
        document_path="example/path/to/document",
        text_input="Example input text",
        user_metadata={},
        relevant_concepts=[
            {"name": "Fourier Transform", "domain": "Mathematics"},
            {"name": "Machine Learning", "domain": "Computer Science"},
        ],
        concept_applications={},
        error=None,
    )

    roadmap_agent = AgentRoadmap()
    asyncio.run(
        roadmap_agent.generate_roadmap(state, "Shazam, a music recognition application")
    )
    print(json.dumps(state, indent=2))
