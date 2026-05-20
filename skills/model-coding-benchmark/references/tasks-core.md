# 核心6题（必做）

这6个任务覆盖编程能力的6个维度，设计上互相独立，可并行执行。
核心6题的分数保证跨次可比，不得修改任务内容。

## T1 代码生成：csv_stats.py

**维度**：代码生成
**源文件**：users.csv
**Prompt**：

在当前目录创建 csv_stats.py，读取 users.csv 文件，实现以下功能：
1. 解析 CSV（不依赖 pandas，用标准库）
2. 计算每个 department 的平均薪资、最高薪资、最低薪资
3. 计算整体年龄中位数
4. 找出入职最早的员工
5. 输出格式化的统计报告

要求：代码可直接 python csv_stats.py 运行，输出清晰美观。只创建这一个文件。完成后运行 python csv_stats.py 验证。

**评分要点**：
- 正确性：计算结果是否正确（平均/最高/最低薪资、中位数、最早入职）
- 代码质量：类型转换（salary用float而非int）、路径处理、类型注解
- 完整性：5个功能是否全部实现
- 工具使用：是否运行验证
- 效率：完成速度

## T2 工具调用：buggy_sort.py 修 bug

**维度**：工具调用
**源文件**：buggy_sort.py
**执行模式**：两轮交互（测试反馈循环）

**第一轮 Prompt**：

请完成以下操作：
1. 读取 buggy_sort.py 文件
2. 运行它，记录报错信息
3. 找出所有 bug 并逐一说明
4. 修复所有 bug
5. 运行 python3 verify_t2.py buggy_sort.py 验证修复（verify 脚本已在当前目录）

每一步都要实际执行，不要跳过。

**第一轮结束后**：运行 `python3 verify_t2.py buggy_sort.py`，记录输出。

- 如果 `VERIFY: PASS`：任务完成，记录"一轮通过"，不进入第二轮。
- 如果 `VERIFY: FAIL`：进入第二轮，将失败输出反馈给模型。

**第二轮 Prompt**（仅在第一轮 verify 失败时发送）：

运行验证脚本后发现以下测试仍未通过：

{verify_output}

请根据失败信息，继续修复剩余问题，确保所有测试通过。

**第二轮结束后**：再次运行 `python3 verify_t2.py buggy_sort.py`，记录最终结果。

**结果记录**（写入 timing.log）：
- 一轮通过：`{model}__T2: {elapsed}s (OK, round=1)`
- 二轮通过：`{model}__T2: {elapsed}s (OK, round=2)`
- 未通过：`{model}__T2: {elapsed}s (FAIL)`

**内置 bug（共6个）**：
1. merge_sort: `left[i] >= right[j]` 应为 `<=`（升序）
2. merge: 缺少 `result.extend(right[j:])`
3. binary_search: `high = len(arr)` 应为 `len(arr) - 1`
4. binary_search: `low = mid` 应为 `mid + 1`
5. binary_search: `high = mid` 应为 `mid - 1`
6. quick_sort: `quick_sort(right) + middle + quick_sort(left)` 左右互换

**评分要点**：
- 正确性：6个 bug 是否全部找到并修复（verify 脚本客观验证；一轮通过无扣分，二轮通过扣2分）
- 代码质量：修复是否引入新问题
- 完整性：是否逐步执行了读→运行→定位→修复→验证
- 工具使用：过程透明度（是否展示具体 bug 和修复细节）
- 效率：完成速度（含两轮总时间）

## T3 Debug：api_server.py 中间件穿透

**维度**：Debug
**源文件**：api_server.py
**Prompt**：

api_server.py 是一个简易 Web 框架。目前有一个问题：当使用 auth_middleware 时，POST /users 请求没有带 token 时应该返回 401，但实际运行发现即使不带 token 也返回 200。请：
1. 读取 api_server.py 并理解代码
2. 定位这个 bug 的根因
3. 修复它
4. 运行 python3 verify_t3.py api_server.py 验证修复（verify 脚本已在当前目录）

