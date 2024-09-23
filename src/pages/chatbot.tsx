import Page from '@/components/page';
import React, { useEffect, useState, useRef} from 'react';
import _ from 'lodash';
import * as chat from '@botpress/chat';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [client, setClient] = useState<any>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [listener, setListener] = useState<any>(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const initChat = async () => {
      const apiUrl = `https://chat.botpress.cloud/18d59c6d-437f-4fb8-98d3-c615ed30faf2`;
      const chatClient = await chat.Client.connect({ apiUrl });
      setClient(chatClient);

      const { conversation } = await chatClient.createConversation({});
      setConversationId(conversation.id);

      // Set up the listener for incoming messages
      const messageListener = await chatClient.listenConversation({ id: conversation.id });
      setListener(messageListener);

      // Listen for message events
      const onMessage = (ev: chat.Events['message_created']) => {
        if (ev.userId !== chatClient.user.id) {
          // Only update state if the message is from the bot
          if (ev.payload.type === 'text') {
            let cleanedText = ev.payload.text;
            if (cleanedText.startsWith("I encountered an issue")) {
              cleanedText = "Thinking...";
            } else {
              cleanedText = ev.payload.text.replace(/^.*?1/, '').replace(/\*\*[^*]+\*\*/g, '').replace(/["']/g, '').replace(/(\d+)/g, '\n$1').replace(/2\..*/g, '').replace(/1\. : /g, '');
            }
            //const cleanedText = ev.payload.text.replace(/\*\*[^*]+\*\*/g, '').replace(/["']/g, '').replace(/^I encountered an issue/i, 'Thinking...');
            setMessages((prev) => [...prev, { sender: 'bot', text: cleanedText }]);
          }
        }
      };

      messageListener.on('message_created', onMessage);
    };

    initChat().catch(console.error);

    // Cleanup listener on component unmount
    return () => {
      if (listener) {
        listener.off('message_created', onMessage);
      }
    };
  }, []);

  const handleSend = async () => {
    if (!input.trim() || !conversationId || !client) return;

    const userMsg: Message = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);

    // Send message to the bot
    await client.createMessage({
      conversationId,
      payload: {
        type: 'text',
        text: input,
      },
    });
    setInput('');
  };

  return (
    <div style={{ height: "calc(100vh - 68px)", width: "20%", margin: "0 auto", border: "1px solid black", borderRadius: "8px", overflowY: "auto"}}>
      <div className="overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`my-2 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              style={{ maxWidth: '100%', wordBreak: 'break-word', color: message.sender === 'user' ? 'black' : 'blue', backgroundColor: message.sender === 'user' ? 'lightgray' : 'lightgray'}}
            >
              {message.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div style={{left: "100000px"}}>
        <div className="justify-center items-center h-screen">
          <input
            type="text"
            className="flex-grow p-2 border rounded-l-lg focus:outline-none"
            placeholder="Ask a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button
            className="bg-blue-500 text-white p-2 rounded-r-lg hover:bg-blue-600"
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default function Home() {
  return (
    <Page>
      <div className="min-h-screen flex items-center justify-center bg-gray-200">
        <ChatBot />
      </div>
    </Page>
  );
}
