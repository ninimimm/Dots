# Точки
Выполнил: Чернов Никита
# Описание продукта
Данное приложение является реализацией игры Точки. Оно поддерживает игра от 2 до 4 игроков. Играть можно как с друзьями, так и с компьютером.
# Подробности реализации
Класс Game реализует логику обработку следующего хода игры. Также создан таймер для контроля игры - если человек долго не может определиться с ходом, то он автоматически выбывает из игры. Тем самым сохраняется динамика игры, и каждый из игроков постоянно находится в напряжении, продумывая следующие ходы.

В классе Gui реализован пользовательский интерфейс и различные варианты запуска игры. Также здесь происходит выбор настроек игры и просмотр таблицы лидеров.

В классе City реализована основная логика поиска маршрутов в графе созданных точек. Эффективно написанный алгоритм DFS позволяет быстро находить циклы с вражескими точками и тем самым программа работает моментально, не тратя большое время на поиск. Иначе игровое окно бы зависало и это вводило бы игроков в заблуждение.

В классе PC реализована двух ботов, сложного и легкого.

Также реализовано сохранение результатов игроков, вследствие чего есть таблица лидеров. Она хранит лучшие результаты каждого пользователя в игре против сложного бота.

В правильности работы методов можно не сомневаться, написано множество тестов, проверяющих корректность поиска в графе, окраски захваченной зоны, а также на сам процесс игры.
# Правила игры Точки
Ознакомиться с правилами данной игры можно по данной ссылке: https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D1%87%D0%BA%D0%B8_(%D0%B8%D0%B3%D1%80%D0%B0)