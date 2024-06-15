const { default: SpotifyPlugin } = require("@distube/spotify");
const { default: SoundCloudPlugin } = require("@distube/soundcloud");
const {DisTube} = require("distube");
const Discord = require("discord.js");
const scheme = require('./schemas/settings-schema');
/**
 * 
 * @param {Discord.Client} client 
 */
module.exports = async(client)=>{
    
    client.distube =  new DisTube(client,{
        emitNewSongOnly:false,
        savePreviousSongs:true,
        emitAddListWhenCreatingQueue:true,
        nsfw:true,
       plugins:[
         new SpotifyPlugin({
           api:{
            clientId:"65948cf6d552454790a615c1320bb7ae",
            clientSecret:"2f4566def0be4a6684e4d8ecde25837f"
           }
         }),
         new SoundCloudPlugin()
       ]
      })

     
      const status = queue =>
      `Volume: \`${queue.volume}%\` | Loop: \`${
        queue.repeatMode ? (queue.repeatMode === 2 ? 'Queue' : 'This song') : 'Off'
      }\` | Autoplay: \`${queue.autoplay ? 'On' : 'Off'}\``
    
    client.distube.on("playSong",async(queue ,song )=>{
      const server = await scheme.findOne({server_id:queue.id});
      
      let textChannel = queue.textChannel;
      if(server.music_settings.channel) textChannel = await client.channels.cache.get(`${server.music_settings.channel}`);
      if(!textChannel) textChannel = queue.textChannel;
    
      
      const embed = new Discord.EmbedBuilder()
      .setColor(0xc7ffea)
      .setAuthor({name:"🎧 Now playing...",iconURL:client.user.avatarURL()})
       .setTitle(song.name)
       .setURL(song.url)
       .setDescription(`Duration:** ${song.formattedDuration}**\n${status(queue)}`)
       .setFooter({text:`${song.user.tag}`,iconURL:song.user.displayAvatarURL({dynamic:true})})
      .setThumbnail(song.thumbnail)
    
      return await textChannel.send({embeds:[embed]}).catch(err => {});
    })
    
    .on("addSong",async (queue,song)=>{
      const server = await scheme.findOne({server_id:queue.id});
      
      let textChannel = queue.textChannel;
      if(server.music_settings.channel) textChannel = await client.channels.cache.get(`${server.music_settings.channel}`);
      if(!textChannel) textChannel = queue.textChannel;

      const embed = new Discord.EmbedBuilder()
      .setColor(0xc7ffea)
      .setAuthor({name:"🎶 Added...",iconURL:client.user.avatarURL()})
       .setTitle(song.name)
       .setURL(song.url)
       .setDescription(`Duration:** ${song.formattedDuration}**\n${status(queue)}`)
       .setFooter({text:`@${song.user.tag}`,iconURL:song.user.displayAvatarURL({dynamic:true})})
       .setTimestamp()
      .setThumbnail(song.thumbnail)
     
      return await textChannel.send({embeds:[embed]}).catch(err => {});
    })
    .on("addList",async (queue,playList) =>{
      const server = await scheme.findOne({server_id:queue.id});
      
      let textChannel = queue.textChannel;
      if(server.music_settings.channel) textChannel = await client.channels.cache.get(`${server.music_settings.channel}`);
      if(!textChannel) textChannel = queue.textChannel;
/// fix  ${playList.songs.length} song(s). ${playList.formattedDuration}.
      const embed = new Discord.EmbedBuilder()
      .setColor(0xc7ffea)
      .setAuthor({name:`🎶 Added "${playList.name}"`,iconURL:client.user.avatarURL(),url:playList.url})
      .setThumbnail(playList.thumbnail)
      .setDescription(`||${playList.url}||`)
      .setFooter({text:`${playList.user.tag}`,iconURL:playList.user.displayAvatarURL({dynamic:true})})
       .setTimestamp()
      return await textChannel.send({embeds:[embed]}).catch(err => {});
    })
    .on("initQueue",async (queue) =>{
      queue.volume = 100;
    })
    .on("finish", async queue =>{})
    .on("error",async (channel,error) =>{
        console.log(channel)
      const server = await scheme.findOne({server_id:channel});
      
      let textChannel = channel;
      if(server.music_settings.channel) textChannel = await client.channels.cache.get(`${server.music_settings.channel}`);
      if(!textChannel) textChannel = queue.textChannel;

      return await textChannel.send(`An error has ocurred => \`\`${error}\`\``).catch(err => {});
    });
}