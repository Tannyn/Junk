# -*- coding: utf-8 -*-
import sys
import time
import math
import random
import datetime
import telepot
import sqlite3
import urllib
#from urllib.parse import quote
#import telepot.helper
#from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#from telepot.delegate import (per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)


magicItemArray=['*Wand of Create Wand -* 1 charge, creates a Wand of Create Wand.','*Orb of Slope Detection -* Place the orb somewhere you suspect there might be a slope and you can use it to discern the direction and approximate steepness of any slope there might be. May fail on extremely rough or sticky surfaces.','*Deck of 52 Things -* As a Deck of Many Things, except the effect of each card is that the drawer gains possession of one of 52 nonmagical playing cards.','*Ring of Three Least Wishes -* Ring that holds three charges of Least Wish, AKA Prestidigitation.','*Wand of Horse Missile -* Launches tiny (about the size of a duck) horses. Wand comes with 100 charges.','*Tree Token, Feather -* A tree which, on command, permanently turns into a feather.','*Bag of Withholding -* As a Bag of Holding, but sentient and disinclined to let you take items out.','*Scroll of Rock to Rock -* Turns a sedimentary rock into a metamorphic rock.','*Scroll of Detect Alignment -* Allows you to discern the alignment of a block of text, i.e. left, right, centered, or justify.','*Placebo of Cure Light Wounds -* The drinker believes that (s)he has healed 1d6 hit points.','*Scroll of Raise Dead -* Levitates one corpse, as Levitate.','*Axe of the Dwarvish Lesser Nobility -* As the Axe of the Dwarvish Lords, except not at all and it''s actually just a normal axe that was owned by a member of the Dwarvish nobility.','*Orb of Dragon-kin -* Has power over any non-dragon who self-identifies as a dragon.','*Wand of Stone Shape -* Creates basic shapes such as circles, squares and triangles out of stone.','*Potion of Wakefulness -* Allows the drinker to avoid fatigue due to lack of resting for several extra hours. Is actually coffee.','*Portable Whole -* Any surface against which it is placed becomes whole and unbroken until it is removed.','*1.25-staff -* A +1 quarterstaff.','*Scroll of Rock to Roll -* Turns rocks into music.','*Wand of Wall of Mice -* As Wall of Ice, but instead creates a swarm of mice in each space which would have been occupied by ice.','*Scroll of Protection from Gourd -* Protects you from gourds.','*Everburning Torch -* As a normal Everburning Torch except that it constantly insults the user, referring to its insults as "sick burns".','*Scroll of Deeper Dorkness -* The target becomes an extreme dork.','*Bag of Ticks, Gray -* As a Bag of Tricks, Gray but contains only ticks. These ticks have 1 hit point and basically can''t hurt anything.','*Bag of Chicks, Gray -* As a Bag of Tricks, Gray but contains only baby chickens.','*Wand of Launch Boat -* Launches one boat as if fired from a crossbow. Unfortunately, crossbows are notoriously bad at firing boats.','*Bathrobe of the Archmagi -* As a Robe of the Archmagi but with none of the cool powers because why would an Archmage need his cool robe powers when he''s taking a bath.','*Everlasting Rations -* So inedible that they last forever due to not being eaten.','*Scroll of Mud to Roc -* Transmutes some mud into a roc, which is likely to try to eat you.','*Helm of Paradoxes -* On command, prevents command word-activated items, including itself, from functioning for 1 round.','*Ring of Three Fishes -* A ring with three charges of Summon Fish I.','*Arthur, Ring of the Britons -* This sentient ring causes the wearer to speak in a British accent and use phrases such as "you wot mate" and "listen here you lil shit". The ring itself speaks in a posh, high-class British accent.']

