import sys, os, time
import xml.etree.ElementTree as ET
from subprocess import *

ES_INPUT = '/opt/retropie/configs/all/emulationstation/es_input.cfg'
RETROARCH_CFG = '/opt/retropie/configs/all/retroarch-joypads/'
FBA_ROMPATH = '/home/pi/RetroPie/roms/fba/'

capcom_fight = [
    'mshvsf', 'vsav', 
    'sfa', 'sfa2', 'sfa3', 
    'sf2', 'sf2ce', 'ssf2',
    'sfiii', 'sfiii3'
    ]
snk_fight = [
    'kof94', 'kof95', 'kof96', 'kof97', 'kof98', 'kof99', 
    'rbff1', 'rbff2', 'rbffspec', 
    'samsho', 'samsho2', 'samsho3', 'samsho4', 
    'fatfury1', 'fatfury2', 'fatfury3', 'fatfurysp',
    'aof', 'aof2' 
    ]
shoot = [
    '1941', '1942', '1943', '1944',
    'gunbird', 'gunbird2',
    'mazinger',
    'tengai'
    ]

retroarch_key = {}
user_key = {}
capcom_map = {}
snk_map = {}
shoot_map = {}
default_map = {}
turbo_key = ''

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


def load_es_cfg():
    doc = ET.parse(ES_INPUT)
    root = doc.getroot()
    #tag = root.find('inputConfig')
    tags = root.findall('inputConfig')
    num = 1
    for i in tags:
        print str(num) + ". " + i.attrib['deviceName']
        num = num+1
    dev_select = input('\nSelect your joystick: ')

    return tags[dev_select-1].attrib['deviceName']


def load_retroarch_cfg(dev_name):

    print 'Device Name: ', dev_name, '\n'

    f = open(RETROARCH_CFG + dev_name + '.cfg', 'r')
    while True:
        line = f.readline()
        if not line: 
            break
        #line = line.replace('\"','')
        line = line.replace('\n','')
        line = line.replace('input_','')
        line = line.replace('_btn','')
        line = line.replace('_axis','')
        words = line.split()
        retroarch_key[words[0]] = words[2].replace('"','')
       
    f.close()
    #print 'Retroarch Key:', retroarch_key, '\n'

    
def load_layout():

    print ' -(1)-----  -(2)-----  -(3)----- '
    print ' | X Y L |  | Y X L |  | L Y X | '
    print ' | A B R |  | B A R |  | R B A | '
    print ' ---------  ---------  --------- '

    es_conf = input('\nSelect your joystick layout: ')

    if es_conf != 1 and es_conf != 2 and es_conf != 3:
        print 'input error!!'
        sys.exit()
    else:
        if es_conf == 1:
            user_key['1'] = 'x'
            user_key['2'] = 'y'
            user_key['3'] = 'l'
            user_key['4'] = 'a'
            user_key['5'] = 'b'
            user_key['6'] = 'r'
        elif es_conf == 2:
            user_key['1'] = 'y'
            user_key['2'] = 'x'
            user_key['3'] = 'l'
            user_key['4'] = 'b'
            user_key['5'] = 'a'
            user_key['6'] = 'r'
        elif es_conf == 3:
            user_key['1'] = 'l'
            user_key['2'] = 'y'
            user_key['3'] = 'x'
            user_key['4'] = 'r'
            user_key['5'] = 'b'
            user_key['6'] = 'a'


