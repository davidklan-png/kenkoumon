const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Explicitly set the project root
config.projectRoot = __dirname;

// Ensure watch folders include only the mobile directory
config.watchFolders = [__dirname];

module.exports = config;
