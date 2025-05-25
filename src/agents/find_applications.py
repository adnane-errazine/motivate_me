# -*- coding: utf-8 -*-
"""Agent to extract applications for significant concepts.
find_applications.py
"""

import json
import logging
import base64
import asyncio
from src.config import config

from mistralai import Mistral

from src.data_models import WorkflowState, ApplicationData
from src.utils import search_google_images

logger = logging.getLogger(__name__)


def encode_image(image_path: str) -> str:
    """Encode image file to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


class AgentApplicationsFinder:
    """Agent to find fascinating real-world applications for significant concepts"""

    def __init__(self):
        self.mistral_client = Mistral(api_key=config.MISTRAL_API_KEY)

    async def find_applications_node(self, state: WorkflowState) -> WorkflowState:
        """Find fascinating real-world applications for each significant concept"""
        try:
            logger.info("Finding real-world applications for concepts")

            concept_applications = {}

            for concept in state["relevant_concepts"]:
                concept_name = concept["name"]
                domain = concept.get("domain", "")

                # Generate applications prompt
                applications_prompt = f"""
                    For the {domain} concept "{concept_name}", find 1-2 fascinating real-world applications that would excite and motivate learners, especially young learners.

                    Focus on:
                    - Modern technology applications (apps, devices, systems)
                    - Surprising everyday applications
                    - Cutting-edge research or industry uses
                    - Applications that show the power and relevance of this concept

                    Examples of the kind of applications I want:
                    - Fourier Transform → Shazam music recognition, JPEG compression, MRI imaging, noise cancellation
                    - Machine Learning → Netflix recommendations, autonomous cars, medical diagnosis
                    - Graph Theory → GPS navigation, social networks, supply chain optimization

                    For each application, provide:
                    1. name: Clear, recognizable name (company/product if applicable)
                    2. brief_description: 1 sentence summary of what it does (e.g. "Shazam identifies songs from short audio clips") will be used to query Google Images
                    3. description: Extended description of how this application uses the concept, its significance, wow factor and any interesting details, wow 
                    
                    Return as JSON array.
                    """
                # Prepare messages for Mistral chat
                messages = [
                    {
                        "role": "system",
                        "content": "You are an expert at connecting abstract mathematical/scientific/linguistic concepts to exciting real-world applications that inspire learning.",
                    },
                    {"role": "user", "content": applications_prompt},
                ]

                response = self.mistral_client.chat.complete(
                    model=config.MISTRAL_MODEL,
                    messages=messages,
                    # max_tokens=2000,
                    response_format={"type": "json_object"},
                    # temperature=0.4
                )
                # Parse the response
                try:
                    raw_response = response.choices[0].message.content
                    applications = json.loads(raw_response)
                    if not isinstance(applications, list):
                        applications = [applications]
                    for application in applications:
                        application["images"] = await search_google_images(concept_name)
                except json.JSONDecodeError:
                    # Fallback parsing
                    import re

                    json_match = re.search(
                        r"\[.*\]", response.choices[0].message.content, re.DOTALL
                    )
                    if json_match:
                        applications = json.loads(json_match.group())
                    else:
                        logger.warning(
                            f"Could not parse applications for {concept_name}"
                        )
                        applications = []

                concept_applications[concept_name] = applications
                logger.info(
                    f"Found {len(applications)} applications for {concept_name}"
                )

                # Small delay to respect rate limits
                await asyncio.sleep(0.05)

            state["concept_applications"] = concept_applications

            logger.info(f"Found applications for {len(concept_applications)} concepts")

        except Exception as e:
            logger.error(f"Error finding applications: {e}")
            state["error"] = str(e)

        return state


if __name__ == "__main__":
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

    finder = AgentApplicationsFinder()
    asyncio.run(finder.find_applications_node(state))
    print(json.dumps(state, indent=2))
