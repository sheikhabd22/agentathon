import React from "react";
import { NavLink } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import Silk from "@/components/Prism";
import "./SimpleLanding.css";

const SimpleLanding = () => {
  return (
    <div className="simple-landing">
      {/* 
         Increased speed and noiseIntensity for "more visible silk"
         Color remains white but interacts with the background multiply blend mode 
      */}
      <Silk speed={2.5} noiseIntensity={2.5} />

      <motion.div
        className="simple-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <h1>
          Supercharge Your Business with <span style={{ background: 'linear-gradient(90deg, #4285F4, #9B72CB, #D96570)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Agentic Intelligence</span>
        </h1>

        <p>
          Deploy autonomous AI agents that work 24/7 to analyze complex datasets, predict market trends,
          and automate risk assessment. Our multi-agent system integrates seamlessly with your
          existing workflow to unlock actionable insights that drive growth.
        </p>

        <NavLink to="/dashboard" className="gemini-btn">
          <span>Launch AI Console</span>
          <ArrowRight size={18} style={{ position: 'relative', zIndex: 1 }} />
        </NavLink>

        <div className="trust-text">
          Trusted by next-gen startups & enterprises
        </div>
      </motion.div>
    </div>
  );
};

export default SimpleLanding;
