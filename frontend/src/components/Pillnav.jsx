// src/components/Pillnav.jsx
import React from "react";
import { NavLink } from "react-router-dom";

const Pillnav = ({ items }) => {
  return (
    <nav
      style={{
        width: "100%",
        borderBottom: "1px solid #e5e7eb",
        backgroundColor: "#ffffff",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "16px 24px",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <ul
          style={{
            display: "flex",
            gap: "16px",
            listStyle: "none",
            padding: 0,
            margin: 0,
            alignItems: "center",
          }}
        >
          {items.map((item) => (
            <li key={item.href}>
              <NavLink
                to={item.href}
                style={({ isActive }) => ({
                  padding: "8px 16px",
                  borderRadius: "9999px",
                  border: "1px solid #2563eb",
                  color: isActive ? "#ffffff" : "#2563eb",
                  backgroundColor: isActive ? "#2563eb" : "transparent",
                  fontSize: "14px",
                  fontWeight: 500,
                  textDecoration: "none",
                  whiteSpace: "nowrap",
                  display: "inline-block",
                })}
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Pillnav;
