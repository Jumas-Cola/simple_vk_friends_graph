simple_vk_friends_graph ![Python 3.6](https://pp.userapi.com/c846523/v846523407/b716d/N3RXKWFcPS0.jpg)
======
**simple_vk_friends_graph** – скрипт на Python для построения графа дружеских связей, для социальной сети Вконтакте (vk.com)

```python
...
# рекурсивный проход по друзьям, друзьям друзей и т.д.
Parser.deep_friends(user_id, depth)

# проход по заданному списку пользователей
Parser.users_by_list(users)

# чтение графа из файла
G = nx.read_edgelist(path="grid.edgelist", delimiter=":")

# отрисовка графа в .png изображение
Graph = Drawer()
Graph.graph = G
Graph.draw()
...

```

Пример графа
------------
![граф дружеских связей](https://pp.userapi.com/c852136/v852136711/57d4/WG3lPVdsSzw.jpg)

Есть два режима:
* рекурсивный проход по друзьям пользователя
* построение по заданному списку пользователей


Настройка внешнего вида графа
------------
```python
...
options = {
            'node_color': '#A0CBE2', # цвет узла
            'node_size': 3500, # размер узла
            'edge_color': '#C0C0C0', # цвет соединений
            'font_size': 7, # размер шрифта
            'with_labels': True # печатать ли заголовки узлов
        }
...

```