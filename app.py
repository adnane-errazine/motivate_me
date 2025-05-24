import asyncio

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
        image_path="",
        text_input="",
        user_metadata={},
        significant_concepts=[
            {"name": "Fourier Transform", "domain": "Signal Processing"}
        ],
        concept_applications={},

        error=None
    )

    agent = AgentApplicationsFinder()
    asyncio.run(agent.run(state))
    print(state)