def set_keymap():
    
    global turbo_key

    print '\n\n'
    print ' -(1)--------  -(2)-------- '
    print ' | LP MP HP |  | LK MK HK | '
    print ' | LK MK HK |  | LP MP HP | '
    print ' ------------  ------------ '

    capcom_conf = input('\nSelect a layout for capcom fighting games: ')
    if capcom_conf != 1 and capcom_conf != 2:
        print 'input error!!'
        sys.exit() 
    else:
        if capcom_conf == 1:
            capcom_map['1'] = user_key['1']     # LP
            capcom_map['9'] = user_key['2']     # MP
            capcom_map['10'] = user_key['3']    # HP
            capcom_map['0'] = user_key['4']     # LK
            capcom_map['8'] = user_key['5']     # MK
            capcom_map['11'] = user_key['6']    # HK
        elif capcom_conf == 2:
            capcom_map['1'] = user_key['4']     # LP
            capcom_map['9'] = user_key['5']     # MP
            capcom_map['10'] = user_key['6']    # HP
            capcom_map['0'] = user_key['1']     # LK
            capcom_map['8'] = user_key['2']     # MK
            capcom_map['11'] = user_key['3']    # HK

    print '\n\n'
    print ' -(1)-----  -(2)-----  -(3)----- '
    print ' | C D   |  | A B   |  | D     | '
    print ' | A B   |  | C D   |  | A B C | '
    print ' ---------  ---------  --------- '

    snk_conf = input('\nSelect a layout for snk fighting games: ')
    if snk_conf != 1 and snk_conf != 2 and snk_conf != 3:
        print 'input error!!'
        sys.exit() 

    else:
        if snk_conf == 1:
            snk_map['0'] = user_key['4']    # A
            snk_map['8'] = user_key['5']    # B
            snk_map['1'] = user_key['1']    # C
            snk_map['9'] = user_key['2']    # D
        elif snk_conf == 2:
            snk_map['0'] = user_key['1']
            snk_map['8'] = user_key['2']
            snk_map['1'] = user_key['4']
            snk_map['9'] = user_key['5']
        elif snk_conf == 3:
            snk_map['0'] = user_key['4']
            snk_map['8'] = user_key['5']
            snk_map['1'] = user_key['6']
            snk_map['9'] = user_key['1']

    print '\n\n'
    print ' -(1)-----  -(2)-----  -(3)------ '
    print ' | B  C  |  | A  A* |  | A* B C | '
    print ' | A  A* |  | B  C  |  | A  B C | '
    print ' ---------  ---------  ---------- '

    shoot_conf = input('\nSelect a layout for shooting games (* Turbo): ')
    if shoot_conf != 1 and shoot_conf != 2 and shoot_conf != 3:
        print 'input error!!'
        sys.exit() 

    else:
        if shoot_conf == 1:
            shoot_map['0'] = user_key['4'] + user_key['5']   # A
            shoot_map['8'] = user_key['1']    # B
            shoot_map['1'] = user_key['2']    # C
            turbo_key = retroarch_key[user_key['5']]
        elif shoot_conf == 2:
            shoot_map['0'] = user_key['1'] + user_key['2'] 
            shoot_map['8'] = user_key['4']
            shoot_map['1'] = user_key['5']
            turbo_key = retroarch_key[user_key['2']]
        elif shoot_conf == 3:
            shoot_map['0'] = user_key['4'] + user_key['1'] 
            shoot_map['8'] = user_key['5'] + user_key['2'] 
            shoot_map['1'] = user_key['6'] + user_key['3']
            turbo_key = retroarch_key[user_key['1']]
         
    print '\n\n'
    print ' -(1)-----  -(2)-----  -(3)----- '
    print ' | C D   |  | A B   |  | D     | '
    print ' | A B   |  | C D   |  | A B C | '
    print ' ---------  ---------  --------- '
    
    default_conf = input('\nSelect a layout for other games: ')
    print '\n'
    if default_conf != 1 and default_conf != 2 and default_conf != 3:
        print 'input error!!'
        sys.exit() 

    else:
        if default_conf == 1:
            default_map['0'] = user_key['4']
            default_map['8'] = user_key['5']
            default_map['1'] = user_key['1']
            default_map['9'] = user_key['2']
        elif default_conf == 2:
            default_map['0'] = user_key['1']
            default_map['8'] = user_key['2']
            default_map['1'] = user_key['4']
            default_map['9'] = user_key['5']
        elif default_conf == 3:
            default_map['0'] = user_key['4']
            default_map['8'] = user_key['5']
            default_map['1'] = user_key['6']
            default_map['9'] = user_key['1']


