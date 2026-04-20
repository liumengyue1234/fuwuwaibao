# 审思明辨——智判法案双擎系统
# API 文档

## 目录

1. [得理开放平台 API](#得理开放平台-api)
2. [腾讯混元大模型 API](#腾讯混元大模型-api)
3. [腾讯文档 API](#腾讯文档-api)

---

## 得理开放平台 API

### 概述

得理开放平台提供法律场景的底层案例和法规接口，支持关键字检索和语义检索。

**API 基础地址**: `https://openapi.delilegal.com/api/qa/v3`

**认证方式**: Header 认证
```
appid: QthdBErlyaYvyXul
secret: EC5D455E6BD348CE8E18BE05926D2EBE
```

### 1. 类案检索 API

**接口地址**: `/search/queryListCase`

**请求方法**: POST

**CURL 示例**:
```bash
curl -X POST 'https://openapi.delilegal.com/api/qa/v3/search/queryListCase' \
-H "appid: QthdBErlyaYvyXul" \
-H "secret: EC5D455E6BD348CE8E18BE05926D2EBE" \
-d '{
  "pageNo": 1,
  "pageSize": 5,
  "sortField": "correlation",
  "sortOrder": "desc",
  "condition": {
    "keywordArr": ["工伤认定 上下班途中"]
  }
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| sortField | string | 是 | 排序字段：`correlation`(相关性) 或 `time`(时间) |
| sortOrder | string | 是 | 排序方式：`asc`(升序) 或 `desc`(降序) |
| condition | object | 是 | 查询条件 |
| condition.keywordArr | array | 是 | 关键词数组 |
| condition.courtLevelArr | array | 否 | 法院层级：["0":最高院, "1":高院, "2":中院, "3":基层院] |
| condition.caseYearStart | int | 否 | 案例年份起始 |
| condition.caseYearEnd | int | 否 | 案例年份结束 |
| condition.judgementTypeArr | array | 否 | 文书类型：["30":判决书, "31":裁决书, "32":调解书, "33":决定书] |

**响应示例**:
```json
{
  "success": true,
  "code": 0,
  "msg": "",
  "body": {
    "total": 100,
    "dataList": [
      {
        "id": "xxx",
        "caseName": "张三与XX公司工伤保险待遇纠纷案",
        "court": "北京市朝阳区人民法院",
        "judgeDate": "2023-05-15",
        "reason": "工伤保险待遇纠纷",
        "result": "判决被告支付原告工伤保险待遇..."
      }
    ]
  }
}
```

### 2. 法规检索 API

**接口地址**: `/search/queryListLaw`

**请求方法**: POST

**CURL 示例**:
```bash
curl -X POST 'https://openapi.delilegal.com/api/qa/v3/search/queryListLaw' \
-H "appid: QthdBErlyaYvyXul" \
-H "secret: EC5D455E6BD348CE8E18BE05926D2EBE" \
-d '{
  "pageNo": 1,
  "pageSize": 5,
  "sortField": "correlation",
  "sortOrder": "desc",
  "condition": {
    "keywords": ["工伤保险条例"],
    "fieldName": "semantic"
  }
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageNo | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| sortField | string | 是 | 排序字段：`correlation` 或 `time` |
| sortOrder | string | 是 | 排序方式：`asc` 或 `desc` |
| condition | object | 是 | 查询条件 |
| condition.keywords | array | 是 | 关键词数组 |
| condition.fieldName | string | 是 | 检索方式：`title`(关键词) 或 `semantic`(语义) |

**响应示例**:
```json
{
  "success": true,
  "code": 0,
  "msg": "",
  "body": {
    "total": 50,
    "dataList": [
      {
        "id": "xxx",
        "title": "工伤保险条例",
        "levelName": "行政法规",
        "publisherName": "国务院",
        "publishDate": "2010-12-20",
        "activeDate": "2011-01-01"
      }
    ]
  }
}
```

### 3. 法规详情 API

**接口地址**: `/search/lawInfo`

**请求方法**: GET

**CURL 示例**:
```bash
curl -X GET 'https://openapi.delilegal.com/api/qa/v3/search/lawInfo?lawId={law_id}&merge=true' \
-H "Content-Type: application/json" \
-H "appid: QthdBErlyaYvyXul" \
-H "secret: EC5D455E6BD348CE8E18BE05926D2EBE"
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| lawId | string | 是 | 法规ID（从法规检索列表获取） |
| merge | boolean | 否 | 是否合并内容不拆分，默认 true |

**响应示例**:
```json
{
  "success": true,
  "code": 0,
  "msg": "",
  "body": {
    "activeDate": "2011-01-01",
    "issuedNo": "国务院令第586号",
    "lawsId": "xxx",
    "levelName": "行政法规",
    "publishDate": "2010-12-20",
    "publisherName": "国务院",
    "title": "工伤保险条例",
    "timelinessName": "现行有效",
    "lawDetailContent": "第一章 总则\n第一条 为了保障因工作遭受事故伤害..." 
  }
}
```

---

## 腾讯混元大模型 API

### 概述

通过腾讯元器平台创建智能体，调用混元大模型 API。

**API 基础地址**: `https://yuanqi.tencent.com/openapi/v1/agent/chat/completions`

### 认证方式

使用 Bearer Token 认证，Token 即为 appkey。

### 获取凭证

1. **appid**: 智能体配置 → 应用发布 → 服务状态 → 体验链接 → appid
2. **appkey**: 智能体调试页面 → 应用发布 → API管理 → appkey

### 调用示例

**CURL**:
```bash
curl -X POST 'https://yuanqi.tencent.com/openapi/v1/agent/chat/completions' \
-H "Content-Type: application/json" \
-H "Authorization: Bearer {your_appkey}" \
-d '{
  "assistant_id": "{your_assistant_id}",
  "user_id": "legal_user",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "劳动合同解除的经济补偿金如何计算？"
        }
      ]
    }
  ]
}'
```

**Python**:
```python
import requests
import json

url = 'https://yuanqi.tencent.com/openapi/v1/agent/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {your_appkey}'
}
data = {
    "assistant_id": "{your_assistant_id}",
    "user_id": "legal_user",
    "stream": False,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "劳动合同解除的经济补偿金如何计算？"
                }
            ]
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| assistant_id | string | 是 | 助手ID |
| user_id | string | 是 | 用户ID |
| stream | boolean | 否 | 是否流式返回，默认 false |
| messages | array | 是 | 对话内容，最多40条 |
| messages[n].role | string | 是 | 角色：`user` 或 `assistant` |
| messages[n].content | array | 是 | 内容列表 |
| messages[n].content[m].type | string | 是 | 内容类型：`text` 或 `image_url` |
| messages[n].content[m].text | string | 否 | 文本内容 |
| custom_variables | object | 否 | 自定义变量（工作流场景） |

### 响应参数

```json
{
  "id": "xxx",
  "created": 1234567890,
  "choices": [
    {
      "index": 0,
      "finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "根据《劳动合同法》第四十七条..."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 200,
    "total_tokens": 300
  }
}
```

### 注意事项

1. **并发限制**: 目前元器智能体 API 并发限制为 10，请勿短时间内大量调用
2. **Token 限制**: messages 长度最多为 40 条，建议定期清理历史
3. **模型选择**: 建议选择更长上下文的模型（如 200K、128K），避免输出 null

---

## 腾讯文档 API

### 概述

用于将诉讼策略报告导出至腾讯文档。

### 认证方式

使用 OAuth 2.0 认证。

### 主要功能

1. 创建文档
2. 更新文档内容
3. 分享文档

### 使用说明

请参考 [腾讯文档开放平台文档](https://docs.qq.com/)

---

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 认证失败 | 检查 appid/appkey |
| 403 | 权限不足 | 检查接口权限 |
| 429 | 请求过于频繁 | 降低调用频率 |
| 500 | 服务器错误 | 联系技术支持 |

### 调试建议

1. **输出为 null**: 选择更长上下文的模型（200K/128K）
2. **ArrayString 错误**: 检查参数类型是否为数组类型
3. **超时**: 增加请求超时时间
