import React from "react";
import { NavLink } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import FloatingLines from "@/components/FloatingLines";
import "./SimpleLanding.css";

const SimpleLanding = () => {
  return (
    <div className="simple-landing">
      {/* 
         New FloatingLines Background with Google-ish Colors 
         Using a gradient that hints at Blue, Red, Yellow, Green
      */}
      <FloatingLines
        linesGradient={["#4285F4", "#EA4335", "#FBBC05", "#34A853"]}
        animationSpeed={0.5}
        lineCount={[4]}
        lineDistance={[4]}
        enabledWaves={['bottom', 'middle']}
        mixBlendMode="screen"
      />

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
