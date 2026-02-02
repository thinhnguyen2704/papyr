def unshift_text(text, shift=-1):
    """
    Shifts each character in the text by a specific number of positions
    in the standard A-Z alphabet to test the offset theory.
    """
    result = ""
    for char in text:
        if 'A' <= char <= 'Z':
            # Shift uppercase
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            # Shift lowercase
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            # Keep punctuation/spaces as is
            result += char
    return result

# Testing the result from your log
test_word = "WJFUUIBOI" 
prediction = unshift_text(test_word)

print(f"Original Prediction: {test_word}")
print(f"Shifted Result (-1): {prediction}")

if prediction == "VIETTHANH":
    print("\n✅ MATCH FOUND! Your dictionary is offset by exactly +1.")
    print("This confirms the missing newline caused the index shift.")