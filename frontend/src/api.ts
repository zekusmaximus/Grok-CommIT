const API_URL = 'http://localhost:8000';

export interface ChatResponse {
    role: string;
    content: string;
    phase?: string;
}

export const sendMessage = async (content: string, history: any[]): Promise<ChatResponse> => {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: content,
                history: history
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Error sending message:', error);
        return {
            role: 'assistant',
            content: 'Error: Could not connect to the Cognitive Engine. Is the backend running?'
        };
    }
};
