import logging
from typing import Dict, List, Any

import httpx

from src.config import config

logger = logging.getLogger(__name__)


async def search_google_images(query: str) -> List[Dict[str, Any]]:
    """Search for images using Google Custom Search API"""
    # TODO: Change this before demo
    # TODO: This is only for development purposes
    return [{
        "url": "https://mriquestions.com/uploads/3/4/5/7/34572113/9600204_orig.gif",
        "title": "Fourier Transform (FT) - Questions and Answers in MRI",
        "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx4ju1Vn2qlWb3xLNM4mbDrG2TIhMR0CfS_AF-suLC6NCg0acuqn3NVg&s",
        "context": "Fourier Transform (FT) - Questions and Answers in MRI",
        "width": 708,
        "height": 570
    }]

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
