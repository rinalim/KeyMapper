import sys, os, time
import xml.etree.ElementTree as ET
from subprocess import *

ES_INPUT = '/opt/retropie/configs/all/emulationstation/es_input.cfg'
RETROARCH_CFG = '/opt/retropie/configs/all/retroarch-joypads/'
ADVMAME_RC = '/opt/retropie/configs/mame-advmame/advmame.rc'
ADVJ = '/opt/retropie/emulators/advmame/bin/advj'

capcom_fight = ['mshvsf', 'vsav', 'sfa', 'sfa2', 'sfa3', 'sf2', 'sf2ce']
snk_fight = ['kof94', 'kof95', 'kof96', 'kof97', 'kof98', 'kof99', 'rbff1', 'rbff2', 'rbffspec', 'samsho', 'samsho2', 'samsho3', 'samsho4', 'fatfury1', 'fatfury2', 'fatfury3', 'fatfurysp', 'aof', 'aof2' ]

retroarch_key = {}
advmame_key = {}
user_key = {}
capcom_map = {}
snk_map = {}
default_map = {}

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


def run_advj():
    #run_cmd('stdbuf -oL ' + ADVJ + ' -device_joystick raw > /tmp/advj &')
    #time.sleep(1)
    #run_cmd('killall -9 advj')

    print 'Move your joystick lever...'
    run_cmd('stdbuf -oL ' + ADVJ + ' -device_joystick raw > /tmp/advj &')
    joy_index = ''
    ret_axis = ''
    while ret_axis == '':
        f = open('/tmp/advj', 'r')
        while ret_axis == '':
            line = f.readline()
            if not line: 
                break
            if '65536' in line:
                words = line.split(',')
                joy_index = words[0]
                axises = words[2].replace(' ','').split(']')
                #print axises
                for axis in axises:
                    if '65536' in axis:
                        print 'Axis ' + axis[0] + ' detected!'
                        ret_axis = axis[0]
                        break
                #words = line.split()
                #if words[1] != '(':
                #    key = words[1][2:]
        else:
            time.sleep(0.1)
    advmame_key['axis'] = ret_axis
    run_cmd('killall -9 advj')
    f.close()

    fr = open('/tmp/advj', 'r')
    line = fr.readline() # skip the 1st line
    dev_name = ''
    while True:
        line = fr.readline()
        if not line: 
            break
        if line[:3] == 'joy':
            words = line.split("'")
            #words = words[0].split(" ")
            fw = open('/tmp/' + words[3].replace("'","") + '.advj', 'w')
            if line[:len(joy_index)] == joy_index:
                dev_name = words[3].replace("'","")
        if line == '\n':
            fw.close()
            break
        fw.write(line)
    fr.close()    

    return dev_name


def load_es_cfg():
    doc = ET.parse(ES_INPUT)
    root = doc.getroot()
    #tag = root.find('inputConfig')
    tags = root.findall('inputConfig')
    num = 1
    for i in tags:
        print str(num) + ". " + i.attrib['deviceName']
        num = num+1
    dev_select = input('\nSelect a layout for capcom fighting games: ')

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

    f = open('/tmp/' + dev_name + '.advj', 'r')
    while True:
        line = f.readline()
        if not line or line == '\n': 
            break   
        line = line.replace('\n','')
        words = line.split()
        if words[0] == 'joy':
            advmame_key['id'] = words[2].replace("\'","")
        if words[0] == 'button':
            value = words[2].replace('[','')
            value = value.replace(']','')
            advmame_key[words[1]] = value
    f.close()
    #print 'Advmame Key:', advmame_key, '\n'

    
