#1
import pandas as pd
#1. Загрузка файла в DataFrame
file = r'C:\Users\Maral\hospital_patient_treatment.xlsx'
try:
    df = pd.read_excel(file)
    print("Файл загружен!\n")
    #2. Вывод первых 5 строк
    print("--- Первые 5 строк данных ---")
    print(df.head())
    print("-" * 30)
    #3. Определение количества строк и столбцов
    rows, cols = df.shape
    print(f"\nКоличество строк: {rows}")
    print(f"Количество столбцов: {cols}")
    print("-" * 30)
    #4. Просмотр типов данных всех колонок
    print("\n--- Типы данных колонок ---")
    print(df.dtypes)
    print("-" * 30)
    #5. Подсчет количества пропусков в каждой колонке
    print("\n--- Количество пропусков в каждой колонке ---")
    print(df.isnull().sum())
except Exception as e:
    print(f"Произошла ошибка: {e}")

#2
#1. Находим уникальные значения в колонке Treatment_Type и сохраняем в список
treatment_types_list = df['Treatment_Type'].unique().tolist()
#2. Находим уникальные значения в колонке Department и сохраняем в список
departments_list = df['Department'].unique().tolist()
#Вывод результатов
print("--- Список типов лечения (Treatment_Type) ---")
print(treatment_types_list)
print("\n--- Список отделений (Department) ---")
print(departments_list)

#3
#1. Создаем список всех Patient_ID в верхнем регистре
patient_id_upper = df['Patient_ID'].astype(str).str.upper().tolist()
#2. Создаем список длины каждого Patient_ID
patient_id_length = df['Patient_ID'].astype(str).str.len().tolist()
#3. Находим среднюю длину идентификаторов
average_id_length = sum(patient_id_length) / len(patient_id_length)
#Вывод результатов
print("--- Первые 5 идентификаторов в верхнем регистре ---")
print(patient_id_upper[:5])

print("\n--- Первые 5 значений длины идентификаторов ---")
print(patient_id_length[:5])

print(f"\nСредняя длина идентификатора: {average_id_length:.2f}")

#4
#1. Фильтрация пациентов: возраст > 65 и Risk_Score >= 0.7
high_risk_elderly = df[(df['Age'] > 65) & (df['Risk_Score'] >= 0.7)]
#2. Выбор конкретных столбцов для вывода
columns = ['Patient_ID', 'Age', 'Diagnosis', 'Risk_Score']
#3. Вывод первых 10 строк результата
print(f"Пациенты подходящие под критерии: {len(high_risk_elderly)}")
print("-" * 50)
print(high_risk_elderly[columns].head(10))

#5
#1. Создаем новую колонку Cost_per_Treatment
df['Cost_per_Treatment'] = df['Treatment_Cost'] / (df['Lab_Test_Count'] + df['Medication_Count'] + 1)
#2. Сортируем данные по новой колонке в порядке убывания
top_expensive_treatments = df.sort_values(by='Cost_per_Treatment', ascending=False).head(10)
#Вывод результатов
columns = ['Patient_ID', 'Treatment_Cost', 'Lab_Test_Count', 'Medication_Count', 'Cost_per_Treatment']
print("--- Топ-10 пациентов с максимальной стоимостью на одну процедуру ---")
print(top_expensive_treatments[columns])

#6
#1. Преобразуем колонки в формат даты (на случай, если они загрузились как строки)
df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])
#2. Создаем колонку Hospital_Stay_Days
df['Hospital_Stay_Days'] = (df['Discharge_Date'] - df['Admission_Date']).dt.days
#3. Находим среднюю продолжительность пребывания
average_stay = df['Hospital_Stay_Days'].mean()
#4. Выводим топ-10 пациентов с самой долгой госпитализацией
top_long_stays = df.sort_values(by='Hospital_Stay_Days', ascending=False).head(10)
#Вывод результатов
print(f"Средняя продолжительность пребывания в больнице: {average_stay:.1f} дней")
print("\n--- Топ-10 пациентов по длительности госпитализации ---")
columns = ['Patient_ID', 'Admission_Date', 'Discharge_Date', 'Hospital_Stay_Days']
print(top_long_stays[columns])

#7
#1. Поиск пациентов с диагнозом, содержащим "Cardiac"
cardiac_patients = df[df['Diagnosis'].str.contains('Cardiac', case=False, na=False)]
#2. Выбор необходимых столбцов для вывода
columns = ['Patient_ID', 'Diagnosis', 'Treatment_Type', 'Days_in_Hospital']
#Вывод результатов
print(f"Количество пациентов Cardiac: {len(cardiac_patients)}")
print("-" * 70)
if not cardiac_patients.empty:
    print(cardiac_patients[columns].head(10))
else:
    print("Пациенты с диагнозом 'Cardiac' не найдены.")

#8
#1. Сортировка по стоимости лечения (Treatment_Cost) по убыванию
top_10_expensive = df.sort_values(by='Treatment_Cost', ascending=False).head(10)
#2. Сортировка по возрасту (Age) по возрастанию
top_10_youngest = df.sort_values(by='Age', ascending=True).head(10)
#Вывод результатов
print("--- ТОП-10 САМЫХ ДОРОГИХ КУРСОВ ЛЕЧЕНИЯ ---")
print(top_10_expensive[['Patient_ID', 'Diagnosis', 'Treatment_Cost']])
print("\n" + "="*50 + "\n")
print("--- ТОП-10 САМЫХ МОЛОДЫХ ПАЦИЕНТОВ ---")
print(top_10_youngest[['Patient_ID', 'Age', 'Department', 'Diagnosis']])

#9
#1. Расчет индекса активности (Activity_Index)
df['Activity_Index'] = (df['Lab_Test_Count'] + df['Medication_Count'] + df['Physical_Therapy_Sessions']) / (df['Days_in_Hospital'] + 1)
#2. Сортировка по индексу активности в порядке убывания
top_active_patients = df.sort_values(by='Activity_Index', ascending=False).head(5)
#3. Вывод топ-5 самых "активных" пациентов
print("--- ТОП-5 ПАЦИЕНТОВ ПО ИНДЕКСУ АКТИВНОСТИ ---")
columns = [
    'Patient_ID',
    'Lab_Test_Count',
    'Medication_Count',
    'Physical_Therapy_Sessions',
    'Days_in_Hospital',
    'Activity_Index'
]
print(top_active_patients[columns])

#10
#1. Создаем генератор icu_patients
icu_patients = (row for row in df[df['ICU_Stay'] == 1].itertuples())
#2. Вывод первых 20 пациентов из генератора
print(f"{'Patient_ID':<15} | {'Department':<15} | {'Days':<5} | {'Cost':<10}")
print("-" * 55)
try:
    for i in range(20):
        patient = next(icu_patients)
        print(f"{patient.Patient_ID:<15} | {patient.Department:<15} | {patient.Days_in_Hospital:<5} | {patient.Treatment_Cost:<10.2f}")
except StopIteration:
    print("\n--- Конец данных ---")
