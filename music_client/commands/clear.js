const Discord = require("discord.js");
const scheme = require("../schemas/settings-schema");

module.exports = {
    name: 'clear',
    description:'ping command',
    /**
     * 
     * @param {Discord.Client} client 
     * @param {*} interaction 
     * @param {*} args 
     * @returns 
     */
      execute: async(client,interaction,args)=>{
  
           const queue = client.distube.getQueue(interaction);
           const channel = (await interaction.guild.members.fetch(interaction.member.id)).voice;
     
           const pp = await scheme.findOne({server_id:interaction.guildId})
           const role = pp.music_settings.role;
           if(role !== undefined && interaction.guild.roles.cache.get(String(role))){
            if(!interaction.member.roles.cache.get(String(role)) && !interaction.memberPermissions.has("Administrator")) return interaction.reply({embeds:[new Discord.EmbedBuilder()
              .setColor('Red')
              .setAuthor({name:`Missing Permissions!.`,iconURL:client.user.displayAvatarURL()})
              .setDescription(`You must have <@&${role}> role to use music commands.`)
              ],ephemeral:true})
           }
        

         const me = (await interaction.guild.members.fetchMe());
        if(!channel.channel) return interaction.reply({embeds:[new Discord.EmbedBuilder()
        .setColor('Red')
        .setAuthor({name:"You must be in a voice channel before using this command.",iconURL:client.user.displayAvatarURL()})
        ],ephemeral:true})
        if(me.voice?.channelId && channel.channelId !== me.voice.channelId) return interaction.reply({embeds:[new Discord.EmbedBuilder()
          .setColor('Red')
          .setAuthor({name:"You must be in the same voice channel as me.",iconURL:client.user.displayAvatarURL()})
          ],ephemeral:true})
          
         const chh = client.guilds.cache.get(interaction.guildId)
         if(!queue){
          return interaction.reply({embeds:[new Discord.EmbedBuilder()
         .setColor('Red')
         .setAuthor({name:"There's no songs in the queue.",iconURL:client.user.displayAvatarURL()})
         
        
         ]})
        }
     await queue.stop();
   
    return interaction.reply({embeds:[new Discord.EmbedBuilder()
      .setColor("Green")
      .setAuthor({name:`Queue cleared. ✅`,iconURL:client.user.displayAvatarURL()}) 
    ]})
  }
  };