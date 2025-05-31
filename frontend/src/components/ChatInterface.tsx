import { useState, useRef, useEffect } from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { Message, ConceptData, ApplicationData } from "@/types/chat";
import { APIService } from "@/services/apiService";

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const apiService = APIService.getInstance();

  // Check if we have any assistant messages to determine layout
  const hasAssistantMessages = messages.some(msg => msg.role === "assistant");

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages.length]);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      apiService.stopPolling();
    };
  }, []);

  const handleConceptClick = (concept: ConceptData) => {
    console.log("Concept clicked:", concept);

    const detailMessage: Message = {
      id: Date.now().toString(),
      content: `Let me explain more about "${concept.name}" in the ${concept.domain} domain...`,
      role: "assistant",
      timestamp: new Date(),
      responseType: "text",
    };

    setMessages(prev => [...prev, detailMessage]);
  };

  const handleApplicationClick = (application: ApplicationData) => {
    console.log("Application clicked:", application);

    // Convert backend roadmap format to frontend format
    const roadmapData = application.RoadmapData?.map((roadmap, index) => {
      const allDescriptions = [
        ...(roadmap.description_1 || []),
        ...(roadmap.description_2 || []),
        ...(roadmap.description_3 || [])
      ];

      return allDescriptions.map((desc, descIndex) => ({
        id: `${index}-${descIndex}`,
        title: Array.isArray(desc) ? desc[0] || "Learning Step" : "Learning Step",
        description: Array.isArray(desc) ? desc[2] || desc[1] || "Description not available" : "Description not available",
        level: descIndex < (roadmap.description_1?.length || 0) ? 1 : 
               descIndex < ((roadmap.description_1?.length || 0) + (roadmap.description_2?.length || 0)) ? 2 : 3,
        prerequisites: [],
        estimatedTime: Array.isArray(desc) ? desc[1] || "Varies" : "Varies"
      }));
    }).flat() || [];

    const roadmapMessage: Message = {
      id: Date.now().toString(),
      content: `Here's the learning roadmap for ${application.name}:`,
      role: "assistant",
      timestamp: new Date(),
      responseType: "roadmap",
      roadmapData: roadmapData
    };

    setMessages(prev => [...prev, roadmapMessage]);
  };

  const handleImageClick = (imageUrl: string, context: string) => {
    console.log("Image clicked:", imageUrl, "Context:", context);

    // Generate a roadmap based on the context
    const roadmapResponse = generateRoadmapResponse("implementing Photoshop filters");

    const roadmapMessage: Message = {
      id: Date.now().toString(),
      content: roadmapResponse.content,
      role: "assistant",
      timestamp: new Date(),
      responseType: roadmapResponse.responseType,
      roadmapData: roadmapResponse.roadmapData,
    };

    setMessages(prev => [...prev, roadmapMessage]);
  };

  const handleRoadmapItemClick = (nodeId: string, title: string) => {
    console.log("Roadmap item clicked:", nodeId, title);

    // Generate detailed response about the roadmap item
    const detailMessage: Message = {
      id: Date.now().toString(),
      content: `Let me explain more about "${title}"...\n\nThis is a crucial step in your learning journey. Here are the key concepts you need to master and resources to get started.`,
      role: "assistant",
      timestamp: new Date(),
      responseType: "text",
    };

    setMessages(prev => [...prev, detailMessage]);
  };

  const generateRoadmapResponse = (topic: string) => {
    // Mock roadmap data - in real app this would come from API
    const roadmapData = [
      {
        id: "1",
        title: "Mathematics Fundamentals",
        description: "Linear algebra, calculus, and signal processing basics",
        level: 1,
        prerequisites: [],
        estimatedTime: "2-3 months"
      },
      {
        id: "2",
        title: "Digital Image Processing",
        description: "Understanding pixels, color spaces, and basic transformations",
        level: 1,
        prerequisites: [],
        estimatedTime: "1-2 months"
      },
      {
        id: "3",
        title: "Fourier Transform Theory",
        description: "Understanding frequency domain analysis and applications",
        level: 2,
        prerequisites: ["1"],
        estimatedTime: "2-4 weeks"
      },
      {
        id: "4",
        title: "Filter Design",
        description: "Creating and implementing digital filters for image processing",
        level: 2,
        prerequisites: ["1", "2"],
        estimatedTime: "3-4 weeks"
      },
      {
        id: "5",
        title: "Advanced Image Effects",
        description: "Implementing complex filters and effects like those in Photoshop",
        level: 3,
        prerequisites: ["3", "4"],
        estimatedTime: "2-3 months"
      }
    ];

    return {
      content: `Here's your learning roadmap for ${topic}:`,
      responseType: "roadmap" as const,
      roadmapData
    };
  };

  const handleSendMessage = async (content: string, images?: File[]) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: "user",
      timestamp: new Date(),
      images: images?.map(file => URL.createObjectURL(file)),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Stop any existing polling
      apiService.stopPolling();

      // Submit query to API (don't wait for completion)
      await apiService.submitQuery(content, images?.[0]);

      // Create loading message only for applications since concepts aren't in the API response
      const applicationsMessage: Message = {
        id: `${Date.now()}-applications`,
        content: "Finding real-world applications...",
        role: "assistant",
        timestamp: new Date(),
        responseType: "applications",
        isLoading: true,
      };

      setMessages(prev => [...prev, applicationsMessage]);

      // Start polling for updates immediately
      apiService.startPolling(
        (concepts, timestamp) => {
          console.log("Concepts updated:", concepts, timestamp);
          // Since concepts aren't in your API response, we could add a concepts message here if needed
        },
        (applications, timestamp) => {
          console.log("Applications updated:", applications, timestamp);
          const allApplications = Object.values(applications).flat();
          setMessages(prev => prev.map(msg =>
            msg.id === applicationsMessage.id
              ? {
                  ...msg,
                  isLoading: allApplications.length === 0,
                  applicationsData: allApplications,
                  content: allApplications.length > 0 ? "Here are real-world applications:" : "Finding real-world applications..."
                }
              : msg
          ));
        }
      );

      setIsLoading(false);
    } catch (error) {
      console.error("Error sending message:", error);
      setIsLoading(false);

      // Show error message
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: "Sorry, there was an error processing your request. Please try again.",
        role: "assistant",
        timestamp: new Date(),
        responseType: "text",
      };

      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const simulateStreamingResponse = (messageId: string, fullText: string) => {
    let currentText = "";
    let currentIndex = 0;

    const streamInterval = setInterval(() => {
      if (currentIndex < fullText.length) {
        currentText += fullText[currentIndex];
        currentIndex++;

        setMessages(prev =>
          prev.map(msg =>
            msg.id === messageId
              ? { ...msg, content: currentText }
              : msg
          )
        );
      } else {
        setMessages(prev =>
          prev.map(msg =>
            msg.id === messageId
              ? { ...msg, isStreaming: false }
              : msg
          )
        );
        clearInterval(streamInterval);
      }
    }, 5);
  };

  if (!hasAssistantMessages) {
    // Initial centered layout
    return (
      <div className="flex flex-col h-screen max-w-[80%] mx-auto">
        {/* Centered content */}
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="w-full max-w-2xl space-y-6">
            <div className="text-center space-y-4">
              <h2 className="text-3xl font-bold text-gray-800" style={{textShadow: '1px 1px 2px #ffffff '}}>
                motivaty
              </h2>
              <p className="text-lg text-gray-600">
                What do you need help with?
              </p>
            </div>

            {/* Centered Input */}
            <div className="transition-all duration-700 ease-in-out">
              <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Standard chat layout after first response
  return (
    <div className="flex flex-col h-screen max-w-[80%] mx-auto">
      {/* Messages Container */}
      <div className="flex-1 overflow-scroll">
        <MessageList
          messages={messages}
          isLoading={isLoading}
          onImageClick={handleImageClick}
          onRoadmapItemClick={handleRoadmapItemClick}
          onConceptClick={handleConceptClick}
          onApplicationClick={handleApplicationClick}
        />
        <div ref={messagesEndRef} />
      </div>

      {/* Input - animates into position */}
      <div className="backdrop-blur-sm p-4 transition-all duration-700 ease-in-out animate-fade-in">
        <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;
