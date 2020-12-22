#time in hour format, range 0 to 23
current_time = 0

time_dict = {
        "เที่ยงคืน": 0,
        "ตีหนึ่ง": 1,
        "ตีสอง": 2,
        "ตีสาม": 3,
        "ตีสี่": 4,
        "ตีห้า": 5,
        "หกโมงเช้า": 6,
        "เจ็ดโมง": 7,
        "แปดโมง": 8,
        "เก้าโมง": 9,
        "สิบโมง": 10,
        "สิบเอ็ดโมง": 11,
        "เที่ยงวัน": 12,
        "บ่ายโมง": 13,
        "บ่ายสอง": 14,
        "บ่ายสาม": 15,
        "สี่โมง": 16,
        "ห้าโมง": 17,
        "หกโมงเย็น": 18,
        "หนึ่งทุ่ม": 19,
        "สองทุ่ม": 20,
        "สามทุ่ม": 21,
        "สี่ทุ่ม": 22,
        "ห้าทุ่ม": 23
    }

class House:
    owner_name = ""
    rooms = {}
    scheduled_times = []

    obj_lists = {
            "ไฟ": "light",
            "ก๊อกน้ำ": "water"
        }

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
        command_open_index = str_command.find("เปิด")
        command_close_index = str_command.find("ปิด")
        if command_open_index == 0 :
            command = "turn_on"
        if command_close_index == 0 :
            command = "turn_off"

        #Object detector, in case there's more than just a light
        obj_target = ""
        for obj in self.obj_lists :
            if obj in str_command:
                obj_target = self.obj_lists[obj]
                break

        #Room reading, it catches the first added rooms first.
        room_name = ""
        for room in self.rooms :
            if room in str_command:
                room_name = room
                break

        #Scheduler, optional one
        global time_dict
        time_cmd = ""
        time_cmd_hour = 0
        for time in time_dict:
            if time in str_command:
                time_cmd = time
                time_cmd_hour = time_dict[time]
                break
        
        #End if required texts are not present
        if (command == "") or (obj_target == "") or (room_name == ""):
            print("Invalid Command")
            return

        #simple trigger without scheduled time
        if time_cmd == "":
            self.trigger(command, obj_target, room_name)
        else:
            #scheduled time, by append time
            self.scheduled_times.append({
                    "command": command,
                    "obj_target": obj_target,
                    "room_name": room_name,
                    "time_cmd_hour": time_cmd_hour
                })
            print(f"Scheduled : %s, %s, %s, %d:00" % (command, obj_target, room_name, time_cmd_hour))
            return

        print("Done!")

    def trigger(self, command, obj_target, room_name):
        #command, obj_target, room_name, are all strings
        target_room = self.rooms[room_name]
        if command == "turn_on":
            target_room.trigger_on(obj_target)
        elif command =="turn_off":
            target_room.trigger_off(obj_target)

    def print_all_rooms_stages(self):
        for room in self.rooms :
            self.rooms[room].print_stage()

    def display_time(self):
        global current_time
        print(f"Now %d:00." % (current_time))

    def progress_an_hour(self):
        global current_time
        if current_time < 24:
            current_time += 1
        else :
            current_time = 0
        print(f"An hour has passed, now %d:00." % (current_time))
        
        #if reached the schedule, trigger light
        for schedule in self.scheduled_times:
            if current_time == schedule["time_cmd_hour"] :
                command = schedule["command"]
                obj_target = schedule["obj_target"]
                room_name = schedule["room_name"]
                self.trigger(command, obj_target, room_name)
                print("Time : Scheduled operation complete!")
        

class Room:
    room_name = ""
    room_str = ""
    light_open = False
    water_open = False

    def __init__(self, room_name, room_str):
        self.room_name = room_name
        self.room_str = room_str

    def trigger_on(self, obj):
        #obj is a string
        if obj == "light" :
            self.light_open = True
        elif obj == "water":
            self.water_open = True

    def trigger_off(self, obj):
        #obj is a string
        if obj == "light" :
            self.light_open = False
        elif obj == "water":
            self.water_open = False

    def print_stage(self):
        light_status = ""
        water_status = ""
        
        if self.light_open :
            light_status = "on"
        else :
            light_status = "off"
            
        if self.water_open :
            water_status = "on"
        else :
            water_status = "off"
            
        print(f"%s : light %s, water %s" % (self.room_name, light_status, water_status))


house = House("My House")
house.add_room("bed_room","ห้องนอน")
house.add_room("bath_room","ห้องน้ำ")
house.add_room("kitchen","ห้องครัว")

print(house.owner_name)

print()
print("Stage 1")
house.display_time()
house.print_all_rooms_stages()
print()

house.command("เปิดไฟห้องนอนหน่อย")

print()
print("Stage 2")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("ปิดไฟห้องนอนหน่อย")
house.command("เปิดไฟห้องครัวหน่อย")

print()
print("Stage 3")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("หน่อย")
house.command("อะไร")
house.command("ห้องครัว")
house.command("ปิดไฟ")
house.command("เปิดห้องนอน")
house.command("เปิดห้องก๊อกน้ำ")

print()
print("Stage 4")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("เปิดไฟห้องนอนตอนหกโมงเช้าหน่อย")
house.command("เปิดไฟห้องน้ำตอนเจ็ดโมงเช้าหน่อย")

print()
print("Stage 5")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("เปิดก๊อกน้ำห้องน้ำตอนเจ็ดโมงเช้าหน่อย")
house.command("เปิดก๊อกน้ำห้องครัวตอนแปดโมงเช้าหน่อย")

print()
print("Stage 6")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("ปิดก๊อกน้ำห้องน้ำตอนแปดโมงเช้าหน่อย")

print()
print("Stage 7")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

print()
print("Stage 8")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

print()
print("Stage 9")
house.progress_an_hour()
house.print_all_rooms_stages()
print()
