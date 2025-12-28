const User = require('../models/User');

// Business logic for user data (currently most logic is simple enough for controller)
// But keeping this layer for future expansion (e.g. updating profile logic)

const getUserById = async (id) => {
    return await User.findById(id);
};

const updateUser = async (id, data) => {
    // Prevent updating password through this method
    delete data.password;
    delete data.role; // Prevent role escalation via update

    const user = await User.findByIdAndUpdate(id, data, {
        new: true,
        runValidators: true
    });

    return user;
};

module.exports = {
    getUserById,
    updateUser
};