def get_advmame_key():

    run_cmd('stdbuf -oL ' + ADVJ + ' > /tmp/advj &')
    key = ''
    while True:
        f = open('/tmp/advj', 'r')
        while True:
            line = f.readline()
            if not line: 
                break
            if '->' in line:
                words = line.split()
                if words[1] != '(':
                    key = words[1][2:]
        if key != '':
            break
        else:
            time.sleep(0.1)
    run_cmd('killall -9 advj')
    return key


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
            user_key['1'] = retroarch_key['x']
            user_key['2'] = retroarch_key['y']
            user_key['3'] = retroarch_key['l']
            user_key['4'] = retroarch_key['a']
            user_key['5'] = retroarch_key['b']
            user_key['6'] = retroarch_key['r']
        elif es_conf == 2:
            user_key['1'] = retroarch_key['y']
            user_key['2'] = retroarch_key['x']
            user_key['3'] = retroarch_key['l']
            user_key['4'] = retroarch_key['b']
            user_key['5'] = retroarch_key['a']
            user_key['6'] = retroarch_key['r']
        elif es_conf == 3:
            user_key['1'] = retroarch_key['l']
            user_key['2'] = retroarch_key['y']
            user_key['3'] = retroarch_key['x']
            user_key['4'] = retroarch_key['r']
            user_key['5'] = retroarch_key['b']
            user_key['6'] = retroarch_key['a']
        '''
        if es_conf == 1:
            key_order = ['x', 'y', 'l', 'a', 'b', 'r', 'select', 'start']
        elif es_conf == 2:
            key_order = ['y', 'x', 'l', 'b', 'a', 'r', 'select', 'start']
        elif es_conf == 3:
            key_order = ['l', 'y', 'x', 'r', 'b', 'a', 'select', 'start']

        i = 0
        for key in key_order:
            print 'Push ' + key_order[i].capitalize() + ' button'
            res = get_advmame_key()
            print '->', res
            i = i+1
            if i < 7:
                user_key[str(i)] = res
                advmame_key[key] = res
            elif i == 7:
                user_key['select'] = res
            elif i == 8:
                user_key['start'] = res
        '''
        #print user_key


def set_keymap():

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
            capcom_map['1'] = user_key['1']
            capcom_map['2'] = user_key['2']
            capcom_map['3'] = user_key['3']
            capcom_map['4'] = user_key['4']
            capcom_map['5'] = user_key['5']
            capcom_map['6'] = user_key['6']
        elif capcom_conf == 2:
            capcom_map['1'] = user_key['4']
            capcom_map['2'] = user_key['5']
            capcom_map['3'] = user_key['6']
            capcom_map['4'] = user_key['1']
            capcom_map['5'] = user_key['2']
            capcom_map['6'] = user_key['3']

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
            snk_map['1'] = user_key['4']
            snk_map['2'] = user_key['5']
            snk_map['3'] = user_key['1']
            snk_map['4'] = user_key['2']
        elif snk_conf == 2:
            snk_map['1'] = user_key['1']
            snk_map['2'] = user_key['2']
            snk_map['3'] = user_key['4']
            snk_map['4'] = user_key['5']
        elif snk_conf == 3:
            snk_map['1'] = user_key['4']
            snk_map['2'] = user_key['5']
            snk_map['3'] = user_key['6']
            snk_map['4'] = user_key['1']

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
            default_map['1'] = user_key['4']
            default_map['2'] = user_key['5']
            default_map['3'] = user_key['1']
            default_map['4'] = user_key['2']
        elif default_conf == 2:
            default_map['1'] = user_key['1']
            default_map['2'] = user_key['2']
            default_map['3'] = user_key['4']
            default_map['4'] = user_key['5']
        elif default_conf == 3:
            default_map['1'] = user_key['4']
            default_map['2'] = user_key['5']
            default_map['3'] = user_key['6']
            default_map['4'] = user_key['1']


