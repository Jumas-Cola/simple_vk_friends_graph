
import matplotlib.pyplot as plt
import networkx as nx
import vk_api


class Drawer(object):
    def __init__(self, file_name='graph.png'):
        self.graph = nx.Graph()
        self.file_name = file_name

    def draw(self):
        options = {
            'node_color': '#A0CBE2', # цвет узла
            'node_size': 3500, # размер узла
            'edge_color': '#C0C0C0', # цвет соединений
            'font_size': 7, # размер шрифта
            'with_labels': True # печатать ли заголовки узлов
        }
        nx.draw(self.graph, pos=nx.spring_layout(self.graph), **options)
        # устанавливаем размер изображения в дюймах
        plt.gcf().set_size_inches(40, 40)
        plt.savefig(self.file_name)

    def getRGBfromI(RGBint, maximum, red=115, blue=218):
        green = int(RGBint*(255/maximum))
        return red, green, blue

    def draw_with_colors(self, maximum):
        color_map = []
        for node in self.graph:
            power = int(node.split('/')[-1])
            color_map.append('#%02x%02x%02x' % Drawer.getRGBfromI(power, maximum))
        options = {
            'node_color': color_map, # цвет узла
            'node_size': 3500, # размер узла
            'edge_color': '#C0C0C0', # цвет соединений
            'font_size': 7, # размер шрифта
            'with_labels': True # печатать ли заголовки узлов
        }
        nx.draw(self.graph, pos=nx.spring_layout(self.graph), **options)
        # устанавливаем размер изображения в дюймах
        plt.gcf().set_size_inches(40, 40)
        plt.savefig(self.file_name)


