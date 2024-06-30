import argparse
import sys
from spellchecker import SpellChecker

def read_file(file_path):
    """Reads the content of the file from the given path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)

def write_file(file_path, content):
    """Writes the content to the given file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_corrected_word(word, suggestions):
    """Gets the user's choice for the correct word."""
    print(f"Mispelled word: '{word}'")
    for i, suggestion in enumerate(suggestions):
        print(f"{i + 1}: {suggestion}")
    
    while True:
        try:
            choice = int(input(f"Choose the correct word for '{word}' (1-{len(suggestions)}): "))
            if 1 <= choice <= len(suggestions):
                return suggestions[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def correct_spelling(text):
    """Corrects spelling errors in the text."""
    spell = SpellChecker()
    words = text.split()
    corrected_words = []

    for word in words:
        if word.lower() in spell:
            corrected_words.append(word)
        else:
            suggestions = list(spell.candidates(word))
            if suggestions:
                corrected_word = get_corrected_word(word, suggestions)
                corrected_words.append(corrected_word)
            else:
                print(f"No suggestions for '{word}', keeping original.")
                corrected_words.append(word)

    return ' '.join(corrected_words)

def main():
    """Main function to run the program."""
    parser = argparse.ArgumentParser(description='Spell check and correction.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Input file name')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file name')
    args = parser.parse_args()

    input_text = read_file(args.file)
    corrected_text = correct_spelling(input_text)
    write_file(args.output, corrected_text)
    print(f"Corrected text saved to '{args.output}'.")

if __name__ == "__main__":
    main()