不要修改中间件的逻辑，只修复框架本身。

**根因**：`auth_middleware` 定义了但从未通过 `app.use()` 注册到中间件链。
**最小修复**：添加一行 `app.use(auth_middleware)`。

**评分要点**：
- 正确性：是否定位到真正根因（未注册中间件），而非误判为"框架不支持路由级中间件"
- 代码质量：修复是否最小化（一行 vs 重构框架）
- 完整性：是否写了验证测试
- 工具使用：是否运行验证
- 效率：完成速度（此题是效率分水岭，精准定位可4分钟，过度设计可能17分钟）

## T4 代码理解：api_server.py 分析

**维度**：代码理解
**源文件**：api_server.py
**Prompt**：

读取 api_server.py，回答以下问题：
1. Router.match 是如何实现路径参数匹配的？用 /users/<id> 匹配 /users/42 为例，解释匹配过程
2. 中间件链的执行顺序是什么？如果注册了 A、B 两个中间件，请求到达 handler 的完整调用链是什么？
3. _apply_middleware 中的 chain 函数为什么使用闭包 + 索引递增而不是简单的 for 循环？
4. 如果要支持 PUT 和 DELETE 方法，最少改几行代码？具体改哪里？

请用中文回答，回答要精准，不要泛泛而谈。

**评分要点**：
- 正确性：4个问题的回答是否准确
- 代码质量：回答是否条理清晰、有代码示例
- 完整性：是否回答了所有4个问题
- 工具使用：是否引用了源码行号
- 效率：完成速度
- 注意：Q4 "最少改几行" 容易过度估计或前后矛盾

## T5 代码重构：buggy_sort.py 原地排序

**维度**：代码重构
**源文件**：buggy_sort.py（假设 bug 已修好）
**Prompt**：

读取 buggy_sort.py（假设 bug 已修好），完成以下重构：
1. 把 merge_sort 和 quick_sort 改为原地排序（in-place），不创建新数组
2. 添加一个泛型排序函数 smart_sort(arr, strategy='merge')，strategy 可以是 merge 或 quick
3. 为所有函数添加类型注解
4. 添加 docstring 说明时间/空间复杂度
5. 运行 python3 verify_t5.py buggy_sort.py 确保重构后测试仍通过（verify 脚本已在当前目录）

只修改这一个文件。

**评分要点**：
- 正确性：原地排序是否正确（注意 merge_sort 原地化可能退化为 O(n²)）
- 代码质量：类型注解、docstring 是否完整
- 完整性：5个要求是否全部满足
- 工具使用：是否运行测试验证
- 效率：完成速度
- 注意：原地 merge 导致 O(n²) 是常见陷阱，应在 docstring 中诚实标注

## T6 综合实战：blog_api.py

**维度**：综合实战
**源文件**：api_server.py（基于此框架扩展）
**Prompt**：

基于 api_server.py 框架，创建 blog_api.py 实现一个博客 API：
1. CRUD for posts: GET /posts, GET /posts/<id>, POST /posts, PUT /posts/<id>, DELETE /posts/<id>
2. 内存存储（用 dict）
3. 支持 query 参数过滤：GET /posts?author=xxx
4. 日志中间件：记录每个请求的 method、path、响应状态码
5. 错误处理中间件：捕获 handler 异常返回 500
6. 添加分页支持：GET /posts?page=1&limit=10

运行 python3 verify_t6.py blog_api.py 验证（verify 脚本已在当前目录）。

**评分要点**：
- 正确性：CRUD、过滤、分页、中间件是否全部正确
- 代码质量：框架扩展方式（继承 vs monkey-patch）、query string 解析、代码结构
- 完整性：6个需求是否全部实现
- 工具使用：是否运行验证
- 效率：完成速度
