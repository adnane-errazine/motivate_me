
import { Message } from "@/types/chat";
import { cn } from "@/lib/utils";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

interface TextWithImagesResponseProps {
  message: Message;
  onImageClick?: (imageUrl: string, context: string) => void;
}

const TextWithImagesResponse = ({ message, onImageClick }: TextWithImagesResponseProps) => {
  return (
    <div className="space-y-4">
      {/* Text Content */}
      <div className="whitespace-pre-wrap break-words">
        {message.content}
        {message.isStreaming && (
          <span className="inline-block w-2 h-5 bg-current ml-1 animate-pulse" />
        )}
      </div>

      {/* Carousel for Images */}
      {message.images && message.images.length > 0 && (
        <div className="mt-6">
          <Carousel className="w-full max-w-xl mx-auto">
            <CarouselContent>
              {message.images.map((image, index) => (
                <CarouselItem key={index}>
                  <div className="p-1">
                    <div
                      className={cn(
                        "relative group cursor-pointer rounded-lg overflow-hidden",
                        "border-2 border-transparent hover:border-blue-300",
                        "transition-all duration-200 hover:scale-[1.02] hover:shadow-lg",
                        "bg-white"
                      )}
                      onClick={() => onImageClick?.(image, message.content)}
                    >
                      <img
                        src={image}
                        alt={`Response image ${index + 1}`}
                        className="w-full h-64 object-cover rounded-lg"
                      />
                      
                      {/* Hover overlay */}
                      <div className="absolute inset-0 bg-blue-400/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg" />
                      
                      {/* Click indicator */}
                      <div className="absolute top-2 right-2 bg-blue-400 text-white text-xs px-2 py-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        Click to explore
                      </div>
                    </div>

                    {/* Caption below the image */}
                    {message.imageCaptions && message.imageCaptions[index] && (
                      <div className="mt-3 px-2">
                        <p className="text-gray-600 text-sm font-medium text-center">
                          {message.imageCaptions[index]}
                        </p>
                      </div>
                    )}
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      )}
    </div>
  );
};

export default TextWithImagesResponse;
