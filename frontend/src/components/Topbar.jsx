import React from 'react';
import { Search, Bell, HelpCircle, User } from 'lucide-react';
import './Topbar.css';

const Topbar = ({ title }) => {
    return (
        <header className="topbar">
            <div className="topbar-left">
                <h1 className="page-title">{title}</h1>
            </div>

            <div className="topbar-center">
                <div className="search-bar">
                    <Search size={18} className="search-icon" />
                    <input type="text" placeholder="Search resources, risks, or agents..." />
                </div>
            </div>

            <div className="topbar-right">
                <button className="icon-btn">
                    <HelpCircle size={20} />
                </button>
            </div>
        </header>
    );
};

export default Topbar;
