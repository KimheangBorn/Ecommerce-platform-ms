const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const logger = require('./utils/logger');
const { errorHandler } = require('./middleware/error.middleware');

// Route files
const authRoutes = require('./routes/auth.routes');
const userRoutes = require('./routes/user.routes');
const healthRoutes = require('./routes/health.routes');

const app = express();

// Body parser
app.use(express.json());

// Security headers
app.use(helmet());

// Enable CORS
app.use(cors());

// Mount routers
app.use('/api/users', authRoutes);
app.use('/api/users', userRoutes);
app.use('/health', healthRoutes);

// Error Handler
app.use(errorHandler);

module.exports = app;
