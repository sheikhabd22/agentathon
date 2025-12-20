import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, AlertTriangle, BrainCircuit, MessageSquare, Settings, LogOut } from 'lucide-react';
import './Sidebar.css';

const Sidebar = () => {
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/risks', label: 'Risk Assessment', icon: AlertTriangle },
    { path: '/agents', label: 'Agent Intelligence', icon: BrainCircuit },
    { path: '/chat', label: 'AI Assistant', icon: MessageSquare },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-area">
          <span className="logo-text">Agentic Analytics</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <item.icon size={20} className="nav-icon" />
            <span className="nav-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>


    </aside>
  );
};

export default Sidebar;
