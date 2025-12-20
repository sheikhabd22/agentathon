import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Topbar from '../components/Topbar';
import './DashboardLayout.css';

const DashboardLayout = () => {
    const location = useLocation();

    const getTitle = (pathname) => {
        if (pathname.includes('dashboard')) return 'Unified Intelligence Dashboard';
        if (pathname.includes('risks')) return 'Risk Assessment';
        if (pathname.includes('agents')) return 'AI Agent Intelligence';
        if (pathname.includes('chat')) return 'AI Assistant';
        return 'Dashboard';
    };

    return (
        <div className="dashboard-layout">
            <Sidebar />
            <div className="main-content-wrapper">
                <Topbar title={getTitle(location.pathname)} />
                <main className="content-area">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;
