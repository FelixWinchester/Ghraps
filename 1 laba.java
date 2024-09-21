import java.io.*;
import java.util.*;

public class Graph {
    private Map<Integer, List<Integer>> adjacencyList;

    // Конструктор по умолчанию
    public Graph() {
        this.adjacencyList = new HashMap<>();
    }

    // Конструктор, заполняющий данные графа из файла
    public Graph(String filename) throws IOException {
        this();
        loadGraphFromFile(filename);
    }

    // Конструктор-копия
    public Graph(Graph other) {
        this.adjacencyList = new HashMap<>(other.adjacencyList);
    }

    // Метод для добавления вершины
    public void addVertex(int vertex) {
        adjacencyList.putIfAbsent(vertex, new ArrayList<>());
    }

    // Метод для добавления ребра (дуги)
    public void addEdge(int from, int to) {
        addVertex(from);
        addVertex(to);
        adjacencyList.get(from).add(to);
    }

    // Метод для удаления вершины
    public void removeVertex(int vertex) {
        adjacencyList.values().forEach(e -> e.remove(Integer.valueOf(vertex)));
        adjacencyList.remove(vertex);
    }

    // Метод для удаления ребра (дуги)
    public void removeEdge(int from, int to) {
        List<Integer> edges = adjacencyList.get(from);
        if (edges != null) {
            edges.remove(Integer.valueOf(to));
        }
    }

    // Метод для создания списка рёбер на основе списка смежности
    public List<Edge> getEdgeList() {
        List<Edge> edges = new ArrayList<>();
        for (Map.Entry<Integer, List<Integer>> entry : adjacencyList.entrySet()) {
            int from = entry.getKey();
            for (int to : entry.getValue()) {
                edges.add(new Edge(from, to));
            }
        }
        return edges;
    }

    // Метод для вывода списка смежности в файл
    public void writeAdjacencyListToFile(String filename) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (Map.Entry<Integer, List<Integer>> entry : adjacencyList.entrySet()) {
                writer.write(entry.getKey() + ": " + entry.getValue());
                writer.newLine();
            }
        }
    }

    // Метод для загрузки графа из файла
    private void loadGraphFromFile(String filename) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(":");
                int vertex = Integer.parseInt(parts[0].trim());
                String[] edges = parts[1].trim().split(",");
                for (String edge : edges) {
                    addEdge(vertex, Integer.parseInt(edge.trim()));
                }
            }
        }
    }

    // Вложенный класс для представления рёбер графа
    public static class Edge {
        private final int from;
        private final int to;

        public Edge(int from, int to) {
            this.from = from;
            this.to = to;
        }

        public int getFrom() {
            return from;
        }

        public int getTo() {
            return to;
        }

        @Override
        public String toString() {
            return "(" + from + " -> " + to + ")";
        }
    }

    // Метод для отображения списка смежности
    public void displayAdjacencyList() {
        for (Map.Entry<Integer, List<Integer>> entry : adjacencyList.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }

    // Основной метод для консольного интерфейса
    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in);
        Graph graph = new Graph();

        while (true) {
            System.out.println("\nВыберите действие:");
            System.out.println("1. Добавить вершину");
            System.out.println("2. Добавить ребро");
            System.out.println("3. Удалить вершину");
            System.out.println("4. Удалить ребро");
            System.out.println("5. Показать список смежности");
            System.out.println("6. Сохранить список смежности в файл");
            System.out.println("7. Загрузить граф из файла");
            System.out.println("0. Выход");

            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Введите номер вершины: ");
                    int vertexToAdd = scanner.nextInt();
                    graph.addVertex(vertexToAdd);
                    break;

                case 2:
                    System.out.print("Введите начало ребра: ");
                    int fromVertex = scanner.nextInt();
                    System.out.print("Введите конец ребра: ");
                    int toVertex = scanner.nextInt();
                    graph.addEdge(fromVertex, toVertex);
                    break;

                case 3:
                    System.out.print("Введите номер вершины для удаления: ");
                    int vertexToRemove = scanner.nextInt();
                    graph.removeVertex(vertexToRemove);
                    break;

                case 4:
                    System.out.print("Введите начало ребра для удаления: ");
                    int fromEdge = scanner.nextInt();
                    System.out.print("Введите конец ребра для удаления: ");
                    int toEdge = scanner.nextInt();
                    graph.removeEdge(fromEdge, toEdge);
                    break;

                case 5:
                    graph.displayAdjacencyList();
                    break;

                case 6:
                    System.out.print("Введите имя файла для сохранения: ");
                    String saveFileName = scanner.next();
                    graph.writeAdjacencyListToFile(saveFileName);
                    break;

                case 7:
                    System.out.print("Введите имя файла для загрузки: ");
                    String loadFileName = scanner.next();
                    graph.loadGraphFromFile(loadFileName);
                    break;

                case 0:
                    System.out.println("Выход из программы.");
                    scanner.close();
                    return;

                default:
                    System.out.println("Неверный выбор. Пожалуйста, попробуйте снова.");
            }
        }
    }
}
