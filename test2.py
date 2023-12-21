# Example list of strings
strings = [
    "Hello",
    "OpenAI",
    "Python",
    "GPT"
]

# Determine the maximum length of the strings
max_length = max(len(s) for s in strings)

# Align strings based on their last character
aligned_strings = [s.rjust(max_length) for s in strings]

# Print aligned strings
for aligned_str in aligned_strings:
    print(aligned_str)

# Align strings based on their first character
aligned_strings = [s.ljust(max_length) for s in strings]
for aligned_str in aligned_strings:
    print(aligned_str)
