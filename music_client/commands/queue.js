const Discord = require("discord.js");

module.exports = {
    name: 'queue',
    description:'ping command',
    /**
     * 
     * @param {Discord.Client} client 
     * @param {*} interaction 
     * @param {*} args 
     * @returns 
     */
      execute: async(client,interaction,args)=>{
        const channel = (await interaction.guild.members.fetch(interaction.member.id)).voice;
           const queue = client.distube.getQueue(interaction);
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

        var listqueue = [];
        var maxsongs = 10;

        for(let i = 0; i < queue.songs.length; i+=maxsongs){
          var songs = queue.songs.slice(i,i + maxsongs);
          listqueue.push(songs.map((song,index) => `**\`${i+ ++index}\`** - [\`${song.name}\`](${song.url})`).join("\n "))
        }       

        var limit = listqueue.length;
        var embeds = [];
        
         for(let i = 0; i< limit; i++){
           let desc = String(listqueue[i]).substring(0,2048);
           const status = queue =>
           `Volume: \`${queue.volume}%\` | Loop: \`${
             queue.repeatMode ? (queue.repeatMode === 2 ? 'Queue' : 'This song') : 'Off'
           }\` | Autoplay: \`${queue.autoplay ? 'On' : 'Off'}\``
           let embed = new Discord.EmbedBuilder()
           .setTitle(`🎶 ${interaction.member.guild.name}'s queue - \`[${queue.songs.length} ${queue.songs.length > 1 ? "Songs": "Songs"}]\``)
           .addFields({name:"Options", value:`${status(queue)}`})
           .setColor('Yellow')
           .setDescription(desc)
           
             if(queue.songs.length > 1) embed.addFields({name:`🔉 Now playing`,value:`[\`${queue.songs[0].name}\`](${queue.songs[0].url}) **${queue.songs[0].formattedDuration}**`}).setThumbnail(queue.songs[0].thumbnail)
               await embeds.push(embed)
         }
        pagination()
         async function pagination(){
           let actualPage = 0;
           if(embeds.length === 1) return interaction.reply({embeds:[embeds[0]]});

           let button_back = new Discord.ButtonBuilder().setStyle("Success").setCustomId("back").setEmoji("⬅").setLabel("Back")
           let button_home = new Discord.ButtonBuilder().setStyle("Success").setCustomId("home").setEmoji("🏠").setLabel("Home")
           let button_next = new Discord.ButtonBuilder().setStyle("Success").setCustomId("next").setEmoji("➡").setLabel("Next")
           let embedpages = await interaction.reply({
            embeds:[embeds[0].setFooter({text:`Page ${actualPage+1}/${embeds.length}`})],
            components: [new Discord.ActionRowBuilder().addComponents([button_back,button_home,button_next])]
           })
 
            const rrr = await interaction.fetchReply();
           const collector = rrr.createMessageComponentCollector({filter: i => i?.isButton() && i?.user && i?.user.id == interaction.user.id && i?.message.author.id == client.user.id,time:30000});
           
           collector.on("collect",async b =>{
   
             if(b?.user.id !== interaction.user.id) return;

             switch(b?.customId){
               case "back":{
                 collector.resetTimer();
                 if(actualPage !== 0){
                   actualPage -= 1;
                   
                   await interaction.editReply({embeds:[embeds[actualPage].setFooter({text:`Page ${actualPage+1}/${embeds.length}`})],components:[rrr.components[0]]}).catch(() =>{});
                    await b?.deferUpdate();

                 }else{
                  actualPage = embeds.length - 1;
                   
                  await interaction.editReply({embeds:[embeds[actualPage].setFooter({text:`Page ${actualPage+1}/${embeds.length}`})],components:[rrr.components[0]]}).catch(() =>{});
                   await b?.deferUpdate();

                 }
               }
               break;
                case "home":{

                  collector.resetTimer();

                  actualPage = 0;

                   
                  await interaction.editReply({embeds:[embeds[actualPage].setFooter({text:`Page ${actualPage+1}/${embeds.length}`})],components:[rrr.components[0]]}).catch(() =>{});
                   await b?.deferUpdate();
                }
                break;
                case "next":{

                  collector.resetTimer();
                             
                    if(actualPage < embeds.length -1){
                      actualPage++
                      await interaction.editReply({embeds:[embeds[actualPage].setFooter({text:`Page ${actualPage+1}/${embeds.length}`})],components:[rrr.components[0]]}).catch(() =>{});
                   await b?.deferUpdate();
                    }else{
                       actualPage = 0;

                       await interaction.editReply({embeds:[embeds[actualPage].setFooter({text:`Page ${actualPage+1}/${embeds.length}`})],components:[rrr.components[0]]}).catch(() =>{});
                   await b?.deferUpdate();
                    }
                }
                break;
               default:
               break;
             }
           });
           collector.on("end",async i=>{
            let button_back = new Discord.ButtonBuilder().setStyle("Success").setCustomId("back").setEmoji("⬅").setLabel("Back").setDisabled(true)
            let button_home = new Discord.ButtonBuilder().setStyle("Success").setCustomId("home").setEmoji("🏠").setLabel("Home").setDisabled(true)
            let button_next = new Discord.ButtonBuilder().setStyle("Success").setCustomId("next").setEmoji("➡").setLabel("Next").setDisabled(true)
            
            await interaction.editReply({components:[new Discord.ActionRowBuilder().addComponents([button_back,button_home,button_next])]})
           })
         }

  
    
    }
  };