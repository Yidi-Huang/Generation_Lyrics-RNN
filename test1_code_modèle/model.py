# -*- coding: utf-8 -*-
# file: model.py
# author: JinTian
# time: 07/03/2017 3:07 PM
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



import tensorflow as tf


def rnn_model(model_type, input_shape, vocab_size, rnn_size=128, num_layers=1, learning_rate=0.01):
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        # 添加 LSTM 层，同时传递 num_layers 参数
        *[tf.keras.layers.LSTM(rnn_size, return_sequences=True) for _ in range(num_layers)],
        tf.keras.layers.Dense(vocab_size, activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model



# 调用简化模型函数
vocab_size = 10000  # 假设的词汇表大小
input_shape = (None, 50)  # 每个时间步的特征数为50
model = rnn_model(input_shape, vocab_size)

# 打印模型结构
model.summary()