class Parser:
    def deep_friends(user_id=0, depth=0):
        # Получаем информацию о текущем пользователе
        if not user_id:
            person = vk.method('users.get')
            user_id = person[0]['id']
        else:
            person = vk.method('users.get', {'user_ids': user_id})

        person_name = person[0]['first_name']
        person_last_name = person[0]['last_name']
        person_id = str(person[0]['id'])
        # Получаем список друзей текущего пользователя
        friends = vk.method('friends.get', {'user_id': user_id})
        # Получаем информацию о друзьях текущего пользователя
        friends_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in friends['items']])})

        # Пишем друзей в файл
        f = open('grid.edgelist', 'a', encoding='utf-8')
        for friend in friends_info:
            friend_name = friend['first_name']
            friend_last_name = friend['last_name']
            friend_id = str(friend['id'])
            node = '{}/{}/{}:{}/{}/{}:'.format(person_name,person_last_name,person_id,friend_name,friend_last_name,friend_id)+'{}\n'
            f.write(node)
        f.close()

        # Если глубина не равна 0 - вызываем функцию для всех друзей текущего пользователя
        if depth == 0:
            return
        else:
            for friend in friends['items']:
                try:
                    Parser.deep_friends(friend, depth-1)
                except:
                    print('Cant get friends of id'+str(friend))

    def users_by_list(user_list):
        for friend in user_list:
            try:
                Parser.deep_friends(friend, 0)
            except:
                print('Cant get friends of id' + str(friend))

    def mutual_friends_with_colors(user_id=0):
        # Получаем информацию о текущем пользователе
        if not user_id:
            person = vk.method('users.get')
            user_id = person[0]['id']
        else:
            person = vk.method('users.get', {'user_ids': user_id})
        person_name = person[0]['first_name']
        person_last_name = person[0]['last_name']
        person_id = str(person[0]['id'])
        # Получаем список друзей текущего пользователя
        friends = vk.method('friends.get', {'user_id': user_id})
        # Получаем информацию о друзьях текущего пользователя
        friends_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in friends['items']])})

        # Составляем словарь "популярности"
        powers={}
        for friend in friends['items']:
            try:
                mutuals = vk.method('friends.getMutual', {'source_uid': person_id, 'target_uid': friend})
                powers[str(friend)]={'count':len(mutuals), 'items':mutuals}
            except:
                powers[str(friend)]={'count':0, 'items':[]}

        # Пишем друзей в файл
        f = open('grid.edgelist', 'a', encoding='utf-8')
        for friend in friends_info:
            friend_name = friend['first_name']
            friend_last_name = friend['last_name']
            friend_id = str(friend['id'])
            node = '{}/{}/{}/{}:{}/{}/{}/{}:'.format(person_name,person_last_name,person_id,0,friend_name,friend_last_name,friend_id,powers[friend_id]['count'])+'{}\n'
            f.write(node)
            # Получаем информацию о связях текущего друга
            mutuals = powers[friend_id]['items']
            if mutuals:
                mutuals_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in mutuals])})
                for mutual in mutuals_info:
                    mutual_name = mutual['first_name']
                    mutual_last_name = mutual['last_name']
                    mutual_id = str(mutual['id'])
                    node = '{}/{}/{}/{}:{}/{}/{}/{}:'.format(friend_name,friend_last_name,friend_id,powers[friend_id]['count'],mutual_name,mutual_last_name,mutual_id,powers[mutual_id]['count'])+'{}\n'
                    f.write(node)
        f.close()
        maximum = 0
        for i in powers:
        	if powers[i]['count'] > maximum:
        		maximum = powers[i]['count']
        return maximum

    def mutual_friends(user_id=0):
        # Получаем информацию о текущем пользователе
        if not user_id:
            person = vk.method('users.get')
            user_id = person[0]['id']
        else:
            person = vk.method('users.get', {'user_ids': user_id})
        person_name = person[0]['first_name']
        person_last_name = person[0]['last_name']
        person_id = str(person[0]['id'])
        # Получаем список друзей текущего пользователя
        friends = vk.method('friends.get', {'user_id': user_id})
        # Получаем информацию о друзьях текущего пользователя
        friends_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in friends['items']])})

        # Пишем друзей в файл
        f = open('grid.edgelist', 'a', encoding='utf-8')
        for friend in friends_info:
            friend_name = friend['first_name']
            friend_last_name = friend['last_name']
            friend_id = str(friend['id'])
            node = '{}/{}/{}:{}/{}/{}:'.format(person_name,person_last_name,person_id,friend_name,friend_last_name,friend_id)+'{}\n'
            f.write(node)
            try:
                # Получаем информацию о связях текущего друга
                mutuals = vk.method('friends.getMutual', {'source_uid': person_id, 'target_uid': friend['id']})
                mutuals_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in mutuals])})
                for mutual in mutuals_info:
                    mutual_name = mutual['first_name']
                    mutual_last_name = mutual['last_name']
                    mutual_id = str(mutual['id'])
                    node = '{}/{}/{}:{}/{}/{}:'.format(friend_name,friend_last_name,friend_id,mutual_name,mutual_last_name,mutual_id)+'{}\n'
                    f.write(node)
            except:
                print('Cant get mutuals of id'+str(person_id),'with id'+str(friend['id']))
        f.close()





if __name__ == "__main__":
    login = 'login'
    password = 'password'
    user_id = 0	# id пользователя, для которого необходимо построить граф (0 - текущий пользователь)
    depth = 1	# глубина рекурсивного прохода по друзьям
    users = [87896266, 174594973]

    # авторизация Вк
    vk = vk_api.VkApi(login=login, password=password)
    vk.auth()

    # определение перекрёстных связей с визуализацией популярности
    maximum = Parser.mutual_friends_with_colors(user_id)

    # определение перекрёстных связей среди друзей пользователя
    #Parser.mutual_friends(user_id)

    # рекурсивный проход по друзьям, друзьям друзей и т.д.
    # Parser.deep_friends(user_id, depth)

    # проход по заданному списку пользователей
    # Parser.users_by_list(users)

    # чтение графа из файла
    G = nx.read_edgelist(path="grid.edgelist", delimiter=":")

    # отрисовка графа в .png изображение
    Graph = Drawer()
    Graph.graph = G
    #Graph.draw()
    Graph.draw_with_colors(maximum)
