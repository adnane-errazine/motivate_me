
import { Message, RoadmapNode } from "@/types/chat";
import { cn } from "@/lib/utils";

interface RoadmapResponseProps {
  message: Message;
  onRoadmapItemClick?: (nodeId: string, title: string) => void;
}

const RoadmapResponse = ({ message, onRoadmapItemClick }: RoadmapResponseProps) => {
  const roadmapData = message.roadmapData || [];

  // Group nodes by level for better visualization
  const nodesByLevel = roadmapData.reduce((acc, node) => {
    if (!acc[node.level]) acc[node.level] = [];
    acc[node.level].push(node);
    return acc;
  }, {} as Record<number, RoadmapNode[]>);

  const levels = Object.keys(nodesByLevel).map(Number).sort((a, b) => a - b);

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="text-center">
        <h3 className="text-xl font-bold text-gray-800 mb-2">Learning Roadmap</h3>
        <p className="text-gray-600">{message.content}</p>
      </div>

      {/* Roadmap Visualization */}
      <div className="space-y-8">
        {levels.map((level, levelIndex) => (
          <div key={level} className="relative">
            {/* Level indicator */}
            <div className="flex items-center mb-4">
              <div className="bg-blue-400 text-white text-sm font-medium px-3 py-1 rounded-full">
                Level {level}
              </div>
              {levelIndex < levels.length - 1 && (
                <div className="flex-1 h-px bg-gray-300 ml-4" />
              )}
            </div>

            {/* Nodes at this level */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {nodesByLevel[level].map((node, nodeIndex) => (
                <div
                  key={node.id}
                  className={cn(
                    "bg-white border-2 rounded-lg p-4 cursor-pointer transition-all duration-200",
                    "hover:border-blue-300 hover:shadow-lg hover:scale-[1.02]",
                    node.isCompleted 
                      ? "border-green-300 bg-green-50" 
                      : "border-gray-200 hover:border-blue-300"
                  )}
                  onClick={() => onRoadmapItemClick?.(node.id, node.title)}
                >
                  {/* Node content */}
                  <div className="space-y-2">
                    <h4 className="font-semibold text-gray-800">{node.title}</h4>
                    <p className="text-sm text-gray-600">{node.description}</p>
                    
                    {/* Metadata */}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      {node.estimatedTime && (
                        <span className="bg-gray-100 px-2 py-1 rounded">
                          {node.estimatedTime}
                        </span>
                      )}
                      {node.prerequisites.length > 0 && (
                        <span className="text-orange-600">
                          {node.prerequisites.length} prereq{node.prerequisites.length > 1 ? 's' : ''}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Connection line to next level */}
                  {levelIndex < levels.length - 1 && nodeIndex === 0 && (
                    <div className="absolute left-1/2 bottom-0 w-px h-8 bg-gray-300 transform translate-y-full -translate-x-1/2" />
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RoadmapResponse;
