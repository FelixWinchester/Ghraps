class Graph:
    def __init__(self, directed=False, adjacency_list=None, weighted=False):
        if adjacency_list is None:
            self.adjacency_list = {}
        else:
            self.adjacency_list = {v: list(adj) for v, adj in adjacency_list.items()}
        self.directed = directed
        self.weighted = weighted  # Атрибут для определения взвешенности графа

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Определяем тип графа (направленный/ненаправленный) и взвешенный/невзвешенный
        header = lines[0].strip().lower().split()
        self.directed = header[0] == 'directed'
        self.weighted = header[1] == 'weighted'

        # Используем словарь для хранения графа
        self.graph = {}
        all_vertices = set()

        for i, line in enumerate(lines[1:]):
            parts = line.strip().split()

            if len(parts) == 1:
                vertex = parts[0]
                all_vertices.add(vertex)
                self.graph.setdefault(vertex, [])
                continue

            if self.weighted:
                u, v, weight = parts[0], parts[1], float(parts[2])
                all_vertices.update([u, v])
                self.graph.setdefault(u, []).append((v, weight))
                if not self.directed:
                    if u != v:
                        self.graph.setdefault(v, []).append((u, weight))
            else:
                u, v = parts[0], parts[1]
                all_vertices.update([u, v])
                self.graph.setdefault(u, []).append((v, None))
                if not self.directed:
                    if u != v:
                        self.graph.setdefault(v, []).append((u, None))

        # Обеспечиваем наличие всех вершин, включая обособленные
        for vertex in all_vertices:
            if vertex not in self.graph:
                self.graph[vertex] = []

        # Копируем данные из self.graph в self.adjacency_list для дальнейшего использования
        self.adjacency_list = self.graph.copy()

        # Вывод содержимого графа:
        print(f"Граф из файла '{filename}' загружен. Вот его содержимое:")
        for vertex, edges in self.graph.items():
            if edges:
                if self.weighted:
                    edges_str = ', '.join(f"{v} (вес: {weight})" for v, weight in edges)
                else:
                    edges_str = ', '.join(v for v, _ in edges)
                print(f"{vertex}: {edges_str}")
            else:
                if self.directed:
                    has_incoming = any(vertex in [v for v, _ in adj] for adj in self.graph.values())
                    if has_incoming:
                        print(f"{vertex}: нет исходящих рёбер")
                    else:
                        print(f"{vertex}: нет рёбер")
                else:
                    print(f"{vertex}: нет рёбер")

        # Вывод типа графа:
        graph_type = "Ориентированный" if self.directed else "Неориентированный"
        weight_type = "Взвешенный" if self.weighted else "Невзвешенный"
        print(f"Тип графа: {graph_type}, {weight_type}")

    def display_adjacency_list(self):
        for vertex in self.adjacency_list:
            if self.weighted:
                edges = ', '.join(f"{adj} ({weight})" for adj, weight in self.adjacency_list[vertex])
            else:
                edges = ', '.join(str(adj) for adj, *_ in self.adjacency_list[vertex])
            print(f"{vertex}: {edges if edges else ''}")

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
        else:
            print(f"Вершина {vertex} уже существует.")

    def add_edge(self, u, v, weight=None, overwrite=False):
        # Проверяем существование обеих вершин
        if u not in self.adjacency_list or v not in self.adjacency_list:
            print(f"Ошибка: Вершины '{u}' и/или '{v}' не существуют.")
            return False

        # Определяем вес ребра
        if self.weighted:
            if weight is None:
                print("Ошибка: Для взвешенного графа необходимо указать вес ребра.")
                return False
        else:
            weight = None  # В невзвешенном графе вес не хранится

        # Проверяем существование ребра
        if self.weighted:
            existing_edge = next(((i, w) for i, (neighbor, w) in enumerate(self.adjacency_list[u]) if neighbor == v),
                                 None)
        else:
            existing_edge = next((i for i, (neighbor,) in enumerate(self.adjacency_list[u]) if neighbor == v), None)

        if existing_edge:
            if overwrite:
                index, _ = existing_edge
                if self.weighted:
                    self.adjacency_list[u][index] = (v, weight)
                else:
                    self.adjacency_list[u][index] = (v,)
                print(f"Ребро {u}-{v} обновлено.")
            else:
                print(f"Ребро {u}-{v} уже существует.")
                return False  # Указывает, что ребро уже существует и не было перезаписано
        else:
            if self.weighted:
                self.adjacency_list[u].append((v, weight))
                print(f"Ребро {u}-{v} добавлено с весом {weight}.")
            else:
                self.adjacency_list[u].append((v,))
                print(f"Ребро {u}-{v} добавлено.")

        if not self.directed and u != v:
            existing_reverse_edge = next(((i, w) for i, (neighbor, w) in enumerate(self.adjacency_list[v]) if neighbor == u), None)
            if existing_reverse_edge:
                if overwrite and self.weighted:
                    index, _ = existing_reverse_edge
                    self.adjacency_list[v][index] = (u, weight)
            else:
                if self.weighted:
                    self.adjacency_list[v].append((u, weight))
                else:
                    self.adjacency_list[v].append((u,))
        return True  # Указывает, что ребро было успешно добавлено или обновлено

    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            # Удаляем все рёбра, связанные с этой вершиной
            self.adjacency_list.pop(vertex)
            for adj in self.adjacency_list:
                if self.weighted:
                    self.adjacency_list[adj] = [(v, w) for v, w in self.adjacency_list[adj] if v != vertex]
                else:
                    self.adjacency_list[adj] = [v for v, *_ in self.adjacency_list[adj] if v != vertex]
        else:
            print(f"Вершина {vertex} не существует.")

    def remove_edge(self, u, v):
        if u in self.adjacency_list:
            if self.weighted:
                original_length = len(self.adjacency_list[u])
                self.adjacency_list[u] = [(x, w) for x, w in self.adjacency_list[u] if x != v]
                if len(self.adjacency_list[u]) < original_length:
                    print(f"Ребро {u}-{v} удалено.")
                else:
                    print(f"Ребро {u}-{v} не существует.")
            else:
                original_length = len(self.adjacency_list[u])
                self.adjacency_list[u] = [x for x, *_ in self.adjacency_list[u] if x != v]
                if len(self.adjacency_list[u]) < original_length:
                    print(f"Ребро {u}-{v} удалено.")
                else:
                    print(f"Ребро {u}-{v} не существует.")

            if not self.directed:
                if self.weighted:
                    self.adjacency_list[v] = [(x, w) for x, w in self.adjacency_list[v] if x != u]
                else:
                    self.adjacency_list[v] = [x for x, *_ in self.adjacency_list[v] if x != u]
        else:
            print(f"Вершина {u} не существует.")

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                # Записываем тип графа
                type_line = f"{'directed' if self.directed else 'undirected'} {'weighted' if self.weighted else 'unweighted'}\n"
                file.write(type_line)

                # Записываем вершины и рёбра
                for vertex, edges in self.adjacency_list.items():
                    if not edges:
                        # Записываем вершину без рёбер
                        file.write(f"{vertex}\n")
                    else:
                        for edge in edges:
                            neighbor = edge[0]
                            weight = edge[1] if self.weighted else None
                            if self.directed or (not self.directed and vertex < neighbor):
                                if self.weighted:
                                    file.write(f"{vertex} {neighbor} {weight}\n")
                                else:
                                    file.write(f"{vertex} {neighbor}\n")
            print(f"Граф успешно сохранён в файл '{filename}'.")
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")

    def __str__(self):
        # Вывод графа в виде строки с указанием весов рёбер, включая петли
        result = ""
        for vertex in self.adjacency_list:
            result += f"{vertex}: "
            if self.weighted:
                edges = ", ".join(f"{adj} ({weight})" for adj, weight in self.adjacency_list[vertex])
            else:
                edges = ", ".join(adj for adj, *_ in self.adjacency_list[vertex])
            result += f"{edges}\n"
        return result

    def edges(self):
        edge_list = []
        seen_edges = set()
        for vertex in self.adjacency_list:
            for edge in self.adjacency_list[vertex]:
                neighbor = edge[0]
                weight = edge[1] if self.weighted else None
                if self.directed:
                    edge_repr = (vertex, neighbor, weight) if self.weighted else (vertex, neighbor)
                    edge_list.append(edge_repr)
                else:
                    # Для неориентированного графа избегаем дублирования ребер
                    edge_key = tuple(sorted([vertex, neighbor]))
                    if edge_key not in seen_edges:
                        edge_repr = (vertex, neighbor, weight) if self.weighted else (vertex, neighbor)
                        edge_list.append(edge_repr)
                        seen_edges.add(edge_key)
        return edge_list

    def compare_outdegree(self, vertex): # Полустепень
        """
        Выводит вершины, полустепень исхода которых больше, чем у заданной вершины.
        """
        if vertex not in self.adjacency_list:
            print(f"Вершина '{vertex}' не найдена в графе.")
            return

        outdegree_vertex = len(self.adjacency_list[vertex])  # Полустепень исхода для заданной вершины
        print(f"Полустепень исхода вершины '{vertex}': {outdegree_vertex}")

        # Сравнение полустепеней исхода
        for v in self.adjacency_list:
            if len(self.adjacency_list[v]) > outdegree_vertex:
                print(f"Вершина '{v}' имеет большую полустепень исхода ({len(self.adjacency_list[v])}).")

    def find_loops(self): # Поиск петлей
        """
        Выводит вершины, в которых есть петли (ребро, начинающееся и заканчивающееся в одной и той же вершине).
        """
        loops = [vertex for vertex in self.adjacency_list if any(neighbor == vertex for neighbor, *_ in self.adjacency_list[vertex])]

        if loops:
            print("Вершины с петлями:", ", ".join(loops))
        else:
            print("В графе нет вершин с петлями.")

    def remove_hanging_vertices(self):
        # Продолжаем удаление висячих вершин до тех пор, пока они есть в графе
        while True:
            # Находим все висячие вершины
            hanging_vertices = [v for v, adj in self.adjacency_list.items() if len(adj) == 1]

            # Если висячих вершин нет, выходим из цикла
            if not hanging_vertices:
                break

            # Удаляем все висячие вершины
            for vertex in hanging_vertices:
                # Удаляем все упоминания висячей вершины в её соседях
                for neighbor in self.adjacency_list[vertex]:
                    neighbor_vertex = neighbor[0]
                    if neighbor_vertex in self.adjacency_list:
                        if self.weighted:
                            self.adjacency_list[neighbor_vertex] = [
                                (v, w) for v, w in self.adjacency_list[neighbor_vertex] if v != vertex
                            ]
                        else:
                            self.adjacency_list[neighbor_vertex] = [
                                v for v, *_ in self.adjacency_list[neighbor_vertex] if v != vertex
                            ]
                # Удаляем саму висячую вершину из графа
                del self.adjacency_list[vertex]

    def is_acyclic(self):
        if not self.directed:
            print("Граф не ориентированный.")
            return False

        visited = set()
        rec_stack = set()

        def dfs(vertex):
            if vertex in rec_stack:
                return True
            if vertex in visited:
                return False

            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor, *_ in self.adjacency_list.get(vertex, []):
                if dfs(neighbor):
                    return True

            rec_stack.remove(vertex)
            return False

        for node in self.adjacency_list:
            if node not in visited:
                if dfs(node):
                    print("Граф содержит циклы.")
                    return False

        print("Граф ацикличен.")
        return True

    def find_shortest_paths(self, start_vertex):
        if start_vertex not in self.adjacency_list:
            print(f"Вершина '{start_vertex}' не найдена в графе.")
            return

    # Инициализация расстояний и очереди
        distances = {vertex: float('inf') for vertex in self.adjacency_list}
        distances[start_vertex] = 0
        queue = [start_vertex]  # Очередь для обхода BFS

    # BFS для вычисления кратчайших путей
        while queue:
            current = queue.pop(0)
            for neighbor, *_ in self.adjacency_list.get(current, []):
                if distances[neighbor] == float('inf'):  # Если сосед не посещён
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

    # Разделение вершин на достижимые и недостижимые
        reachable = {v: d for v, d in distances.items() if d < float('inf')}
        unreachable = [v for v, d in distances.items() if d == float('inf')]

    # Сначала выводим кратчайшие пути
        print(f"Кратчайшие пути из вершины '{start_vertex}':")
        for vertex, distance in sorted(reachable.items(), key=lambda item: item[1]):
            print(f"  - До вершины '{vertex}': {distance} шаг(ов).")

    # Затем выводим недостижимые вершины
        if unreachable:
            print("\nНедостижимые вершины:")
            for vertex in unreachable:
                print(f"  - Вершина '{vertex}' недостижима.")

    def find_minimum_spanning_tree(self):
        if self.directed:
            print("Граф ориентированный. Невозможно найти минимальное остовное дерево.")
            return

        # Инициализация структур данных
        mst = []
        visited = set()
        start_vertex = next(iter(self.adjacency_list))
        visited.add(start_vertex)

        # Функция для нахождения ребра с минимальным весом
        def find_min_edge(visited):
            min_edge = None
            min_weight = float('inf')
            for u in visited:
                for v, weight in self.adjacency_list[u]:
                    if v not in visited and weight < min_weight:
                        min_weight = weight
                        min_edge = (u, v, weight)
            return min_edge

        # Алгоритм Прима
        while len(visited) < len(self.adjacency_list):
            min_edge = find_min_edge(visited)
            if min_edge:
                u, v, weight = min_edge
                mst.append(min_edge)
                visited.add(v)

        # Вывод минимального остовного дерева
        print("Минимальное остовное дерево:")
        for edge in mst:
            print(f"Ребро {edge[0]}-{edge[1]} с весом {edge[2]}")

    def find_all_shortest_paths(self):
        if not self.adjacency_list:
            print("Граф пуст.")
            return

        # Инициализация матрицы расстояний
        distances = {vertex: {v: float('inf') for v in self.adjacency_list} for vertex in self.adjacency_list}

        # Вычисление кратчайших путей для всех пар вершин
        for start_vertex in self.adjacency_list:
            distances[start_vertex][start_vertex] = 0
            queue = [start_vertex]  # Очередь для обхода BFS

            while queue:
                current = queue.pop(0)
                for neighbor, *_ in self.adjacency_list.get(current, []):
                    if distances[start_vertex][neighbor] == float('inf'):  # Если сосед не посещён
                        distances[start_vertex][neighbor] = distances[start_vertex][current] + 1
                        queue.append(neighbor)

        # Вывод длин кратчайших путей для всех пар вершин
        print("Длины кратчайших путей для всех пар вершин:")
        for start_vertex in distances:
            for end_vertex in distances[start_vertex]:
                distance = distances[start_vertex][end_vertex]
                if distance == float('inf'):
                    print(f"Путь из вершины '{start_vertex}' до вершины '{end_vertex}' не существует.")
                else:
                    print(f"Путь из вершины '{start_vertex}' до вершины '{end_vertex}': {distance} шаг(ов).")

