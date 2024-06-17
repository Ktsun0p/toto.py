const schema = require('./schemas/settings-schema');

module.exports = async (client,discord,id) =>{
    
   const server = await schema.findOne({
        server_id: String(id)
    })
    if(server) return;
    else{
        await schema.findOneAndUpdate({
            server_id: id
        },{
            music_settings:{
                channel:'None',
                role:'None'
             }
        },{upsert:true,new:true}).then(console.log("Successfully created settings-schema"))
        
    }

    }