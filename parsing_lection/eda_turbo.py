import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'turbo_cars.csv'), encoding='utf-8-sig')

print(df.head())
print(df.shape)
print(df.dtypes)

# убираем строки без названия и фото
df = df[df['name'].notna() & (df['name'].str.strip() != '')]
df = df[df['photos'].notna() & (df['photos'].str.strip() != '')]

# вытаскиваем тип топлива из колонки с двигателем
df['fuel_type'] = df['specs_Двигатель'].str.split(r'[/,]').str[-1].str.strip().str.lower()
df['fuel_fallback'] = df['specs_Тип топлива'].str.lower().str.strip()
df['fuel'] = df['fuel_type'].where(df['fuel_type'].notna(), df['fuel_fallback'])

# дроп ненужного
drop_cols = [
    'specs_VIN', 'specs_Гос номер', 'specs_Комплектация',
    'specs_Мощность', 'specs_Объем двигателя', 'specs_Тип топлива',
    'specs_Учёт', 'specs_Двигатель', 'fuel_type', 'fuel_fallback',
    'url', 'image_url'
]
df = df.drop(columns=drop_cols)

# цена
df['price_soms'] = df['price_soms'].fillna(df['price'])
df = df.drop(columns=['price'])

# пропуски числовых
df['mileage_km'] = df['mileage_km'].fillna(df['mileage_km'].median())
df['year_from_catalog'] = df['year_from_catalog'].fillna(df['year_from_catalog'].median())
df['photos_count'] = df['photos_count'].fillna(df['photos_count'].median())
df['specs_Год выпуска'] = df['specs_Год выпуска'].fillna(df['specs_Год выпуска'].mode()[0])
df['fuel'] = df['fuel'].fillna(df['fuel'].mode()[0])

# коробка
df['specs_Коробка передач'] = df['specs_Коробка передач'].fillna(df['specs_Коробка'])
df['specs_Коробка передач'] = df['specs_Коробка передач'].fillna(df['specs_Коробка передач'].mode()[0])
df['specs_Коробка передач'] = df['specs_Коробка передач'].replace({'АКПП': 'автомат'})
df = df.drop(columns=['specs_Коробка'])

columns_to_fill = ['specs_Кузов', 'specs_Наличие', 'specs_Обмен',
            'specs_Привод', 'specs_Цвет', 'specs_Регион, город',
            'specs_Состояние', 'specs_Таможня']
for columns_mode in columns_to_fill:
    df[columns_mode] = df[columns_mode].fillna(df[columns_mode].mode()[0])

# дата публикации
df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
df['published_hour'] = df['published_at'].dt.hour
df['published_weekday'] = df['published_at'].dt.weekday
df = df.drop(columns=['published_at'])

# пробег
df['specs_Пробег'] = df['specs_Пробег'].fillna(df['specs_Пробег ( км )'])
df = df.drop(columns=['specs_Пробег ( км )'])

# бинарные признаки
df['has_extra_info'] = df['specs_Прочее'].notna().astype(int)
df['has_installment'] = df['specs_Рассрочка'].notna().astype(int)
df = df.drop(columns=['specs_Прочее', 'specs_Рассрочка'])

df['specs_Руль'] = df['specs_Руль'].str.lower().str.strip().map({'слева': 0, 'справа': 1}).fillna(0).astype(int)

# чистим числа от пробелов и лишних символов
def clean_num(s):
    s = s.astype(str).str.replace(r'\s+', '', regex=True).str.replace(r'[^\d]', '', regex=True)
    return pd.to_numeric(s, errors='coerce')

for columns_mode in ['price_soms', 'specs_Пробег']:
    cleaned = clean_num(df[columns_mode])
    df[columns_mode] = cleaned.fillna(cleaned.median()).astype(int)

for columns_mode in ['year_from_catalog', 'mileage_km', 'photos_count', 'specs_Год выпуска']:
    df[columns_mode] = pd.to_numeric(df[columns_mode], errors='coerce').fillna(0).astype(int)

# кодируем таможню и топливо
df['specs_Таможня'] = df['specs_Таможня'].str.lower().str.strip().map(
    {'растаможен': 0, 'не растаможен': 1}
).fillna(-1).astype(int)

fuel_map = {'бензин': 0, 'дизель': 1, 'гибрид': 2, 'электро': 3, 'газ': 4, 'газ-бензин': 5}
df['specs_Двигатель'] = df['fuel'].map(fuel_map).fillna(-1).astype(int)
df = df.drop(columns=['fuel'])

print(df.isnull().sum())
print("дубликаты:", df.duplicated().sum())
df = df.drop_duplicates()

