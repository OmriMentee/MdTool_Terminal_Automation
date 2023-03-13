import math
import time
import pycandle
import keyboard
import time
import sys
import os
import subprocess

class Can_motor_class():
    def __init__(self):
        self.motor_id = ""
        self.motor_baud = ""
        self.motor_name = ""
        self.motor_type = ""
        self.error_code = ""
        self.is_calibrated = False
        self.motor_pos = ""


    #===================
    #=======SETERS======
    # ==================
    def set_motor_id(self,new_id):
        # TODO: this method should check if id is actual new before changing it
        pass

    def set_motor_baud(self,new_baud):
        # mdtool config can <current ID> <new ID> <baud> <watchdog period[ms]> <termination>
        cmd_str = 'mdtool config can ' + self.motor_id + ' ' + self.motor_id + ' ' + new_baud + ' ' + '200'
        md_reply_txt = os.popen(
            cmd_str).readlines()  # Ask mdtool for to change baud with const 200ms WD - id stay the same

    def calibrate_motor(self):
        pass

    def ser_zero_pos(self):
        pass

    # ===================
    # =======GETERS======
    # ==================
    def get_motor_id(self):
        return self.motor_id

    def get_motor_id(self):
        return self.motor_baud

    def get_motor_name(self):
        return self.motor_name

    def get_motor_type(self):
        return self.motor_type

    def get_erro_code(self):
        return self.error_code

    def get_motor_pos(self):
        return self.motor_pos



    ########################################
    ########################################

    import math
    import time
    import pycandle
    import keyboard
    import time
    import sys
    import os
    import subprocess

    def approve_calib():
        keyboard.write(" Y", delay=0.1)
        keyboard.press("enter")

    def auto_calibraion(id):
        keyboard.write(" Y", delay=0.1)
        keyboard.press("enter")
        os.system("mdtool setup calibration " + str(id))

    def auto_ping(baud):
        os.system("mdtool ping " + baud)

    def auto_ping_all(baud):
        os.system("mdtool ping all")


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

    def ger_motor_name(id_for_name):
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
