from Character import CreateCharacter

create = CreateCharacter()
# create.createRandomCharacter("Suiren", realm=0, level=0)



create.path = "./enemies"
# create.createRandomCharacter("Zangetsu", realm=4, level=5)
# create.createRandomCharacter("Baji", realm=4, level=6)
# create.createRandomCharacter("Mikey", realm=5, level=0)
# create.createRandomCharacter("Draken", realm=4, level=7)

for i in range(1,6):
    create.createRandomCharacter(f"5_{i}", realm=4, level=i)
