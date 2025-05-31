
import { Message } from "@/types/chat";
import MessageBubble from "./MessageBubble";
import LoadingIndicator from "./LoadingIndicator";

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  onImageClick?: (imageUrl: string, context: string) => void;
  onRoadmapItemClick?: (nodeId: string, title: string) => void;
  onConceptClick?: (concept: any) => void;
  onApplicationClick?: (application: any) => void;
}

const MessageList = ({ 
  messages, 
  isLoading, 
  onImageClick, 
  onRoadmapItemClick,
  onConceptClick,
  onApplicationClick 
}: MessageListProps) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6">
      {messages.map((message, index) => (
        <MessageBubble
          key={message.id}
          message={message}
          isLast={index === messages.length - 1}
          onImageClick={onImageClick}
          onRoadmapItemClick={onRoadmapItemClick}
          onConceptClick={onConceptClick}
          onApplicationClick={onApplicationClick}
        />
      ))}
      {isLoading && <LoadingIndicator />}
    </div>
  );
};

export default MessageList;
