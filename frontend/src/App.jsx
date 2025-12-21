import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import RiskAssessment from "./pages/RiskAssessment";
import AgentExplanation from "./pages/AgentExplanation";
import SimpleLanding from "./pages/SimpleLanding";
import ChatInterface from "./pages/ChatInterface";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <Routes>
        {/* Landing page — NO NAVBAR */}
        <Route path="/" element={<SimpleLanding />} />

        {/* App pages — WITH NAVBAR + DASHBOARD LAYOUT */}
        <Route
          element={
            <>
              <Navbar />
              <DashboardLayout />
            </>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/risks" element={<RiskAssessment />} />
          <Route path="/agents" element={<AgentExplanation />} />
          <Route path="/chat" element={<ChatInterface />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