goblinMachineArray=['It dehydrates potions into pills.','It turns any humanoid race into another humanoid race at random.','It turns any humanoid race into a goblin.','It creates harmless cattle of random flavor.','It attacks as level 10 fighter. ten slicing blade attacks as +3 vorpal blades.','It spits out a hundred pythons.','It answers questions about the dungeon/region. just like goblins, they always say the opposite of the truth.', 'It''s a demon vending machine.','It''s a mechanized exo-skeleton that doubles your strength and defenses, but uses you to its own ends (usually attacks the party). you are not being controlled mentally–just physically.','It distracts you from a much simpler machine in the room–one that doesn’t even look like a machine, but allows time or planar travel.','It''s broke. You should roll a save at -4 or be charmed into trying to fix it for 1d4 months, sparing no expense to get it home, buy parts, etc. it cannot be fixed.','It processes corpses into meat products.','It circumsizes titans.','It lays large eggs. what hatches?','It dispenses 10 x d100 killer bees.','It tells bad jokes constantly.','It teleconferences with similar machine on far-away planet. 1D4: 1-aliens 2-faeries 3- demons 4-mirror universe versions of yourselves.','It teleports party to mirror universe where alignments are opposite (and the shaved have beards).','It mends armor and weapons, then eats them all and melts them down into ingots.','It is the best cook on this side of planet.']

stickerList=['BQADAgADnQADkZj7B9s8pwABpRpGnwI','BQADAgADeQADkZj7B-vUaCw96j9cAg','BQADAgADWwADkZj7B3IAAUDn40fMmwI','BQADAgADSwADkZj7B0pauBkOunH8Ag','BQADAgADPQADkZj7BwdEZZGxPapeAg','BQADAgADcwADkZj7B6b1KIYuGS_3Ag','BQADAgADdwADkZj7B3dowdEnMiEMAg']

npcRaceArray=['Human', 'Dwarf', 'Elf', 'Hafling', 'Gnome', 'Half-Orc', 'Half-Elf', 'Tiefling', 'Dragonborn', 'Aasimar', 'Aarakocra', 'Genasi', 'Goliath']

