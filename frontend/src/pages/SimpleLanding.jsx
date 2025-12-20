import React from "react";
import { NavLink } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import "./SimpleLanding.css";

const SimpleLanding = () => {
  return (
    <div className="simple-landing">
      <motion.div
        className="simple-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >

        <h1>
          Intelligence for <br />
          Business Decisions
        </h1>

        <p>
          Agentic Analytics continuously monitors your financial and operational
          data to detect risks and growth signals before humans notice them.
        </p>

        <NavLink to="/dashboard" className="cta-btn">
          Launch Console <ArrowRight size={18} />
        </NavLink>

        <div className="trust-text">
          Trusted by 500+ growing teams
        </div>
      </motion.div>

    </div>
  );
};

export default SimpleLanding;
