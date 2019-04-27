# -------------------------------------------------------------------------------------------------------------------
import sys
import string,random
import math
import psycopg2
import os

from datetime import datetime
from collections import defaultdict

try:
    import discord
    from discord.ext.commands import Bot
except ImportError:
    print("Discord.py がインストールされていません。\nDiscord.pyをインストールしてください。")
    sys.exit(1)
# -------------------------------------------------------------------------------------------------------------------
client = Bot(command_prefix='&',pm_help=True)
all_member = "571660891888680960"
get_user = "571660916584611840"
get_bot = "571660925401301002"
count = 0
counts = 0
number = 0
left = '⏪'
right = '⏩'


def predicate(message,l,r):
    def check(reaction,user):
        if reaction.message.id != message.id or user == client.user:
            return False
        if l and reaction.emoji == left:
            return True
        if r and reaction.emoji == right:
            return True
        return False

    return check


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="<help | ver:1.0.0"))


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    if not member.server.id == "571513405920510004":
        return
    await client.edit_channel(client.get_channel(all_member),
                              name="MEMBER COUNT :{}".format(len(member.server.members)))
    await client.edit_channel(client.get_channel(get_user),name="USER COUNT : {}".format(
        len([member for member in member.server.members if not member.bot])))
    await client.edit_channel(client.get_channel(get_bot),
                              name="BOT COUNT : {}".format(
                                  len([member for member in member.server.members if member.bot])))


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_remove(member):
    if not member.server.id == "571513405920510004":
        return
    await client.edit_channel(client.get_channel(all_member),
                              name="MEMBER COUNT :{}".format(len(member.server.members)))
    await client.edit_channel(client.get_channel(get_user),name="USER COUNT : {}".format(
        len([member for member in member.server.members if not member.bot])))
    await client.edit_channel(client.get_channel(get_bot),
                              name="BOT COUNT : {}".format(
                                  len([member for member in member.server.members if member.bot])))


