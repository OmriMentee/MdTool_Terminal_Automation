import keyboard
import time
import os

from Can_motor_class import Can_motor_class

# Const list
BAUD_1M = "1M"
BAUD_2M = "2M"
BAUD_5M = "5M"
BAUD_8M = "8M"
INDEX_1M = 0
INDEX_8M = 1
NO_ERROR = "0x0"


class MdtoolAutomationTool:
    def __init__(self):
        self.clean_id_lists = None
        self.clean_baud_lines = None
        self.id_lists_with_txt = None
        self.relevant_id_list = None

        self.num_of_motors = None

        self.id_list_1M = None
        self.id_list_2M = None
        self.id_list_5M = None
        self.id_list_8M = None

        self.update_mdtool_data()

    def update_mdtool_data(self):
        self.get_id_lists()  # that's where clean lists
        self.id_list_1M = self.get_baud_list(BAUD_1M)
        self.id_list_2M = self.get_baud_list(BAUD_2M)
        self.id_list_5M = self.get_baud_list(BAUD_5M)
        self.id_list_8M = self.get_baud_list(BAUD_8M)
        self.num_of_motors = len(self.id_list_1M) + len(self.id_list_2M) + len(self.id_list_5M) + len(self.id_list_8M)
        print("1M motors id list: {}".format(self.id_list_1M))
        print("8M motors id list: {} \n".format(self.id_list_8M))
        print("total number of motor is: {}".format(self.num_of_motors))

    def create_motor_list(self, baud):
        motor_list = []
        if baud == BAUD_1M:
            relevant_list = self.id_list_1M
        elif baud == BAUD_8M:
            relevant_list = self.id_list_8M
        else:
            print("cant create motor list - baud error")
            return

        for id in relevant_list:
            new_motor = Can_motor_class()
            new_motor.set_motor_id(id)
            new_motor.set_motor_baud(baud)
            motor_list.append(new_motor)
        if len(motor_list) <= 0:
            print("list was not created")
            return

        return motor_list

    def get_id_lists(self):
        # TODO: added connection issue exception here

        ping_txt_list = os.popen(
            'mdtool ping all').readlines()  # Ask mdtool for setup info and stor it in list of strings

        cut_from_ind = []
        # Find relevant text from ping cmd and cut unnecessary text:
        for line in ping_txt_list:
            # print("this is line {}".format(line.strip()) + " line[0] is {}".format(line[0]))
            # print("line[0] is {}".format(line[0]))
            if line.find("1:") != -1:
                cut_from_ind.append(ping_txt_list.index(line))

        # Take relevant lines with unnecessary 'dirty' txt in
        dirty_motor_lists = []
        dirty_baud_lines = []
        for ind in cut_from_ind:
            dirty_motor_lists.append(ping_txt_list[ind:])
            dirty_baud_lines.append(ping_txt_list[ind - 2])

        # Take only id txt from lines:
        self.id_lists_with_txt = []
        for dirty_list in dirty_motor_lists:
            # print(dirty_list)
            if dirty_motor_lists.index(dirty_list) == len(dirty_motor_lists) - 1:
                self.id_lists_with_txt.append(dirty_list)
            else:
                for item in dirty_list:
                    # print("this is item: {}".format(item))
                    if item.find('[') == 0:
                        self.id_lists_with_txt.append(
                            dirty_list[dirty_motor_lists.index(dirty_list):dirty_list.index(item)])
                        break

        # Take only the bauds that was found
        self.clean_baud_lines = []
        for dirty_baud in dirty_baud_lines:
            m_index = dirty_baud.index("M")
            self.clean_baud_lines.append(dirty_baud[m_index - 1:m_index + 1])

        # clean txt from id_lists_with_txt:
        ID_LENGTH = 5
        self.clean_id_lists = []
        for baud_group in self.id_lists_with_txt:
            clean_id_group = []
            for id_with_txt in baud_group:
                if id_with_txt.find("=") != -1:
                    not_trimmed_id = id_with_txt[id_with_txt.find("=") + 1:id_with_txt.find("=") + ID_LENGTH]
                    clean_id_group.append(not_trimmed_id.strip())
                else:
                    break
            self.clean_id_lists.append(clean_id_group)

        # print("this is id_lists_with_txt: {}".format(self.id_lists_with_txt))
        print("this is id_lists_with_txt: {}".format(self.id_lists_with_txt))
        print("this is clean_baud_lines: {}".format(self.clean_baud_lines))
        print("this is clean_id_lists: {}".format(self.clean_id_lists))

    def get_baud_list(self, baud):
        if baud not in self.clean_baud_lines:
            print("get_baud_list: " + baud + " not found")
            return [-1]
        baud_index = self.clean_baud_lines.index(baud)
        relevant_list_with_txt = self.clean_id_lists[baud_index]
        return relevant_list_with_txt

    def set_motor_id(self, motor_id, new_id):
        # TODO: this method should check if id is actual new before changing it
        motor_baud = get_motor_baud(motor_id)
        # mdtool config can <current ID> <new ID> <baud> <watchdog period[ms]> <termination>
        cmd_str = 'mdtool config can ' + motor_id + ' ' + new_id + ' ' + motor_baud + ' ' + '200'
        md_reply_txt = os.popen(
            cmd_str).readlines()  # Ask mdtool for to change baud with const 200ms WD - id stay the same

        pass

    def set_motor_baud(self, motor_id, new_baud):
        # mdtool config can <current ID> <new ID> <baud> <watchdog period[ms]> <termination>
        cmd_str = 'mdtool config can ' + motor_id + ' ' + motor_id + ' ' + new_baud + ' ' + '200'
        md_reply_txt = os.popen(
            cmd_str).readlines()  # Ask mdtool for to change baud with const 200ms WD - id stay the same

    def set_same_baud(self, new_baud):
        # init vars:
        baud_changed = False
        for same_baud_list in self.clean_id_lists:
            current_baud_group = self.clean_baud_lines[self.clean_id_lists.index(same_baud_list)]
            if current_baud_group == new_baud:
                print("no need to replace" + str(same_baud_list) + " it is already in baud " + new_baud)
                baud_changed = True
                continue
            else:
                for motor in same_baud_list:
                    self.set_motor_baud(motor, new_baud)
                    print("motor id " + motor + " baud changed to " + new_baud)
                    baud_changed = True

        # TBD - added set verification
        if baud_changed == False:
            print("ERROR: new baud was not set.")
            return False

        return True

    def get_motor_baud(self, motor_id):
        # retuns motor's baud for given id
        motor_baud = ""
        if self.id_list_1M.index(motor_id) != -1:
            motor_baud = BAUD_1M
        elif self.id_list_8M.index(motor_id) != -1:
            motor_baud = BAUD_8M
        else:
            print("ERROR: motor ID not found")

        return motor_baud

    def get_motor_error_code(self, motor_id):
        # Will return error string for given motor id
        # TODO: add exception for non id case
        NO_SETUP_ERROR = "0x0"  # TODO: move this to const list
        setup_txt_list = os.popen(
            'mdtool setup info ' + motor_id).readlines()  # Ask mdtool for setup info and stor it in list of strings
        error_line = setup_txt_list.pop()  # Error value is the last item in setup info
        error_value = error_line[error_line.index(":") + 1:]
        error_value = error_value.strip()
        # print(error_value)
        # if error_value != NO_SETUP_ERROR:
        #     print("error not good man!")
        # else:
        #     print("yyay")
        return error_value

    def get_all_error_codes(self):
        # TODO: error list and the rest here should be represented as dict
        all_bauds_errors = []
        for baud_group in self.clean_id_lists:
            error_list = []
            for motor in baud_group:
                # print(motor + " error code is: " + self.get_motor_error_code(motor))
                error_list.append(self.get_motor_error_code(motor))

            all_bauds_errors.append(error_list)

        # TODO: added error nuber verification
        # if len(error_list) != self.num_of_motors:
        #     print("get error list ERROR")
        #
        return all_bauds_errors

    def get_motor_type(self, motor_id):
        # Will return error string for given motor id
        # TODO: add exception for non id case
        NO_SETUP_ERROR = "0x0"  # TODO: move this to const list
        setup_txt_list = os.popen(
            'mdtool setup info ' + motor_id).readlines()  # Ask mdtool for setup info and stor it in list of strings
        type_ind = 0
        for line in setup_txt_list:
            if line.find("name") != -1:
                type_ind = setup_txt_list.index(line)
                break
        type_line = setup_txt_list[type_ind]
        return type_line

    def get_motor_type_list(self):
        for baud_group in self.clean_id_lists:
            for motor in baud_group:
                motor_type = self.get_motor_type(motor)
                print(motor + motor_type)

    def calibrate_motor(self, motor_id, error_verification=False):
        # init vars:
        motor_is_calibrated = False

        error_state = ""

        keyboard.write(" Y", delay=0.3)
        keyboard.press_and_release("enter")
        os.system("mdtool setup calibration " + motor_id)

        if error_verification == True:
            motor_is_calibrated = False
            time.sleep(30)
            error_state = self.get_motor_error_code(motor_id)
            if error_state != NO_ERROR:
                print("motor " + motor_id + "have the following error: " + error_state)
                motor_is_calibrated = False  # this line is redundant
            else:
                motor_is_calibrated = True
                print("motor " + motor_id + " calibration done without errors. error state= " + error_state)
        else:
            motor_is_calibrated = True

        return motor_is_calibrated

    def auto_calibrate_all(self, error_verification=False):
        for baud_group in self.clean_id_lists:
            ind_calib_done = False
            for motor in baud_group:
                self.calibrate_motor(motor)
                time.sleep(1)
                print("################### sleep bet ################### ")

        error_lists = []
        if error_verification == True:
            motor_is_calibrated = False
            time.sleep(35)
            error_lists = self.get_all_error_codes()
            for baud_group_err in error_lists:
                for motor_err in baud_group_err:
                    if motor_err != NO_ERROR:
                        print("following error found: " + motor_err)
                        motor_is_calibrated = False  # this line is redundant
            print(error_lists)

            #         else:
            #                 motor_is_calibrated = True
            #                 print("motor " + motor_id + " calibration done without errors. error state= " + error_state)
            # motor_is_calibrated = True
            #     # while ind_calib_done==False:
            #     #     print("calibrating motor " + motor)
            #     #     time.sleep(0.5)

    def set_zero_pos_motor(self, motor_id):
        os.system("mdtool config zero " + motor_id)
        # TODO: tbd on using this output as verification.

        # set_zero_txt_list = os.popen(
        #     'mdtool config zero ' + motor_id).readlines()  # Ask mdtool for setup info and stor it in list of strings
        # # print ('zero')

    def set_zero_for_all(self):
        for baud_group in self.clean_id_lists:
            for motor in baud_group:
                self.set_zero_pos_motor(motor)


    ################################################
    ################################################
    ################################################
