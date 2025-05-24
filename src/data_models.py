from typing import Dict, List, Any, Optional, TypedDict

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