
const POLLING_INTERVAL = 2000; // 2 seconds
const BACKEND_URL = "http://localhost:8000";

export class APIService {
    private static instance: APIService;
    private pollingInterval: NodeJS.Timeout | null = null;
    private lastTimestamps = { concepts: 0, applications: 0 };
    private lastApplicationsData: Record<string, any[]> = {};

    static getInstance(): APIService {
        if (!APIService.instance) {
            APIService.instance = new APIService();
        }
        return APIService.instance;
    }

    async submitQuery(content: string, file?: File): Promise<void> {
        console.log({
            'file_name': file?.name || '',
            'user_query': content
        });

        // Start the workflow (don't wait for completion)
        fetch(`${BACKEND_URL}/run_workflow/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                'file_name': file?.name || '',
                'user_query': content
            })
        }).catch(error => {
            console.error("Workflow submission error:", error);
        });

        // Reset timestamps and cached data for new query
        this.lastTimestamps = { concepts: 0, applications: 0 };
        this.lastApplicationsData = {};
    }

    startPolling(
        onConceptsUpdate: (concepts: any[], timestamp: number) => void,
        onApplicationsUpdate: (applications: Record<string, any[]>, timestamp: number) => void
    ): void {
        console.log("Start polling...");

        if (this.pollingInterval) {
            console.log("Already polling...");
            return; // Already polling
        }

        const poll = async () => {
            try {
                const response = await this.fetchData();

                // Check if we have new concepts data
                if (response.data?.last_relevant_concepts_timestamp &&
                    response.data.last_relevant_concepts_timestamp > this.lastTimestamps.concepts) {
                    onConceptsUpdate(
                        response.data.relevant_concepts || [],
                        response.data.last_relevant_concepts_timestamp
                    );
                    this.lastTimestamps.concepts = response.data.last_relevant_concepts_timestamp;
                }

                // Check if we have new applications data OR if roadmap data has been updated
                const currentApplications = response.data?.concept_applications || {};
                const hasNewApplications = response.data?.last_applications_timestamp &&
                    response.data.last_applications_timestamp > this.lastTimestamps.applications;
                
                const hasUpdatedRoadmapData = this.checkForRoadmapUpdates(currentApplications, this.lastApplicationsData);

                if (hasNewApplications || hasUpdatedRoadmapData) {
                    onApplicationsUpdate(
                        currentApplications,
                        response.data?.last_applications_timestamp || Date.now()
                    );
                    
                    if (hasNewApplications) {
                        this.lastTimestamps.applications = response.data.last_applications_timestamp;
                    }
                    
                    // Update cached applications data
                    this.lastApplicationsData = JSON.parse(JSON.stringify(currentApplications));
                }
            } catch (error) {
                console.error("Polling error:", error);
            }
        };

        this.pollingInterval = setInterval(poll, POLLING_INTERVAL);
        // Start polling immediately
        poll();
    }

    private checkForRoadmapUpdates(currentApplications: Record<string, any[]>, lastApplications: Record<string, any[]>): boolean {
        // Check if roadmap data has been updated in any application
        for (const conceptName in currentApplications) {
            const currentApps = currentApplications[conceptName] || [];
            const lastApps = lastApplications[conceptName] || [];
            
            for (let i = 0; i < currentApps.length; i++) {
                const currentApp = currentApps[i];
                const lastApp = lastApps[i];
                
                // If this is a new application or roadmap data has changed
                if (!lastApp || this.hasRoadmapDataChanged(currentApp.RoadmapData, lastApp.RoadmapData)) {
                    console.log(`Roadmap data updated for ${currentApp.name}`);
                    return true;
                }
            }
        }
        return false;
    }

    private hasRoadmapDataChanged(currentRoadmap: any[], lastRoadmap: any[]): boolean {
        // If one is empty and the other isn't, there's a change
        if ((!currentRoadmap || currentRoadmap.length === 0) !== (!lastRoadmap || lastRoadmap.length === 0)) {
            return true;
        }
        
        // If both are empty or undefined, no change
        if ((!currentRoadmap || currentRoadmap.length === 0) && (!lastRoadmap || lastRoadmap.length === 0)) {
            return false;
        }
        
        // If lengths are different, there's a change
        if (currentRoadmap.length !== lastRoadmap.length) {
            return true;
        }
        
        // Compare roadmap data content
        return JSON.stringify(currentRoadmap) !== JSON.stringify(lastRoadmap);
    }

    stopPolling(): void {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    private async fetchData(): Promise<{ status: string; data?: any; message?: string }> {
        const response = await fetch(`${BACKEND_URL}/get_workflow_state/`);

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        return await response.json();
    }
}
