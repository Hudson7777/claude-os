# 扩展任务（可选）

扩展任务不计入核心6题分数，单独计分。当用户说"跑扩展题"时执行。

**轮换机制**：每季度可从扩展题中选一道替换核心题（需同时更新 tasks-core.md 并将被替换的题目移入此文件）。替换前须确认新题有对应 verify 脚本或明确的客观评分标准。

---

## E1 并发编程：concurrent_crawler.py

**维度**：并发与异步
**源文件**：无（从零创建）

**Prompt**：

在当前目录创建 concurrent_crawler.py，实现一个并发 URL 爬虫：
1. 接受一个 URL 列表（硬编码5个公开 URL，用 httpbin.org 的接口即可）
2. 用 threading 或 asyncio 并发请求，最大并发数为3
3. 每个请求设置3秒超时，超时则重试一次
4. 收集所有结果（状态码、响应时间、是否超时）
5. 输出汇总报告：成功数/失败数/平均响应时间

要求：代码可直接运行，展示并发效果（打印每个请求的开始/完成时间）。

**评分要点**：
- 正确性：并发是否真正并行（不是串行），超时和重试是否正确
- 代码质量：线程安全、资源清理、类型注解
- 完整性：5个功能是否全部实现
- 工具使用：是否运行验证并展示并发效果
- 效率：完成速度（参考 T2/T3/T5 档位）

---

## E2 数据库交互：simple_orm.py

**维度**：数据库操作
**源文件**：无（从零创建）

**Prompt**：

在当前目录创建 simple_orm.py，基于 sqlite3 实现一个简单 ORM：
1. Model 基类，子类通过类属性声明字段（如 `name: str`, `age: int`）
2. 支持：create_table()、insert(obj)、query(filter=None)、update(id, **kwargs)、delete(id)
3. 支持事务：with db.transaction(): 块内操作原子提交，异常自动回滚
4. 写一个 User 模型演示完整 CRUD 流程

要求：只用标准库，代码可直接运行。完成后演示：插入3条记录、查询、更新、删除，输出每步结果。

**评分要点**：
- 正确性：CRUD 是否正确，事务回滚是否有效
- 代码质量：ORM 抽象是否干净，字段类型映射
- 完整性：5个操作 + 事务 + 演示全部实现
- 工具使用：是否运行验证
- 效率：完成速度（参考 T6 档位）

---

## E3 正则表达式：template_engine.py

**维度**：字符串处理与解析
**源文件**：无（从零创建）

**Prompt**：

在当前目录创建 template_engine.py，实现一个简易模板引擎：
1. 变量替换：`{{ variable }}`
2. 条件语句：`{% if condition %}...{% endif %}`（支持简单布尔值和比较）
3. 循环语句：`{% for item in list %}...{% endfor %}`
4. 支持嵌套（for 内可以有 if）
5. 写测试验证以上4种场景

要求：只用标准库，不依赖 Jinja2。完成后运行测试。

**评分要点**：
- 正确性：4种语法是否全部正确，嵌套是否支持
- 代码质量：解析器结构是否清晰，错误提示是否友好
- 完整性：4种语法 + 嵌套 + 测试全部实现
- 工具使用：是否运行测试验证
- 效率：完成速度（参考 T2/T3/T5 档位）

---

## E4 文件处理：log_parser.py

**维度**：文件 I/O 与数据处理
**源文件**：生成测试日志文件（见下方）

**测试数据生成**（在 Step 1 初始化时运行）：

```python
# 生成 sample.log
import random, datetime
lines = []
levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
services = ["api", "db", "cache", "worker"]
for i in range(200):
    ts = datetime.datetime(2024, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=i*30)
    level = random.choice(levels)
    service = random.choice(services)
    lines.append(f"{ts.isoformat()} [{level}] [{service}] message {i}")
with open("sample.log", "w") as f:
    f.write("\n".join(lines))
```

