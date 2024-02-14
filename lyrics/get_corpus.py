import os
import re


def process_dossier(dossier_path):
    # Extract the name of the dossier directory
    dossier_name = os.path.basename(dossier_path)

    # Output file path
    output_file = os.path.join(dossier_path, f"{dossier_name}.txt")

    txt_files = [file for file in os.listdir(dossier_path) if file.endswith(".txt")]

    # Process each text file
    with open(output_file, "w", encoding="utf-8") as output:
        for file_name in txt_files:
            file_path = os.path.join(dossier_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            lines = [line.strip() for line in lines if line.strip()]

            processed_content = " _ ".join(lines)
            processed_content = re.sub(r"(\w)([.,!?;:])", r"\1 \2", processed_content)
            processed_content = re.sub(r"(\w)'(t|s|d)\b", r"\1 '\2", processed_content)
            processed_content = processed_content.lower()
            output.write(processed_content + "\n")


# Example usage:
#dossier_directory = "./taylor-swift"
#process_dossier(dossier_directory)


