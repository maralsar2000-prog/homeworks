#1
with open("data.txt", "w", encoding= "utf-8") as f:
    f.write("Привет\n")


with open("data.txt", "r", encoding= "utf-8") as f:
    content= f.read()
    print(content)

    # 2
    with open("file.txt", "w") as f:
        for i in range(1, 11):
            f.write(str(i) + "\n")

    with open("file.txt", "r") as f:
        content = f.read()
        print(content)

        # 3
        mylist = ["марал", "назерке", "диана", "зере"]
        with open("names.txt", "w", encoding="utf-8") as f:
            for name in mylist:
                f.write(name + "\n")

        with open("names.txt", "r", encoding="utf-8") as f:
            for obj in f:
                print(obj.capitalize())

                # csv
                import csv

                data = [
                    ["Имя", "Возраст"],
                    ["Марал", 17],
                    ["Диана", 18],
                ]
                with open("file.csv", "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(data)

                import csv

                with open("file.csv", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        print(row["Имя"], row["Возраст"])
