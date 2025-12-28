const User = require('../models/User');
const { generateToken, generateRefreshToken } = require('../services/auth.service');
const redisClient = require('../utils/redis');
const logger = require('../utils/logger');
const jwt = require('jsonwebtoken');

/**
 * @desc    Register user
 * @route   POST /api/users/register
 * @access  Public
 */
exports.register = async (req, res) => {
    try {
        const { name, email, password, role } = req.body;

        // Check if user exists
        const userExists = await User.findOne({ email });
        if (userExists) {
            return res.status(400).json({ success: false, error: 'User already exists' });
        }

        // Create user
        const user = await User.create({
            name,
            email,
            password,
            role
        });

        sendTokenResponse(user, 201, res);
    } catch (error) {
        logger.error(error);
        res.status(500).json({ success: false, error: error.message });
    }
};

/**
 * @desc    Login user
 * @route   POST /api/users/login
 * @access  Public
 */
exports.login = async (req, res) => {
    try {
        const { email, password } = req.body;

        // Validate email & password
        if (!email || !password) {
            return res.status(400).json({ success: false, error: 'Please provide an email and password' });
        }

        // Check for user
        const user = await User.findOne({ email }).select('+password');
        if (!user) {
            return res.status(401).json({ success: false, error: 'Invalid credentials' });
        }

        // Check if password matches
        const isMatch = await user.matchPassword(password);
        if (!isMatch) {
            return res.status(401).json({ success: false, error: 'Invalid credentials' });
        }

        sendTokenResponse(user, 200, res);
    } catch (error) {
        logger.error(error);
        res.status(500).json({ success: false, error: error.message });
    }
};

/**
 * @desc    Get current logged in user
 * @route   GET /api/users/me
 * @access  Private
 */
exports.getMe = async (req, res) => {
    try {
        const user = await User.findById(req.user.id);
        res.status(200).json({ success: true, data: user });
    } catch (error) {
        logger.error(error);
        res.status(500).json({ success: false, error: error.message });
    }
};

/**
 * @desc    Log user out / Clear cookie
 * @route   POST /api/users/logout
 * @access  Private
 */
exports.logout = async (req, res) => {
    try {
        if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
            const token = req.headers.authorization.split(' ')[1];

            // Blacklist token for duration of its validity (15m usually, setting to 1h to be safe)
            // or decode it to get exact expiry
            const decoded = jwt.decode(token);
            let ttl = 3600; // default 1h
            if (decoded && decoded.exp) {
                ttl = decoded.exp - Math.floor(Date.now() / 1000);
            }

            if (ttl > 0) {
                await redisClient.setEx(`blacklist:${token}`, ttl, 'true');
            }
        }

        res.status(200).json({ success: true, data: {} });
    } catch (error) {
        logger.error(error);
        res.status(500).json({ success: false, error: error.message });
    }
};

/**
 * @desc    Refresh Token
 * @route   POST /api/users/refresh
 * @access  Public
 */
exports.refreshToken = async (req, res) => {
    const { refreshToken } = req.body;

    if (!refreshToken) {
        return res.status(400).json({ success: false, error: 'Refresh token required' });
    }

    try {
        const decoded = jwt.verify(refreshToken, process.env.JWT_SECRET);
        const user = await User.findById(decoded.id);

        if (!user) {
            return res.status(404).json({ success: false, error: 'User not found' });
        }

        const accessToken = generateToken(user._id, user.role);

        res.status(200).json({
            success: true,
            accessToken
        });
    } catch (error) {
        return res.status(401).json({ success: false, error: 'Invalid refresh token' });
    }
};

// Helper function to send token
const sendTokenResponse = (user, statusCode, res) => {
    const accessToken = generateToken(user._id, user.role);
    const refreshToken = generateRefreshToken(user._id);

    res.status(statusCode).json({
        success: true,
        user: {
            id: user._id,
            name: user.name,
            email: user.email,
            role: user.role
        },
        accessToken,
        refreshToken
    });
};
