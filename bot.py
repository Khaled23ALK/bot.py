import discord
from discord.ext import commands
import logging

# إعداد التسجيل في الملف لتوثيق الحوادث
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# حدث عندما يتم حذف قناة
@bot.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    logging.info(f"تم حذف القناة {channel.name} في السيرفر {guild.name}")
    
    # إرسال تنبيه للمشرفين
    admin_channel = discord.utils.get(guild.text_channels, name='general')  # تأكد من وجود قناة للتنبيه
    if admin_channel:
        await admin_channel.send(f"تم حذف القناة {channel.name} في السيرفر!")
    
    # محاولة استعادة القناة المحذوفة
    await guild.create_text_channel(channel.name)  # إذا كانت القناة نصية، يمكن تعديلها حسب الحاجة

# حدث عندما يتم حذف دور
@bot.event
async def on_guild_role_delete(role):
    guild = role.guild
    logging.info(f"تم حذف الدور {role.name} في السيرفر {guild.name}")
    
    # إرسال تنبيه للمشرفين
    admin_channel = discord.utils.get(guild.text_channels, name='general')  # تأكد من وجود قناة للتنبيه
    if admin_channel:
        await admin_channel.send(f"تم حذف الدور {role.name} في السيرفر!")
    
    # محاولة استعادة الدور المحذوف
    try:
        await guild.create_role(name=role.name)
    except discord.Forbidden:
        logging.error("البوت ليس لديه صلاحية لإنشاء الأدوار!")

# حدث عندما يتم تعديل أي شيء في السيرفر (مثلاً تغيير صلاحيات القنوات)
@bot.event
async def on_guild_channel_update(before, after):
    # إذا تم تعديل القناة بطريقة غير مرغوب فيها
    if before.name != after.name:  # على سبيل المثال إذا تم تغيير اسم القناة
        logging.info(f"تم تغيير اسم القناة من {before.name} إلى {after.name}")
        admin_channel = discord.utils.get(after.guild.text_channels, name='general')
        if admin_channel:
            await admin_channel.send(f"تم تغيير اسم القناة من {before.name} إلى {after.name}")

# تشغيل البوت
@bot.event
async def on_ready():
    print(f'البوت {bot.user} جاهز للعمل!')

bot.run("توكن_البوت_هنا")
