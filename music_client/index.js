const discord = require('discord.js')
const {GatewayIntentBits} = require("discord.js")
const mongoose = require('mongoose')
const dotenv = require('dotenv')
dotenv.config({path:'../.env'})
const distube_client = require("./distube_client")
const token = process.env.TOKEN
const command_handler = require('./command_handler')
const client = new discord.Client({intents:[GatewayIntentBits.Guilds,GatewayIntentBits.GuildVoiceStates]})

client.on('ready', async ()=>{
    await mongoose.connect('mongodb://localhost:27017/TotoBot').then(console.log("Connected to DB"))
    let commands = client.application?.commands
    await create_commands(commands)
    try {
        distube_client(client)
        command_handler(client, discord)
    } catch (error) {
        console.log(error)
    }
    console.log(`Successfully logged in as ${client.user?.tag}\n In ${client.guilds.cache.size} servers.`)
})

async function create_commands(commands){
    const play_command = new discord.SlashCommandBuilder()
    .setName('play')
    .setDescription('🎵 play a song in your voice chat!')
    .addStringOption((option)=>option
    .setName("song")
    .setDescription('The song title.')
    .setRequired(true)
    )
    const skip_command = new discord.SlashCommandBuilder()
    .setName('skip')
    .setDescription('🎵 skip the current song.')

    const stop_command = new discord.SlashCommandBuilder()
    .setName('stop')
    .setDescription('🎵 stop the music.')

    const queue_command = new discord.SlashCommandBuilder()
    .setName('queue')
    .setDescription('🎵 get the music queue.')

    const clear_command = new discord.SlashCommandBuilder()
    .setName('clear')
    .setDescription('🎵 clears the queue.')

    const loop_command = new discord.SlashCommandBuilder()
    .setName('loop')
    .setDescription('🎵 Toggle loop.')
    .addStringOption((option)=>option
    .setName('type')
    .setDescription('The loop type.')
    .setRequired(true)
    .addChoices(
        {name:'Song',value:'song'},
        {name:'Queue', value:'queue'},
        {name:'Off',value:'off'}
    )
    )

    const autoplay_command = new discord.SlashCommandBuilder()
    .setName('autoplay')
    .setDescription('🎵 Toggle autoplay.')

    const shuffle_command = new discord.SlashCommandBuilder()
    .setName('shuffle')
    .setDescription('🎵 shuffle the music queue.')

    const remove_command = new discord.SlashCommandBuilder()
    .setName('remove')
    .setDescription('🎵 remove a specific song in the queue.')
    .addIntegerOption((option)=>option
    .setName("position")
    .setDescription("The song position")
    .setRequired(true)
    )

    const jump_command = new discord.SlashCommandBuilder()
    .setName('jump')
    .setDescription('🎵 jump to a specific song in the queue.')
    .addIntegerOption((option)=>option
    .setName("position")
    .setDescription("The song position")
    .setRequired(true)
    )
    cmds = [
        play_command,
        skip_command,
        queue_command,
        loop_command,
        jump_command,
        autoplay_command,
        shuffle_command,
        remove_command,
        clear_command,
        stop_command
    ]
    for (let index = 0; index < cmds.length; index++) {
        const command = cmds[index];
        await commands.create(command.toJSON())
    }
}
client.login(token)