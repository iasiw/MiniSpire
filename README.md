# MiniSpire

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一个支持联机PVP和单人PVE的卡牌游戏对战平台，集成遗传算法进行AI训练，通过WebSocket实现实时对战。

## ✨ 核心特性

- 🎮 **双模式对战**：支持玩家对战（PVP）和人机对战（PVE）
- 🤖 **AI智能对手**：使用遗传算法训练的AI对手
- 🔗 **动态匹配系统**：
  - 单人连接时自动进入PVE模式
  - 多人连接时按连接顺序配对（每2人组成PVP对局）
  - 奇数人数时最后加入的玩家进行PVE对战
- 💾 **数据持久化**：使用SQLite数据库存储玩家数据和训练结果
- 🌐 **WebSocket实时通信**：低延迟的对战体验
- 🎨 **Web可视化界面**：简洁直观的游戏操作面板

## 🧠 AI训练系统

程序使用前需要先训练AI模型：

```bash
# 启动遗传算法训练
python src/genetic_algorithm.py
```

训练完成后：
- `data.db` 数据库将自动生成并存储训练好的AI参数
- AI将具备基本的对战能力，可用于PVE模式

## 📦 项目结构

```
MiniSpire/
├── src/                          # 核心源代码目录
│   ├── cards.py                  # 卡牌定义与效果
│   ├── config.py                 # 配置文件（端口、路径等）
│   ├── constants.py              # 游戏常量定义
│   ├── data.py                   # 数据处理模块
│   ├── entities.py               # 游戏实体类（玩家、卡牌等）
│   ├── functions.py              # 通用功能函数
│   ├── genetic_algorithm.py      # 遗传算法AI训练核心
│   ├── play.py                   # 游戏对战逻辑
│   ├── sql.py                    # 数据库操作基础类
│   ├── sql_function.py           # 数据库高级操作
│   ├── training_function.py      # AI训练辅助函数
│   └── websocket_router.py       # WebSocket路由与消息处理
├── static/                       # 静态资源文件
│   ├── get_card.js               # 抽卡界面逻辑
│   ├── login.js                  # 登录界面逻辑
│   ├── play.js                   # 对战界面逻辑
│   └── start.js                  # 开始界面逻辑
├── templates/                    # HTML模板文件
│   ├── get_card.html             # 抽卡界面
│   ├── login.html                # 登录界面
│   ├── play.html                 # 对战界面
│   └── start.html                # 开始界面
├── .gitignore                    # Git忽略文件配置
├── data.db                       # SQLite数据库（训练/登录后自动生成）
├── LICENSE                       # MIT许可证
├── main.py                       # 后端主程序入口
├── README.md                     # 项目说明文档
└── requirements.txt              # 项目依赖列表
```

## 🚀 快速开始

### 环境要求
- Python 3.8 或更高版本
- 依赖包见 `requirements.txt`

### 安装与运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/iasiw/MiniSpire.git
   cd MiniSpire
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **训练AI模型**（必需步骤）
   ```bash
   python src/genetic_algorithm.py
   ```
   等待训练完成，`data.db` 将自动生成。

4. **启动游戏服务器**
   ```bash
   python main.py
   ```
   服务启动后，WebSocket服务将在配置的地址监听（默认 `ws://localhost:8000`）。

5. **开始游戏**
   - 打开浏览器访问 `http://localhost:8000`
   - 注册/登录账号
   - 等待其他玩家连接或直接开始PVE对战

### 测试训练功能
```bash
python test_training.py
```

## 🎮 对战匹配规则

| 连接人数 | 匹配规则 |
|---------|---------|
| 1人 | 自动进入PVE模式（VS AI） |
| 2人 | 组成1场PVP对局 |
| 3人 | 2人PVP + 1人PVE |
| 4人 | 2场PVP对局 |
| 5人 | 2场PVP + 1人PVE |
| ... | 以此类推 |

**匹配算法**：按照玩家连接顺序依次配对，优先组成PVP对局，剩余单人进行PVE对战。

## 🛠️ 核心模块说明

### 后端模块
- **`main.py`**：WebSocket服务器启动与生命周期管理
- **`src/websocket_router.py`**：消息路由与对战逻辑协调
- **`src/play.py`**：PVP/PVE对战核心逻辑
- **`src/genetic_algorithm.py`**：遗传算法AI训练实现
- **`src/sql.py` & `src/sql_function.py`**：数据库操作（玩家数据、对战记录）
- **`src/entities.py`**：游戏实体（玩家、卡牌、技能等）

### 前端模块
- **`templates/`**：4个核心页面（登录、抽卡、对战、开始）
- **`static/*.js`**：对应页面的交互逻辑与WebSocket通信

### 数据库
- **`data.db`**：SQLite数据库，存储玩家账号、卡牌收藏、AI参数、对战历史

## 🔧 配置说明

修改 `src/config.py` 可调整：
- 服务器端口与地址
- WebSocket路径
- 数据库路径
- 游戏规则参数（卡牌数量、初始生命值等）
- AI训练参数（种群大小、迭代次数等）

## 📊 数据库生成时机

- **AI训练后**：运行 `genetic_algorithm.py` 自动创建 `data.db` 并存储AI权重
- **用户登录后**：首次登录时自动初始化玩家数据表

## 🤝 贡献

欢迎提出问题、建议或贡献代码。请遵循以下步骤：
1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

项目维护者：**iasiw**  
GitHub：[@iasiw](https://github.com/iasiw)

---

**提示**：
- 首次运行请确保已完成AI训练（`python src/genetic_algorithm.py`），否则PVE模式无法正常工作
- `data.db` 会在训练或首次登录时自动生成，无需手动创建
- 此项目仍在积极开发中，部分功能可能变更。欢迎提交 Issue 反馈问题！
```
