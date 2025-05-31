
export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  images?: string[];
  imageCaptions?: string[];
  isStreaming?: boolean;
  responseType?: "text" | "text_with_images" | "roadmap" | "concepts" | "applications";
  roadmapData?: RoadmapNode[];
  conceptsData?: ConceptData[];
  applicationsData?: ApplicationData[];
  isLoading?: boolean;
}

export interface RoadmapNode {
  id: string;
  title: string;
  description: string;
  level: number;
  prerequisites: string[];
  isCompleted?: boolean;
  estimatedTime?: string;
}

export interface ConceptData {
  name: string;
  type: string;
  domain: string;
  significance: string;
  confidence: number;
}

export interface ApplicationData {
  name: string;
  brief_description: string;
  description: string;
  images: ApplicationImage[];
  RoadmapData: RoadmapData[];
}

export interface ApplicationImage {
  url: string;
  title: string;
  thumbnail: string;
  context: string;
  width: number;
  height: number;
}

export interface RoadmapData {
  title: string;
  description_1: string[][];
  description_2: string[][];
  description_3: string[][];
  application: string;
}

export interface APIResponse {
  uuid: string;
  last_relevant_concepts_timestamp: number;
  last_applications_timestamp: number;
  document_path: string;
  text_input: string;
  user_metadata: {
    background: string;
  };
  relevant_concepts: ConceptData[];
  concept_applications: Record<string, ApplicationData[]>;
  error: string | null;
}
