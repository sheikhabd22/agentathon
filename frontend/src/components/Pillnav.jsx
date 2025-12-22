// src/components/Pillnav.jsx
import React from "react";
import { NavLink } from "react-router-dom";
import { Moon, Sun } from "lucide-react";

const Pillnav = ({ items, isTransparent, onToggleTheme, currentTheme }) => {
  return (
    <nav
      style={
        isTransparent
          ? {
            width: "100%",
            backgroundColor: "transparent",
            borderBottom: "1px solid rgba(255,255,255,0.1)", // subtle border for landing
          }
          : {
            width: "100%",
            borderBottom: "1px solid var(--color-border)",
            backgroundColor: "var(--color-bg-surface)",
          }
      }
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "16px 24px",
          display: "flex",
          justifyContent: "space-between", // Spread to allow toggle on right
          alignItems: "center",
        }}
      >
        <ul
          style={{
            display: "flex",
            gap: "16px",
            listStyle: "none",
            padding: 0,
            margin: "0 auto", // Keep nav items centered
            alignItems: "center",
            transform: "translateX(20px)", // Counter-balance the toggle to keep visual center
          }}
        >
          {items.map((item) => (
            <li key={item.href}>
              <NavLink
                to={item.href}
                style={({ isActive }) => ({
                  padding: "8px 16px",
                  borderRadius: "9999px",
                  border: isTransparent
                    ? isActive
                      ? "1px solid #8ab4f8"
                      : "1px solid transparent"
                    : isActive
                      ? "1px solid var(--color-primary)"
                      : "1px solid transparent",
                  color: isTransparent
                    ? isActive
                      ? "#8ab4f8"
                      : "#e8eaed"
                    : isActive
                      ? "#ffffff" // Active in normal mode (pill)
                      : "var(--color-text-secondary)",
                  backgroundColor: isTransparent
                    ? isActive
                      ? "rgba(138, 180, 248, 0.1)"
                      : "transparent"
                    : isActive
                      ? "var(--color-primary)"
                      : "transparent",
                  fontSize: "14px",
                  fontWeight: 500,
                  textDecoration: "none",
                  whiteSpace: "nowrap",
                  display: "inline-block",
                  transition: "all 0.2s",
                })}
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>

        {/* Theme Toggle */}
        <button
          onClick={onToggleTheme}
          style={{
            background: "transparent",
            border: "1px solid var(--color-border)",
            borderRadius: "50%",
            width: "36px",
            height: "36px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            color: isTransparent ? "#e8eaed" : "var(--color-text-primary)",
            borderColor: isTransparent ? "rgba(255,255,255,0.2)" : "var(--color-border)",
          }}
        >
          {currentTheme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>
    </nav>
  );
};

export default Pillnav;