npcQuirkArray=['Scar','Monocle','Gaps between teeth','Rash','Tattoo','Missing limb, joints, fingers, teeth','Spits when','talking','Fidgets','Picks ears','Rubs hands together','Sucks on teeth','Mismatched eyes','Acne','Overweight','Underweight','Always eating or drinking','Bites fingernails','Wandering eye','Facial piercing','Limp','Lisp','Foreign clothing','Accent','Uses long words incorrectly','Rubs chin','Tugs on ear','Picks nose','Bites lower lip','Trims or cleans nails with long knife','Twirls hair','with finger','Single hair or beard braid','Many hair or beard braids','Rings or bells in hair or','beard braids','Smells like sweat','Smells like dogs','Smells like horses','Smells like cheap cologne','Smells like expensive cologne','Smells like cedar wood','Smells like tobacco','Smells like','lavender','Smells like alcohol','Smells like soap','Smells like roses','Scratches','Has leaves in','hair or clothing','Wears flower in hair or clothing','Squints','Sniffs often','Braggart','Never looks','anyone in the eye','Superstitious','Unusual jewelry','Freckles','Pockmarked skin','Eye tic','Bucktoothed','Talks loudly','Whispers','Holier than thou attitude','Makes puns','Clumsy','Quotes','famous poet, regularly','Quotes religious text','Refers to self in third person','Chews grass, stick, or leaves','Closely examines everything','Keeps hand on weapon','Keeps hands','in pockets','Hairless','Exotic weapon','Claps hands often','Smacks palm with fist','Asks often','about his own appearance','Rubs palms on thighs','Stretches often','Seems cold or hot','Yawns often','Polishes brooch or buckle often','Rubs luckstone or fetish','Twirls coin between fingers','Always','wears thick, leather gloves','High squeaky voice','Offers exotic beverages or foods','Oily skin or hair','Obvious cosmetics','Lazy eye','Always wears ‘lucky’ hat, scarf, ring','Mole','Always wears favorite color','Wears clothes too big or too small','Wears obvious wig','Uses','a parasol','Picks teeth with knife or fingernails','Waxed facial hair','Belches loud and often','Sneezes often','Coughs regularly','Blinks often','Roll twice','Wine colored birthmark','Rubs eyes','often','Chews on braid or lock of hair','Bites fingernails or cuticles','Polishes spectacles, never','wears them','Twists ring','Picks lint off clothes, his and PCs','Has hiccups','Watering eye(s)','Taps foot or drums fingers','Sunburn and peeling skin','Dark tan','Very pale','Toothless','Dressed in furs or leather','Dressed in formal attire','Dressed in silks and lace','Has','black eye','Bruised extremities','Arm in sling','Bandaged extremity','Stutters','Tongue tied','Mixes languages','Mixes gibberish with words','Keeps arms folded','Picks at scabs or loose skin','Dresses colorblind','Has wart on hand, covers it always','Hand covers mouth while speaking','Keeps','hand on PCs shoulder','Carries crumbs to feed birds','Hands coppers to beggar children','Speaks to animals like people','Speaks to ‘spirits’','Has paint stained hands and clothes','Wears scarf around ankles or wrists','Wears vest with bell buttons','Fascinated by fire','Fascinated by non human races','Clothes have bulging pouches','Archaic speech','Spotless, glossy','boots','Rope burns around neck or wrists','Pasted on moustache or beard','Hair dye covering collar','Writes down everything PC says','Wears armor covered in runes','Has vampire bite scars on neck','Has arthritis in hands','Rubs old knee injury','Avoids crowds','Nose bleeds','Wears notched belt','Wears well tended ancient weapon','Refers to good old days often','Wears heart shaped beauty mark','Has one or more gold teeth','Ogles opposite sex openly','Paper cuts and ink stained fingers','Serious burn scar','Rings sewn on clothes with fetishes','Clothes made of woven leaves','Pregnant woman','Rubs calluses on palms with thumb','Carries cloth covered basket','Sharpens','knife with whetstone','Spit polishes thick, fancy bracelet','Hard of hearing','Gives a','different name every meeting','Regularly blows stray hair out of eyes','Bows before speaking and after','Flatulent','Hooks thumbs in belt and bounces','Walks like a sailor','Crumbs in beard and clothes','Food stained face','Wine stained ‘moustache’','Carries small snake, mouse, or lizard','Wears','foreign style clothes','Has long, lacquered nails','Mute, speaks through sign language','Blind, sees through familiar’s eyes','Uses foul language','Runny nose','Always late','Instructs','PCs on latest fashion','Bad cook, begs PCs to eat','Rubs large belly often','Blatantly','pouts','Calls PCs by wrong names','Convinced PCs need reforming','Giggles,','inappropriately','Wears ancient fashions','Combs hair with fingers','Jingles coins','in pocket or pouch','Intoxicated or acting','Talks in rhyme','Plays with charm on necklace','Roll','twice','Says “hmm – hmm” often','Asks rhetorical questions and answers','Denies','gossiping and proceeds to gossip','Falsely claims he is an adventurer too','Greatly','exaggerates','Nods often','Gestures wildly with hands','Carries satchel filled with junk','Hacking cough','Sweats profusely','Shaving cuts on face','Military manner','Animal bite or claw scar','Sleepy','Always out of breath','Sketches PC while talking','Flips key ring with finger','Covered','with road dust','Rolls “R’s” while speaking','Snorts while laughing','Complains of','heartburn','Talks of health problems','Loses items and asks PCs to help look','Survived torture, has','no fingernails','Vegetarian','Only eats meat','Conceited','Pathological liar','Taps foot incessantly','Rubs back of neck']

appearanceArray=['Distinctive jewelry','Piercings','Flamboyant or outlandish clothes','Formal, clean clothes','Ragged,','ty','thes','Pronounced scar','Missing teeth','Missing fingers','Unusual eye color or','colors','Tattoos','Birthmark','Unusual skin color','Bald','Braided beard or hair','Unusual hair color','Nervous eye twitch','Distinctive nose','Distinctive posture','Exceptionally beautiful','ceptionally ugly','Missing limb','Cleft lip','Androgynous']

mannerismArray=['Prone to singing or humming','Speaks in a peculiar way','Particularly low or high voice','Enunciates realy clearly','Speaks loudly','Whispers','Uses flowery speech or long words','Frequently uses the wrong word','Uses colorful exclamations','Makes constant jokes or puns','Prone to predictions of doom','Fidgets','Squints','Stares into the distance','Chews something','Paces','Taps fingers','Bites fingernails','Twirls hair or tugs beard','ares intently','Closes eyes when talking','Leans against vertical surfaces','Taps feet']

