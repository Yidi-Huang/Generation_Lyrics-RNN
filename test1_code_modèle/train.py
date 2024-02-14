# -*- coding: utf-8 -*-
# file: main.py
# author: JinTian
# time: 11/03/2017 9:53 AM
# Copyright 2017 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
import os
import argparse
import numpy as np
import tensorflow as tf
from model import rnn_model  # 确保model.py在同一目录下
from lyrics.lyrics import process_lyrics, generate_batch

# 设置命令行参数
parser = argparse.ArgumentParser(description='TensorFlow Poems Training Script TensorFlow 2.x')
parser.add_argument('--batch_size', type=int, default=64, help='batch size')
parser.add_argument('--learning_rate', type=float, default=0.01, help='learning rate')
parser.add_argument('--model_dir', type=str, default=os.path.abspath('./model'), help='model save path')
parser.add_argument('--file_path', type=str, default=os.path.abspath('./data/taylor-swift.txt'), help='file name of poems')
parser.add_argument('--epochs', type=int, default=50, help='train how many epochs')
args = parser.parse_args()

def run_training():
    if not os.path.exists(args.model_dir):
        os.makedirs(args.model_dir)

    # 加载词嵌入并生成批次数据
    embeddings_list = process_lyrics(args.file_path)
    x_batches, y_batches = generate_batch(args.batch_size, embeddings_list)

    # 假设vocab_size根据您的数据集调整
    vocab_size = 10000  # 需要根据您的数据集实际情况进行调整
    input_shape = (None, 50)  # 根据您的词向量维度调整
    print("Input shape before calling rnn_model:", input_shape)

    # 构建模型
    model = rnn_model('lstm', input_shape, vocab_size, rnn_size=128, num_layers=2, learning_rate=args.learning_rate)

    # 准备数据集
    x_data = np.array(x_batches, dtype=object)
    y_data = np.array(y_batches, dtype=object)
    dataset = tf.data.Dataset.from_generator(lambda: zip(x_data, y_data), output_types=(tf.float32, tf.int32))
    dataset = dataset.padded_batch(args.batch_size)

    # 训练模型
    model.fit(dataset, epochs=args.epochs)

    # 保存模型
    model.save(os.path.join(args.model_dir, 'lyrics_model.h5'))

if __name__ == '__main__':
    run_training()
