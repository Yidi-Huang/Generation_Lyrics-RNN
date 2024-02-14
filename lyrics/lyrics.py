import gensim.downloader as api
import numpy as np

start_token = "<B> "
end_token = " <E>"

start = "<B>"
end = "<E>"


def process_lyrics(file_name):
    # Load GloVe word embeddings
    wv = api.load("glove-wiki-gigaword-50")

    # Initialize matrices for start and end tokens
    start_token_embedding = np.ones_like(wv["i"])
    end_token_embedding = -1 * np.ones_like(wv["i"])

    embeddings_list = []  # List to store embeddings of each word in each line

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = start_token + line.strip() + end_token
            # Split the line into words
            words = line.strip().split()
            if not words:
                continue

            line_embeddings = []  # List to store embeddings of each word in the line

            for word in words:
                if word == start:
                    embedding = start_token_embedding
                elif word == end:
                    embedding = end_token_embedding
                elif word in wv:
                    embedding = wv[word]
                else:
                    # Handle out of vocabulary words
                    embedding = np.zeros_like(
                        wv["hello"]
                    )  # Replace 'hello' with any other word
                line_embeddings.append(embedding)

            embeddings_list.append(line_embeddings)

    return embeddings_list


# Example usage:
# file_name = "./taylor-swift/taylor-swift.txt"  # Replace with the path to your file
# processed_embeddings = process_lyrics(file_name)
# print(processed_embeddings)

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
# file_name = './taylor-swift/taylor-swift.txt'  # Replace with the path to your file
# processed_embeddings = process_lyrics(file_name)

# Assuming batch_size = 2 for demonstration purposes
# batch_size = 2
# x_batches, y_batches = generate_batch(batch_size, processed_embeddings)

# Printing the generated batches for demonstration
# for i, (x_batch, y_batch) in enumerate(zip(x_batches, y_batches)):
# print(f"Batch {i+1}:")
# print("X_batch shape:", x_batch.shape)
# print("Y_batch shape:", y_batch.shape)
# print("X_batch content:")
# print(x_batch)
# print("Y_batch content:")
# print(y_batch)
# print()
