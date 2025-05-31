
import { Message } from "@/types/chat";

interface TextResponseProps {
  message: Message;
}

const TextResponse = ({ message }: TextResponseProps) => {
  return (
    <div className="whitespace-pre-wrap break-words">
      {message.content}
      {message.isStreaming && (
        <span className="inline-block w-2 h-5 bg-current ml-1 animate-pulse" />
      )}
    </div>
  );
};

export default TextResponse;
