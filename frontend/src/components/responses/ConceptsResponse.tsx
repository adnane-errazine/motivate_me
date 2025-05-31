
import { Message, ConceptData } from "@/types/chat";
import { cn } from "@/lib/utils";

interface ConceptsResponseProps {
  message: Message;
  onConceptClick?: (concept: ConceptData) => void;
}

const ConceptsResponse = ({ message, onConceptClick }: ConceptsResponseProps) => {
  const concepts = message.conceptsData || [];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-800 mb-2">Key Concepts</h3>
        <p className="text-gray-600">{message.content}</p>
      </div>

      {/* Concepts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {concepts.map((concept, index) => (
          <div
            key={index}
            className={cn(
              "bg-white border-2 rounded-lg p-4 cursor-pointer transition-all duration-200",
              "hover:border-blue-300 hover:shadow-lg hover:scale-[1.02]",
              "border-gray-200"
            )}
            onClick={() => onConceptClick?.(concept)}
          >
            {/* Concept Header */}
            <div className="flex items-start justify-between mb-3">
              <div>
                <h4 className="font-semibold text-gray-800">{concept.name}</h4>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                    {concept.type}
                  </span>
                  <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                    {concept.domain}
                  </span>
                </div>
              </div>
              <div className="bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                {Math.round(concept.confidence * 100)}%
              </div>
            </div>

            {/* Significance */}
            <p className="text-sm text-gray-600 line-clamp-3">
              {concept.significance}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConceptsResponse;
