const mongoose = require("mongoose");


const schema = new mongoose.Schema({
    server_id:{type:Number,required:true},
    music_settings:{
       channel:{type:String},
       role:{type:String}
    }
})
module.exports = mongoose.model("servers",schema);