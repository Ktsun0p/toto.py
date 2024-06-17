const Discord = require("discord.js");
const scheme = require("../schemas/settings-schema");
module.exports = {
    name: 'loop',
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
    
           const pp = await scheme.findOne({server_id:interaction.guildId.toString()})
           const role = pp.music_settings.role;
           if(role !== undefined && interaction.guild.roles.cache.get(role)){
            if(!interaction.member.roles.cache.get(role) && !interaction.memberPermissions.has("Administrator")) return interaction.reply({embeds:[new Discord.EmbedBuilder()
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
 
         if(!queue){
          return interaction.reply({embeds:[new Discord.EmbedBuilder()
         .setColor('Red')
         .setAuthor({name:"There's no songs in the queue.",iconURL:client.user.displayAvatarURL()})
         
        
         ]})
        }

   
  let mode = null
  let textt = null;
    switch (args._hoistedOptions[0].value) {
      case 'off':
        mode = 0
        textt = "Off."
        break
      case 'song':
        mode = 1
        textt = "Song."
        break
      case 'queue':
        mode = 2
        textt = "Queue."
        break
    }
    mode = queue.setRepeatMode(mode)
    return interaction.reply({embeds:[new Discord.EmbedBuilder()
      .setColor("Green")
      .setAuthor({name:`Loop: ${textt}`,iconURL:client.user.displayAvatarURL()}) 
    ]})
  }
  };