def input_graph_from_keyboard():
    n = int(input("Введите количество вершин: "))
    m = int(input("Введите количество рёбер: "))
    
    graph = {i: [] for i in range(n)}
    
    print("Введите рёбра в формате 'u v' (u -> v):")
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
    
    return graph

def input_graph_from_file(filename):
    graph = {}
    with open(filename, 'r') as file:
        n, m = map(int, file.readline().split())
        graph = {i: [] for i in range(n)}
        for _ in range(m):
            u, v = map(int, file.readline().split())
            graph[u].append(v)
    return graph

def find_vertices_with_greater_outdegree(graph, target_vertex):
    # Считаем полустепени исхода для каждой вершины
    out_degrees = {vertex: len(neighbors) for vertex, neighbors in graph.items()}
    
    # Полустепень исхода для заданной вершины
    target_out_degree = out_degrees.get(target_vertex, 0)
    
    # Поиск вершин, у которых полустепень исхода больше, чем у заданной вершины
    result = [vertex for vertex, out_degree in out_degrees.items() if out_degree > target_out_degree]
    
    return result

def main():
    print("Выберите способ ввода графа:")
    print("1. Ввести граф с клавиатуры")
    print("2. Прочитать граф из файла")
    
    choice = input("Ваш выбор (1 или 2): ")
    
    if choice == "1":
        graph = input_graph_from_keyboard()
    elif choice == "2":
        filename = input("Введите имя файла: ")
        graph = input_graph_from_file(filename)
    else:
        print("Некорректный выбор. Завершение программы.")
        return
    
    target_vertex = int(input("Введите вершину, для которой нужно сравнить полустепени исхода: "))
    
    result = find_vertices_with_greater_outdegree(graph, target_vertex)
    
    if result:
        print(f"Вершины с полустепенью исхода больше, чем у вершины {target_vertex}: {result}")
    else:
        print(f"Нет вершин с полустепенью исхода больше, чем у вершины {target_vertex}.")

if __name__ == "__main__":
    main()
