import ChatInterface from "@/components/ChatInterface";
import Background from "/gradient-optimized_4.svg"

const Index = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50" style={{
            backgroundImage: `url(${Background})`,
            backgroundSize: '300% 2600px',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center top',
        }}>
            <ChatInterface/>
        </div>
    );
};

export default Index;
