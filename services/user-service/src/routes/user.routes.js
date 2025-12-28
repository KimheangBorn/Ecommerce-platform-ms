const express = require('express');
const {
    getUsers,
    getUser,
    updateDetails,
    deleteUser
} = require('../controllers/user.controller');

const User = require('../models/User');
const { protect, authorize } = require('../middleware/auth.middleware');

const router = express.Router();

// Protect all routes
router.use(protect);

router.put('/updatedetails', updateDetails);

// Admin only routes
router.use(authorize('admin'));

router.route('/')
    .get(getUsers);

router.route('/:id')
    .get(getUser)
    .delete(deleteUser);

module.exports = router;
