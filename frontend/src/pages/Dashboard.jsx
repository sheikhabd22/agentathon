import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Database, ShoppingCart, CreditCard, Users, Activity } from 'lucide-react';
import { motion } from 'framer-motion';
import './Dashboard.css';

const defaultFallbackData = [
    { name: 'Mon', revenue: 4000, orders: 240, active: 2400 },
    { name: 'Tue', revenue: 3000, orders: 139, active: 2210 },
    { name: 'Wed', revenue: 2000, orders: 980, active: 2290 },
    { name: 'Thu', revenue: 2780, orders: 390, active: 2000 },
    { name: 'Fri', revenue: 1890, orders: 480, active: 2181 },
    { name: 'Sat', revenue: 2390, orders: 380, active: 2500 },
    { name: 'Sun', revenue: 3490, orders: 430, active: 2100 },
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
    visible: { y: 0, opacity: 1 }
};

export default function Dashboard() {
    const [data, setData] = useState(defaultFallbackData);
    const [summary, setSummary] = useState({
        revenue: '$24,680',
        customers: '1,248',
        pending_orders: '86'
    });

    useEffect(() => {
        let mounted = true;

        // Fetch monitoring overview (summary)
        fetch('/monitoring/overview')
            .then((r) => {
                if (!r.ok) throw new Error('overview fetch failed');
                return r.json();
            })
            .then((res) => {
                if (!mounted) return;
                if (res && res.summary) {
                    setSummary((prev) => ({
                        revenue: res.summary.revenue ?? prev.revenue,
                        customers: res.summary.customers ?? prev.customers,
                        pending_orders: res.summary.pending_orders ?? prev.pending_orders
                    }));
                }
            })
            .catch(() => {
                // keep fallback
            });

        // Fetch full monitoring snapshot (timeseries)
        fetch('/api/monitoring')
            .then((r) => {
                if (!r.ok) throw new Error('snapshot fetch failed');
                return r.json();
            })
            .then((snap) => {
                if (!mounted) return;
                if (!snap) return;
                if (Array.isArray(snap.timeseries)) {
                    setData(snap.timeseries);
                } else if (snap.metrics && Array.isArray(snap.metrics.timeseries)) {
                    setData(snap.metrics.timeseries);
                } else if (snap.metrics && Array.isArray(snap.metrics.history)) {
                    setData(snap.metrics.history);
                }
            })
            .catch(() => {
                // ignore and keep fallback
            });

        return () => { mounted = false; };
    }, []);

    return (
        <motion.div className="dashboard-container" variants={containerVariants} initial="hidden" animate="visible">
            {/* Top Status Bar */}
            <motion.div className="status-grid" variants={itemVariants}>
                <div className="status-card">
                    <div className="status-icon success"><Database size={16} /></div>
                    <div>
                        <div className="status-label">CRM Connected</div>
                        <div className="status-sub">Last sync: 2 min ago</div>
                    </div>
                    <div className="status-dot success"></div>
                </div>
                <div className="status-card">
                    <div className="status-icon success"><ShoppingCart size={16} /></div>
                    <div>
                        <div className="status-label">Shopify Linked</div>
                        <div className="status-sub">246 products active</div>
                    </div>
                    <div className="status-dot success"></div>
                </div>
                <div className="status-card">
                    <div className="status-icon warning"><CreditCard size={16} /></div>
                    <div>
                        <div className="status-label">Stripe Payments</div>
                        <div className="status-sub">Action required</div>
                    </div>
                    <div className="status-dot warning"></div>
                </div>
            </motion.div>

            {/* Metrics Row */}
            <motion.div className="metrics-grid" variants={itemVariants}>
                <div className="metric-card">
                    <div className="metric-header">
                        <span className="metric-title">Total Revenue</span>
                        <span className="metric-trend positive"><ArrowUpRight size={16} /> +12.5%</span>
                    </div>
                    <div className="metric-value">{summary.revenue}</div>
                    <div className="metric-chart">
                        <ResponsiveContainer width="100%" height={60}>
                            <AreaChart data={data}>
                                <Area type="monotone" dataKey="revenue" stroke="#1a73e8" fill="#e8f0fe" strokeWidth={2} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="metric-card">
                    <div className="metric-header">
                        <span className="metric-title">Active Customers</span>
                        <span className="metric-trend positive"><ArrowUpRight size={16} /> +5.2%</span>
                    </div>
                    <div className="metric-value">{summary.customers}</div>
                    <div className="metric-chart">
                        <ResponsiveContainer width="100%" height={60}>
                            <AreaChart data={data}>
                                <Area type="monotone" dataKey="active" stroke="#188038" fill="#e6f4ea" strokeWidth={2} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="metric-card">
                    <div className="metric-header">
                        <span className="metric-title">Pending Orders</span>
                        <span className="metric-trend negative"><ArrowDownRight size={16} /> -2.4%</span>
                    </div>
                    <div className="metric-value">{summary.pending_orders}</div>
                    <div className="metric-chart">
                        <ResponsiveContainer width="100%" height={60}>
                            <BarChart data={data}>
                                <Bar dataKey="orders" fill="#f29900" radius={[2, 2, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </motion.div>

            {/* Main Timeline / Intelligence View */}
            <motion.div className="main-chart-section card" variants={itemVariants}>
                <div className="chart-header">
                    <h3>Unified Activity Timeline</h3>
                    <div className="chart-actions">
                        <button className="btn-outline btn-sm">Day</button>
                        <button className="btn-outline btn-sm active">Week</button>
                        <button className="btn-outline btn-sm">Month</button>
                    </div>
                </div>
                <div className="chart-container">
                    <ResponsiveContainer width="100%" height={300}>
                        <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#1a73e8" stopOpacity={0.1} />
                                    <stop offset="95%" stopColor="#1a73e8" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorOrders" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#f29900" stopOpacity={0.1} />
                                    <stop offset="95%" stopColor="#f29900" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#5f6368', fontSize: 12 }} dy={10} />
                            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#5f6368', fontSize: 12 }} />
                            <CartesianGrid vertical={false} stroke="#e8eaed" />
                            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)' }} />
                            <Area type="monotone" dataKey="revenue" stroke="#1a73e8" fillOpacity={1} fill="url(#colorRevenue)" strokeWidth={2} name="Revenue" />
                            <Area type="monotone" dataKey="orders" stroke="#f29900" fillOpacity={1} fill="url(#colorOrders)" strokeWidth={2} name="Orders" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </motion.div>

            <motion.div className="insights-grid" variants={itemVariants}>
                <div className="card insight-card">
                    <div className="insight-header">
                        <Activity size={20} className="text-primary" />
                        <h4>Sales Anomaly Detected</h4>
                    </div>
                    <p>Unusual spike in orders from region "California". AI Agent is verifying inventory levels.</p>
                    <button className="btn btn-outline" style={{ marginTop: 'auto' }}>View Details</button>
                </div>

                <div className="card insight-card">
                    <div className="insight-header">
                        <Users size={20} className="text-success" />
                        <h4>Customer Retention</h4>
                    </div>
                    <p>Returning customer rate increased by <strong>15%</strong> this week due to the new loyalty campaign.</p>
                    <button className="btn btn-outline" style={{ marginTop: 'auto' }}>View Report</button>
                </div>
            </motion.div>
        </motion.div>
    );
}
