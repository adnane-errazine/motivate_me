




from src.config import config

from mistralai import Mistral

from src.data_models import WorkflowState

import logging

logger = logging.getLogger(__name__)


class AgentRoadmap:
    def __init__(self):
        self.mistral_client = Mistral(api_key=config.MISTRAL_API_KEY)
        
    async def generate_roadmap(self, state: WorkflowState) -> WorkflowState:
        """Generate a personalized learning roadmap based on the user's interests and goals"""
        try:
            logger.info("Generating personalized learning roadmap")
            
            
            # Prepare the prompt for generating the roadmap
            system_prompt = """
            """
            
            user_message = f""
            
            # Prepare messages for Mistral chat
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Call Mistral API to generate the roadmap
            response = self.mistral_client.chat.complete(
                model=config.MISTRAL_MODEL,
                messages=messages,
            )
            
            # Parse the response to extract the roadmap
            roadmap = response.choices[0].message.content.strip()
            
            # Update the state with the generated roadmap
            state["roadmap"] = roadmap
            
            return state
        
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            raise e
        
        