# метки для графиков
fuel_labels = {0: 'бензин', 1: 'дизель', 2: 'гибрид', 3: 'электро', 4: 'газ', 5: 'газ-бензин', -1: 'неизвестно'}
customs_labels = {0: 'растаможен', 1: 'не растаможен', -1: 'неизвестно'}
df['тип топлива'] = df['specs_Двигатель'].map(fuel_labels)
df['таможня'] = df['specs_Таможня'].map(customs_labels)





# ================= графики =================

plt.figure(figsize=(7, 4))
sns.histplot(df['price_soms'], bins=50, kde=True)
plt.title('распределение цены'); plt.xlabel('цена (сом)'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.boxplot(x=df['price_soms'])
plt.title('выбросы по цене'); plt.xlabel('цена (сом)')
plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.histplot(df['mileage_km'], bins=50, kde=True)
plt.title('распределение пробега'); plt.xlabel('пробег (км)'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.boxplot(x=df['mileage_km'])
plt.title('выбросы по пробегу'); plt.xlabel('пробег (км)')
plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.histplot(df['year_from_catalog'], bins=30, kde=True)
plt.title('распределение года выпуска'); plt.xlabel('год'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='тип топлива', order=df['тип топлива'].value_counts().index)
plt.title('кол-во машин по типу топлива'); plt.xlabel('тип топлива'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='specs_Коробка передач', order=df['specs_Коробка передач'].value_counts().index)
plt.title('кол-во машин по коробке передач'); plt.xlabel('коробка передач'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='specs_Кузов', order=df['specs_Кузов'].value_counts().index)
plt.xticks(rotation=30, ha='right')
plt.title('кол-во машин по типу кузова'); plt.xlabel('кузов'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
sns.countplot(data=df, x='specs_Привод', order=df['specs_Привод'].value_counts().index)
plt.title('кол-во машин по приводу'); plt.xlabel('привод'); plt.ylabel('кол-во')
plt.grid(True); plt.tight_layout(); plt.show()

print(df.groupby('тип топлива')['price_soms'].median())
plt.figure(figsize=(7, 4))
sns.barplot(data=df, x='тип топлива', y='price_soms')
plt.title('средняя цена по типу топлива'); plt.xlabel('тип топлива'); plt.ylabel('цена (сом)')
plt.grid(True); plt.tight_layout(); plt.show()

print(df.groupby('specs_Привод')['price_soms'].median())
plt.figure(figsize=(7, 4))
sns.barplot(data=df, x='specs_Привод', y='price_soms')
plt.title('средняя цена по приводу'); plt.xlabel('привод'); plt.ylabel('цена (сом)')
plt.grid(True); plt.tight_layout(); plt.show()

print(df.groupby('таможня')['price_soms'].median())
plt.figure(figsize=(6, 4))
sns.barplot(data=df, x='таможня', y='price_soms')
plt.title('средняя цена по статусу таможни'); plt.xlabel('таможня'); plt.ylabel('цена (сом)')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
plt.scatter(df['mileage_km'], df['price_soms'], alpha=0.3, s=10)
plt.title('связь цены и пробега'); plt.xlabel('пробег (км)'); plt.ylabel('цена (сом)')
plt.grid(True); plt.tight_layout(); plt.show()

plt.figure(figsize=(7, 4))
plt.scatter(df['year_from_catalog'], df['price_soms'], alpha=0.3, s=10)
plt.title('связь цены и года выпуска'); plt.xlabel('год'); plt.ylabel('цена (сом)')
plt.grid(True); plt.tight_layout(); plt.show()

# корреляция
df = df.drop(columns=['тип топлива', 'таможня'])

corr_cols = [
    'price_soms', 'mileage_km', 'year_from_catalog', 'photos_count',
    'specs_Двигатель', 'specs_Таможня', 'has_extra_info',
    'has_installment', 'published_hour', 'published_weekday',
]
corr = df[corr_cols].corr()

plt.figure(figsize=(10, 7))
sns.heatmap(corr, annot=True, cmap='RdBu_r')
plt.title('корреляционная матрица')
plt.tight_layout(); plt.show()

print(corr['price_soms'].sort_values(ascending=False))

print("""
итоги:

1. большинство машин на бензине, дизель и газ встречаются намного реже
2. самый популярный кузов - седан и внедорожник 5 дв
3. преобладает автоматическая коробка передач
4. чем новее машина — тем выше цена
5. пробег и цена отрицательно коррелируют — чем больше пробег тем дешевле
6. большинство машин растаможены
7. привод в основном передний, полный встречается реже и стоит дороже

""")