const mongoose = require('mongoose');

const serverSchema = new mongoose.Schema({
    server_id: { type: String, required: true },
    music_settings: {
        channel: { type: String },
        role: { type: String }
    }
},{versionKey:false});

const ServerModel = mongoose.model('Server', serverSchema);

module.exports = ServerModel;
