import os

def replace_word_in_files(directory, old_word, new_word):
    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt" or ".html"):
            file_path = os.path.join(directory, filename)
            try:
                # Open and read the file
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Replace the target word
                updated_content = content.replace(old_word, new_word)

                # Write the updated content back to the file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(updated_content)

                print(f"Replaced '{old_word}' with '{new_word}' in {filename}")

            except Exception as e:
                print(f"An error occurred with file {filename}: {e}")

# Define the directory and words to replace
directory_path = "./raw_txt"  # Replace with the path to your directory
word_to_replace = "Jimmy"
replacement_word = "Jimmy's Social Space Application"

# Call the function
replace_word_in_files(directory_path, word_to_replace, replacement_word)
