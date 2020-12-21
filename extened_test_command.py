time_dict = {
        "เที่ยงคืน": "0:00"
        "ตีหนึ่ง": "1:00"
    }

class House:
    owner_name = ""
    rooms = {}
    time = 0

    def __init__(self, owner_name):
        self.owner_name = owner_name

    def add_room(self, room_name, room_str):
        room = Room(room_name, room_str)
        #add key and value of rooms
        self.rooms.update({room_str: room})

    def command(self, str_command):
        #Command reading, only works if the required words are at the start.
        command = "none"
        command_open_index = str_command.find("เปิดไฟ")
        command_close_index = str_command.find("ปิดไฟ")
        if command_open_index == 0 :
            command = "turn_on_light"
        if command_close_index == 0 :
            command = "turn_off_light"

        #Room reading, it catches the first added rooms first.
        room_name = ""
        for room in self.rooms :
            if room in str_command:
                room_name = room
                break
        
        time = ""

        #simple trigger without scheduled time
        target_room = self.rooms[room_name]
        if command == "turn_on_light":
            target_room.trigger_light_on()
        elif command =="turn_off_light":
            target_room.trigger_light_off()
        else:
            print("error")

    def print_all_rooms_stages(self):
        for room in self.rooms :
            self.rooms[room].print_stage()
        

class Room:
    room_name = ""
    room_str = ""
    light_open = False

    def __init__(self, room_name, room_str):
        self.room_name = room_name
        self.room_str = room_str

    def trigger_light_on(self):
        self.light_open = True

    def trigger_light_off(self):
        self.light_open = False

    def print_stage(self):
        if self.light_open :
            print(self.room_str+"ไฟเปิดอยู่")
        else :
            print(self.room_str+"ไฟปิดแล้ว")


house = House("My House")
house.add_room("bed_room","ห้องนอน")
house.add_room("bath_room","ห้องน้ำ")
house.add_room("kitchen","ห้องครัว")
print("Time 1")
house.print_all_rooms_stages()
house.command("เปิดไฟห้องนอนหน่อย")
print("Time 2")
house.print_all_rooms_stages()
