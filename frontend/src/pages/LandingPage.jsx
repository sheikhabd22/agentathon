import React from 'react';
import { NavLink } from 'react-router-dom';
import { BrainCircuit, Shield, TrendingUp, ArrowRight, Check } from 'lucide-react';
import { motion } from 'framer-motion';
import FloatingLines from '../components/FloatingLines';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <div className="landing-page">
            <nav className="landing-nav container">
                <div className="landing-logo">
                    <div className="logo-icon-lg">
                        <BrainCircuit size={28} color="white" />
                    </div>
                    <span>Agentic Analytics</span>
                </div>
                <div className="landing-links">
                    <a href="#features">Features</a>
                    <a href="#pricing">Pricing</a>
                    <NavLink to="/dashboard" className="btn btn-primary">Launch Console</NavLink>
                </div>
            </nav>

            <header className="hero-section container">
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                >
                    <div className="hero-badge">New: Autonomous Risk Detection</div>
                    <h1>The Intelligence Layer<br />For Your Business</h1>
                    <p className="hero-sub">
                        Stop drowning in spreadsheets. Connect your CRM, Payments, and E-commerce data into a single autonomous system that finds risks before they become problems.
                    </p>
                    <div className="hero-actions">
                        <NavLink to="/dashboard" className="btn btn-primary btn-lg">
                            Get Started <ArrowRight size={20} style={{ marginLeft: 8 }} />
                        </NavLink>
                        <button className="btn btn-outline btn-lg">Watch Demo</button>
                    </div>
                    <div className="hero-trust">
                        <span>Trusted by 500+ small businesses</span>
                    </div>
                </motion.div>

                <div className="hero-bg-animation" style={{ position: 'absolute', right: 0, top: 0, width: '50%', height: '100%', pointerEvents: 'none', zIndex: 0 }}>
                    <FloatingLines
                        enabledWaves={['top', 'middle', 'bottom']}
                        lineCount={[10, 15, 20]}
                        lineDistance={[0.3, 0.2, 0.1]}
                        bendRadius={5.0}
                        bendStrength={-0.5}
                        interactive={true}
                        parallax={true}
                    />
                </div>

                <motion.div
                    className="hero-visual"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                >
                    <div className="visual-card-stack">
                        <motion.div
                            className="v-card card-1"
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
                        >
                            <Shield size={32} className="text-primary" />
                            <div className="v-text">Risk Detected</div>
                            <div className="v-sub">Cash Flow <span className="negative">-12%</span></div>
                        </motion.div>

                        <motion.div
                            className="v-card card-2"
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 5, delay: 1, ease: "easeInOut" }}
                        >
                            <TrendingUp size={32} className="text-success" />
                            <div className="v-text">Growth Signal</div>
                            <div className="v-sub">Retention <span className="positive">+5%</span></div>
                        </motion.div>

                        <div className="main-preview">
                            {/* Abstract representation of dashboard */}
                            <div className="preview-header"></div>
                            <div className="preview-grid"></div>
                        </div>
                    </div>
                </motion.div>
            </header>

            <section className="features-section" id="features">
                <div className="container">
                    <h2 className="section-title">Why choose Agentic?</h2>
                    <div className="features-grid">
                        <motion.div
                            className="feature-item"
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.1 }}
                        >
                            <div className="f-icon"><BrainCircuit size={32} /></div>
                            <h3>Autonomous Agents</h3>
                            <p>Agents monitoring your data 24/7, alerting you only when it matters.</p>
                        </motion.div>
                        <motion.div
                            className="feature-item"
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.2 }}
                        >
                            <div className="f-icon"><Shield size={32} /></div>
                            <h3>Proactive Protection</h3>
                            <p>Forecast cash flow dips and supply chain delays weeks in advance.</p>
                        </motion.div>
                        <motion.div
                            className="feature-item"
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.3 }}
                        >
                            <div className="f-icon"><TrendingUp size={32} /></div>
                            <h3>Unified Growth</h3>
                            <p>Correlate disparate data points to find hidden revenue opportunities.</p>
                        </motion.div>
                    </div>
                </div>
            </section>

            <footer className="landing-footer">
                <div className="container">
                    <p>&copy; 2025 Agentic Analytics Inc.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
