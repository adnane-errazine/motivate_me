import asyncio
import json

from src.agents.find_applications import AgentApplicationsFinder
from src.data_models import WorkflowState


def main():
    print("Hello from motivate-me!")


if __name__ == "__main__":
    # Example usage
    # RUN :
    # .\.venv\Scripts\activate.bat
    # python app.py

    state = WorkflowState(
        document_path="",
        text_input="",
        user_metadata={},
        relevant_concepts=[
            {"name": "Fourier Transform", "domain": "Signal Processing"}
        ],
        concept_applications={},

        error=None
    )

    agent = AgentApplicationsFinder()
    asyncio.run(agent.run(state))
    print(json.dumps(state, indent=2))
