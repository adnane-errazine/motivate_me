import httpx
import logging
from typing import Dict, List, Any, Optional, TypedDict
from src.config import config

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



async def _search_google_images(query: str) -> List[Dict[str, Any]]:
    """Search for images using Google Custom Search API"""
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": config.GOOGLE_API_KEY,
            "cx": config.GOOGLE_CSE_ID,
            "q": query,
            "searchType": "image",
            "safe": config.IMAGE_SEARCH_SAFE,
            "num": config.MAX_IMAGE_RESULTS,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            images = []

            for item in data.get("items", []):
                images.append(
                    {
                        "url": item.get("link"),
                        "title": item.get("title"),
                        "thumbnail": item.get("image", {}).get("thumbnailLink"),
                        "context": item.get("snippet", ""),
                        "width": item.get("image", {}).get("width"),
                        "height": item.get("image", {}).get("height"),
                    }
                )

            return images

    except Exception as e:
        logger.error(f"Error searching images for '{query}': {e}")
        return []