@client.event
async def on_message(message):
    if datetime.now().strftime("%H:%M:%S") == datetime.now().strftime(
            "12:00:00") or message.content == ">update-message":
        if message.author.server_permissions.administrator:
            if not message.server.id == "571513405920510004":
                return
            await client.delete_message(message)
            counter = 0
            all_message = "571660933915607040"
            channel_name = client.get_channel(all_message)
            for i in message.server.channels:
                async for log in client.logs_from(i,limit=99999999999):
                    if log.server.id == message.server.id:
                        counter += 1
            await client.edit_channel(channel_name,name="MESSAGE COUNT : {}".format(counter))
            return
    help_message = ["""
            -------------------------------
            This BOT was produced by Mr.𝗠𝗞𝗠𝗞𝟭𝟭𝟬𝟭™#3577
            And Code was written by Mr.The.First.Step#3454.
            If you has question. please ask to Mr.The.First.Step#3454 in DM.

            -------------------------------
            BOT ULR[HERE](<https://discordapp.com/api/oauth2/authorize?client_id=455685397817589770&permissions=268504241&scope=bot>)
            BOT Code[HERE](<https://github.com/Anijaaa/Question/blob/master/question.py>)
            -------------------------------""",
            """
            Command-List
            It is illustrated Original-ID at `[0iKV5]`.
            Actually real is different so be careful.
            
            -------------------------------
            `<q-c question-content` or `<question-create question-content`
            ↳You can ask a question!!
            ↳Ask what you are concerned about yourself!
            ↳↳[Example:<q-c Why Earth was blue?]

            -------------------------------
            `<question-editing Original-ID question-content`
            ↳When you create question, Original-ID will create!
            ↳Use this command, when you want to change question-content.
            ↳↳[Example:<question-editing 0iKV5 Maybe earth was red!!]
            ※This command can used only yourself question!

            -------------------------------
            `<question-delete Original-ID`
            ↳You can delete input Original-ID question!
            ↳If your question was solution. Use this command!
            ↳↳[Example:<question-delete 0iKV5]
            ※This command can used only yourself question!
            
            -------------------------------
            `<question-list`
            ↳You can view all question until now!
            
            -------------------------------
            `<locate Original-ID`
            ↳You can view input ID questions details.
            ↳You can view at answer content until now too.
            ↳↳[Example:<locate 0iKV5]
            
            -------------------------------""",
            """
            Command-List
            It is illustrated Original-ID at `[0iKV5]`.
            Actually real is different so be careful.
            
            -------------------------------
            `<answer Original-ID answer-content`
            ↳This command can use all people!
            ↳When you want to answer the question.please use this!
            ↳↳[Example:<answer 0iKV5 The earth is not red...]
            
            -------------------------------
            `<best-answer Question-Original-ID`
            ↳This command is Best-answer function!
            ↳Please use this command, when you indebted.
            ↳↳[Example:<best-answer 0iKV5]

            -------------------------------
            `<answer-top`
            ↳Ranking about Best-answer number of times!

            -------------------------------"""]

    if message.content == "<help":
        index = 0
        embed = discord.Embed(
            title="Help-List:",
            description=help_message[index],
            color=discord.Color(0xc088ff),
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        msg = await client.send_message(message.channel,embed=embed)
        while True:
            l = index != 0
            r = index != len(help_message) - 1
            if l:
                await client.add_reaction(msg,left)
            if r:
                await client.add_reaction(msg,right)
            react,user = await client.wait_for_reaction(check=predicate(msg,l,r))
            if react.emoji == left:
                index -= 1
            elif react.emoji == right:
                index += 1
            embed = discord.Embed(
                title="Help-List:",
                description=help_message[index],
                color=discord.Color(0xc088ff),
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )
            await client.edit_message(msg,embed=embed)
            await client.clear_reactions(msg)

    if message.content.startswith("<question-create"):
        def randomname(n):
            a = ''.join(random.choices(string.ascii_letters + string.digits,k=n))
            return a

        numbers = randomname(5)
        content = message.content[17:]
        if content == "":
            embed = discord.Embed(
                description=f"Hey {message.author.mention}!\nPlease input content!",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return
        
        out_words = ["しね","金！暴力！SEX！（迫真）","おっぱい","ちんこ","まんこ","殺す","ちんぽ","おちんちん","アナル","sex","セックス","オナニー","おちんぽ","ちくび",
                     "乳首","陰茎","うざい","黙れ","きもい","やりますねぇ！","覚醒剤","覚せい剤","麻薬","コカイン","SEX","害児","pornhub","xvideo","せっくす",
                     "mother fucker","金正恩","penis","fuck","死ね","殺す","アホ","赤ちゃん製造ミルク","ザー汁","ザーメン","精液","精子","こ↑こ↓",
                     "やりますねぇ"]
        if any([True for s in out_words if s in content]):
            embed = discord.Embed(
                description=f"Hey {message.author.mention}!\nYour question were inputed prohibited term so you can't create this question.",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            await client.delete_message(message)
            return

        ans = db_write(
            str(numbers),
            int(message.author.id),
            str(content)
        )
        if ans == True:
            embed = discord.Embed(
                description=f"{message.author.mention}\n\n`{content}`\n\nOriginal-ID:{numbers}",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="Creation time:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content.startswith("<q-c"):
        def randomname(n):
            a = ''.join(random.choices(string.ascii_letters + string.digits,k=n))
            return a

        numbers = randomname(5)
        content = message.content[5:]
        if content == "":
            embed = discord.Embed(
                description=f"Hey {message.author.mention}!\nPlease input content!",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return
        
        out_words = ["しね","金！暴力！SEX！（迫真）","おっぱい","ちんこ","まんこ","殺す","ちんぽ","おちんちん","アナル","sex","セックス","オナニー","おちんぽ","ちくび",
                     "乳首","陰茎","うざい","黙れ","きもい","やりますねぇ！","覚醒剤","覚せい剤","麻薬","コカイン","SEX","害児","pornhub","xvideo","せっくす",
                     "mother fucker","金正恩","penis","fuck","死ね","殺す","アホ","赤ちゃん製造ミルク","ザー汁","ザーメン","精液","精子","こ↑こ↓",
                     "やりますねぇ"]
        if any([True for s in out_words if s in content]):
            embed = discord.Embed(
                description=f"Hey {message.author.mention}!\nYour question were inputed prohibited term so you can't create this question.",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            await client.delete_message(message)
            return

        ans = db_write(
            str(numbers),
            int(message.author.id),
            str(content)
        )
        if ans == True:
            embed = discord.Embed(
                description=f"{message.author.mention}さん\n\n`{content}`\n\nID:{numbers}",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="Creation time:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content == "<question-list":
        async def message_number(numbers):
            if len(list(db_read())) == 0:
                embed = discord.Embed(
                    title="Question-list until now:",
                    description="No question now",
                    color=discord.Color(0xc088ff),
                )
                await client.send_message(message.channel,embed=embed)
                return
            page = 1
            for row2 in db_read_count():
                join = "".join(numbers[(page - 1) * 5:page * 5])
                embed = discord.Embed(
                    title="Question-List until now:",
                    description=join + f"-------------------------------\n\nTotal number of views:{int(row2[0])} | Total number of answers:{int(row2[1])}",
                    color=discord.Color(0xc088ff),
                )
                embed.set_footer(
                    text=f"You are viwing {page} in {math.ceil(len(numbers) / 5}!"
                )
                msg = await client.send_message(message.channel,embed=embed)
                while True:
                    l = page != 1
                    r = page < len(numbers) / 5
                    if l:
                        await client.add_reaction(msg,left)
                    if r:
                        await client.add_reaction(msg,right)
                    react,user = await client.wait_for_reaction(check=predicate(msg,l,r))
                    if react.emoji == left:
                        page -= 1
                    elif react.emoji == right:
                        page += 1
                    for row2 in db_read_count():
                        join = "".join(numbers[(page - 1) * 5:page * 5])
                        embed = discord.Embed(
                            title="Question-List until now:",
                            description=join + f"-------------------------------\n\nTotal number of views:{int(row2[0])} | Total number of answers:{int(row2[1])}",
                            color=discord.Color(0xc088ff),
                        )
                        embed.set_footer(
                            text=f"You are viwing {page} in {math.ceil(len(numbers) / 5}!"
                        )
                        await client.edit_message(msg,embed=embed)
                        await client.clear_reactions(msg)

        numbers = []
        for row in db_read():
            numbers.append("".join(
                f"""-------------------------------\n<@{row[1]}>'s question!\n\n`{str(row[2])}`\n\nNumber of views：{row[3]}\nNumber of answers：{row[4]}\nOriginal-ID：{str(row[0])}\n\n"""))
        else:
            await message_number(numbers)

    if message.content.startswith("<question-editing"):
        content = message.content[24:]
        for row in list(db_read()):
            if int(row[1]) == int(message.author.id):
                ans = db_access(
                    str(message.content.split()[1]),
                    str(content)
                )
                if str(row[0]) == message.content.split()[1]:
                    if ans == True:
                        embed = discord.Embed(
                            title="QUESTION:",
                            description=f"Original-ID：`{message.content.split()[1]}`\nThis question was created by <@{message.author.id}>\n\n**change content:**\n`{content}`",
                            color=discord.Color(0xc088ff),
                            timestamp=message.timestamp
                        )
                        embed.set_footer(
                            text="Change time:"
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
        else:
            embed = discord.Embed(
                title="",
                description=f"If this command didn't reaction.\nThat means you don't have Authorityto change this Original-ID...",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="Current time:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content.startswith("<locate"):
        async def answer_all(numbers):
            global embeds
            if db_count_up_1(str(message.content.split()[1])):
                for row in list(db_read()):
                    if str(row[0]) == message.content.split()[1]:
                        embed = discord.Embed(
                            title="QUESTION:",
                            description=f"""<@{row[1]}>'s question!\n\n`{str(row[2])}`\n\nNumber of views：{row[3]}\nNumber of answers：{row[4]}\nOriginal-ID：{str(row[0])}\n""",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                for row1 in db_get_answer():
                    page = 1
                    join = "".join(numbers[(page - 1) * 2:page * 2])
                    if str(row1[0]) == message.content.split()[1]:
                        embeds = discord.Embed(
                            description=join + "-------------------------------",
                            color=discord.Color(0xc088ff),
                            timestamp=message.timestamp
                        )
                        embeds.set_footer(
                            text="Current time:"
                        )
                        msg = await client.send_message(message.channel,embed=embeds)
                        while True:
                            l = page != 1
                            r = page < len(numbers) / 2
                            if l:
                                await client.add_reaction(msg,left)
                            if r:
                                await client.add_reaction(msg,right)
                            react,user = await client.wait_for_reaction(check=predicate(msg,l,r))
                            if react.emoji == left:
                                page -= 1
                            elif react.emoji == right:
                                page += 1
                            join = "".join(numbers[(page - 1) * 2:page * 2])
                            embeds = discord.Embed(
                                description=join + "-------------------------------",
                                color=discord.Color(0xc088ff),
                                timestamp=message.timestamp
                            )
                            embeds.set_footer(
                                text="Current time:"
                            )
                            await client.edit_message(msg,embed=embeds)
                            await client.clear_reactions(msg)

        numbers = []
        for row1 in db_get_answer():
            if str(row1[0]) == message.content.split()[1]:
                numbers.append("".join(
                    [f"""-------------------------------\n<@{int(row1[2])}>'s question!\n`{row1[1]}`\n\n"""]))
                print(numbers)
        await answer_all(numbers)

    if message.content.startswith("<answer "):
        def randomname(n):
            a = ''.join(random.choices(string.ascii_letters + string.digits,k=n))
            return a

        if message.content[14:] == "":
            embed = discord.Embed(
                description=f"Hey {message.author.mention}!\nPlease input content!",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return
        
        numbers = randomname(5)
        
        out_words = ["しね","金！暴力！SEX！（迫真）","おっぱい","ちんこ","まんこ","殺す","ちんぽ","おちんちん","アナル","sex","セックス","オナニー","おちんぽ","ちくび",
                     "乳首","陰茎","うざい","黙れ","きもい","やりますねぇ！","覚醒剤","覚せい剤","麻薬","コカイン","SEX","害児","pornhub","xvideo","せっくす",
                     "mother fucker","金正恩","penis","fuck","死ね","殺す","アホ","赤ちゃん製造ミルク","ザー汁","ザーメン","精液","精子","こ↑こ↓",
                     "やりますねぇ"]
        if any([True for s in out_words if s in message.content]):
            embed = discord.Embed(
                description=f"Hey {message.author.mention}!\nYour question were inputed prohibited term so you can't create this question.",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            await client.delete_message(message)
            return
                                                             
        for row in list(db_read()):
            if str(row[0]) == message.content.split()[1]:
                if db_count_up(str(message.content.split()[1])):
                    global counts
                    counts += 1
                    if db_answer(message.content.split()[1],message.content[14:],int(message.author.id),str(numbers)) == True:
                        embed = discord.Embed(
                            title="QUESTION:",
                            description=f"<@{int(message.author.id)}>\nAnswer content:\n\n`{message.content[14:]}`",
                            color=discord.Color(0xc088ff),
                            timestamp=message.timestamp
                        )
                        embed.set_footer(
                            text="Current time:"
                        )
                        await client.send_message(message.channel,embed=embed)
                        for row1 in db_get_answer():
                            if int(row1[2]) == int(message.author.id):
                                if str(row1[0]) == str(row[0]):
                                    user = await client.get_user_info(f"{int(row[1])}")
                                    embeds = discord.Embed(
                                        title="QUESTION:",
                                        description=f"From <@{int(message.author.id)}>\nAnswer to: `{str(row[2])}`\n\nAnswer-content:\n\n`{message.content[14:]}`\n\nQuestion-Original-ID:{numbers}",
                                        color=discord.Color(0xc088ff),
                                        timestamp=message.timestamp
                                    )
                                    embeds.set_footer(
                                        text="Current time:"
                                    )
                                    await client.send_message(user,embed=embeds)
                                    return

    if message.content.startswith("<best-answer"):
        if db_get_best_answer(str(message.content.split()[1])) == True:
            embed = discord.Embed(
                description=f"This question was already granted a best answer.",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="Current time:"
            )
            await client.send_message(message.channel,embed=embed)
            return
        else:
            for row,row1 in zip(list(db_read()),db_get_answer()):
                if str(row1[3]) == message.content.split()[1]:
                    if int(row1[2]) == int(message.author.id):
                        embed = discord.Embed(
                            description=f"Hey {message.author.mention}\nYou can't select yourself answer to best answer!!",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
                    if message.content.split()[1] == "":
                        embed = discord.Embed(
                        description=f"Hey {message.author.mention}!\nPlease input content!",
                        color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
                    if db_write_best_answer(str(message.content.split()[1])) == True:
                        if db_access_answer(str(message.content.split()[1]),str(row1[1])):
                            if str(row1[0]) == str(row[0]):
                                user = await client.get_user_info(f"{int(row1[2])}")
                                embeds = discord.Embed(
                                    title="QUESTION:",
                                    description=f"You selected <@{int(row1[2])}>'s answer to best answer!!",
                                    color=discord.Color(0xc088ff),
                                    timestamp=message.timestamp
                                )
                                embeds.set_footer(
                                    text="Current time:"
                                )
                                await client.send_message(message.channel,embed=embeds)
                                embeds = discord.Embed(
                                    title="QUESTION:",
                                    description=f"Your answer were selected to best answer!!\n\nAnswer to: `{str(row[2])}`\n\nAnswer-content:\n\n`{row1[1]}`",
                                    color=discord.Color(0xc088ff),
                                    timestamp=message.timestamp
                                )
                                embeds.set_footer(
                                    text="Current time:"
                                )
                                await client.send_message(user,embed=embeds)
                                return db_count_up_2(int(row1[2])) == True

    if message.content == "<answer-top":
        async def send(member_data):
            embed = discord.Embed(
                title="Best-Answer-Top10",
                color=discord.Color(0xc088ff),
                description=member_data
            )
            await client.send_message(message.channel,embed=embed)

        i = 1
        member_data = ""
        for row in db_get():
            print(row)
            member_data += "No.{0}: <@{1}> [`Total:{2}times`]\n".format(i,row[0],row[1])
            if i % 10 == 0:
                await send(member_data)
                member_data = ""
            i += 1
        else:
            await send(member_data)
            return

    if message.content.startswith("<question-delete"):
        if message.content.split()[1] == "":
            embed = discord.Embed(
            description=f"Hey {message.author.mention}!\nPlease input content!",
            color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return

        for row in list(db_read()):
            if int(row[1]) == int(message.author.id):
                if str(row[0]) == message.content.split()[1]:
                    if db_reset_question(int(message.author.id),str(message.content.split()[1])) == True:
                        embed = discord.Embed(
                            description=f"<@{message.author.id}> was deleted own question!",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
        else:
            embed = discord.Embed(
                description=f"If this command didn't reaction.\nThat means you don't have Authorityto change this Original-ID...",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="Current time:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content.startswith(">>question-delete"):
        for row in list(db_read()):
            kengensya = ["304932786286886912","439725181389373442"]
            if message.author.id in kengensya:
                if str(row[0]) == message.content.split()[1]:
                    if db_reset_all_question(str(message.content.split()[1])) == True:
                        embed = discord.Embed(
                            description=f"<@{message.author.id}> was deleted question forcibly!",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
            else:
                embed = discord.Embed(
                    description="This command can only use this bot owner!",
                    color=discord.Color(0xc088ff),
                )
                await client.send_message(message.channel,embed=embed)
                return

def db_read():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute('''SELECT create_id,create_name,question,locate_number,answer_id from question;''')
    ans = c.fetchall()
    for row in ans:
        yield (row[0],row[1],row[2],row[3],row[4])
    else:
        con.commit()
        c.close()
        con.close()


def db_read_count():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute('''SELECT sum(locate_number),sum(answer_id) from question;''')
    ans = c.fetchall()
    for row in ans:
        yield (row[0],row[1])
    else:
        con.commit()
        c.close()
        con.close()


def db_access(create_id,question):
    create_id = str(create_id)
    question = str(question)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("""UPDATE question set question=%s where create_id=%s;""",(question,create_id))
    con.commit()
    c.close()
    con.close()
    return True


def db_count_up(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("UPDATE question set answer_id = answer_id + 1 where create_id=%s;",(create_id,))
    con.commit()
    c.close()
    con.close()
    return True


def db_count_up_1(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("UPDATE question set locate_number = locate_number + 1 where create_id=%s;",(create_id,))
    con.commit()
    c.close()
    con.close()
    return True


def db_write(create_id,create_name,question,):
    create_id = str(create_id)
    create_name = int(create_name)
    question = str(question)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("INSERT INTO question(create_id, create_name, question,locate_number,answer_id) VALUES(%s,%s,%s,0,0);",
              (create_id,create_name,question))
    con.commit()
    c.close()
    con.close()
    return True


def db_count_up_2(create_name):
    create_name = int(create_name)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_number(create_name Bigint);")
    c.execute("INSERT INTO question_number(create_name) VALUES(%s);",
              (create_name,))
    print(con)
    con.commit()
    c.close()
    con.close()
    return True

def db_get():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_number(create_name Bigint);")
    c.execute("select create_name, count(*) from question_number group by create_name order by count(*) desc")
    ans = c.fetchall()
    for row in ans:
        print(row)
        yield (row[0],row[1])

def db_get_answer_number(create_name):
    create_name = int(create_name)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute('''SELECT create_name from question_test where create_name=%s;''',(create_name,))
    ans = c.fetchall()
    for row in ans:
        yield (row)
    else:
        con.commit()
        c.close()
        con.close()

def db_get_answer():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute('''SELECT create_id,answer_questions,create_name,number_id from question_test;''')
    ans = c.fetchall()
    for row in ans:
        yield (row[0],row[1],row[2],row[3])
    else:
        con.commit()
        c.close()
        con.close()

def db_access_answer(create_id,answer_question):
    create_id = str(create_id)
    answer_question = str(answer_question)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
            "CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute("""UPDATE question_test set answer_questions='Best-Answer!!\n' || %s where number_id=%s;""",(answer_question,create_id,))
    con.commit()
    c.close()
    con.close()
    return True

def db_answer(create_id,answer_question,create_name,number_id):
    create_id = str(create_id)
    answer_question = str(answer_question)
    create_name = int(create_name)
    number_id = str(number_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute("INSERT INTO question_test(answer_questions, create_id, create_name, number_id) VALUES(%s,%s,%s,%s);",
              (answer_question,create_id,create_name,number_id))
    con.commit()
    c.close()
    con.close()
    return True

def db_write_best_answer(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question_answer(create_id varchar);")
    c.execute("INSERT INTO question_answer(create_id) VALUES(%s);",
              (create_id,))
    con.commit()
    c.close()
    con.close()
    return True

def db_get_best_answer(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question_answer(create_id varchar);")
    c.execute('SELECT * FROM question_answer WHERE create_id=%s;',(create_id,))
    if c.fetchall():
        con.commit()
        c.close()
        con.close()
        return True

def db_reset_question(create_name,create_id):
    create_name = int(create_name)
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("delete from question where create_name=%s AND create_id=%s;",(create_name,create_id,))
    con.commit()
    c.close()
    con.close()
    return True


def db_reset_all_question(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("delete from question where create_id=%s;",(create_id,))
    con.commit()
    c.close()
    con.close()
    return True


client.run(os.environ.get("TOKEN"))
