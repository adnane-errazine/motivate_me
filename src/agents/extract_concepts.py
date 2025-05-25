# -*- coding: utf-8 -*-
"""Agent to extract significant  concepts from lecture material.
extract_concepts.py
"""

import json
import logging
import base64
import os
from pdf2image import convert_from_path
from src.config import config

from mistralai import Mistral

from src.data_models import WorkflowState

logger = logging.getLogger(__name__)


class AgentConceptsExtractor:
    """Agent to extract significant mathematical/scientific concepts from lecture material"""

    def __init__(self):
        self.mistral_client = Mistral(api_key=config.MISTRAL_API_KEY)

    async def extract_relevant_concepts_node(
        self, state: WorkflowState
    ) -> WorkflowState:
        """Extract only significant mathematical/scientific concepts, filtering out basic elements"""
        try:
            logger.info("Extracting relevant concepts")

            # Prepare the prompt - focus on major concepts only
            system_prompt = """You are an expert at identifying significant mathematical, scientific, and engineering concepts from academic material. 

            IMPORTANT: Extract concepts, theorems, phenomena, and advanced mathematical/scientific principles. 
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
            1. name: The official name of the theorem/concept/phenomenon
            2. type: (theorem, principle, method, phenomenon, etc.)
            3. domain: (mathematics, physics, engineering, computer science, etc.)
            4. significance: Why this concept is important and powerful
            5. confidence: Your confidence this is correctly identified (0.0-1.0)

            Return a JSON array with only the most significant 2-4 concepts. Quality over quantity."""

            # Create a directory for the current workflow
            output_dir = create_uuid_directory(state["uuid"])

            # if  state["document_path"].endswith(".pdf"):
            # Convert the PDF to images and save them in the output directory
            # image_files = convert_pdf_to_images(state["document_path"], output_dir)
            #    pass
            if (
                state["document_path"].endswith(".jpg")
                or state["document_path"].endswith(".jpeg")
                or state["document_path"].endswith(".png")
            ):
                # If it's an image, we can directly use it
                image_files = [state["document_path"]]

            # Prepare user message
            user_content = f"""Analyze this lecture material for significant mathematical/scientific concepts.

            Additional context: {state["text_input"]}
            User background: {json.dumps(state["user_metadata"])}

            Focus on identifying theorems, principles, or phenomena that have real-world applications."""

            # Initialize messages with the system prompt
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_content}],
                },
            ]

            if state["document_path"].endswith(".pdf"):
                uploaded_pdf = self.mistral_client.files.upload(
                    file={
                        "file_name": state["document_path"],
                        "content": open(state["document_path"], "rb"),
                    },
                    purpose="ocr",
                )
                signed_url = self.mistral_client.files.get_signed_url(
                    file_id=uploaded_pdf.id
                )
                messages[1]["content"].append(
                    {
                        "type": "document_url",
                        "document_url": signed_url.url,
                    }
                )

            if (
                state["document_path"].endswith(".jpg")
                or state["document_path"].endswith(".jpeg")
                or state["document_path"].endswith(".png")
            ):
                # Encode and append each image
                for counter, image_path in enumerate(image_files):
                    image_base64 = encode_image(image_path)
                    messages[1]["content"].append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        }
                    )
                    if counter >= 6:
                        logger.info("Limiting to 6 images for performance")
                        break

            response = self.mistral_client.chat.complete(
                model=config.MISTRAL_MODEL_VISION,
                messages=messages,
                response_format={"type": "json_object"},
                # max_tokens=1500,
                # temperature=0.2,
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
            relevant_concepts = [
                c
                for c in concepts
                if c.get("confidence", 0) >= 0.7  # Higher threshold for significance
            ][:10]  # Max 4 significant concepts

            state["relevant_concepts"] = relevant_concepts
            logger.info(
                f"Extracted {len(relevant_concepts)} significant concepts: {[c['name'] for c in relevant_concepts]}"
            )

        except Exception as e:
            logger.error(f"Error extracting significant concepts: {e}")
            state["error"] = str(e)

        return state


def encode_image(image_path: str) -> str:
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def create_uuid_directory(uuid: str) -> str:
    """
    Create a directory named after the UUID inside the 'tmp' folder.
    Returns the path to the created directory.
    """
    directory_path = os.path.join("tmp", uuid)
    os.makedirs(directory_path, exist_ok=True)
    return directory_path


def convert_pdf_to_images(pdf_path: str, output_folder: str) -> list:
    """
    Convert each page of the PDF to an image and save them in the output folder.
    Returns a list of image file paths.
    """
    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []
    for i, image in enumerate(images):
        image_filename = f"page_{i + 1}.jpg"
        image_path = os.path.join(output_folder, image_filename)
        image.save(image_path, "JPEG")
        image_paths.append(image_path)
    return image_paths


if __name__ == "__main__":
    import asyncio

    # RUN :
    # .\.venv\Scripts\activate.bat
    # python -m src.agents.extract_concepts
    # Example usage
    state = WorkflowState(
        uuid="test-uuid-1234",
        document_path="tmp/lecture8-fouriertransforms.pdf",
        text_input="This lecture covers advanced topics in signal processing.",
        user_metadata={"background": "First year engineering student"},
        relevant_concepts=[],
        concept_applications={},
        error=None,
    )

    agent = AgentConceptsExtractor()
    result_state = asyncio.run(agent.extract_relevant_concepts_node(state))
    print(json.dumps(result_state, indent=2))
