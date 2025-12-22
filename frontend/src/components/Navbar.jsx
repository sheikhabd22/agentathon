import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Pillnav from "./Pillnav";

const Navbar = () => {
  const location = useLocation();
  const isLanding = location.pathname === "/";
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <div style={isLanding ? { position: "absolute", top: 0, left: 0, width: "100%", zIndex: 100 } : {}}>
      <Pillnav
        items={[
          { label: "Home", href: "/" },
          { label: "Dashboard", href: "/dashboard" },
          { label: "Risks", href: "/risks" },
          { label: "Agents", href: "/agents" },
          { label: "Chat", href: "/chat" },
        ]}
        activeHref={location.pathname}
        isTransparent={isLanding}
        onToggleTheme={toggleTheme}
        currentTheme={theme}
      />
    </div>
  );
};

export default Navbar;
