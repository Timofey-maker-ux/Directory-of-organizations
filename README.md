# Organizations API

API для работы с организациями. Все эндпоинты защищены API-ключом (`x-api-key`).

**Authentication:** Передавайте API-ключ в заголовке `x-api-key`.

```http
GET /organizations/...
Header: x-api-key: `<your_api_key>`
```

---

## Эндпоинты

### 1. Получить организации по зданию

**Endpoint:**

```
GET /organizations/by-building/{building_id}
```

**Описание:** Возвращает все организации, находящиеся в указанном здании.

**Path Parameters:**

| Параметр    | Тип | Описание  |
| ----------- | --- | --------- |
| building_id | int | ID здания |

**Response:**

* `200 OK` — список организаций (`List[OrganizationRead]`)
* `404 Not Found` — если организации не найдены

---

### 2. Поиск организаций по виду деятельности

**Endpoint:**

```
GET /organizations/search/by-activity
```

**Query Parameters:**

| Параметр      | Тип | Описание                               |
| ------------- | --- | -------------------------------------- |
| activity_name | str | Название вида деятельности или подвида |

**Response:**

* `200 OK` — список организаций (`List[OrganizationRead]`)
* `404 Not Found` — если активности или организации не найдены

---

### 3. Поиск организаций в радиусе

**Endpoint:**

```
GET /organizations/geo/radius
```

**Query Parameters:**

| Параметр      | Тип   | Описание               |
| ------------- | ----- | ---------------------- |
| lat           | float | Широта точки           |
| lon           | float | Долгота точки          |
| radius_meters | float | Радиус поиска в метрах |

**Response:**

* `200 OK` — список организаций (`List[OrganizationRead]`)
* `404 Not Found` — если организации не найдены

---

### 4. Поиск организаций по bounding box

**Endpoint:**

```
GET /organizations/geo/bbox
```

**Query Parameters:**

| Параметр | Тип   | Описание                      |
| -------- | ----- | ----------------------------- |
| lat1     | float | Верхняя/нижняя граница широты |
| lon1     | float | Левая граница долготы         |
| lat2     | float | Верхняя/нижняя граница широты |
| lon2     | float | Правая граница долготы        |

**Response:**

* `200 OK` — список организаций (`List[OrganizationRead]`)
* `404 Not Found` — если организации не найдены

---

### 5. Получить организацию по ID

**Endpoint:**

```
GET /organizations/{org_id}
```

**Path Parameters:**

| Параметр | Тип | Описание       |
| -------- | --- | -------------- |
| org_id   | int | ID организации |

**Response:**

* `200 OK` — объект организации (`OrganizationRead`)
* `404 Not Found` — если организация не найдена

---

### 6. Поиск организаций по названию

**Endpoint:**

```
GET /organizations/search/by-name
```

**Query Parameters:**

| Параметр | Тип | Описание                          |
| -------- | --- | --------------------------------- |
| query    | str | Строка поиска (минимум 2 символа) |

**Response:**

* `200 OK` — список организаций (`List[OrganizationRead]`)
* `404 Not Found` — если организации не найдены



## Пример ответа

Пример объекта `OrganizationRead`:

```json
{
  "name": "Мясной дом",
  "phones": [
    "+7-999-111-22-33"
  ],
  "id": 1,
  "building": {
    "id": 1,
    "address": "ул. Ленина, 1",
    "latitude": 55.7558,
    "longitude": 37.6176
  },
  "activities": [
    {
      "id": 1,
      "name": "Еда",
      "parent_id": null
    },
    {
      "id": 2,
      "name": "Мясная продукция",
      "parent_id": 1
    },
    {
      "id": 3,
      "name": "Колбасы",
      "parent_id": 2
    }
  ]
}
```

Все эндпоинты возвращают данные в формате JSON. Ошибки возвращаются с HTTP-кодами и сообщением в поле `detail`.
