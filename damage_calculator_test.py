
att = 2385
matt = 2380

defence = 3247
mdefence = 2348

sword_attack = [30, 10]
qi_attack = [10, 30]
major_qi_attack = [10, 50]
composite = [15,15]

def damage_reduction_percentage(att, skill_att, defence):
    # if skill_att == 0:
    #     return 1
    # reduction = defence/(1.75*(skill_att+att))

    reduction = defence/(((skill_att/100)+1)*att)
    return reduction

def damage(att, defence, skill_att):
    reduction = damage_reduction_percentage(att, skill_att, defence)
    print(f"reduction: {reduction}")
    damage = att+skill_att-(reduction*(att+skill_att))
    if damage < 0:
        return 0
    return damage

print("sword attack")
phys_damage = damage(att, defence, sword_attack[0])
print(f"phys_damage: {phys_damage}")
magic_damage = damage(matt, mdefence, sword_attack[1])
print(f"magic_damage: {magic_damage}")
print(f"TOTAL DAMAGE: {phys_damage+magic_damage}")


print("\nqi attack")
phys_damage = damage(att, defence, qi_attack[0])
print(f"phys_damage: {phys_damage}")
magic_damage = damage(matt, mdefence, qi_attack[1])
print(f"magic_damage: {magic_damage}")
print(f"TOTAL DAMAGE: {phys_damage+magic_damage}")

print("\nmajor qi attack")
phys_damage = damage(att, defence, major_qi_attack[0])
print(f"phys_damage: {phys_damage}")
magic_damage = damage(matt, mdefence, major_qi_attack[1])
print(f"magic_damage: {magic_damage}")
print(f"TOTAL DAMAGE: {phys_damage+magic_damage}")

print("\ncomposite")
phys_damage = damage(att, defence, composite[0])
print(f"phys_damage: {phys_damage}")
magic_damage = damage(matt, mdefence, composite[1])
print(f"magic_damage: {magic_damage}")
print(f"TOTAL DAMAGE: {phys_damage+magic_damage}")
