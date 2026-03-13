def tiny_hash(message):
    # Step 1 — convert message to numbers
    bytes_list = [ord(c) for c in message]
    print("Step 1 - bytes:", bytes_list)

    # Step 2 — mix the numbers together
    mixed = 0
    for b in bytes_list:
        mixed = (mixed * 31 + b) % 256  # mod destroys reversibility
    print("Step 2 - mixed:", mixed)

    # Step 3 — spread the bits
    spread = (mixed ^ (mixed << 3)) % 256
    print("Step 3 - spread:", spread)

    return hex(spread)

print(tiny_hash("hello"))
print(tiny_hash("hellp"))  # one letter change
print(tiny_hash("hello"))  # same input same output




# mod 256    → destroys magnitude — you cannot know original size
# × 31       → prime multiplication mixes bits together
# XOR shift  → spreads information across all bits