class DataFrame:
    def __init__(self, data: dict):
        # Генерираме списък от дължините на всички колони
        lengths = [len(v) for v in data.values()]
        # Проверяваме дали има подадени колони и дали всички са с еднаква дължина
        if not lengths or any(length != lengths[0] for length in lengths):
            raise ValueError("Всички колони трябва да са с еднакъв брой елементи")
        # Запаметяваме реда на колоните
        self._columns = list(data.keys())
        # Копираме данните във вътрешен речник, за да не модифицираме външния
        self._data = {col: list(data[col]) for col in self._columns}

    @property
    def shape(self):
        # Брой редове = дължина на първата колона (или 0 ако няма колони)
        rows = len(next(iter(self._data.values()), []))
        # Брой колони = дължина на списъка с имена на колони
        cols = len(self._columns)
        return (rows, cols)

    def __getitem__(self, column):
        # Достъп до колона за четене: df["column"]
        if column not in self._data:
            raise KeyError(f"Няма такава колона: {column!r}")
        return self._data[column]

    def __setitem__(self, column, values):
        # Достъп до колона за запис: df["column"] = values
        rows = self.shape[0]
        # Проверяваме дали дължината на новата колона съвпада с броя редове
        if len(values) != rows:
            raise ValueError(f"Дължината на колоната ({len(values)}) не съвпада с броя редове ({rows})")
        # Ако колоната не съществува, я добавяме в списъка с имена
        if column not in self._columns:
            self._columns.append(column)
        # Записваме или презаписваме стойностите във вътрешния речник
        self._data[column] = list(values)

    def __str__(self):
        # Форматираме заглавния ред: име на колони, разделени с " | "
        header = " | ".join(self._columns)
        # Сглобяваме всеки ред от таблицата
        rows = []
        for i in range(self.shape[0]):
            # Взимаме i-тата стойност от всяка колона
            row = [str(self._data[col][i]) for col in self._columns]
            rows.append(" | ".join(row))
        table = "\n".join(rows)
        # Връщаме низ с размерността, заглавния ред и данните
        return f"DataFrame ({self.shape[0]}×{self.shape[1]})\n{header}\n{table}"

    # За да имаме еднакво представяне и в интерактивен режим
    __repr__ = __str__


if __name__ == "__main__":
    # Създаваме DataFrame с две колони: name и age
    df = DataFrame({
        "name": ["Гошо", "Пешо"],
        "age": [30, 16]
    })
    print(df.shape)         # (2, 2)
    print(df["name"])       # ['Гошо', 'Пешо']

    # Добавяме нова колона height
    df["height"] = [175, "по-висок от Стан"]
    print(df.shape)         # (2, 3)
    print(df)
    # Резултат:
    # DataFrame (2×3)
    # name | age | height
    # Гошо  | 30  | 175
    # Пешо  | 16  | по-висок от Стан
