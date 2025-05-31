
import { Message } from "@/types/chat";
import TextResponse from "./responses/TextResponse";
import TextWithImagesResponse from "./responses/TextWithImagesResponse";
import RoadmapResponse from "./responses/RoadmapResponse";
import ConceptsResponse from "./responses/ConceptsResponse";
import ApplicationsResponse from "./responses/ApplicationsResponse";

interface ResponseRendererProps {
  message: Message;
  onImageClick?: (imageUrl: string, context: string) => void;
  onRoadmapItemClick?: (nodeId: string, title: string) => void;
  onConceptClick?: (concept: any) => void;
  onApplicationClick?: (application: any) => void;
}

const ResponseRenderer = ({ 
  message, 
  onImageClick, 
  onRoadmapItemClick,
  onConceptClick,
  onApplicationClick 
}: ResponseRendererProps) => {
  switch (message.responseType) {
    case "text_with_images":
      return (
        <TextWithImagesResponse 
          message={message} 
          onImageClick={onImageClick}
        />
      );
    case "roadmap":
      return (
        <RoadmapResponse 
          message={message} 
          onRoadmapItemClick={onRoadmapItemClick}
        />
      );
    case "concepts":
      return (
        <ConceptsResponse 
          message={message} 
          onConceptClick={onConceptClick}
        />
      );
    case "applications":
      return (
        <ApplicationsResponse 
          message={message} 
          onApplicationClick={onApplicationClick}
        />
      );
    default:
      return <TextResponse message={message} />;
  }
};

export default ResponseRenderer;
