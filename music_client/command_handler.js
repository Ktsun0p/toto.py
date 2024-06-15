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
        await cmd.execute(client,interaction,options)
 
      if(!cmd){
         return interaction.reply({
              embeds:[
                  new Discord.EmbedBuilder()
                  .setColor(0x39987c)
                  .setDescription(`**Something went wrong while executing this command.**`)
              ]
          })
      }
      
        
      })

}
