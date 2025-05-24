import httpx
import logging
from typing import Dict, List, Any
from src.config import config

logger = logging.getLogger(__name__)


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
