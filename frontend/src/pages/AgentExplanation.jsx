import React, { useState } from 'react';
import { ChevronRight, Database, Search, BrainCircuit, ShieldCheck, AlertTriangle } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import './AgentExplanation.css';

const reasoningSteps = [
    {
        step: 1,
        title: 'Data Ingestion',
        desc: 'Aggregated data from QuickBooks (Sales), Stripe (Payments), and Shopify (Inventory) for the period Dec 1 - Dec 18.',
        icon: Database,
        status: 'complete'
    },
    {
        step: 2,
        title: 'Pattern Recognition',
        desc: 'Detected anomaly in "Cash Flow" vs "Accounts Payable". Deviation of 22% from historical baseline.',
        icon: Search,
        status: 'complete'
    },
    {
        step: 3,
        title: 'Risk Modeling',
        desc: 'Projected cash reserves against upcoming tax liabilities due on Jan 15. Probability of shortfall calculated at 88%.',
        icon: BrainCircuit,
        status: 'active'
    },
    {
        step: 4,
        title: 'Verification',
        desc: 'Cross-referenced with pending invoices. Confirmed 3 major clients are late on payments (Net30 violation).',
        icon: ShieldCheck,
        status: 'pending'
    }
];

const data = [
    { name: 'Financial Data', value: 40, color: '#1a73e8' },
    { name: 'Historical Patterns', value: 30, color: '#f29900' },
    { name: 'External Indicators', value: 20, color: '#188038' },
    { name: 'User Rules', value: 10, color: '#9aa0a6' },
];

const AgentExplanation = () => {
    const [activeIndex, setActiveIndex] = useState(2);

    return (
        <motion.div
            className="agent-container"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="explanation-header">
                <div className="risk-context">
                    <div className="badge-high">High Severity Risk</div>
                    <h1>Cash Flow Instability Forecast Analysis</h1>
                    <p>Agent #402 Analyzing financial health based on multi-source signals.</p>
                </div>
                <div className="confidence-score">
                    <div className="score-ring">
                        <span className="score-value">94%</span>
                        <span className="score-label">Confidence</span>
                    </div>
                </div>
            </div>

            <div className="explanation-grid">
                <div className="reasoning-chain card">
                    <h3>Decison Trace</h3>
                    <div className="steps-container">
                        {reasoningSteps.map((step, index) => (
                            <motion.div
                                key={index}
                                className={`step-item ${index <= activeIndex ? 'active' : ''}`}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.2 }}
                            >
                                <div className="step-icon">
                                    <step.icon size={20} />
                                </div>
                                <div className="step-content">
                                    <div className="step-title">{step.title}</div>
                                    <div className="step-desc">{step.desc}</div>
                                </div>
                                {index < reasoningSteps.length - 1 && <div className="step-line"></div>}
                            </motion.div>
                        ))}
                    </div>
                </div>

                <motion.div
                    className="evidence-panel"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                >
                    <div className="card mb-4">
                        <h3>Signal Composition</h3>
                        <div style={{ width: '100%', height: 200 }}>
                            <ResponsiveContainer>
                                <PieChart>
                                    <Pie data={data} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                                        {data.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="legend">
                            {data.map(d => (
                                <div key={d.name} className="legend-item">
                                    <span className="dot" style={{ backgroundColor: d.color }}></span>
                                    {d.name} ({d.value}%)
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="card">
                        <h3>Data Sources Used</h3>
                        <div className="source-list">
                            <div className="source-item">
                                <Database size={16} /> QuickBooks Online (Last synced 10m ago)
                            </div>
                            <div className="source-item">
                                <Database size={16} /> Stripe API (Real-time)
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </motion.div>
    );
};

export default AgentExplanation;
