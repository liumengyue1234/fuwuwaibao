# 审思明辨——智判法案双擎系统
# Shen Si Ming Bian - Intelligent Legal Assistant System

**面向法律从业者的智能辅助平台**

融合对话式问答、精准法条检索、相似案例匹配与诉讼策略推演四大核心能力，以腾讯混元大模型为认知引擎，实现"法条+案例"双擎驱动的智能问答与深度推理。

## 四大核心能力

### 1. 对话式法律问答
- 基于腾讯混元大模型的自然语言理解
- 实时推送相关法条、司法解释
- 专业法律术语解析与通俗解读

### 2. 精准法条检索
- 接入得理开放平台法规检索API
- 支持关键词检索与语义检索
- 智能关联相关司法解释

### 3. 相似案例匹配
- 接入得理开放平台类案检索API
- 基于案情特征的智能匹配
- 裁判要旨与判决结果分析

### 4. 诉讼策略推演
- 智能切换"对方律师"视角
- 自动生成质证意见
- 风险提示与诉讼策略报告

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户交互层 (Streamlit)                  │
├─────────────────────────────────────────────────────────┤
│                  业务逻辑层 (Python Core)                  │
├───────────────┬─────────────────┬────────────────────────┤
│  得理开放平台   │   腾讯混元API   │     腾讯云向量数据库   │
│  (法条/案例)   │  (认知引擎)     │      (知识库)         │
├───────────────┴─────────────────┴────────────────────────┤
│                  腾讯文档API (报告导出)                     │
└─────────────────────────────────────────────────────────┘
```

## 核心技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 认知引擎 | 腾讯混元大模型 | 智能问答与推理 |
| 知识库 | 腾讯云向量数据库 | 高质量法律知识库 |
| 案例API | 得理开放平台 | 类案检索 |
| 法规API | 得理开放平台 | 法规检索 |
| 智能体 | 腾讯元器 | 工作流编排 |
| 文档导出 | 腾讯文档API | 报告导出 |

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env 填入以下配置：
# 腾讯云账号密钥
TC_SECRET_ID=your_secret_id
TC_SECRET_KEY=your_secret_key

# 腾讯混元API (通过腾讯元器获取)
HUNYUAN_APP_ID=your_app_id
HUNYUAN_APP_KEY=your_app_key

# 得理开放平台
DELILEGAL_APP_ID=QthdBErlyaYvyXul
DELILEGAL_SECRET=EC5D455E6BD348CE8E18BE05926D2EBE
```

### 启动应用

```bash
streamlit run app.py
```

## 项目结构

```
fuwuwaibao/
├── app.py                    # Streamlit主应用
├── config.py                 # 配置管理
├── .env.example              # 环境变量模板
├── requirements.txt          # 依赖列表
├── README.md                 # 项目说明
├── docs/                     # 技术文档
│   ├── API_DOCUMENTATION.md  # API文档
│   ├── DEPLOYMENT.md         # 部署指南
│   └── USER_GUIDE.md         # 用户手册
├── core/                     # 核心模块
│   ├── __init__.py
│   ├── legal_qa.py           # 法律问答
│   ├── law_search.py          # 法条检索
│   ├── case_matching.py      # 案例匹配
│   └── strategy.py           # 诉讼策略
├── services/                 # 服务层
│   ├── __init__.py
│   ├── deli_service.py        # 得理API服务
│   ├── hunyuan_service.py    # 混元API服务
│   └── tencent_doc.py        # 腾讯文档服务
├── utils/                    # 工具函数
│   ├── __init__.py
│   └── helpers.py
└── tests/                    # 测试
    └── test_legal_qa.py
```

## 服创赛参赛信息

- **赛道**: D06 - 腾讯开悟赛道
- **作品名称**: 审思明辨——智判法案双擎系统
- **团队**: [你的团队名]
- **成员**: [成员列表]

## 联系方式

- 参赛同学专属福利: 小理AI全功能6个月兑换码 `ZX4688`
- 得理AI网址: https://www.delilegal.com/ai

## License

MIT License
