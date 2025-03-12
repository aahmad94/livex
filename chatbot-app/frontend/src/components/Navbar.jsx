import React from 'react';
import './Navbar.css';

const Navbar = ({ onSearch }) => {
    return (
        <nav className="navbar">
            <div className="navbar-logo">ChatBot</div>
            <input
                type="text"
                placeholder="Search..."
                className="search-bar"
                onChange={(e) => onSearch(e.target.value)}
            />
        </nav>
    );
};

export default Navbar; 