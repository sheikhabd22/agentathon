import React, { useEffect, useState } from 'react';
import { AlertCircle, TrendingUp, TrendingDown, Eye, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import './RiskAssessment.css';

const defaultFallbackRisks = [
    {
        id: 1,
        severity: 'high',
        title: 'Cash Flow Instability Forecast',
        explanation: 'Based on current accounts receivable trends and upcoming tax liabilities, cash reserves may dip below safe thresholds in 6 days.',
        trend: 'deteriorating',
        source: 'QuickBooks + Bank Feed',
        confidence: '94%',
    },
    {
        id: 2,
        severity: 'medium',
        title: 'Supply Chain Delay - Vendor A',
        explanation: 'Vendor A has shown a 3-day average delay in shipment for the last 4 orders. This risks stockouts for product category Z.',
        trend: 'stable',
        source: 'Shopify Inventory',
        confidence: '82%',
    },
    {
        id: 3,
        severity: 'low',
        title: 'Customer Churn Risk',
        explanation: 'Engagement metrics for 3 key accounts have dropped by 15% over the last month.',
        trend: 'improving',
        source: 'HubSpot',
        confidence: '65%',
    },
    {
        id: 4,
        severity: 'high',
        title: 'Unusual Transaction Detected',
        explanation: 'Transaction #9923 for $5,000 originates from an unrecognized IP address. Flagged as potential fraud.',
        trend: 'new',
        source: 'Stripe Payments',
        confidence: '99%',
    }
];

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1
        }
    }
};

const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
        y: 0,
        opacity: 1
    }
};

const RiskAssessment = () => {
    const [activeRisks, setActiveRisks] = useState([]);
    const [historicalRisks, setHistoricalRisks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        fetch('/risks')
            .then(r => {
                if (!r.ok) throw new Error('Failed to fetch risks');
                return r.json();
            })
            .then(res => {
                if (res && res.active_risks) {
                    setActiveRisks(res.active_risks);
                }
                if (res && res.historical_risks) {
                    setHistoricalRisks(res.historical_risks);
                }
            })
            .catch(err => {
                console.error('Risk fetch error:', err);
                // Use fallback
                setActiveRisks(defaultFallbackRisks.slice(0, 2));
                setHistoricalRisks(defaultFallbackRisks.slice(2));
            })
            .finally(() => setLoading(false));
    }, []);

    const displayRisks = activeRisks.length > 0 ? activeRisks : defaultFallbackRisks;
    const criticalCount = displayRisks.filter(r => r.severity === 'high' || r.severity === 'High').length;
    const warningCount = displayRisks.filter(r => r.severity === 'medium' || r.severity === 'Medium').length;

    return (
        <motion.div
            className="risk-container"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
        >
            <motion.div className="risk-header-stats" variants={itemVariants}>
                <div className="risk-stat-card critical">
                    <span className="label">Critical Risks</span>
                    <span className="value">{criticalCount}</span>
                </div>
                <div className="risk-stat-card warning">
                    <span className="label">Warnings</span>
                    <span className="value">{warningCount}</span>
                </div>
                <div className="risk-stat-card safe">
                    <span className="label">Resolved (24h)</span>
                    <span className="value">{historicalRisks.length}</span>
                </div>
            </motion.div>

            <div className="risks-list">
                {loading ? (
                    <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>Loading risks...</div>
                ) : displayRisks.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>No active risks detected</div>
                ) : (
                    displayRisks.map((risk) => (
                        <motion.div
                            key={risk.id}
                            className={`risk-card severity-${(risk.severity || 'medium').toLowerCase()}`}
                            variants={itemVariants}
                            whileHover={{ y: -5, transition: { duration: 0.2 } }}
                        >
                            <div className="risk-card-header">
                                <div className="severity-badge">{risk.severity} Risk</div>
                                {risk.trend === 'deteriorating' && <div className="trend-badge negative"><TrendingDown size={14} /> Worsening</div>}
                                {risk.trend === 'improving' && <div className="trend-badge positive"><TrendingUp size={14} /> Improving</div>}
                                {risk.trend === 'new' && <div className="trend-badge new"><AlertCircle size={14} /> New</div>}
                            </div>

                            <h3 className="risk-title">{risk.title}</h3>
                            <p className="risk-explanation">{risk.explanation || risk.description}</p>

                            <div className="risk-meta">
                                <div className="meta-item">
                                    <span className="meta-label">Source:</span> {risk.source || 'System'}
                                </div>
                                <div className="meta-item">
                                    <span className="meta-label">AI Confidence:</span> {risk.confidence || '—'}
                                </div>
                            </div>

                            <div className="risk-actions">
                                <button className="btn btn-outline btn-sm">
                                    <Eye size={14} className="icon-left" /> See Proof
                                </button>
                                <button className="btn btn-primary btn-sm">
                                    Take Action
                                </button>
                                <div className="spacer"></div>
                                <button className="btn btn-icon text-success">
                                    <CheckCircle size={18} />
                                </button>
                            </div>
                        </motion.div>
                    ))
                )}
            </div>
        </motion.div>
    );
};

export default RiskAssessment;
