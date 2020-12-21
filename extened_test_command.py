current_time = 0

time_dict = {
        "เที่ยงคืน": "0:00",
        "ตีหนึ่ง": "1:00",
        "เจ็ดโมงเช้า": "7:00",
        "บ่ายโมง": "13:00",
        "สามทุ่ม": "21:00"
    }

class House:
    owner_name = ""
    rooms = {}

    def __init__(self, owner_name):
        self.owner_name = owner_name

    def add_room(self, room_name, room_str):
        room = Room(room_name, room_str)
        #add key and value of rooms
        self.rooms.update({room_str: room})

    def command(self, str_command):
        print("Reading command : "+str_command)
        #Command reading, only works if the required words are at the start.
        command = ""
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

        #Scheduler, optional one
        global time_dict
        time_cmd = ""
        for time in time_dict:
            if time in str_command:
                time_cmd = time
                break
        
        #End if required texts are not present
        if command == "" and room_name == "":
            print("Invalid Command and Room!")
            return
        if command == "":
            print("Invalid Command!")
            return
        if room_name == "":
            print("Invalid Room!")
            return

        #simple trigger without scheduled time
        if time_cmd == "":
            target_room = self.rooms[room_name]
            if command == "turn_on_light":
                target_room.trigger_light_on()
            elif command =="turn_off_light":
                target_room.trigger_light_off()

        print("Done!")

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
            print(self.room_name+" : light on")
        else :
            print(self.room_name+" : light off")


house = House("My House")
house.add_room("bed_room","ห้องนอน")
house.add_room("bath_room","ห้องน้ำ")
house.add_room("kitchen","ห้องครัว")

print(house.owner_name)

print()
print("Stage 1")
house.print_all_rooms_stages()
print()

house.command("เปิดไฟห้องนอนหน่อย")

print()
print("Stage 2")
house.print_all_rooms_stages()
print()

house.command("ปิดไฟห้องนอนหน่อย")
house.command("เปิดไฟห้องครัวหน่อย")

print()
print("Stage 3")
house.print_all_rooms_stages()
print()

house.command("หน่อย")
house.command("อะไร")
house.command("ห้องครัว")
house.command("ปิดไฟ")

print()
print("Stage 4")
house.print_all_rooms_stages()
print()
