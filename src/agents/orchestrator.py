import asyncio
import base64
import json
import logging
from typing import Dict, List, Any, Optional, TypedDict
from pathlib import Path


from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


from src.config import config


from src.utils import _search_google_images
from src.agents.extract_concepts import extract_relevant_concepts

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowState(TypedDict):
    """State structure for the LangGraph workflow"""

    image_path: str
    text_input: str
    user_metadata: Dict[str, Any]
    significant_concepts: List[Dict[str, Any]]  # Major theorems/phenomena only
    concept_applications: Dict[str, List[Dict[str, Any]]]  # Real-world applications
    application_images: Dict[str, List[Dict[str, Any]]]  # Images for each application
    combined_content: List[Dict[str, Any]]  # Final rich content combining everything
    final_output: Dict[str, Any]
    error: Optional[str]


class Orchestrator:
    """Orchestrator class to manage the LangGraph workflow"""

    def __init__(self):
        self.client = MistralAsyncClient(api_key=config.MISTRAL_API_KEY)
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)

        workflow.add_note("extract_relevant_concepts", self._extract_relevant_concepts)
