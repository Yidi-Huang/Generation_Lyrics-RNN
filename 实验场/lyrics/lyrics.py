import gensim.downloader as api
import numpy as np
import math

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



def generate_batches(batch_size, poems_embeddings):
    # 动态调整批次大小以适应数据集大小
    batch_size = min(batch_size, len(poems_embeddings))
    
    # 计算需要多少个批次，向上取整以包括所有数据
    n_chunks = math.ceil(len(poems_embeddings) / batch_size)
    x_batches = []
    y_batches = []

    for i in range(n_chunks):
        # 确保即使在最后一个批次也能正确切片
        batch = poems_embeddings[i * batch_size: min((i + 1) * batch_size, len(poems_embeddings))]

        if not batch:  # 如果批次为空，则跳过
            continue

        # 计算批次中每首诗的最大长度
        max_length = max(len(poem) for poem in batch)
        embedding_dim = len(batch[0][0])  # 获取嵌入维度

        # 初始化 x_data 和 y_data 数组
        x_data = np.zeros((len(batch), max_length, embedding_dim), dtype=np.float32)
        y_data = np.zeros((len(batch), max_length, embedding_dim), dtype=np.float32)

        for j, poem in enumerate(batch):
            poem_length = len(poem)
            x_data[j, :poem_length-1, :] = poem[:-1]  # 最后一个嵌入不用于x
            y_data[j, :poem_length-1, :] = poem[1:]   # 从第二个词开始作为y

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
