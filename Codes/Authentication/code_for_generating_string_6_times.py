import itertools

def generate_all_strings_with_repetition():
    # Generate all combinations of two lowercase letters
    suffixes = [''.join(combo) for combo in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=2)]
    # Combine each suffix with "admin_"
    all_strings = [f"admin_{suffix}" for suffix in suffixes]
    # Repeat each string six times
    repeated_strings = [s for s in all_strings for _ in range(6)]
    return repeated_strings

# Generate the list
final_strings = generate_all_strings_with_repetition()

# Save to a file
with open("output.txt", "w") as file:
    for string in final_strings:
        file.write(f"{string}\n")

print("Strings saved to output.txt")