def update_fba_rmp(index):

    if os.path.isdir('/opt/retropie/configs/fba/FinalBurn Neo') == False:
        run_cmd('mkdir /opt/retropie/configs/fba/FinalBurn\ Neo')
    # print default_map
    buf = ''
    run_cmd("sed -i \'/input_player" + str(index) + "/d\' /opt/retropie/configs/fba/FinalBurn\ Neo/FinalBurn\ Neo.rmp")
    f = open('/opt/retropie/configs/fba/FinalBurn Neo/FinalBurn Neo.rmp', 'a')
    for key in default_map:
        res = 'input_player' + str(index) + '_btn_' + default_map[key] + ' = ' + '\"' + key + '\"'
        buf += res + '\n'
    f.write(buf)
    f.close()
    for game in capcom_fight:
        buf = ''
        run_cmd("sed -i \'/input_player" + str(index) + "/d\' /opt/retropie/configs/fba/FinalBurn\ Neo/" + game + ".rmp")
        f = open('/opt/retropie/configs/fba/FinalBurn Neo/' + game + '.rmp', 'a')
        for key in capcom_map:
            res = 'input_player' + str(index) + '_btn_' + capcom_map[key] + ' = ' + '\"' + key + '\"'
            buf += res + '\n'
        f.write(buf)
        f.close()
    # print snk_map
    for game in snk_fight:
        buf = ''
        run_cmd("sed -i \'/input_player" + str(index) + "/d\' /opt/retropie/configs/fba/FinalBurn\ Neo/" + game + ".rmp")
        f = open('/opt/retropie/configs/fba/FinalBurn Neo/' + game + '.rmp', 'a')
        for key in snk_map:
            res = 'input_player' + str(index) + '_btn_' + snk_map[key] + ' = ' + '\"' + key + '\"'
            buf += res + '\n'
        f.write(buf)
        f.close()
    # print shoot_map
    for game in shoot:
        buf = ''
        run_cmd("sed -i \'/input_player" + str(index) + "/d\' /opt/retropie/configs/fba/FinalBurn\ Neo/" + game + ".rmp")
        f = open('/opt/retropie/configs/fba/FinalBurn Neo/' + game + '.rmp', 'a')
        for key in shoot_map:
            res = 'input_player' + str(index) + '_btn_' + shoot_map[key][0] + ' = ' + '\"' + key + '\"'
            buf += res + '\n'
            if len(shoot_map[key]) == 2:
                res = 'input_player' + str(index) + '_btn_' + shoot_map[key][1] + ' = ' + '\"' + key + '\"'
                buf += res + '\n'
        f.write(buf)
        f.close()
        if os.path.isfile(FBA_ROMPATH + game + ".zip.cfg") == True:
            run_cmd("sed -i \'/input_player" + str(index) + "_turbo_btn/d\' " + FBA_ROMPATH + game + ".zip.cfg")
        if turbo_key != '':
            run_cmd("echo 'input_player" + str(index) + "_turbo_btn = " + turbo_key + "' >> " + FBA_ROMPATH + game + ".zip.cfg")
    if os.path.isdir('/home/pi/.config/retroarch/config/remaps') == True:
        run_cmd('cp -r /opt/retropie/configs/fba/FinalBurn\ Neo /home/pi/.config/retroarch/config/remaps')

if __name__ == "__main__":

    index = int(sys.argv[1])

    print '\n*************************'
    print '** KeyMapper for FBNeo **'
    print '*************************\n'

    dev_name = load_es_cfg()
    load_retroarch_cfg(dev_name)
    load_layout()
    set_keymap()
    update_fba_rmp(index)
