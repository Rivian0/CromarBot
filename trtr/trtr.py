import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

class Trtr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_unit_pages(self, row):
        unitembed=discord.Embed(title=row['Name'], color=0x67b870)
        supportembed=discord.Embed(title=row['Name'], color=0x67b870)
        unitembed.set_thumbnail(url=row['Portrait'])
        supportembed.set_thumbnail(url=row['Portrait'])
        unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
        unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
        bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
        unitembed.add_field(name="Bases", value=bases, inline=False)
        growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
        unitembed.add_field(name="Growths", value=growths, inline=False)
        ranks = trtr_get_ranks(row)
        unitembed.add_field(name="Ranks", value=ranks, inline=False)
        if (row['Promotion Class'] != "None"):
            gains = trtr_get_gains(row)
            unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
        
        # with open('7s/7s supports.csv', newline='') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for supportrow in reader:
        #         if(row['Name'] == supportrow['Name']):
        #             supportstring = ""
        #             if(supportrow['Partner 1'] != '0'):
        #                 supportstring += supportrow['Partner 1'] + " : Base: " + supportrow['Starting Value 1'] + " | Growth: +" + supportrow['Growth 1'] + "\n"
        #             supportembed.add_field(name="", value=supportstring, inline=False)


        page_groups = [
            pages.PageGroup(
            pages=[unitembed], 
            label="Main Unit Data",
            description="Standard unit data: base stats, growths, etc.",
            use_default_buttons=False,
            default=True,
            ),
            # pages.PageGroup(
            # pages=[supportembed],
            # label="Supports",
            # description="Support data for the unit",
            # use_default_buttons=False,
            # )
        ]

        if(row['Name'] == "Ava"):
            bonusembed=discord.Embed(title=row['Name'], color=0x67b870)
            bonusembed.set_thumbnail(url=row['Portrait'])
            bonusgrowths = "HP " + "140" + "% | " + "Atk " + "40" + "% | Skl " + "50" + "% | " + "Spd " + "50" + "% | " + "Lck " + "40" + "% | " + "Def " + "35" + "% | " + "Res " + "45" + "%"
            bonusembed.add_field(name="Growths", value=bonusgrowths, inline=False)
            bonusembed.set_footer(text="Ava will have these growths after her promotion at the end of Chapter 13.")
            page_groups.append(pages.PageGroup(pages=[bonusembed], label="Secondary Growths", description="Growths after promotion", use_default_buttons=False))


        return page_groups
    
    trtr = discord.SlashCommandGroup("trtr", "Get The Road To Ruin data")

    public_test_ids = [1039354532167176303,1081749141480288256]

    @trtr.command(description = "Get The Road To Ruin unit data", guild_ids=public_test_ids)
    @option("name", description = "Name of the character to get data for")
    async def unit(self, ctx, name: str):
        stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
        with open('trtr/trtr unit.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            was_found = False
            for row in reader:
                stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
                if(stripped_row.lower() == stripped_name.lower()):
                    paginator = pages.Paginator(pages=self.get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
                    await paginator.respond(ctx.interaction)
                    was_found = True
                    break
            if (not was_found):
                await ctx.response.send_message("That unit does not exist.")


def trtr_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'None'):
        ranks += "Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'None'):
        ranks += "Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'None'):
        ranks += "Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'None'):
        ranks += "Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'None'):
        ranks += "Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'None'):
        ranks += "Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'None'):
        ranks += "Light: " + row['Light'] + " | "
    if (row['Dark'] != 'None'):
        ranks += "Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def trtr_get_gains(row):
    gains = ""
    gains += row['Promotion Class'] + '\n'
    if (row['HP Gains'] != '0'):
        gains += "HP: +" + row['HP Gains'] + " | "
    if (row['Atk Gains'] != '0'):
        gains += "Atk: +" + row['Atk Gains'] + " | "
    if (row['Skl Gains'] != '0'):
        gains += "Skl: +" + row['Skl Gains'] + " | "
    if (row['Spd Gains'] != '0'):
        gains += "Spd: +" + row['Spd Gains'] + " | "
    if (row['Def Gains'] != '0'):
        gains += "Def: +" + row['Def Gains'] + " | "
    if (row['Res Gains'] != '0'):
        gains += "Res: +" + row['Res Gains'] + " | "
    if (row['Con Gains'] != '0'):
        gains += "Con: +" + row['Con Gains'] + " | "
    if (row['Mov Gains'] != '0'):
        if (int(row['Mov Gains']) > 0):
            gains += "Mov: +" + row['Mov Gains'] + " | "
        else:
            gains += "Mov: " + row['Mov Gains'] + " | "
    gains = gains[:-3]
    gains += "\n"
    gains2 = ""
    if (row['Sword Gains'] != 'None'):
            gains2 += "Sword: " + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
            gains2 += "Lance: " + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
            gains2 += "Axe: " + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
            gains2 += "Bow: " + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
            gains2 += "Staff: " + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
            gains2 += "Anima: " + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
            gains2 += "Light: " + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
            gains2 += "Dark: " + row['Dark Gains'] + " | "
    if (len(gains2) > 0):
        gains2 = gains2[:-3]
    return gains + gains2



def setup(bot):
    bot.add_cog(Trtr(bot))