import discord
import csv
import re
import random
from discord.ext import commands, pages
from discord import option

def get_unit_pages(row):
    unitembed=discord.Embed(title=row['Name'], color=0xb56c22)
    supportembed=discord.Embed(title=row['Name'], color=0xb56c22)
    unitembed.set_thumbnail(url=row['Portrait'])
    supportembed.set_thumbnail(url=row['Portrait'])
    unitembed.add_field(name="Lv " + row['Lv'] + " ", value=row['Class'], inline=True)
    unitembed.add_field(name="Affinity: ", value=row['Affinity'], inline=True)
    bases = "HP " + row['HP'] + " | " + "Atk " + row['Atk'] + " | Skl " + row['Skl'] + " | " + "Spd " + row['Spd'] + " | " + "Lck " + row['Luck'] + " | " + "Def " + row['Def'] + " | " + "Res " + row['Res'] + " | " + "Con " + row['Con'] + " | " + "Mov " + row['Move']
    unitembed.add_field(name="Bases", value=bases, inline=False)
    growths = "HP " + row['HP Growth'] + "% | " + "Atk " + row['Atk Growth'] + "% | Skl " + row['Skl Growth'] + "% | " + "Spd " + row['Spd Growth'] + "% | " + "Lck " + row['Luck Growth'] + "% | " + "Def " + row['Def Growth'] + "% | " + "Res " + row['Res Growth'] + "%"
    unitembed.add_field(name="Growths", value=growths, inline=False)
    ranks = sevens_get_ranks(row)
    unitembed.add_field(name="Ranks", value=ranks, inline=False)
    if (row['Promotion Class'] != "None"):
        gains = sevens_get_gains(row)
        unitembed.add_field(name="Promotion Gains", value=gains, inline=False)
    
    with open('7s/7s supports.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for supportrow in reader:
            if(row['Name'] == supportrow['Name']):
                supportstring = ""
                if(supportrow['Partner 1'] != '0'):
                    supportstring += supportrow['Partner 1'] + " : Base: " + supportrow['Starting Value 1'] + " | Growth: +" + supportrow['Growth 1'] + "\n"
                if(supportrow['Partner 2'] != '0'):
                    supportstring += supportrow['Partner 2'] + " : Base: " + supportrow['Starting Value 2'] + " | Growth: +" + supportrow['Growth 2'] + "\n"
                if(supportrow['Partner 3'] != '0'):
                    supportstring += supportrow['Partner 3'] + " : Base: " + supportrow['Starting Value 3'] + " | Growth: +" + supportrow['Growth 3'] + "\n"
                if(supportrow['Partner 4'] != '0'):
                    supportstring += supportrow['Partner 4'] + " : Base: " + supportrow['Starting Value 4'] + " | Growth: +" + supportrow['Growth 4'] + "\n"
                if(supportrow['Partner 5'] != '0'):
                    supportstring += supportrow['Partner 5'] + " : Base: " + supportrow['Starting Value 5'] + " | Growth: +" + supportrow['Growth 5'] + "\n"
                if(supportrow['Partner 6'] != '0'):
                    supportstring += supportrow['Partner 6'] + " : Base: " + supportrow['Starting Value 6'] + " | Growth: +" + supportrow['Growth 6'] + "\n"
                if(supportrow['Partner 7'] != '0'):
                    supportstring += supportrow['Partner 7'] + " : Base: " + supportrow['Starting Value 7'] + " | Growth: +" + supportrow['Growth 7'] + "\n"
                supportembed.add_field(name="", value=supportstring, inline=False)
    supportembed.set_footer(text="In Seven Siblings, supports are increased once at the start of a chapter if units are simultaneously deployed. 80 points are needed to reach C support, 160 for B, and 240 for A.")


    page_groups = [
        pages.PageGroup(
        pages=[unitembed], 
        label="Main Unit Data",
        description="Standard unit data: base stats, growths, etc.",
        use_default_buttons=False,
        default=True,
        ),
        pages.PageGroup(
        pages=[supportembed],
        label="Supports",
        description="Support data for the unit",
        use_default_buttons=False,
        )
    ]
    return page_groups


async def unit(ctx, name: str):
    stripped_name = re.sub(r'[^a-zA-Z0-9]','', name)
    with open('7s/7s unit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        was_found = False
        for row in reader:
            stripped_row = re.sub(r'[^a-zA-Z0-9]','', row['Name'])
            if(stripped_row.lower() == stripped_name.lower()):
                paginator = pages.Paginator(pages=get_unit_pages(row), show_menu=True, show_disabled=False, show_indicator=False, menu_placeholder="Select page to view", timeout =120, disable_on_timeout = True)
                await paginator.respond(ctx.interaction)
                was_found = True
                break
        if (not was_found):
            await ctx.response.send_message("That unit does not exist.")

def sevens_get_ranks(row):
    ranks = ""
    if (row['Sword'] != 'None'):
        ranks += "<:TypeSword:1082455058484052089>Sword: " + row['Sword'] + " | "
    if (row['Lance'] != 'None'):
        ranks += "<:TypeLance:1082455057242529843>Lance: " + row['Lance'] + " | "
    if (row['Axe'] != 'None'):
        ranks += "<:TypeAxe:1082455056143622144>Axe: " + row['Axe'] + " | "
    if (row['Bow'] != 'None'):
        ranks += "<:TypeBow:1082455054000341013>Bow: " + row['Bow'] + " | "
    if (row['Staff'] != 'None'):
        ranks += "<:TypeStaff:1082455051819298868>Staff: " + row['Staff'] + " | "
    if (row['Anima'] != 'None'):
        ranks += "<:TypeAnima:1082455053257932801>Anima: " + row['Anima'] + " | "
    if (row['Light'] != 'None'):
        ranks += "<:TypeLight:1082455050330316810>Light: " + row['Light'] + " | "
    if (row['Dark'] != 'None'):
        ranks += "<:TypeDark:1082455049143320649>Dark: " + row['Dark'] + " | "
    if (len(ranks) > 0):
        ranks = ranks[:-3]
    else:
        ranks = "None"
    return ranks

def sevens_get_gains(row):
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
            gains2 += "<:TypeSword:1082455058484052089>" + row['Sword Gains'] + " | "
    if (row['Lance Gains'] != 'None'):
            gains2 += "<:TypeLance:1082455057242529843>" + row['Lance Gains'] + " | "
    if (row['Axe Gains'] != 'None'):
            gains2 += "<:TypeAxe:1082455056143622144>" + row['Axe Gains'] + " | "
    if (row['Bow Gains'] != 'None'):
            gains2 += "<:TypeBow:1082455054000341013>" + row['Bow Gains'] + " | "
    if (row['Staff Gains'] != 'None'):
            gains2 += "<:TypeStaff:1082455051819298868>" + row['Staff Gains'] + " | "
    if (row['Anima Gains'] != 'None'):
            gains2 += "<:TypeAnima:1082455053257932801>" + row['Anima Gains'] + " | "
    if (row['Light Gains'] != 'None'):
            gains2 += "<:TypeLight:1082455050330316810>" + row['Light Gains'] + " | "
    if (row['Dark Gains'] != 'None'):
            gains2 += "<:TypeDark:1082455049143320649>" + row['Dark Gains'] + " | "
    if (len(gains2) > 0):
        gains2 = gains2[:-3]
    return gains + gains2