import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chatbot.css';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [email, setEmail] = useState('');
    const [timer, setTimer] = useState(0);
    const [isLoading, setIsLoading] = useState(false);
    const messageViewRef = useRef(null);

    // Timer effect
    useEffect(() => {
        let interval;
        if (isOpen) {
            interval = setInterval(() => setTimer(t => t + 1), 1000);
        }
        return () => clearInterval(interval);
    }, [isOpen]);

    // Scroll to bottom effect
    useEffect(() => {
        if (messageViewRef.current) {
            messageViewRef.current.scrollTop = messageViewRef.current.scrollHeight;
        }
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || !email) return;
        
        const userMessage = { role: 'user', content: input };
        setMessages([...messages, userMessage]);
        setInput('');
        setIsLoading(true);
        
        try {
            const response = await axios.post('http://localhost:8000/chat', {
                email,
                messages: [...messages, userMessage]
            });
            
            setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: 'Sorry, I encountered an error. Please try again later.' 
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    const resetChat = () => {
        setMessages([]);
        setTimer(0);
    };

    const closeChat = () => {
        setIsOpen(false);
        setTimer(0);
    };

    return (
        <>
            <button className="chatbot-icon" onClick={() => setIsOpen(true)}>
                💬
            </button>
            
            {isOpen && (
                <div className="chatbot-window">
                    <div className="chatbot-header">
                        <span>{timer}s</span>
                        <div>
                            <button onClick={resetChat}>Reset</button>
                            <button onClick={closeChat}>Close</button>
                        </div>
                    </div>
                    
                    {!email ? (
                        <div className="email-input">
                            <h3>Enter your email to start chatting</h3>
                            <input
                                type="email"
                                placeholder="Your email address..."
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                onKeyPress={handleKeyPress}
                            />
                            <button 
                                onClick={() => email && setEmail(email)}
                                disabled={!email}
                            >
                                Start Chatting
                            </button>
                        </div>
                    ) : (
                        <>
                            <div className="message-view" ref={messageViewRef}>
                                {messages.length === 0 ? (
                                    <div className="welcome-message">
                                        <p>Hello! I'm your Cal.com assistant. I can help you:</p>
                                        <ul>
                                            <li>Check available time slots</li>
                                            <li>Book new events</li>
                                            <li>List your scheduled events</li>
                                            <li>Cancel or reschedule events</li>
                                        </ul>
                                        <p>How can I help you today?</p>
                                    </div>
                                ) : (
                                    messages.map((msg, idx) => (
                                        <div key={idx} className={`message ${msg.role}`}>
                                            {msg.content}
                                        </div>
                                    ))
                                )}
                                {isLoading && (
                                    <div className="message assistant loading">
                                        <div className="typing-indicator">
                                            <span></span>
                                            <span></span>
                                            <span></span>
                                        </div>
                                    </div>
                                )}
                            </div>
                            
                            <div className="input-view">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyPress={handleKeyPress}
                                    placeholder="Type your message..."
                                    disabled={isLoading}
                                />
                                <button 
                                    onClick={sendMessage}
                                    disabled={!input.trim() || isLoading}
                                >
                                    Send
                                </button>
                            </div>
                        </>
                    )}
                </div>
            )}
        </>
    );
};

export default Chatbot; 