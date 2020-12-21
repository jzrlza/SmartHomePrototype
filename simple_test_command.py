fullstring = "เปิดไฟห้องนอนหน่อย"
substring = "ไฟ"

index = fullstring.find(substring)

if index != -1:
    print(index)
else:
    print("Not found!")

