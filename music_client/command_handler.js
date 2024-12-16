const fs = require("fs");
const Discord = require("discord.js");
const dotenv = require('dotenv');
dotenv.config({path:'../.env'});

const en_channel_id = process.env.EN_COMMAND_CHANNEL;
const es_channel_id = process.env.ES_COMMAND_CHANNEL;
/**
 * 
 * @param {Discord.Client} client 
 * @param {Discord} Discord
 */
module.exports = async(client,Discord)=>{

    const en_channel = client.channels.cache.get(en_channel_id.toString());
    const es_channel = client.channels.cache.get(es_channel_id.toString());

    const embed = new Discord.EmbedBuilder({color:Discord.Colors.Yellow});

    const scommands = new Discord.Collection();
    const commands = fs.readdirSync("./commands").filter(file => file.endsWith(".js"));
    for (const file of commands){
    const command = require(`./commands/${file}`);
    scommands.set(command.name,command);
    }

    client.on("interactionCreate", async (interaction) =>{
        if(!interaction.isCommand()) return;
        const {commandName, options} = interaction;
        const cmd = await scommands.get(commandName.toLocaleLowerCase());

        try{
            await cmd.execute(client,interaction,options);
            await es_channel.send({embeds:[embed.setAuthor({name:`Comando \`/${commandName}\` ejecutado correctamente.`,iconURL:client.user.avatarURL()})]})
            await en_channel.send({embeds:[embed.setAuthor({name:`Successfully executed command \`/${commandName}\`.`,iconURL:client.user.avatarURL()})]})
        }catch(e){
            console.log('Error: '+e);
        }
        
      })

}
