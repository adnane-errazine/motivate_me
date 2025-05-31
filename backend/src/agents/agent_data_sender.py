import json
import logging
import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from src.data_models import WorkflowState

logger = logging.getLogger(__name__)


class AgentDataSender:
    """Agent to send/stream processed data to the frontend"""

    def __init__(self, websocket_handler: Optional[Callable] = None,
                 api_callback: Optional[Callable] = None):
        """
        Initialize the data sender agent

        Args:
            websocket_handler: Optional WebSocket handler for real-time streaming
            api_callback: Optional callback function for API-based communication
        """
        self.websocket_handler = websocket_handler
        self.api_callback = api_callback

    async def send_data_to_frontend_node(self, state: WorkflowState) -> WorkflowState:
        """
        Send processed data to frontend via WebSocket or API callback

        Args:
            state: Current workflow state containing processed data

        Returns:
            Updated workflow state
        """
        try:
            logger.info("Sending data to frontend")

            # Prepare the data payload
            frontend_data = self._prepare_frontend_data(state)

            # Send via WebSocket if available
            if self.websocket_handler:
                await self._send_via_websocket(frontend_data)

            # Send via API callback if available
            if self.api_callback:
                await self._send_via_callback(frontend_data)

            # If no handlers are available, log the data
            if not self.websocket_handler and not self.api_callback:
                logger.info("No frontend handlers configured, logging data")
                logger.info(f"Frontend data: {json.dumps(frontend_data, indent=2)}")

            # Update state to indicate successful transmission
            # state["frontend_status"] = "sent"
            # state["frontend_timestamp"] = datetime.now().isoformat()

            logger.info("Successfully sent data to frontend")

        except Exception as e:
            logger.error(f"Error sending data to frontend: {e}")
            state["error"] = str(e)
            # state["frontend_status"] = "failed"

        return state

    def _prepare_frontend_data(self, state: WorkflowState) -> Dict[str, Any]:
        """
        Prepare and structure data for frontend consumption matching the chat interface schema

        Args:
            state: Current workflow state

        Returns:
            Structured data dictionary for frontend in chat message format
        """
        # Add error information if present
        if state.get("error"):
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": state["error"],
                "message": {
                    "id": str(int(datetime.now().timestamp() * 1000)),
                    "content": f"Sorry, there was an error processing your request: {state['error']}",
                    "role": "assistant",
                    "timestamp": datetime.now().isoformat(),
                    "responseType": "text"
                }
            }

        # Build roadmap data from concepts and applications
        roadmap_data = []
        concept_count = 0

        if state.get("relevant_concepts") and state.get("concept_applications"):
            # Create roadmap items from concepts
            for i, concept in enumerate(state["relevant_concepts"]):
                concept_name = concept.get("name", "")
                concept_applications = state["concept_applications"].get(concept_name, [])

                # Determine level based on prerequisites or importance
                importance = concept.get("importance", 0)
                level = 1 if importance > 0.8 else (2 if importance > 0.5 else 3)

                # Create roadmap item
                roadmap_item = {
                    "id": str(i + 1),
                    "title": concept_name,
                    "description": concept.get("description", f"Master {concept_name} and its applications"),
                    "level": level,
                    "prerequisites": [str(j + 1) for j, prereq_concept in enumerate(state["relevant_concepts"])
                                      if prereq_concept.get("name") in concept.get("prerequisites", []) and j < i],
                    "estimatedTime": self._estimate_learning_time(concept.get("difficulty_level", "medium")),
                    "applications": concept_applications[:3] if concept_applications else [],
                    # Limit to top 3 applications
                    "domain": concept.get("domain", "")
                }

                roadmap_data.append(roadmap_item)
                concept_count += 1

        # Prepare the chat message response
        content_parts = []
        if concept_count > 0:
            content_parts.append(f"I found {concept_count} key concepts for your learning journey.")
            content_parts.append("Here's your personalized learning roadmap:")
        else:
            content_parts.append("I've prepared a learning roadmap based on your query.")

        # Collect images from applications
        response_images = []
        image_captions = []

        for concept_name, applications in state.get("concept_applications", {}).items():
            for app in applications[:2]:  # Limit to 2 applications per concept
                if app.get("images"):
                    for img_url in app["images"][:2]:  # Limit to 2 images per application
                        response_images.append(img_url)
                        image_captions.append(f"{app.get('name', concept_name)}: {app.get('description', '')[:100]}...")

        # Prepare final message data
        message_data = {
            "id": str(int(datetime.now().timestamp() * 1000)),
            "content": "\n\n".join(content_parts),
            "role": "assistant",
            "timestamp": datetime.now().isoformat(),
            "responseType": "roadmap" if roadmap_data else "text_with_images" if response_images else "text",
            "roadmapData": roadmap_data if roadmap_data else None,
            "images": response_images if response_images else None,
            "imageCaptions": image_captions if image_captions else None
        }

        # Remove None values
        message_data = {k: v for k, v in message_data.items() if v is not None}

        frontend_data = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "message": message_data,
            "metadata": {
                "total_concepts": len(state.get("relevant_concepts", [])),
                "total_applications": sum(
                    len(apps) for apps in state.get("concept_applications", {}).values()
                ),
                "processing_complete": True
            }
        }

        return frontend_data

    def _estimate_learning_time(self, difficulty_level: str) -> str:
        """
        Estimate learning time based on difficulty level

        Args:
            difficulty_level: The difficulty level of the concept

        Returns:
            Estimated time string
        """
        time_estimates = {
            "beginner": "1-2 weeks",
            "easy": "1-2 weeks",
            "medium": "2-4 weeks",
            "intermediate": "2-4 weeks",
            "hard": "1-2 months",
            "advanced": "1-2 months",
            "expert": "2-3 months"
        }

        return time_estimates.get(difficulty_level.lower(), "2-4 weeks")

    async def _send_via_websocket(self, data: Dict[str, Any]) -> None:
        """
        Send data via WebSocket connection

        Args:
            data: Data to send to frontend
        """
        try:
            if self.websocket_handler:
                # Send as JSON string
                json_data = json.dumps(data)
                await self.websocket_handler(json_data)
                logger.info("Data sent via WebSocket")
        except Exception as e:
            logger.error(f"Error sending via WebSocket: {e}")
            raise

    async def _send_via_callback(self, data: Dict[str, Any]) -> None:
        """
        Send data via API callback function

        Args:
            data: Data to send to frontend
        """
        try:
            if self.api_callback:
                if asyncio.iscoroutinefunction(self.api_callback):
                    await self.api_callback(data)
                else:
                    self.api_callback(data)
                logger.info("Data sent via API callback")
        except Exception as e:
            logger.error(f"Error sending via API callback: {e}")
            raise

    async def stream_progress_update(self, stage: str, progress: Dict[str, Any]) -> None:
        """
        Stream progress updates to frontend during processing

        Args:
            stage: Current processing stage
            progress: Progress information
        """
        try:
            progress_data = {
                "type": "progress_update",
                "stage": stage,
                "timestamp": datetime.now().isoformat(),
                "progress": progress
            }

            # Send progress via WebSocket if available
            if self.websocket_handler:
                await self._send_via_websocket(progress_data)

            logger.info(f"Progress update sent: {stage}")

        except Exception as e:
            logger.error(f"Error sending progress update: {e}")


# Usage example for integration with the orchestrator
async def create_data_sender_with_websocket(websocket):
    """
    Factory function to create data sender with WebSocket handler

    Args:
        websocket: WebSocket connection object

    Returns:
        Configured AgentDataSender instance
    """

    async def websocket_handler(data):
        await websocket.send_text(data)

    return AgentDataSender(websocket_handler=websocket_handler)


def create_data_sender_with_callback(callback_func):
    """
    Factory function to create data sender with API callback

    Args:
        callback_func: Callback function to handle data

    Returns:
        Configured AgentDataSender instance
    """
    return AgentDataSender(api_callback=callback_func)


# Example integration function for the orchestrator
def integrate_with_orchestrator(orchestrator_instance, frontend_handler=None):
    """
    Integrate the data sender with the existing orchestrator

    Args:
        orchestrator_instance: Instance of the Orchestrator class
        frontend_handler: WebSocket or callback handler for frontend communication
    """
    # Create data sender agent
    data_sender = AgentDataSender(websocket_handler=frontend_handler)

    # Add to orchestrator's workflow
    orchestrator_instance.workflow.add_node(
        "send_data_to_frontend",
        data_sender.send_data_to_frontend_node
    )

    return data_sender