potatoArray=['Potato', 'Yam', 'Murphy', 'Tater', 'Tuber', 'Po-ta-to', 'Fries', ]

count=1

def rollDice(dice, chat_id):
    roll=0;
    if 'd' in dice:
        dices = dice.split('d')
        if int(dices[0]) > 25:
            bot.sendMessage(chat_id, 'That''s too many dice!')
            return
        else:
            for times in range(1,int(dices[0])):
                roll = roll + random.randint(1,int(dices[1]))
            bot.sendMessage(chat_id, roll)
            return
    elif 'D' in dice:
        dices = dice.split('D')
        if int(dices[0]) > 25:
            bot.sendMessage(chat_id, 'That''s too many dice!')
            return
        else:
            for times in range(1,int(dices[0])):
                roll = roll + random.randint(1,int(dices[1]))
            bot.sendMessage(chat_id, roll)
            return
    try:
        if int(dice):
            bot.sendMessage(chat_id, random.randint(1,int(dice)))
            return
    except:
        bot.sendMessage(chat_id, 'Sorry, that''s not a valid roll!')
        return
        #print dices[0]
        #print dices[1]



def pickGender(roll=0):
#If 0 is passed, roll a d100
    if roll == 0:
        roll=random.randint(1,100)

    if roll > 0 and roll < 46:
        return 'male'
    elif roll > 45 and roll < 89:
        return 'female'
    elif roll > 90 and roll < 101:
        return 'non-binary'
    else:
        print 'Gender roll failed'
        return


def pickRace(roll=0):
#If 0 is passed, roll a d100
    if roll == 0:
        roll=random.randint(1,100)


    if roll > 0 and roll < 30:
        return npcRaceArray[0]
    elif roll > 29 and roll < 40:
        return npcRaceArray[1]
    elif roll > 39 and roll < 50:
        return npcRaceArray[2]
    elif roll > 49 and roll < 60:
        return npcRaceArray[3]
    elif roll > 59 and roll < 70:
        return npcRaceArray[4]
    elif roll > 69 and roll < 80:
        return npcRaceArray[5]
    elif roll > 79 and roll < 87:
        return npcRaceArray[6]
    elif roll > 86 and roll < 91:
        return npcRaceArray[7]
    elif roll > 90 and roll < 97:
        return npcRaceArray[8]
    elif roll == 97:
        return npcRaceArray[9]
    elif roll == 98:
        return npcRaceArray[10]
    elif roll == 99:
        return npcRaceArray[11]
    elif roll == 100:
        return npcRaceArray[12]
    else:
        print 'Race roll failed'
        return
        
def pickAppearance(roll=0):
    if roll == 0:
           roll=random.randint(1,len(appearanceArray))
        
    return str(appearanceArray[roll-1])
    
def pickMannerism(roll=0):
    if roll == 0:
            roll=random.randint(1,len(appearanceArray))
        
    return str(appearanceArray[roll-1])
    
def pickQuirk():
    return str(npcQuirkArray[random.randint(0, len(npcQuirkArray)-1)])
#date='0'
#time='0'

def findSpell(spellSearch):
    conn = sqlite3.connect('/var/www/sqlite/dnd35.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM spell WHERE name LIKE ?', (spellSearch,))
    spellDetails = list(c.fetchall())
    print spellDetails
    return spellDetails
    conn.close()
    
def specificSpell(spellIndex):
    conn = sqlite3.connect('/var/www/sqlite/dnd35.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM spell WHERE id = ?', (spellIndex,))
    return list(c.fetchone())
    conn.close()
    
