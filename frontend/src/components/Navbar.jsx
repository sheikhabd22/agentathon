import React from "react";
import { useLocation } from "react-router-dom";
import Pillnav from "./Pillnav";

const Navbar = () => {
  const location = useLocation();

  return (
    <Pillnav
      items={[
        { label: "Home", href: "/" },
        { label: "Dashboard", href: "/dashboard" },
        { label: "Risks", href: "/risks" },
        { label: "Agents", href: "/agents" },
        { label: "Chat", href: "/chat" },
      ]}
      activeHref={location.pathname}
    />
  );
};

export default Navbar;
