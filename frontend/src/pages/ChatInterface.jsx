import React, { useState, useRef, useEffect } from 'react';
import { Send, User, BrainCircuit, Sparkles, Paperclip } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './ChatInterface.css';

const initialMessages = [
    {
        id: 1,
        sender: 'agent',
        content: 'Hello! I am your Autonomous Business Analyst. I have finished scanning your connected data sources. How can I help you today?',
        timestamp: '10:00 AM'
    }
];

const suggestedQueries = [
    "Analyze my cash flow for next month",
    "Why is customer retention dropping?",
    "Draft a email to delayed payers",
    "Show me highest risk transactions"
];

const ChatInterface = () => {
    const [messages, setMessages] = useState(initialMessages);
    const [inputValue, setInputValue] = useState('');
    const [isThinking, setIsThinking] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isThinking]);

    const handleSend = () => {
        if (!inputValue.trim()) return;

        const newUserMsg = {
            id: Date.now(),
            sender: 'user',
            content: inputValue,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        setMessages(prev => [...prev, newUserMsg]);
        setInputValue('');
        setIsThinking(true);

        // Simulate agent response
        setTimeout(() => {
            const agentMsg = {
                id: Date.now() + 1,
                sender: 'agent',
                content: 'I have analyzed the recent transaction data. It appears there is a discrepancy in the "Office Supplies" category which is 15% higher than average. This correlates with the new vendor onboarded last week.',
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            setMessages(prev => [...prev, agentMsg]);
            setIsThinking(false);
        }, 2000);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <motion.div
            className="chat-container"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
        >
            <div className="chat-main">
                <div className="chat-messages">
                    <AnimatePresence>
                        {messages.map((msg) => (
                            <motion.div
                                key={msg.id}
                                className={`message-wrapper ${msg.sender}`}
                                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                                animate={{ opacity: 1, y: 0, scale: 1 }}
                                transition={{ duration: 0.3 }}
                            >
                                <div className="avatar">
                                    {msg.sender === 'agent' ? <BrainCircuit size={20} /> : <User size={20} />}
                                </div>
                                <div className="message-bubble">
                                    <div className="message-content">{msg.content}</div>
                                    <div className="message-time">{msg.timestamp}</div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    {isThinking && (
                        <motion.div
                            className="message-wrapper agent"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            <div className="avatar"><BrainCircuit size={20} /></div>
                            <div className="message-bubble thinking">
                                <span className="dot"></span>
                                <span className="dot"></span>
                                <span className="dot"></span>
                            </div>
                        </motion.div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <div className="chat-input-area">
                    {messages.length < 3 && (
                        <div className="suggestions">
                            {suggestedQueries.map((q, i) => (
                                <button key={i} className="suggestion-chip" onClick={() => setInputValue(q)}>
                                    <Sparkles size={14} /> {q}
                                </button>
                            ))}
                        </div>
                    )}
                    <div className="input-wrapper">
                        <button className="attach-btn"><Paperclip size={20} /></button>
                        <textarea
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask anything about your business data..."
                            rows={1}
                        />
                        <button className="send-btn" onClick={handleSend} disabled={!inputValue.trim()}>
                            <Send size={20} />
                        </button>
                    </div>
                    <div className="disclaimer">
                        AI can make mistakes. Please verify important financial decisions.
                    </div>
                </div>
            </div>
        </motion.div>
    );
};

export default ChatInterface;
