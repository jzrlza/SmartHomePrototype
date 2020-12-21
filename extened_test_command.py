class House:

    owner_name = ""
    rooms = {}

    def __init__(self, owner_name):
        self.owner_name = owner_name

    def add_room(self, room_name, room_str):
        room = Room(room_name)

    def read_command(self, str_command):

        index = str_command.find("เปิดไฟ")
        ##room_name_index = str_command.find(self.room_name)

        if (index != -1) and (room_name_index != -1):
            self.trigger_light()
            #print(index)
        else:
            print("error")




class Room:
    room_name = ""
    light_open = False
    water_open = False

    def __init__(self, room_name):
        self.room_name = room_name

    def trigger_light_on(self):
        self.light_open = True

    def trigger_light_off(self):
        self.light_open = False

    def trigger_water_on(self):
        self.water_open = True

    def trigger_water_off(self):
        self.water_open = False
