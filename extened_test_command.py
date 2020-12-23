#time in hour format, range 0 to 23.
current_time = 0

#time dictionary, Thai language with hour (o clock) numbers.
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

#House class, in case if we handle more than 1 houses, just in case.
class House:
    #::Attributes::
    #just a name, can be blank
    owner_name = ""

    #rooms, as dict, storing Room class object as value, its keys are Thai words.
    rooms = {}

    #scheduled times, as list, storing dicts of scheduled times
    scheduled_times = []

    #Objects to command, must be here as it is simpler
    obj_lists = {
            "ไฟ": "light",
            "ก๊อกน้ำ": "water"
        }

    #::Functions::
    #Initialize
    #"owner name" : is the name of the house's owner, can be blank as "".
    def __init__(self, owner_name):
        self.owner_name = owner_name

    #Add room
    #"room_name" : is the name of the room in English format
    #"room_str" : is the Thai text for refer the room
    def add_room(self, room_name, room_str):
        room = Room(room_name, room_str)
        #add key and value of rooms
        self.rooms.update({room_str: room})

    #Execute command
    #"str_command" : is the text command (string again), suppose it is the voice...
    #...where the house listens to you speaking, and do as you said by what it can do.
    def command(self, str_command):
        #Print
        print("Reading command : "+str_command)
        
        #Command reading, only works if the required words are at the start.
        command = ""
        command_open_index = str_command.find("เปิด")
        command_close_index = str_command.find("ปิด")
        if command_open_index == 0 :
            command = "turn_on"
        if command_close_index == 0 :
            command = "turn_off"

        #Object detector, in case there's more than just a light.
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

        #Scheduler, optional one, it catches the lower numbers first.
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

        #2 paths depends on wether scheduled time or not...
        if time_cmd == "":
            #path 1: simple trigger without scheduled time
            self.trigger(command, obj_target, room_name)
            print("Done!")
        else:
            #path 2: scheduled time, by append time
            self.scheduled_times.append({
                    "command": command,
                    "obj_target": obj_target,
                    "room_name": room_name,
                    "time_cmd_hour": time_cmd_hour
                })
            #Print what have been recorded, for notice the user.
            print(f"Scheduled : %s, %s, %s, %d:00" % (command, obj_target, room_name, time_cmd_hour))
        
    #Trigger the room by command.
    #"command" : is the string of command in Thai natural language, pretend it is a voice.
    #"obj_target" : is the string in English format of the target object to trigger
    #"room_name" : is the string in Thai format of the target room...
    #...it is in this format to handle dict "rooms = {}"
    def trigger(self, command, obj_target, room_name):
        #verify the room's existence
        target_room = self.rooms[room_name]

        #Trigger, choose between either "on" or "off".
        if command == "turn_on":
            target_room.trigger_on(obj_target)
        elif command =="turn_off":
            target_room.trigger_off(obj_target)

    #Print all the house's rooms' stages each.
    #It is this way because of command line format.
    def print_all_rooms_stages(self):
        for room in self.rooms :
            self.rooms[room].print_stage()

    #Print current time.
    def display_time(self):
        global current_time
        print(f"Now %d:00." % (current_time))

    #Progress an hour, use inside the house for lesser code complexity...
    #... because this is where the scheduled commands actually works here!!
    def progress_an_hour(self):
        global current_time
        if current_time < 24:
            current_time += 1
        else :
            current_time = 0
        print(f"An hour has passed, now %d:00." % (current_time))
        
        #If reached the schedule, trigger light!!
        for schedule in self.scheduled_times:
            if current_time == schedule["time_cmd_hour"] :
                command = schedule["command"]
                obj_target = schedule["obj_target"]
                room_name = schedule["room_name"]
                self.trigger(command, obj_target, room_name)
                print("Time : Scheduled operation complete!")
        
#Room class, since we totally need more than 1 rooms.
class Room:
    #::Attributes::
    #room name in English format
    room_name = ""

    #room name in Thai format
    room_str = ""

    #Objects' statuses
    light_open = False
    water_open = False

    #::Functions::
    #Initialize
    #"room_name" : is the room name in English format, cannot be blank.
    #"room_str" : is the room name in Thai format, cannot be blank.
    def __init__(self, room_name, room_str):
        self.room_name = room_name
        self.room_str = room_str

    #Trigger the object on.
    #"obj" : is a string refer to the target object as in English format.
    def trigger_on(self, obj):
        if obj == "light" :
            self.light_open = True
        elif obj == "water":
            self.water_open = True

    #Trigger the object off.
    #"obj" : is a string refer to the target object as in English format.
    def trigger_off(self, obj):
        if obj == "light" :
            self.light_open = False
        elif obj == "water":
            self.water_open = False

    #Print all objects' each of the stages, and also the room's overall current stage.
    def print_stage(self):
        #Dynamic according to what are on or off.
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

        #Print
        print(f"%s : light %s, water %s" % (self.room_name, light_status, water_status))


#Below are testing outputs codes

#Initilize the house, with 3 rooms
house = House("My House")
house.add_room("bed_room","ห้องนอน")
house.add_room("bath_room","ห้องน้ำ")
house.add_room("kitchen","ห้องครัว")

print(house.owner_name)

#Split in stages, in the following example, each stage is per one hour.
#Each stages may or may not execute commands in between.
#Although using Thai command, the display here is in English for an ease of use.
print()
print("Stage 1: Starting stage. At midnight.")
house.display_time()
house.print_all_rooms_stages()
print()

house.command("เปิดไฟห้องนอนหน่อย")

print()
print("Stage 2: Next hour, open bedroom's light.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("ปิดไฟห้องนอนหน่อย")
house.command("เปิดไฟห้องครัวหน่อย")

print()
print("Stage 3: Turn back off bedroom's light, turn on kitchen's instead.")
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
print("Stage 4: Nothing changed, due to a bunch of invalid commands.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("เปิดไฟห้องนอนตอนหกโมงเช้าหน่อย")
house.command("เปิดไฟห้องน้ำตอนเจ็ดโมงเช้าหน่อย")

print()
print("Stage 5: Nothing changed... yet, but soon. Scheduled 2 turn on light events.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("เปิดก๊อกน้ำห้องน้ำตอนเจ็ดโมงเช้าหน่อย")
house.command("เปิดก๊อกน้ำห้องครัวตอนแปดโมงเช้าหน่อย")

print()
print("Stage 6: Nothing changed... yet, but soon. Scheduled 2 turn on water events.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

house.command("ปิดก๊อกน้ำห้องน้ำตอนแปดโมงเช้าหน่อย")

print()
print("Stage 7: 1 scheduled event occur. Bathroom's water saving after 8 o clock.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

print()
print("Stage 8: 2 scheduled events occurs. Bathtime at morning.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()

print()
print("Stage 9: Final sample time, also 2 scheduled events occur.")
house.progress_an_hour()
house.print_all_rooms_stages()
print()
