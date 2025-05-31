import {Message} from "@/types/chat";
import {cn} from "@/lib/utils";
import ResponseRenderer from "./ResponseRenderer";
import LoadingIndicator from "./LoadingIndicator";
import {FileText} from "lucide-react";

interface MessageBubbleProps {
    message: Message;
    isLast: boolean;
    onImageClick?: (imageUrl: string, context: string) => void;
    onRoadmapItemClick?: (nodeId: string, title: string) => void;
    onConceptClick?: (concept: any) => void;
    onApplicationClick?: (application: any) => void;
}

const MessageBubble = ({
                           message,
                           isLast,
                           onImageClick,
                           onRoadmapItemClick,
                           onConceptClick,
                           onApplicationClick
                       }: MessageBubbleProps) => {
    const isUser = message.role === "user";

    return (
        <div
            className={cn(
                "flex w-full animate-fade-in",
                isUser ? "justify-end" : "justify-start"
            )}
        >
            <div
                className={cn(
                    "max-w-[85%] rounded-2xl px-4 py-3 shadow-sm",
                    isUser
                        ? "bg-blue-400 text-white"
                        : "bg-white border border-gray-200 text-gray-800",
                    (message.responseType === "roadmap" || message.responseType === "concepts" || message.responseType === "applications") && "max-w-[95%]"
                )}
            >
                {/* User messages show images differently */}
                {isUser && message.images && message.images.length > 0 && (
                    <div className="mb-3 space-y-2">
                        {message.images.map((image, index) => {
                            const isBlob = image.startsWith("blob:");
                            return isBlob ? (
                                <div
                                    key={index}
                                    className="relative group bg-white rounded-lg p-2 shadow-sm border border-gray-200 flex items-center space-x-2"
                                >
                                    <FileText className="w-8 h-8 text-red-500"/>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-xs font-medium text-gray-900 truncate">PDF Document</p>
                                        <p className="text-xs text-gray-500">Preview unavailable</p>
                                    </div>
                                </div>
                            ) : (
                                <img
                                    key={index}
                                    src={image}
                                    alt={`Uploaded image ${index + 1}`}
                                    className="max-w-full h-auto rounded-lg"
                                    style={{backgroundColor: 'white', padding: '16px', maxWidth: '80%'}}
                                />
                            );
                        })}

                    </div>
                )}

                {/* Content */}
                {isUser ? (
                    <div className="whitespace-pre-wrap break-words">
                        {message.content}
                    </div>
                ) : message.isLoading ? (
                    <LoadingIndicator/>
                ) : (
                    <ResponseRenderer
                        message={message}
                        onImageClick={onImageClick}
                        onRoadmapItemClick={onRoadmapItemClick}
                        onConceptClick={onConceptClick}
                        onApplicationClick={onApplicationClick}
                    />
                )}

                {/* Timestamp */}
                <div
                    className={cn(
                        "text-xs mt-2 opacity-70",
                        isUser ? "text-blue-100" : "text-gray-500"
                    )}
                >
                    {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                    })}
                </div>
            </div>
        </div>
    );
};

export default MessageBubble;
