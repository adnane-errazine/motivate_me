
import { Message, ApplicationData } from "@/types/chat";
import { cn } from "@/lib/utils";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

interface ApplicationsResponseProps {
  message: Message;
  onApplicationClick?: (application: ApplicationData) => void;
}

const ApplicationsResponse = ({ message, onApplicationClick }: ApplicationsResponseProps) => {
  const applications = message.applicationsData || [];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-800 mb-2">Real-World Applications</h3>
        <p className="text-gray-600">{message.content}</p>
      </div>

      {/* Applications Carousel */}
      <div className="w-full max-w-5xl mx-auto">
        <Carousel className="w-full">
          <CarouselContent className="-ml-2 md:-ml-4">
            {applications.map((application, index) => (
              <CarouselItem key={index} className="pl-2 md:pl-4 md:basis-1/2">
                <div
                  className={cn(
                    "bg-white border-2 rounded-lg p-6 cursor-pointer transition-all duration-200 h-full",
                    "hover:border-blue-300 hover:shadow-lg hover:scale-[1.01]",
                    "border-gray-200"
                  )}
                  onClick={() => onApplicationClick?.(application)}
                >
                  {/* Application Header */}
                  <div className="mb-4">
                    <h4 className="text-lg font-semibold text-gray-800 mb-2">
                      {application.name}
                    </h4>
                    <p className="text-sm text-gray-500 mb-3">
                      {application.brief_description}
                    </p>
                    <p className="text-gray-700 leading-relaxed text-sm">
                      {application.description}
                    </p>
                  </div>

                  {/* Application Image */}
                  {application.images && application.images.length > 0 && (
                    <div className="mt-4">
                      <div className="relative group rounded-lg overflow-hidden bg-white">
                        <img
                          src={application.images[0].url}
                          alt={application.images[0].title}
                          className="w-full h-48 object-cover rounded-lg"
                        />
                      </div>
                      <div className="mt-2 px-1">
                        <p className="text-gray-600 text-xs text-center">
                          {application.images[0].title}
                        </p>
                      </div>
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
    </div>
  );
};

export default ApplicationsResponse;
