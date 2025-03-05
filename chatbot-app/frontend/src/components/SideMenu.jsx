import React from 'react';
import './SideMenu.css';

const SideMenu = ({ onSelect, selected }) => {
    return (
        <div className="side-menu">
            <div
                className={`menu-item ${selected === 'Apps' ? 'active' : ''}`}
                onClick={() => onSelect('Apps')}
            >
                <span className="icon">📱</span> Apps
            </div>
            <div
                className={`menu-item ${selected === 'Documents' ? 'active' : ''}`}
                onClick={() => onSelect('Documents')}
            >
                <span className="icon">📄</span> Documents
            </div>
        </div>
    );
};

export default SideMenu; 