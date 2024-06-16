const Discord = require("discord.js");
const scheme = require("../schemas/settings-schema");
module.exports = {
    name: 'play',
    /**
     * 
     * @param {Discord.Client} client 
     * @param {Discord.Interaction} interaction 
     * @param {*} args 
     * @returns 
     */
      execute: async(client,interaction,options)=>{
        const channel = (await interaction.guild.members.fetch(interaction.member.id)).voice;
           const song = options._hoistedOptions[0].value;
         const me = (await interaction.guild.members.fetchMe());
         
         const pp = await scheme.findOne({server_id:interaction.guildId})
         const role = pp.music_settings.role;
         if(role !== undefined && interaction.guild.roles.cache.get(String(role))){
          if(!interaction.member.roles.cache.get(String(role)) && !interaction.memberPermissions.has("Administrator")) return interaction.reply({embeds:[new Discord.EmbedBuilder()
            .setColor(Discord.Colors.DarkRed)
            .setAuthor({name:`Missing Permissions!.`,iconURL:client.user.displayAvatarURL()})
            .setDescription(`You must have <@&${role}> role to use music commands.`)
            ],ephemeral:true})
         }
      
        if(!channel.channel) return interaction.reply({embeds:[new Discord.EmbedBuilder()
        .setColor(Discord.Colors.DarkRed)
        .setAuthor({name:"You must be in a voice channel before using this command.",iconURL:client.user.displayAvatarURL()})
        ],ephemeral:true})
        if(me.voice?.channelId && channel.channelId !== me.voice.channelId) return interaction.reply({embeds:[new Discord.EmbedBuilder()
          .setColor(Discord.Colors.DarkRed)
          .setAuthor({name:"You must be in the same voice channel as me.",iconURL:client.user.displayAvatarURL()})
          ],ephemeral:true})
         const chh = client.guilds.cache.get(interaction.guildId)

        const msg = chh.channels.cache.get(interaction.channelId)

        const songemb = new Discord.EmbedBuilder()
        .setAuthor({name:`🎧 Searching song "${song}"...`,iconURL:client.user.displayAvatarURL()})
        .setColor(Discord.Colors.Green)
        await interaction.reply({embeds:[songemb]}).catch(err => {});


        try {
            await  client.distube.play(channel.channel,song,{
            member:interaction.member,
            textChannel:msg,
            })
        
            const qq = await client.distube.getQueue(interaction);


            const server = await scheme.findOne({server_id:interaction.guildId});

            let textChannel = qq.textChannel;
            if(server.music_settings.channel) textChannel = await client.channels.cache.get(`${server.music_settings.channel}`)
            if(!textChannel) textChannel = interaction.channel;
            if(textChannel)
            await interaction.editReply({embeds:[songemb.setDescription(`**--> ${textChannel}**`)]}).catch(err => {});

            setTimeout(async ()=>{
            await interaction.deleteReply().catch(err =>{});
            },15000)
        }  catch (error) {
            console.log(error)
            songemb
            .setAuthor({name:`⚠️Play Error`,iconURL:client.user.displayAvatarURL()})
            .setColor(Discord.Colors.DarkRed)
            .setFooter({text:"This is not an error? please report it to our support server --> https://kats.uno/totobot/support"})
            let errorCode;

            if(error.errorCode) errorCode = error.errorCode

            else if(error.code) errorCode = error.code

            else{
                return  await interaction.editReply({embeds:[songemb.setDescription(`\`\`\`${error}\`\`\``)]}).catch(err => {});
            }

            switch(errorCode){
                case 'NOT_SUPPORTED_URL':
                errorCode = "This URL is not supported."
                break;
                case 'VOICE_FULL':
                errorCode = "The voice channel is full."
                break;
                case 'ERR_INVALID_URL':
                errorCode = "Invalid URL"
                break;
                case 'VOICE_MISSING_PERMS':
                errorCode = "I don't have permission to join this voice channel"
                break;
                case 'VOICE_CONNECT_FAILED':
                errorCode = "Cannot connect to the voice channel after 30 seconds"
                break;
                case 'NO_RESULT':
                errorCode = "No result found"
                break;
                case 'SPOTIFY_PLUGIN_API_ERROR':
                errorCode = "SPOTIFY_PLUGIN_API not found"
                break;
                case 'SPOTIFY_PLUGIN_NO_RESULT':
                errorCode = "Cannot find this song on YouTube"
                break;
            }
        
            await interaction.editReply({embeds:[songemb.setDescription(`\`\`\`${errorCode}\`\`\``)]}).catch(err => {});
        }      
    }
  };