**Prompt**：

当前目录有一个 sample.log 文件，格式为：`2024-01-01T00:00:00 [LEVEL] [SERVICE] message`

创建 log_parser.py，实现：
1. 解析日志，统计每个 service 的各 level 数量
2. 找出 ERROR 最集中的时间段（按小时统计）
3. 输出结构化报告（表格形式）
4. 支持命令行参数：--level 过滤级别，--service 过滤服务

要求：代码可直接运行，`python log_parser.py` 输出完整报告，`python log_parser.py --level ERROR` 只显示 ERROR。

**评分要点**：
- 正确性：统计结果是否准确，参数过滤是否正确
- 代码质量：解析逻辑是否健壮，报告格式是否清晰
- 完整性：4个功能 + 命令行参数全部实现
- 工具使用：是否运行验证两种调用方式
- 效率：完成速度（参考 T1/T4 档位）

---

## E5 类型系统：add_type_hints.py

**维度**：类型系统与静态分析
**源文件**：untyped_code.py（见下方，在 Step 1 初始化时写入）

**源文件内容**（写入 workspace/untyped_code.py）：

```python
def process_users(users, min_age, department):
    result = []
    for user in users:
        if user["age"] >= min_age and user.get("department") == department:
            result.append({
                "name": user["name"],
                "salary": user["salary"] * 1.1,
                "senior": user["age"] > 40
            })
    return result

def merge_dicts(base, override):
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged

class DataPipeline:
    def __init__(self, steps):
        self.steps = steps
        self.results = []

    def run(self, data):
        current = data
        for step in self.steps:
            current = step(current)
            self.results.append(current)
        return current

    def get_intermediate(self, index):
        if index < len(self.results):
            return self.results[index]
        return None
```

**Prompt**：

读取 untyped_code.py，为所有函数和方法添加完整类型注解：
1. 使用 Python 3.9+ 风格（`list[dict]` 而非 `List[Dict]`）
2. 为 DataPipeline 添加泛型支持（输入类型和输出类型可以不同）
3. 修改后的代码保存到原文件
4. 用 mypy 检查（`mypy untyped_code.py --strict`），确保无错误

要求：不改变任何函数逻辑，只添加类型注解。完成后展示 mypy 输出。

**评分要点**：
- 正确性：mypy --strict 是否无错误
- 代码质量：泛型使用是否合理，注解是否精确（不滥用 Any）
- 完整性：所有函数/方法/类都有注解，包括泛型 DataPipeline
- 工具使用：是否运行 mypy 验证
- 效率：完成速度（参考 T2/T3/T5 档位）

---

## E6 API 集成：github_stats.py

**维度**：API 集成与数据处理
**源文件**：无（从零创建）

**Prompt**：

创建 github_stats.py，调用 GitHub 公开 API（无需认证）获取仓库信息：
1. 获取 python/cpython 仓库的基本信息（stars、forks、open issues）
2. 获取最近10个 closed issues（标题、关闭时间、标签）
3. 计算 issue 平均关闭时长（从创建到关闭）
4. 处理 API 限流：如果收到 429 或剩余请求数 < 5，等待后重试
5. 输出格式化报告

要求：只用标准库（urllib），不用 requests。完成后运行并展示输出。

**评分要点**：
- 正确性：API 调用是否正确，数据解析是否准确
- 代码质量：错误处理、限流处理是否健壮
- 完整性：5个功能全部实现
- 工具使用：是否实际运行并展示真实数据
- 效率：完成速度（参考 T2/T3/T5 档位）

---

## 添加新扩展题规范

添加新题时，必须包含：
- 任务名、维度、难度参考（对应哪个核心题的时间档位）
- 源文件（如有，包含生成脚本）
- 完整 Prompt（可直接粘贴给模型执行）
- 评分要点（5个维度各自的关键区分点）
- 可选：对应的 verify 脚本路径
