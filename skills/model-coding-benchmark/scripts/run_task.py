#!/usr/bin/env python3
"""
Model Coding Benchmark - 单任务运行器 v2（agent 模式）

用法:
  python3 run_task.py \
    --model opus \
    --task-n 1 \
    --workspace /tmp/benchmark/ws_mc_1 \
    --output /tmp/benchmark/results/mc__T1.txt \
    --timeout 600

变更（v2）:
  - 去掉 --print，改为真实 agent 模式
  - 任务通过工作区 TASK.md 下发
  - 三信号联合终止判断：进程退出 / 文件稳定+CPU空闲 / 超时兜底
"""

import argparse
import os
import subprocess
import sys
import time

MC_PATH = os.environ.get("CLAUDE_CLI", "claude")

# 各任务的文件稳定窗口（秒）
STABLE_WINDOWS = {
    1: 60,   # T1 代码生成
    2: 90,   # T2 工具调用
    3: 90,   # T3 Debug
    4: 60,   # T4 代码理解（纯文字，进程退出为主信号）
    5: 90,   # T5 重构
    6: 120,  # T6 综合实战
}

TASK_PROMPTS = {
    1: """在当前目录创建 csv_stats.py，读取 users.csv 文件，实现以下功能：
1. 解析 CSV（不依赖 pandas，用标准库）
2. 计算每个 department 的平均薪资、最高薪资、最低薪资
3. 计算整体年龄中位数
4. 找出入职最早的员工
5. 输出格式化的统计报告

要求：代码可直接 python csv_stats.py 运行，输出清晰美观。只创建这一个文件。完成后运行 python csv_stats.py 验证。""",

    2: """请完成以下操作：
1. 读取 buggy_sort.py 文件
2. 运行它，记录报错信息
3. 找出所有 bug 并逐一说明
4. 修复所有 bug
5. 运行 python3 verify_t2.py buggy_sort.py 验证修复（verify 脚本已在当前目录）

每一步都要实际执行，不要跳过。""",

    3: """api_server.py 是一个简易 Web 框架。目前有一个问题：当使用 auth_middleware 时，POST /users 请求没有带 token 时应该返回 401，但实际运行发现即使不带 token 也返回 200。请：
1. 读取 api_server.py 并理解代码
2. 定位这个 bug 的根因
3. 修复它
4. 运行 python3 verify_t3.py api_server.py 验证修复（verify 脚本已在当前目录）

不要修改中间件的逻辑，只修复框架本身。""",

    4: """读取 api_server.py，回答以下问题：
1. Router.match 是如何实现路径参数匹配的？用 /users/<id> 匹配 /users/42 为例，解释匹配过程
2. 中间件链的执行顺序是什么？如果注册了 A、B 两个中间件，请求到达 handler 的完整调用链是什么？
3. _apply_middleware 中的 chain 函数为什么使用闭包 + 索引递增而不是简单的 for 循环？
4. 如果要支持 PUT 和 DELETE 方法，最少改几行代码？具体改哪里？

请用中文回答，回答要精准，不要泛泛而谈。将答案写入 T4_answer.md 文件。""",

    5: """读取 buggy_sort.py（假设 bug 已修好），完成以下重构：
1. 把 merge_sort 和 quick_sort 改为原地排序（in-place），不创建新数组
2. 添加一个泛型排序函数 smart_sort(arr, strategy='merge')，strategy 可以是 merge 或 quick
3. 为所有函数添加类型注解
4. 添加 docstring 说明时间/空间复杂度
5. 运行 python3 verify_t5.py buggy_sort.py 确保重构后测试仍通过（verify 脚本已在当前目录）

只修改这一个文件。""",

    6: """基于 api_server.py 框架，创建 blog_api.py 实现一个博客 API：
1. CRUD for posts: GET /posts, GET /posts/<id>, POST /posts, PUT /posts/<id>, DELETE /posts/<id>
2. 内存存储（用 dict）
3. 支持 query 参数过滤：GET /posts?author=xxx
4. 日志中间件：记录每个请求的 method、path、响应状态码
5. 错误处理中间件：捕获 handler 异常返回 500
6. 添加分页支持：GET /posts?page=1&limit=10

运行 python3 verify_t6.py blog_api.py 验证（verify 脚本已在当前目录）。""",
}


def write_task_md(workspace: str, task_n: int) -> None:
    """Write TASK.md into the workspace directory."""
    prompt = TASK_PROMPTS[task_n]
    content = f"""# 任务说明

请直接执行以下任务，不要询问确认，完成所有步骤后退出。

{prompt}
"""
    with open(os.path.join(workspace, "TASK.md"), "w", encoding="utf-8") as f:
        f.write(content)


def get_workspace_mtime(workspace: str) -> float:
    """Return the most recent mtime of any file in workspace (recursive)."""
    latest = 0.0
    for root, dirs, files in os.walk(workspace):
        # Skip hidden dirs like .git
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            if fname.startswith("."):
                continue
            try:
                mtime = os.path.getmtime(os.path.join(root, fname))
                if mtime > latest:
                    latest = mtime
            except OSError:
                pass
    return latest


