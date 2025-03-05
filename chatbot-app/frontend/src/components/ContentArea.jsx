import React from 'react';
import './ContentArea.css';

// Generate Lorem Ipsum paragraphs
const generateLoremIpsum = (count) => {
    const loremText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
    return Array(count).fill().map(() => loremText);
};

const ContentArea = ({ page, searchTerm }) => {
    // Generate different content for each page
    const content = page === 'Apps' 
        ? generateLoremIpsum(10)
        : generateLoremIpsum(8);

    // Filter and highlight content based on search term
    const filteredContent = content.map((text, index) => {
        if (searchTerm && !text.toLowerCase().includes(searchTerm.toLowerCase())) {
            return null;
        }
        
        if (searchTerm) {
            // Highlight matching text
            const regex = new RegExp(`(${searchTerm})`, 'gi');
            const highlightedText = text.replace(regex, '<span class="highlight">$1</span>');
            return (
                <p key={index} dangerouslySetInnerHTML={{ __html: highlightedText }} />
            );
        }
        
        return <p key={index}>{text}</p>;
    }).filter(Boolean);

    return (
        <div className="content-area">
            <h2>{page} Page</h2>
            {filteredContent.length > 0 ? filteredContent : <p>No content matches your search.</p>}
        </div>
    );
};

export default ContentArea; 