const fs = require("fs");
const Discord = require("discord.js");
/**
 * 
 * @param {Discord.Client} client 
 * @param {Discord} Discord 
 */
module.exports = async(client,Discord)=>{
    const scommands = new Discord.Collection();
    const commands = fs.readdirSync("./commands").filter(file => file.endsWith(".js"));
    for (const file of commands){
    const command = require(`./commands/${file}`);
    scommands.set(command.name,command)
    }

    client.on("interactionCreate", async (interaction) =>{
        if(!interaction.isCommand()) return;
        const {commandName, options} = interaction;
        const cmd = await scommands.get(commandName.toLocaleLowerCase());
        try{
            await cmd.execute(client,interaction,options)
        }catch(e){
            console.log(e)
        }
        
      })

}
