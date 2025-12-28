const express = require('express');
const mongoose = require('mongoose');
const router = express.Router();

/**
 * @route   GET /health/live
 * @desc    Liveness probe
 * @access  Public
 */
router.get('/live', (req, res) => {
    res.status(200).json({ status: 'UP' });
});

/**
 * @route   GET /health/ready
 * @desc    Readiness probe
 * @access  Public
 */
router.get('/ready', (req, res) => {
    const dbState = mongoose.connection.readyState;
    // 0: disconnected, 1: connected, 2: connecting, 3: disconnecting

    if (dbState === 1) {
        res.status(200).json({ status: 'UP', database: 'connected' });
    } else {
        res.status(503).json({ status: 'DOWN', database: 'disconnected' });
    }
});

/**
 * @route   GET /health/startup
 * @desc    Startup probe
 * @access  Public
 */
router.get('/startup', (req, res) => {
    res.status(200).json({ status: 'UP' });
});

module.exports = router;