def get_process_cpu(pid: int) -> float:
    """Return CPU% for a pid using ps. Returns 0.0 if process not found."""
    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "%cpu="],
            capture_output=True, text=True, timeout=5
        )
        return float(result.stdout.strip()) if result.stdout.strip() else 0.0
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError):
        return 0.0


def run_task(model: str, task_n: int, workspace: str, output_file: str,
             timeout: int) -> dict:
    """
    Run a single benchmark task in agent mode.

    Returns a dict with keys:
      status: 'OK' | 'OK-idle' | 'TIMEOUT' | 'ERROR'
      elapsed: float (seconds)
    """
    stable_window = STABLE_WINDOWS.get(task_n, 90)
    is_text_only = (task_n == 4)  # T4 writes no files, rely on process exit

    # Write TASK.md
    write_task_md(workspace, task_n)

    # Build command — use --print mode so prompt is read from stdin and
    # the process exits naturally when done (no interactive session).
    cmd = [
        MC_PATH, "--code", "--model", model,
        "--dangerously-skip-permissions",
        "--print",
    ]
    prompt_text = "请读取 TASK.md 并完成其中的任务。完成后退出。\n"

    print(f"[RUN] model={model} T{task_n} workspace={workspace} timeout={timeout}s")

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    start_time = time.time()

    # Keep output file open for the full subprocess lifetime so the child's
    # inherited fd remains valid throughout the run.
    try:
        out_f = open(output_file, "w", encoding="utf-8")
    except OSError as e:
        return {"status": "ERROR", "elapsed": 0.0, "detail": str(e)}

    try:
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=workspace,
                stdin=subprocess.PIPE,
                stdout=out_f,
                stderr=subprocess.STDOUT,
            )
            # Write prompt to stdin then close it so the process knows input is done
            proc.stdin.write(prompt_text.encode("utf-8"))
            proc.stdin.close()
        except Exception as e:
            return {"status": "ERROR", "elapsed": 0.0, "detail": str(e)}

        # Monitoring loop
        POLL_INTERVAL = 10        # seconds between polls
        WARMUP = 30               # seconds before stability check starts
        CPU_IDLE_THRESHOLD = 5.0  # %CPU below which we count as idle
        CPU_IDLE_REQUIRED = 3     # consecutive idle samples needed

        cpu_idle_count = 0
        last_mtime = get_workspace_mtime(workspace)
        # Initialize to now so the stability window starts from when we first check,
        # not from process start — prevents false-positive idle if no files are written
        # before the warmup period ends.
        last_file_change_time = time.time()

        while True:
            time.sleep(POLL_INTERVAL)
            elapsed = time.time() - start_time

            # Signal 1: process exited
            ret = proc.poll()
            if ret is not None:
                print(f"[DONE] model={model} T{task_n}: {elapsed:.0f}s (OK, process exited)")
                return {"status": "OK", "elapsed": elapsed}

            # Hard timeout
            if elapsed > timeout:
                proc.kill()
                proc.wait()
                print(f"[DONE] model={model} T{task_n}: {elapsed:.0f}s (TIMEOUT)")
                return {"status": "TIMEOUT", "elapsed": elapsed}

            # T4 text-only: only process-exit signal applies
            if is_text_only:
                continue

            # Warmup period: skip stability checks
            if elapsed < WARMUP:
                continue

            # Signal 2: file stability
            current_mtime = get_workspace_mtime(workspace)
            if current_mtime != last_mtime:
                last_mtime = current_mtime
                last_file_change_time = time.time()
                cpu_idle_count = 0

            file_stable = (time.time() - last_file_change_time) >= stable_window

            # Signal 3: CPU idle
            cpu = get_process_cpu(proc.pid)
            if cpu < CPU_IDLE_THRESHOLD:
                cpu_idle_count += 1
            else:
                cpu_idle_count = 0

            if file_stable and cpu_idle_count >= CPU_IDLE_REQUIRED:
                proc.kill()
                proc.wait()
                print(f"[DONE] model={model} T{task_n}: {elapsed:.0f}s (OK-idle)")
                return {"status": "OK-idle", "elapsed": elapsed}
    finally:
        out_f.close()


def record_timing(output_dir: str, model: str, task_n: int, result: dict) -> None:
    """Append timing entry to results/timing.log."""
    timing_file = os.path.join(output_dir, "results", "timing.log")
    os.makedirs(os.path.dirname(timing_file), exist_ok=True)
    elapsed = result["elapsed"]
    status = result["status"]
    with open(timing_file, "a", encoding="utf-8") as f:
        f.write(f"{model}__T{task_n}: {elapsed:.0f}s ({status})\n")


def main():
    parser = argparse.ArgumentParser(description="Run a single benchmark task (agent mode)")
    parser.add_argument("--model", required=True)
    parser.add_argument("--task-n", type=int, required=True, choices=range(1, 7))
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--output", required=True, help="Path for task output log file")
    parser.add_argument("--output-dir", required=True,
                        help="Root output directory; timing.log written to <output-dir>/results/timing.log")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    result = run_task(
        model=args.model,
        task_n=args.task_n,
        workspace=args.workspace,
        output_file=args.output,
        timeout=args.timeout,
    )

    record_timing(args.output_dir, args.model, args.task_n, result)

    sys.exit(0 if result["status"] in ("OK", "OK-idle") else 1)


if __name__ == "__main__":
    main()