def handle(msg):
    global count
    chat_id = msg['chat']['id']
    
    user = str(msg['from']['username'])
    
    try:
        sticker = str(msg['sticker']['file_id'])
        print sticker
    except:
        command = msg['text'].split()


    #for index in range(len(command)):
        #print command[index]

    if command[0].endswith('@xXPotatobot'):
        command[0] = command[0][:-12]


    print 'Got command: %s' % command[0]


    if command[0] == '/potato':
        bot.sendMessage(chat_id, potatoArray[random.randint(0,len(potatoArray)-1)] + '!')
    elif command[0] == '/potatoes':
        bot.sendSticker(chat_id, str(stickerList[random.randint(1,len(stickerList)-1)]))
        #if user is not 'xXPotatobot':
            #for num in range(0,count):
                #print user
                #count=count+1
        #if count>12:
            #count=1
    # elif command[0] == '/roll20':
        # bot.sendMessage(chat_id, random.randint(1,20))
    # elif command[0] == '/roll6':
        # bot.sendMessage(chat_id, random.randint(1,6))
    # elif command[0] == '/roll10':
        # bot.sendMessage(chat_id, random.randint(1,10))
    # elif command[0] == '/roll100':
        # bot.sendMessage(chat_id, random.randint(1,100))
    # elif command[0] == '/roll12':
        # bot.sendMessage(chat_id, random.randint(1,12))
    # elif command[0] == '/roll8':
        # bot.sendMessage(chat_id, random.randint(1,8))
    # elif command[0] == '/roll4':
        # bot.sendMessage(chat_id, random.randint(1,4))
    # elif command[0] == '/coin':
        # if math.fmod(random.randint(1,100), 2) >= 1:
            # bot.sendMessage(chat_id, 'Heads')
        # else:
            # bot.sendMessage(chat_id, 'Tales')
    # elif command[0] == '/roll':
        # rollDice(command[1], chat_id)
    elif command[0] == '/giveitem':
        try:
            if command[1]:
                bot.sendMessage(chat_id, 'Fine, ' + str(command[1]) + ' can have a ' + magicItemArray[random.randint(1,len(magicItemArray))], 'Markdown')
        except:
            bot.sendMessage(chat_id, 'Fine, you can have a ' + magicItemArray[random.randint(1,len(magicItemArray))], 'Markdown')
    elif command[0] == '/makenpc':
        bot.sendMessage(chat_id, pickRace() +'\n'+ pickGender()+'\n'+ pickAppearance() +'\n'+ pickMannerism() +'\n'+ pickQuirk())
    elif command[0] == '/goblins':
        bot.sendMessage(chat_id, 'There\'s a group of goblins in the valley down yonder that have a powerful machine. Word is that ' + goblinMachineArray[random.randint(0,len(goblinMachineArray))])
    # elif command[0] == '/searchspell':
        # #spell=[0]
        # spell = findSpell('%'+command[1]+'%')
        # print len(spell)
        # for int in range(0, len(spell)):
            # url = spell[int][1].replace(' ', '_')
            # #for y in range(0, len(spell[int])):
                # #spell[int][y] = str(spell[int][y])
            # bot.sendMessage(chat_id, '*Index:* '+str(spell[int][0])+' - *Name:* '+'['+spell[int][1]+'](http://www.dandwiki.com/w/index.php?title=Special%3ASearch&search='+url+')', 'Markdown')
            
        # bot.sendMessage(chat_id, 'Try /getspell <index> to pull specific spells info.')
        
    # elif command[0] == '/getspell':
        # spell = specificSpell(command[1])
        # for int in range(0, len(spell)):
            # spell[int] = str(spell[int])
            # #print spell[int]
            # url = spell[1].replace(' ', '_')
        # bot.sendMessage(chat_id,'*Name:* '+spell[1]+'\n'+'*Description:* '+spell[22]+'\n'+'*Class/Level:* '+spell[7]+'\n'+'*School:* '+spell[4]+'\n'+'[Wiki Link](http://www.dandwiki.com/w/index.php?title=Special%3ASearch&search='+url+')'+'\n'+'*Rulebook:* '+spell[32]+' ', 'Markdown')
#    elif command == '/setdndtime'
#        bot.sendMessage(chat_id, 'What day is D&D on?')
#        def on_callback_query(self, msg):
#            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

bot = telepot.Bot('287837762:AAGaAHjoVYLkRw70WMsyy-ocB9DZi0pGCDc')
bot.message_loop(handle)
print 'I am listneing... '

while 1:
  time.sleep(10)
