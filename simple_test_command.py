class Room:
    room_name = ""
    light_open = False

    def __init__(self, room_name):
        self.room_name = room_name

    def read_command(self, str_command):

        index = str_command.find("เปิดไฟ")
        room_name_index = str_command.find(self.room_name)

        if (index != -1) and (room_name_index != -1):
            self.trigger_light()
            #print(index)
        else:
            print("error")
        
    def trigger_light(self):
        if self.light_open :
            self.light_open = False
        else :
            self.light_open = True

    def print_stage(self):
        print(self.room_name)
        if self.light_open :
            print("ไฟเปิดอยู่")
        else :
            print("ไฟปิดแล้ว")


room1 = Room("ห้องนอน")

room1.print_stage()
room1.read_command("เปิดไฟในห้องน้ำหน่อย")
room1.print_stage()
room1.read_command("เปิดไฟในห้องนอนหน่อย")
room1.print_stage()
