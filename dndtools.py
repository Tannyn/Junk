# -*- coding: utf-8 -*-

import sys
import time
import math
import random
import datetime
import telepot
import sqlite3
import urllib

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
        
def findSpell(spellSearch):
    conn = sqlite3.connect('/var/www/sqlite/dnd35.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM spell WHERE name LIKE ?', (spellSearch,))
    spellDetails = list(c.fetchall())
    #print spellDetails
    return spellDetails
    conn.close()
    
def specificSpell(spellIndex):
    conn = sqlite3.connect('/var/www/sqlite/dnd35.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM spell WHERE id = ?', (spellIndex,))
    return list(c.fetchone())
    conn.close()
    
def findFeat(featSearch):
    conn = sqlite3.connect('/var/www/sqlite/dnd35.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM feat WHERE name LIKE?', (featSearch,))
    featDetails = list(c.fetchall())
    
    return featDetails
    conn.close()
    
def specificFeat(featIndex):
    conn = sqlite3.connect('/var/www/sqlite/dnd35.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM feat WHERE id = ?', (featIndex,))
    return list(c.fetchone())
    conn.close()
    
def handle(msg):
    chat_id = msg['chat']['id']
    
    user = str(msg['from']['username'])
    
    try:
        sticker = str(msg['sticker']['file_id'])
        print sticker
    except:
        command = msg['text'].split()
        
    if command[0].endswith('@dnDToolsBot'):
        command[0] = command[0][:-12]
        
    if command[0] == '/searchspell':
        spell = findSpell('%'+command[1]+'%')
        #print len(spell)
        for int in range(0, len(spell)):
            url = spell[int][1].replace(' ', '_')
            #for y in range(0, len(spell[int])):
                #spell[int][y] = str(spell[int][y])
            bot.sendMessage(chat_id, '*Index:* '+str(spell[int][0])+' - *Name:* '+'['+spell[int][1]+'](http://www.dandwiki.com/wiki/SRD:'+url+')', 'Markdown')
            
        bot.sendMessage(chat_id, 'Try /getspell <index> to pull specific spells info.')
    elif command[0] == '/getspell':
        spell = specificSpell(command[1])
        for int in range(0, len(spell)):
            spell[int] = str(spell[int])
            #print spell[int]
            url = spell[1].replace(' ', '_')
        bot.sendMessage(chat_id,'*Name:* '+spell[1]+'\n'+'*Description:* '+spell[22]+'\n'+'*Class/Level:* '+spell[7]+'\n'+'*School:* '+spell[4]+'\n'+'[Wiki Link](http://www.dandwiki.com/wiki/SRD:'+url+')'+'\n'+'*Rulebook:* '+spell[32]+' ', 'Markdown')
    elif command[0] == '/searchfeat':
        feat = findFeat('%'+command[1]+'%')
        for int in range(0, len(feat)):
            url = feat[int][1].replace(' ', '_')
            bot.sendMessage(chat_id, '*Index:* '+str(feat[int][0])+' - *Name:* '+'['+feat[int][1]+'](http://www.dandwiki.com/wiki/SRD:'+url+')', 'Markdown')
            
        bot.sendMessage(chat_id, 'Try /getfeat <index> to pull specific spells info.')
    elif command[0] == '/getfeat':
        feat = specificFeat(command[1])
        for int in range(0, len(feat)):
            feat[int] = str(feat[int])
            url = feat[1].replace(' ', '_')
        bot.sendMessage(chat_id, '*Name:* '+'['+feat[1]+'](http://www.dandwiki.com/wiki/SRD:'+url+')\n*Type:* '+feat[2]+'\n*Multiple:* '+feat[3]+'\n*Stackable:* '+feat[4]+'\n*Choice:* '+feat[5]+'\n*Prerequisite:* '+feat[6]+'\n*Benefit:* '+feat[7][:-2]+'\n*Normal:* '+feat[8]+'\n*Special:* '+feat[9]+'\n*Reference:* '+feat[11], 'Markdown')
    #Roll commands
    elif command[0] == '/roll20':
        bot.sendMessage(chat_id, random.randint(1,20))
    elif command[0] == '/roll6':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command[0] == '/roll10':
        bot.sendMessage(chat_id, random.randint(1,10))
    elif command[0] == '/roll100':
        bot.sendMessage(chat_id, random.randint(1,100))
    elif command[0] == '/roll12':
        bot.sendMessage(chat_id, random.randint(1,12))
    elif command[0] == '/roll8':
        bot.sendMessage(chat_id, random.randint(1,8))
    elif command[0] == '/roll4':
        bot.sendMessage(chat_id, random.randint(1,4))
    elif command[0] == '/coin':
        if math.fmod(random.randint(1,100), 2) >= 1:
            bot.sendMessage(chat_id, 'Heads')
        else:
            bot.sendMessage(chat_id, 'Tales')
    elif command[0] == '/roll':
        rollDice(command[1], chat_id)

#Keep as EOF
bot = telepot.Bot('294439921:AAFVdgr3UwL7WX_84N5oGn1WtrXoMwHXyco')
bot.message_loop(handle)
print 'I am listneing... '

while 1:
  time.sleep(10)