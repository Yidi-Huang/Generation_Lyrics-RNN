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
dossier_directory = "./taylor-swift"
process_dossier(dossier_directory)

import numpy as np


def generate_batch(batch_size, poems_embeddings):
    n_chunk = len(poems_embeddings) // batch_size
    x_batches = []
    y_batches = []
    for i in range(n_chunk):
        start_index = i * batch_size
        end_index = start_index + batch_size

        batch_embeddings = poems_embeddings[start_index:end_index]

        max_length = max(len(poem_embeddings) for poem_embeddings in batch_embeddings)
        embedding_dim = len(
            batch_embeddings[0][0]
        )  # Assuming all embeddings have the same dimensionality

        x_data = np.zeros((batch_size, max_length, embedding_dim), dtype=np.float32)
        y_data = np.zeros_like(x_data)

        for j, poem_embeddings in enumerate(batch_embeddings):
            poem_length = len(poem_embeddings)
            x_data[j, :poem_length] = poem_embeddings
            y_data[j, : poem_length - 1] = poem_embeddings[
                1:
            ]  # Shift the target one step to the left

        x_batches.append(x_data)
        y_batches.append(y_data)

    return x_batches, y_batches


# Example usage:
file_name = "./taylor-swift/taylor-swift.txt"  # Replace with the path to your file
processed_embeddings = process_poems(file_name)

# Assuming batch_size = 2 for demonstration purposes
batch_size = 2
x_batches, y_batches = generate_batch(batch_size, processed_embeddings)

# Printing the generated batches for demonstration
for i, (x_batch, y_batch) in enumerate(zip(x_batches, y_batches)):
    print(f"Batch {i+1}:")
    print("X_batch shape:", x_batch.shape)
    print("Y_batch shape:", y_batch.shape)
    print("X_batch content:")
    print(x_batch)
    print("Y_batch content:")
    print(y_batch)
    print()