def console_interface():
    purple = "\033[35m"

    initial_choice = input(f"{purple} 1 - работа с графом с помощью файлов, 2 - создание нового графа, 3 - решение дополнительной задачи ").strip()

    if initial_choice == '1':
        filename = input("Введите имя файла с графом: ").strip()
        try:
            graph = Graph()  # Инициализируем граф перед загрузкой
            graph.load_from_file(filename)
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден. Создан пустой граф.")
            graph = create_new_graph()
        except ValueError as ve:
            print(f"Ошибка при загрузке графа: {ve}")
            graph = create_new_graph()

    elif initial_choice == '2':
        graph = create_new_graph()

    elif initial_choice == '3':
        # Новый выбор задачи
        graph = create_new_graph()

        while True:
            print("\nДополнительные задачи:")
            print("1. Сравнить полустепени исхода")
            print("2. Построить граф без висячих вершин")
            print("3. Найти кратчайшие пути из вершины")  # Новый пункт для кратчайших путей
            print("4. Найти минимальное остовное дерево")  # Новый пункт для минимального остовного дерева
            print("5. Найти длины кратчайших путей для всех пар вершин")  # Новый пункт для длин кратчайших путей
            task_choice = input("Выберите номер задачи: ").strip()

            if task_choice == '1':
                vertex = input("Введите вершину для сравнения полустепеней исхода: ").strip()
                graph.compare_outdegree(vertex)
                break

            elif task_choice == '2':
                # Удаляем висячие вершины и выводим новый граф
                graph.remove_hanging_vertices()
                print("\nГраф без висячих вершин:")
                graph.display_adjacency_list()
                break

            elif task_choice == '3':  # Реализация нахождения кратчайших путей
                start_vertex = input("Введите начальную вершину: ").strip()
                graph.find_shortest_paths(start_vertex)
                break

            elif task_choice == '4':  # Реализация нахождения минимального остовного дерева
                graph.find_minimum_spanning_tree()
                break

            elif task_choice == '5':  # Реализация нахождения длин кратчайших путей для всех пар вершин
                graph.find_all_shortest_paths()
                break

            else:
                print("Некорректный ввод. Попробуйте снова.")

        return

    else:
        print("Некорректный выбор. Создан пустой граф.")
        graph = Graph()

    while True:
        bir = "\033[36m"
        print(f"\n{bir}Меню:")
        print("1. Добавить вершину")
        print("2. Добавить ребро")
        print("3. Удалить вершину")
        print("4. Удалить ребро")
        print("5. Показать граф")
        print("6. Показать рёбра графа")
        print("7. Сохранить в файл")
        print("8. Создать копию графа")
        print("9. Загрузить граф из файла")
        print("10. Выполнить дополнительную задачу 1")
        print("11. Выйти")
        print("12. Найти вершины с петлями")
        print("13. Удалить висячие вершины")
        print("14. Проверить, является ли граф ацикличным")
        print("15. Найти кратчайшие пути из вершины")  # Добавлен новый пункт
        print("16. Найти минимальное остовное дерево")  # Добавлен новый пункт
        print("17. Найти длины кратчайших путей для всех пар вершин")  # Добавлен новый пункт

        green = "\033[32m"
        choice = input(f"{green}Введите номер действия: ").strip()

        if choice == '1':
            vertex = input("Введите имя вершины: ").strip()
            graph.add_vertex(vertex)

        elif choice == '2':
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()
            if graph.weighted:
                while True:
                    weight_input = input("Введите вес ребра: ").strip()
                    try:
                        weight = float(weight_input)
                        break
                    except ValueError:
                        print("Неверный формат веса. Пожалуйста, введите число.")
            else:
                weight = None

            edge_exists = any(neighbor == v for neighbor, *_ in graph.adjacency_list.get(u, []))

            if edge_exists:
                overwrite_choice = input(f"Ребро {u}-{v} уже существует. Хотите перезаписать его? (да/нет): ").strip().lower()
                if overwrite_choice in ['да', 'д', 'yes', 'y']:
                    success = graph.add_edge(u, v, weight=weight, overwrite=True)
                    if not success:
                        print("Не удалось перезаписать ребро.")
                else:
                    print("Добавление ребра отменено.")
            else:
                success = graph.add_edge(u, v, weight=weight)
                if not success:
                    print("Не удалось добавить ребро.")

        elif choice == '3':
            vertex = input("Введите имя вершины для удаления: ").strip()
            graph.remove_vertex(vertex)

        elif choice == '4':
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()
            graph.remove_edge(u, v)

        elif choice == '5':
            print("\nТекущий граф:")
            graph.display_adjacency_list()
            graph_type = []
            graph_type.append("Ориентированный" if graph.directed else "Неориентированный")
            graph_type.append("Взвешенный" if graph.weighted else "Невзвешенный")
            print(f"Тип графа: {', '.join(graph_type)}")

        elif choice == '6':
            print("\nСписок рёбер:")
            for edge in graph.edges():
                if graph.weighted:
                    print(f"{edge[0]} - {edge[1]} (Вес: {edge[2]})")
                else:
                    print(f"{edge[0]} - {edge[1]}")

        elif choice == '7':
            filename = input("Введите имя файла для сохранения: ").strip()
            graph.save_to_file(filename)
            print(f"Граф сохранён в файл '{filename}'.")

        elif choice == '8':
            copy_graph = graph.copy()
            print("\nСоздана копия графа. Вот её содержимое:")
            copy_graph.display_adjacency_list()
            graph_type = []
            graph_type.append("Ориентированный" if copy_graph.directed else "Неориентированный")
            graph_type.append("Взвешенный" if copy_graph.weighted else "Невзвешенный")
            print(f"Тип графа копии: {', '.join(graph_type)}")

        elif choice == '9':
            filename = input("Введите имя файла для загрузки графа: ").strip()
            try:
                graph.load_from_file(filename)
            except FileNotFoundError:
                print(f"Файл '{filename}' не найден.")
            except ValueError as ve:
                print(f"Ошибка при загрузке графа: {ve}")

        elif choice == '10':
            vertex = input("Введите вершину для сравнения полустепеней исхода: ").strip()
            graph.compare_outdegree(vertex)

        elif choice == '11':
            break

        elif choice == '12':
            graph.find_loops()

        elif choice == '13':
            graph.remove_hanging_vertices()
            print("\nГраф без висячих вершин:")
            graph.display_adjacency_list()

        elif choice == '14':
            graph.is_acyclic()

        elif choice == '15':  # Вызов кратчайших путей
            start_vertex = input("Введите начальную вершину: ").strip()
            graph.find_shortest_paths(start_vertex)

        elif choice == '16':  # Вызов минимального остовного дерева
            graph.find_minimum_spanning_tree()

        elif choice == '17':  # Вызов длин кратчайших путей для всех пар вершин
            graph.find_all_shortest_paths()

        else:
            print("Некорректный ввод.")

    print("Завершение работы.")

def create_new_graph():
    # Запрашиваем тип графа у пользователя
    while True:
        directed_input = input("Граф ориентированный? (да/нет): ").strip().lower()
        if directed_input in ['да', 'д', 'yes', 'y']:
            directed = True
            break
        elif directed_input in ['нет', 'н', 'no', 'n']:
            directed = False
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

    while True:
        weighted_input = input("Граф взвешенный? (да/нет): ").strip().lower()
        if weighted_input in ['да', 'д', 'yes', 'y']:
            weighted = True
            break
        elif weighted_input in ['нет', 'н', 'no', 'n']:
            weighted = False
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

    graph = Graph(directed=directed, weighted=weighted)
    print("Создан новый граф.")
    graph_type = []
    graph_type.append("Ориентированный" if graph.directed else "Неориентированный")
    graph_type.append("Взвешенный" if graph.weighted else "Невзвешенный")
    print(f"Тип графа: {', '.join(graph_type)}")
    return graph

if __name__ == "__main__":
    console_interface()