def update_advmame_rc(index):
 
        if index == 1:
            target = ['p1_button', 'ui_configure', 'ui_select', 'ui_cancel', 'ui_up', 'ui_down', 'p1_up', 'p1_down', 'p1_left', 'p1_right', 'start1', 'coin1']
        elif index == 2:
            target = ['p2_button', 'p2_up', 'p2_down', 'p2_left', 'p2_right', 'start2', 'coin2']
    
        buf = ''
        f = open(ADVMAME_RC, 'r')
        while True:
            line = f.readline()
            if not line: 
                break
            is_target = 0
            for i in target:
                if i in line:
                    is_target = 1
                    break
            if is_target == 1: 
                continue
            if 'device_joystick' in line:
                line = 'device_joystick raw\n'
            buf += line
        f.close()

        f = open(ADVMAME_RC, 'w')

        # add common keys
        direct_map = {}
        direct_map['h0up'] = ',' + advmame_key['axis'] + ',1,1'
        direct_map['h0down'] = ',' + advmame_key['axis'] + ',1,0'
        direct_map['h0left'] = ',' + advmame_key['axis'] + ',0,1'
        direct_map['h0right'] = ',' + advmame_key['axis'] + ',0,0'
        direct_map['-1'] = ',' + advmame_key['axis'] + ',1,1'
        direct_map['+1'] = ',' + advmame_key['axis'] + ',1,0'
        direct_map['-0'] = ',' + advmame_key['axis'] + ',0,1'
        direct_map['+0'] = ',' + advmame_key['axis'] + ',0,0'
        joystick_id = advmame_key['id']
        adv_select = 'joystick_button[' + joystick_id + ',' + advmame_key[retroarch_key['select']] + ']'
        adv_start = 'joystick_button[' + joystick_id + ',' + advmame_key[retroarch_key['start']] + ']'
        adv_y = 'joystick_button[' + joystick_id + ',' + advmame_key[retroarch_key['y']] + ']'
        adv_a = 'joystick_button[' + joystick_id + ',' + advmame_key[retroarch_key['a']] + ']'

        if index == 1:
            buf += 'input_map[ui_configure] keyboard[0,tab] or ' + adv_y + ' ' + adv_select + '\n'
            buf += 'input_map[ui_select] keyboard[0,enter] or ' + adv_a + '\n'
            buf += 'input_map[ui_cancel] keyboard[0,esc] or ' + adv_select + ' ' + adv_start + '\n'
            buf += 'input_map[ui_up] keyboard[0,up] or joystick_digital[' + joystick_id + direct_map[retroarch_key['up']] + ']\n' 
            buf += 'input_map[ui_down] keyboard[0,down] or joystick_digital[' + joystick_id + direct_map[retroarch_key['down']] + ']\n'
            buf += 'input_map[p1_up] keyboard[0,up] or joystick_digital[' + joystick_id + direct_map[retroarch_key['up']] + ']\n'
            buf += 'input_map[p1_down] keyboard[0,down] or joystick_digital[' + joystick_id + direct_map[retroarch_key['down']] + ']\n'
            buf += 'input_map[p1_left] keyboard[0,left] or joystick_digital[' + joystick_id + direct_map[retroarch_key['left']] + ']\n'
            buf += 'input_map[p1_right] keyboard[0,right] or joystick_digital[' + joystick_id + direct_map[retroarch_key['right']] + ']\n'
            buf += 'input_map[start1] keyboard[0,1] or ' + adv_start + '\n'
            buf += 'input_map[coin1] keyboard[0,5] or ' + adv_select + '\n'
        elif index == 2:
            buf += 'input_map[p2_up] joystick_digital[' + joystick_id + direct_map[retroarch_key['up']] + ']\n'
            buf += 'input_map[p2_down] joystick_digital[' + joystick_id + direct_map[retroarch_key['down']] + ']\n'
            buf += 'input_map[p2_left] joystick_digital[' + joystick_id + direct_map[retroarch_key['left']] + ']\n'
            buf += 'input_map[p2_right] joystick_digital[' + joystick_id + direct_map[retroarch_key['right']] + ']\n'
            buf += 'input_map[start2] ' + adv_start + '\n'
            buf += 'input_map[coin2] ' + adv_select + '\n'
 
        # print default_map
        for key in default_map:
            res = 'input_map[p' + str(index) + '_button' + key + '] joystick_button[' + joystick_id + ',' + default_map[key] + ']'
            buf += res + '\n'
            #print res
        # print capcom_map
        for game in capcom_fight:
            for key in capcom_map:
                res = game + '/input_map[p' + str(index) + '_button' + key + '] joystick_button[' + joystick_id + ',' + capcom_map[key] + ']'
                buf += res + '\n'
                #print res
        # print snk_map
        for game in snk_fight:
            for key in snk_map:
                res = game + '/input_map[p' + str(index) + '_button' + key + '] joystick_button[' + joystick_id + ',' + snk_map[key] + ']'
                buf += res + '\n'
                #print res
        f.write(buf)
        f.close()


if __name__ == "__main__":

    index = int(sys.argv[1])

    print '\n****************************'
    print '** KeyMapper for Advmame **'
    print '****************************\n'

    #dev_name = run_advj()
    dev_name = load_es_cfg()
    load_retroarch_cfg(dev_name)
    load_layout()
    set_keymap()
    update_advmame_rc(index)


