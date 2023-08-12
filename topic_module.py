# -*- coding: utf-8 -*-
"""Topic_module.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/106tkFBDSOvw2AVNHAPXAyn5Q9wBIpxwh
"""

import pandas as pd
import numpy as np

X = pd.read_csv('/content/Modularity.csv',sep=',')

X

import numpy as np
vector_dimension = 1044


num_agents = 117
topics_num = 10
vectors_per_agent = []
topics = []

for _ in range(num_agents):
    random_vector = np.random.rand(vector_dimension)
    vectors_per_agent.append(random_vector)

indices = list(range(1044))
vectors_per_agent.insert(0, indices)
import csv
with open('vectors.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(vectors_per_agent)

for _ in range(topics_num):
    random_vector = np.random.rand(vector_dimension)
    topics.append(random_vector)

indices = list(range(1044))
topics.insert(0, indices)

import csv
with open('vectors_of_topics.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(topics)

W = pd.read_csv('/content/vectors.csv',sep=',')
W



import pandas as pd

# Загрузите таблицы из CSV файлов
table1 = pd.read_csv('/content/Modularity.csv')
table2 = pd.read_csv('/content/vectors.csv')

# Создайте новую таблицу, объединив столбец "Id" из table1 с остальными столбцами из table2
new_table = pd.concat([table1, table2], axis=1)

# Сохраните новую таблицу в CSV файл
new_table.to_csv('new_table.csv', index=False)

Data = pd.read_csv("new_table.csv")
Data

vectors_topics = pd.read_csv('/content/vectors_of_topics.csv')

vectors_topics

grouped_data = Data.groupby('modularity_class').mean()

grouped_data.pop('Id')

grouped_data.to_csv('groups.csv')

import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

# Загрузите данные из CSV файлов в pandas DataFrame
topics_df = pd.read_csv('/content/vectors_of_topics.csv', header=None)
topics_df.reset_index(drop=True, inplace=True)
topics_df.insert(0, 'Topic', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

groups_df = pd.read_csv('/content/groups.csv')
groups_df.reset_index(drop=True, inplace=True)

# Отдельно сохраняем столбец с номерами тем и групп, чтобы он не участвовал в расчетах
topics_numbers = topics_df['Topic']
groups_numbers = groups_df['modularity_class']

# Удаляем столбец с номерами из DataFrame
topics_df.drop(columns=['Topic'], inplace=True)
groups_df.drop(columns=['modularity_class'], inplace=True)

# Преобразуем DataFrame в массив NumPy для вычислений
topics_vectors = topics_df.to_numpy()
groups_vectors = groups_df.to_numpy()

# Создайте пустой список для хранения индексов наиболее близких тем к каждой группе
most_similar_topics_indices = []

# Найдите наиболее близкую тему для каждой группы
for group_vector in groups_vectors:
    similarities = [1 - cosine(group_vector, topic_vector) for topic_vector in topics_vectors]
    most_similar_topic_index = np.argmax(similarities)
    most_similar_topics_indices.append(most_similar_topic_index)

most_similar_topics_indices

result_df = pd.DataFrame({'GroupNumber': groups_numbers, 'MostSimilarTopic': most_similar_topics_indices})

result_df

result_df.to_csv('result.csv', index=False)



import pandas as pd

# Загрузим таблицу "results"
results_df = pd.read_csv('result.csv')

# Создадим словарь, где ключами будут номера групп, а значениями - соответствующие любимые темы
group_topic_mapping = dict(zip(results_df['GroupNumber'], results_df['MostSimilarTopic']))

# Загрузим таблицу "Modularity"
modularity_df = pd.read_csv('Modularity.csv')

# Создадим общую таблицу для агентов с информацией об их группе и любимой теме
agent_info = {'AgentId': modularity_df['Id'],
              'GroupNumber': modularity_df['modularity_class'],
              'FavoriteTopic': modularity_df['modularity_class'].map(group_topic_mapping)}

# Создадим DataFrame на основе словаря
agent_info_df = pd.DataFrame(agent_info)

# Выведем первые строки общей таблицы для проверки
print(agent_info_df.head())

agent_info_df.to_csv('agent_info.csv')

import pandas as pd
import numpy as np

# Load agent_info_df from 'agent_info.csv' with columns AgentId, GroupNumber, FavoriteTopic
agent_info_df = pd.read_csv('agent_info.csv')

topic_probs = {
    'Group_Same': [0.55] + [0.45 / 9] * 9,
    'Group_Different_Same_FavTopic': [0.46] + [0.54 / 9] * 9,
    'Group_Different_Different_FavTopic': [0.25, 0.25] + [0.5 / 8] * 8
}

def select_scenario(group_number_1, group_number_2, fav_topic_1, fav_topic_2):
    if group_number_1 == group_number_2:
        if fav_topic_1 == fav_topic_2:
            return 'Group_Same'
        else:
            return 'Group_Different_Same_FavTopic'
    else:
        if fav_topic_1 == fav_topic_2:
            return 'Group_Different_Same_FavTopic'
        else:
            return 'Group_Different_Different_FavTopic'

def select_topic(scenario, fav_topic):
    topic_probs_for_scenario = topic_probs[scenario]
    topics = list(range(10))
    chosen_topic = np.random.choice(topics, p=topic_probs_for_scenario)

    if chosen_topic == 0:
        return fav_topic
    else:
        return chosen_topic

# Create a DataFrame to store the results
result_df = pd.DataFrame(columns=['AgentId1', 'AgentId2', 'SelectedTopic'])

# Compare each agent with every other agent
for i in range(len(agent_info_df)):
    for j in range(i + 1, len(agent_info_df)):
        agent1 = agent_info_df.iloc[i]
        agent2 = agent_info_df.iloc[j]

        scenario = select_scenario(agent1['GroupNumber'], agent2['GroupNumber'], agent1['FavoriteTopic'], agent2['FavoriteTopic'])
        selected_topic = select_topic(scenario, agent1['FavoriteTopic'])

        result_df = result_df.append({'AgentId1': agent1['AgentId'], 'AgentId2': agent2['AgentId'], 'SelectedTopic': selected_topic}, ignore_index=True)

# Save the result to a CSV file
result_df.to_csv('communication_results.csv', index=False)

import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
import random
import collections

def select_topic(agent_group, favorite_topic):
    num_unique_topics = 11  # Replace with the correct size if needed
    chosen_topic = np.random.choice(num_unique_topics)

    if agent_group == favorite_topic:
        chosen_option = np.random.choice(3)  # Randomly choose from 0, 1, 2
    else:
        chosen_option = np.random.choice(4)  # Randomly choose from 0, 1, 2, 3

    return chosen_option, chosen_topic
class Opinion:
    def __init__(self, x):
        self.x = x

    def clone(self):
        return Opinion(self.x)

    def diff(self, o):
        return self.x - o.x

    def communicate(self, o, pow1, pow2):
        diff = self.diff(o)
        abs_diff = abs(diff)
        k = 1 - abs_diff
        K = 0.1
        speed = diff * k / 2 * K
        k2 = 1
        if pow1 > pow2:
            divis = abs(speed) * (1 - (pow2 / pow1))
            diff1 = abs(speed) - k2 * divis
            diff2 = abs(speed) + k2 * divis
        elif pow2 > pow1:
            divis = abs(speed) * (1 - (pow1 / pow2))
            diff1 = abs(speed) + k2 * divis
            diff2 = abs(speed) - k2 * divis
        else:
            diff1 = abs(speed)
            diff2 = abs(speed)
        if speed < 0:
            diff1 = 0 - diff1
            diff2 = 0 - diff2

        new_op1 = Opinion(self.x - diff1)
        new_op2 = Opinion(o.x + diff2)
        return new_op1, new_op2

    def replace_with_average(self, opinions):
        s = 0
        c = 0
        for o in opinions:
            s += o.x
            c += 1
        self.x = s / c

class Connection:
    def __init__(self, person, strength):
        self.person = person
        self.strength = strength

    def active(self):
        return random.random() < self.strength

class Person:
    def __init__(self, agent_id, group_number, favorite_topic, opinion, power, prof):
        self.connections = []
        self.connections2 = []
        self.opinion = opinion
        self.power = power
        self.prof = prof
        self.prof2 = 0
        self.agent_id = agent_id
        self.group_number = group_number
        self.favorite_topic = favorite_topic

    def add_connection(self, connection):
        self.connections.append(connection)

    def communicate(self):
        new_ops = []
        self.connections2 = self.connections
        self.prof2 = self.prof
        K = 1
        for c in self.connections2:
            if c.active():
                chosen_option, chosen_topic = select_topic(self.group_number, self.favorite_topic)
                if chosen_option == 0:
                    new_op1, new_op2 = self.opinion.communicate(c.person.opinion, self.power, c.person.power)
                elif chosen_option == 1:
                    new_op1, new_op2 = self.opinion.clone(), c.person.opinion.clone()
                elif chosen_option == 2:
                    avg_op = Opinion((self.opinion.x + c.person.opinion.x) / 2)
                    new_op1, new_op2 = avg_op, avg_op
                else:
                    new_op1, new_op2 = Opinion(random.random()), Opinion(random.random())
                new_ops.append((c.person, new_op1, new_op2))

                c.strength += (new_op2.diff(c.person.opinion) * (1 - abs(new_op2.diff(c.person.opinion)))) * 0.1

        return new_ops

    def update_connections(self):
        self.connections = self.connections2
        self.prof = self.prof2

def load_connection_matrix(file_path):
    connection_matrix = pd.read_csv(file_path, sep = ";", index_col=0)
    return connection_matrix.values.tolist()

def cycle():
    ops = []
    for p in people:
        ops.append((p, p.communicate()))

    m = collections.defaultdict(list)
    for p, new_ops in ops:
        for p2, x, y in new_ops:
            m[id(p2)].append(y)
            m[id(p)].append(x)

    for p in people:
        if id(p) in m:
            assert m[id(p)]
            p.opinion.replace_with_average(m[id(p)])

    for p in people:
        p.update_connections()

agent_info_df = pd.read_csv('agent_info.csv')
# Отдельно сохраняем столбцы с номерами групп и любимыми темами, чтобы они не участвовали в расчетах
groups_numbers = agent_info_df['GroupNumber']
most_similar_topics_indices = agent_info_df['FavoriteTopic']




# Преобразуем DataFrame в массив NumPy для вычислений
agent_info_array = agent_info_df.to_numpy()
num_agents, vector_dimension = agent_info_array.shape

# Создаем список объектов Person для каждого агента
people = []
for i in range(num_agents):
    agent_id = agent_info_array[i, 0]  # AgentId в первом столбце (индекс 0)
    group_number = agent_info_array[i, 1]  # GroupNumber во втором столбце (индекс 1)
    favorite_topic = agent_info_array[i, 2]  # FavoriteTopic в третьем столбце (индекс 2)
    opinion_vector = np.random.rand(vector_dimension - 3)  # Здесь можно загрузить вектор из файла, если не нужно генерировать случайные векторы
    people.append(Person(agent_id, group_number, favorite_topic, Opinion(opinion_vector), 1.0, 0.5))

# Создаем связи между агентами на основе матрицы связей
connections_matrix = load_connection_matrix('connections.csv')
for i in range(num_agents):
    for j in range(num_agents):
        if connections_matrix[i][j] > 0:
            people[i].add_connection(Connection(people[j], connections_matrix[i][j]))

# Выполняем цикл общения между агентами
for i in range(1):
    print(i)
    cycle()

import pandas as pd

# Создаем пустой список для хранения данных агентов
agent_data = []

# Получаем информацию об агентах и добавляем ее в список agent_data
for agent in people:
    agent_id = agent.agent_id
    group_number = agent.group_number
    opinion = agent.opinion.x
    agent_data.append([agent_id, group_number, opinion])

# Создаем DataFrame из списка agent_data
columns = ['AgentId', 'GroupNumber', 'Opinion']
df_results = pd.DataFrame(agent_data, columns=columns)

# Сохраняем DataFrame в файл CSV
df_results.to_csv('agent_results.csv', index=False)

# Сохраняем DataFrame в файл Excel
df_results.to_excel('agent_results.xlsx', index=False)

num_agents = 117
connections_matrix = np.zeros((num_agents, num_agents))

# Заполняем матрицу связей на основе информации о связях между агентами
for person in people:
    agent_id = person.agent_id
    for connection in person.connections:
        connected_agent_id = connection.person.agent_id
        strength = connection.strength
        connections_matrix[agent_id - 1][connected_agent_id - 1] = strength

# Создаем DataFrame из матрицы связей
connections_df = pd.DataFrame(connections_matrix)

# Сохраняем DataFrame в CSV файл
connections_df.to_excel('agent_connections_matrix.xlsx', index=False)

connections_df