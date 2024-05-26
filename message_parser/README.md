# Message Parser

## Grammar of Each Command

### 記帳

- command: [!記帳]
- pattern: [!記帳] [日期] [項目] [金額] [類別] [備註]
- required parameter:
    - 日期
    - 項目
    - 金額
    - 類別
    - 備註
- parameter type:
    - 日期: string
    - 項目: string
    - 金額: int
    - 類別: string
    - 備註: string
- function interface
    ```python
    def create_record(user_id, date, item, cost, category, comment)
    ```

### 最近記帳

- command: [!最近記帳]
- pattern: [!最近記帳] [方法] [筆數/天數]
- optional parameter:
    - [方法]
        - 最近筆數
        - 最近天數
    - [筆數/天數]
        - 筆數
        - 天數
- parameter type:
    - 方法: string
    - 筆數/天數: int
- function interface
    ```python
    def show_recent_record(user_id, num=5, days=3, type='num')
    ```

### 查詢

- command: [!查詢]
- pattern: [!查詢] [起始日期] [截止日期]
- required parameter:
    - 起始日期
- optional parameter:
    - 截止日期
- parameter type:
    - 起始日期: string
    - 截止日期: string
- function interface
    ```python
    def search_record(user_id, date_from, date_to=None)
    ```

### 修改記帳

- command: [!修改記帳]
- pattern: [!修改記帳] [Record_ID] [[更改項目] [更改數值]]+
- required parameter:
    - Record_ID
    - 更改項目
    - 更改數值
- parameter type:
    - Record_ID: int
    - 更改項目: string
    - 更改數值: string
- function interface
    ```python
    def update_record(user_id, record_id, item=None, cost=None, category=None, comment=None)
    ```

### 刪除記帳

- command: [!刪除記帳]
- pattern: [!刪除記帳] [Record_ID]
- required parameter:
    - Record_ID
- parameter type:
    - Record_ID: int
- function interface
    ```python
    def delete_record(user_id, record_id)
    ```

### 匯出

- command: [!匯出]
- pattern: [!匯出] [方法]
- optional parameter:
    - 方法
        - 本月: 'this month'
        - 本年: 'this year'
        - 全部: 'all'
- parameter type:
    - 方法: string
- function interface
    ```python
    def export_record(user_id, method='this month')
    ```