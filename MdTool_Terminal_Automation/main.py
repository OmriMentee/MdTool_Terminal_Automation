# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import keyboard
import time
import os
from Mdtool_automtion import MdtoolAutomationTool


def approve_calib():
    keyboard.write(" Y", delay=0.1)
    keyboard.press("enter")


def auto_calibraion(id):
    keyboard.write(" Y", delay=0.1)
    keyboard.press("enter")
    os.system("mdtool setup calibration " + str(id))


def auto_ping(baud):
    os.system("mdtool ping " + baud)


def get_motor_id_list(baud):
    ID_LENGTH = 5
    # Get ping cmd txt plot into list
    ping_txt_list = os.popen(
        'mdtool ping ' + baud).readlines()  # Ask mdtool for setup info and stor it in list of strings

    cut_from_ind = 0
    # Find relevant text from ping cmd and cut unnecessary text:
    for line in ping_txt_list:
        if line.find("1:") != -1:
            cut_from_ind = ping_txt_list.index(line)
            break
    dirty_motor_list = ping_txt_list[cut_from_ind:]

    # create relevant motor list:
    relevant_id_list = []
    for line in dirty_motor_list:
        not_trimmed_id = line[line.find("=") + 1:line.find("=") + ID_LENGTH]
        relevant_id_list.append(not_trimmed_id.strip())
    return relevant_id_list


# def get_setup_txt(id_for_txt)

def get_setup_error(id_str):
    # Will return error string for given motor id
    # TODO: add exception for non id case
    NO_SETUP_ERROR = "0x0"  # TODO: move this to const list
    setup_txt_list = os.popen(
        'mdtool setup info ' + id_str).readlines()  # Ask mdtool for setup info and stor it in list of strings
    error_line = setup_txt_list.pop()  # Error value is the last item in setup info
    error_value = error_line[error_line.index(":") + 1:]
    error_value = error_value.strip()
    # print(error_value)
    # if error_value != NO_SETUP_ERROR:
    #     print("error not good man!")
    # else:
    #     print("yyay")
    return error_value


def get_motor_name(id_for_name):
    # Will return error string for given motor id
    # TODO: add exception for non id case
    NO_SETUP_ERROR = "0x0"  # TODO: move this to const list
    setup_txt_list = os.popen(
        'mdtool setup info ' + id_for_name).readlines()  # Ask mdtool for setup info and stor it in list of strings
    name_ind = 0
    for line in setup_txt_list:
        if line.find("name") != -1:
            name_ind = setup_txt_list.index(line)
            break
    name_line = setup_txt_list[name_ind]

    return name_line


def set_new_id(curr_id, new_id):
    # mdtool config can <current ID> <new ID> <baud> <watchdog period[ms]> <termination>
    cmd_str = 'mdtool config can ' + curr_id + ' ' + new_id + ' ' + '8M 200'
    md_reply_txt = os.popen(cmd_str).readlines()  # Ask mdtool for to change id with const baud of 8M and 200ms WD


def set_new_baud(id_baud, baud):
    # mdtool config can <current ID> <new ID> <baud> <watchdog period[ms]> <termination>
    cmd_str = 'mdtool config can ' + id_baud + ' ' + id_baud + ' ' + baud + ' ' + '200'
    md_reply_txt = os.popen(cmd_str).readlines()  # Ask mdtool for to change baud with const 200ms WD - id stay the same


def save_changes(id):
    # mdtool config can <current ID> <new ID> <baud> <watchdog period[ms]> <termination>
    cmd_str = 'mdtool config save ' + id
    os.system(cmd_str)
    # md_reply_txt = os.popen(cmd_str).readlines()
    # time.sleep(1)
    # cmd_str = 'mdtool setup save ' + id
    # os.system(cmd_str)
    # md_reply_txt = os.popen(cmd_str).readlines()


def get_id_from_sn(sn):
    int_id = 199 + sn
    str_id = str(int_id)
    return str_id


def set_name_for_new_motor(sn):
    # change id and save:
    id_str = get_id_from_sn(sn)
    set_new_id("69", id_str)
    time.sleep(3)
    save_changes(id_str)


def motor_setup_arm_Right():
    s_time = 2
    os.system('mdtool setup motor 200 RMD-X8-S2_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 201 RMD-X8-S2_Hitmp.cfg')
    time.sleep(s_time)
    save_changes("200")
    time.sleep(s_time)
    save_changes("201")

    os.system('mdtool setup motor 202 RMD-X6-S2_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 203 RMD-X6-S2_Hitmp.cfg')
    time.sleep(s_time)
    save_changes("202")
    time.sleep(s_time)
    save_changes("203")

    os.system('mdtool setup motor 204 RMD-X6_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 205 RMD-X6_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 206 RMD-X6_Hitmp.cfg')
    time.sleep(s_time)
    save_changes("204")
    time.sleep(s_time)
    save_changes("205")
    time.sleep(s_time)
    save_changes("206")


def motor_setup_arm_Left():
    s_time = 2
    os.system('mdtool setup motor 207 RMD-X8-S2_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 208 RMD-X8-S2_Hitmp.cfg')
    time.sleep(s_time)
    save_changes("207")
    time.sleep(s_time)
    save_changes("208")

    os.system('mdtool setup motor 209 RMD-X6-S2_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 210 RMD-X6-S2_Hitmp.cfg')
    time.sleep(s_time)
    save_changes("209")
    time.sleep(s_time)
    save_changes("210")

    os.system('mdtool setup motor 211 RMD-X6_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 212 RMD-X6_Hitmp.cfg')
    time.sleep(s_time)
    os.system('mdtool setup motor 213 RMD-X6_Hitmp.cfg')
    time.sleep(s_time)
    save_changes("211")
    time.sleep(s_time)
    save_changes("212")
    time.sleep(s_time)
    save_changes("213")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #
    # lines=[]
    # with open('/home/omri/Downloads/test_arm.csv', 'rt') as f:
    #     data = csv.reader(f)
    #     for row in data:
    #         print(row)
    #         lines.append(row)
    #
    # print(lines[1])

    # set_new_baud("210", "1M")
    # set_new_baud("211", "1M")
    # set_new_baud("212", "1M")
    tool_obj = MdtoolAutomationTool()
    tool_obj.get_motor_type_list()
    # print(tool_obj.get_all_error_codes())

    # tool_obj.set_same_baud("8M")

    tool_obj.set_zero_for_all()

    # save_changes("207")
    # save_changes("208")
    # save_changes("209")
    # save_changes("210")
    # save_changes("211")
    # save_changes("212")
    # save_changes("213")


    # tool_obj.calibrate_motor("209")
    # tool_obj.auto_calibrate_all(True)
    #
    # sn = 14
    # set_name_for_new_motor(sn)

    # motor_setup_arm_Right()

    # motor_setup_arm_Left()

#
# id_list = get_motor_id_list("8M")
# for rel_id in id_list:
#     print(get_setup_error(rel_id))
#     print(f"motor id {rel_id} " + get_motor_name(rel_id))

#     # get_setup_error(222)
