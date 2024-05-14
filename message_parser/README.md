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

### 最近記帳

- command: [!最近記帳]
- pattern: [!最近記帳] [方法] [筆數/天數]
- required parameter:
    - [方法]
        - 最近筆數
        - 最近天數
- optional parameter:
    - [筆數/天數]
        - 筆數
        - 天數
- parameter type:
    - 方法: string
    - 筆數/天數: int

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

### 修改記帳

- command: [!修改記帳]
- pattern: [!修改記帳] [Record_ID] [[更改項目] [更改數值]]+
- required parameter:
    - Record_ID
    - 更改項目
    - 更改數值
- parameter type:
    - Record_ID: string
    - 更改項目: string
    - 更改數值: string

### 刪除記帳

- command: [!刪除記帳]
- pattern: [!刪除記帳] [Record_ID]
- required parameter:
    - Record_ID
- parameter type:
    - Record_ID: string

### 匯出

- command: [!匯出]
- pattern: [!匯出] [方法]
- optional parameter:
    - 方法
        - 本月
        - 本年
        - 全部
- parameter type:
    - 方法: string