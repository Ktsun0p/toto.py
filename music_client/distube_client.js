const { default: SpotifyPlugin } = require("@distube/spotify");
const { default: SoundCloudPlugin } = require("@distube/soundcloud");
const { YouTubePlugin } = require("@distube/youtube")
const {YtDlpPlugin} = require('@distube/yt-dlp')
const {DisTube} = require("distube");
const {DirectLinkPlugin} = require('@distube/direct-link')
const Discord = require("discord.js");
const scheme = require('./schemas/settings-schema');
const dotenv = require('dotenv')
dotenv.config({path:'../.env'})
const CLIENTID = process.env.CLIENTID
const CLIENTSECRET = process.env.CLIENTSECRET
/**
 * 
 * @param {Discord.Client} client 
 */
module.exports = async(client)=>{
    
    client.distube =  new DisTube(client,{
        emitNewSongOnly:false,
        savePreviousSongs:true,
        emitAddListWhenCreatingQueue:true,
        emitAddSongWhenCreatingQueue:false,
        nsfw:true,
        plugins:[
          new YouTubePlugin(),
          new SpotifyPlugin({
            api:{
              clientId:CLIENTID,
              clientSecret:CLIENTSECRET
              }
          }),
         new SoundCloudPlugin(),
         new DirectLinkPlugin(),
         new YtDlpPlugin({update:true}),
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
        console.log(error)
      const server = await scheme.findOne({server_id:channel});
      
      let textChannel = channel;
      if(server.music_settings.channel) textChannel = await client.channels.cache.get(`${server.music_settings.channel}`);
      if(!textChannel) textChannel = queue.textChannel;

      return await textChannel.send(`An error has ocurred => \`\`${error}\`\``).catch(err => {});
    })
    // .on('ffmpegDebug', f=>{
    //   console.log(f)
    // })
}