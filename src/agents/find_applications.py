import json
import logging
import base64
import asyncio
from src.config import config

from mistralai import Mistral

from src.data_models import WorkflowState

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

            for concept in state["significant_concepts"]:
                concept_name = concept["name"]
                domain = concept.get("domain", "")

                # Generate applications prompt
                applications_prompt = f"""
                    For the {domain} concept "{concept_name}", find 3-5 fascinating real-world applications that would excite and motivate learners.

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
                    1. Name: Clear, recognizable name (company/product if applicable)
                    2. Description: How the concept is used (2-3 sentences)
                    3. Impact: Why this application matters
                    4. Visual_keywords: 3-4 keywords for image search
                    5. Wow_factor: What makes this application impressive/surprising

                    Return as JSON array.
                    """
                # Prepare messages for Mistral chat
                messages = [
                    {"role": "system",
                     "content": "You are an expert at connecting abstract mathematical/scientific concepts to exciting real-world applications that inspire learning."},
                    {"role": "user", "content": applications_prompt}
                ]

                response = await self.mistral_client.chat.complete(
                    model=config.MISTRAL_MODEL,
                    messages=messages,
                    max_tokens=1200,
                    temperature=0.4
                )

                try:
                    applications = json.loads(response.choices[0].message.content)
                    if not isinstance(applications, list):
                        applications = [applications]
                except json.JSONDecodeError:
                    # Fallback parsing
                    import re
                    json_match = re.search(r'\[.*\]', response.choices[0].message.content, re.DOTALL)
                    if json_match:
                        applications = json.loads(json_match.group())
                    else:
                        logger.warning(f"Could not parse applications for {concept_name}")
                        applications = []

                concept_applications[concept_name] = applications
                logger.info(f"Found {len(applications)} applications for {concept_name}")

                # Small delay to respect rate limits
                await asyncio.sleep(0.1)

            state["concept_applications"] = concept_applications
            logger.info(f"Found applications for {len(concept_applications)} concepts")

        except Exception as e:
            logger.error(f"Error finding applications: {e}")
            state["error"] = str(e)

        return state

    async def run(self, state: WorkflowState) -> WorkflowState:
        """Run the agent to find applications for significant concepts"""
        logger.info("Running FindApplications agent")

        # Ensure we have significant concepts to work with
        if not state.get("significant_concepts"):
            logger.warning("No significant concepts found, skipping application search")
            return state

        # Run the application finding node
        state = await self.find_applications_node(state)

        # Encode images for each application
        if "concept_applications" in state:
            for concept, applications in state["concept_applications"].items():
                for app in applications:
                    if "image_path" in app:
                        app["image_data"] = encode_image(self, app["image_path"])

        return state


if __name__ == "__main__":
    # Example usage
    # RUN :
    # .\.venv\Scripts\activate.bat
    # python -m src.agents.find_applications

    state = WorkflowState(
        image_path="",
        text_input="",
        user_metadata={},
        significant_concepts=[
            {"name": "Fourier Transform", "domain": "Signal Processing"}
        ],
        concept_applications={},
        application_images={},
        combined_content=[],
        final_output={},
        error=None
    )

    agent = AgentApplicationsFinder()
    asyncio.run(agent.run(state))
    print(state)
