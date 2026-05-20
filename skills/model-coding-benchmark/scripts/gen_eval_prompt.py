#!/usr/bin/env python3
"""
Model Coding Benchmark - 盲评 Prompt 生成器

用法:
  python3 gen_eval_prompt.py \
    --results-dir /tmp/model-benchmark \
    --output /tmp/model-benchmark/eval_prompt.txt

功能:
  - 读取 mapping.txt 获取匿名映射
  - 读取所有结果文件和工作区代码
  - 读取 timing.log 获取耗时数据
  - 生成脱敏后的盲评 prompt
"""

import argparse
import json
import os
import random
import re


TASKS = [
    {"id": "T1", "name": "代码生成：csv_stats.py", "code_file": "csv_stats.py"},
    {"id": "T2", "name": "工具调用：buggy_sort.py 修 bug", "code_file": "buggy_sort.py"},
    {"id": "T3", "name": "Debug：api_server.py 中间件穿透", "code_file": "api_server.py"},
    {"id": "T4", "name": "代码理解：api_server.py 分析", "code_file": None},
    {"id": "T5", "name": "代码重构：buggy_sort.py 原地排序", "code_file": "buggy_sort.py"},
    {"id": "T6", "name": "综合实战：blog_api.py", "code_file": "blog_api.py"},
]

RUBRIC = """
每题5个维度加权，每题满分50分，6题总分300分：

1. 正确性（0-15）：代码是否产生正确结果（最高权重）
   - T2/T5/T6 有 ground truth 验证脚本，verify 结果作为正确性上限：
     VERIFY PASS → 无上限；VERIFY FAIL → 上限9分；无法运行 → 上限6分
   - T2 二轮修复：一轮通过无扣分，二轮通过扣2分

2. 完整性（0-12）：是否满足所有需求

3. 工具使用（0-10）：是否正确使用工具（读文件、运行、验证），过程透明度

4. 代码质量（0-8）：风格、结构、类型注解、可维护性

5. 效率（0-5）：速度分(0-4) + 成功率分(0-1)
   速度分按任务难度分档：
   - T1/T4（简单）: <2min=4, 2-4min=3, 4-7min=2, 7-15min=1, >15min或TIMEOUT=0
   - T2/T3/T5（中等）: <5min=4, 5-8min=3, 8-12min=2, 12-20min=1, >20min或TIMEOUT=0
   - T6（复杂）: <8min=4, 8-12min=3, 12-18min=2, 18-25min=1, >25min或TIMEOUT=0
   成功率分: 完全成功=1, 部分成功=0.5, 失败/TIMEOUT=0
"""


def load_mapping(results_dir):
    """加载或生成匿名映射"""
    mapping_file = os.path.join(results_dir, "mapping.txt")
    if os.path.isfile(mapping_file):
        mapping = {}
        with open(mapping_file, "r") as f:
            for line in f:
                line = line.strip()
                if " = " in line:
                    key, value = line.split(" = ", 1)
                    mapping[key.strip()] = value.strip()
        return mapping

    # 生成新映射
    # 扫描结果文件获取模型名
    models = set()
    results_subdir = os.path.join(results_dir, "results")
    if os.path.isdir(results_subdir):
        for fname in os.listdir(results_subdir):
            if "__" in fname:
                model = fname.split("__")[0]
                models.add(model)

    models = sorted(models)
    random.shuffle(models)
    labels = list("XYZABCDEFGHIJKLMNOPQRSTUVW")
    mapping = {}
    for i, model in enumerate(models):
        mapping[labels[i]] = model

    with open(mapping_file, "w") as f:
        for label, model in mapping.items():
            f.write(f"{label} = {model}\n")

    return mapping


def load_timing(results_dir):
    """加载计时数据"""
    timing = {}
    timing_file = os.path.join(results_dir, "results", "timing.log")
    if not os.path.isfile(timing_file):
        return timing

    with open(timing_file, "r") as f:
        for line in f:
            line = line.strip()
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            timing[key] = value

    return timing


def format_time(seconds_str):
    """格式化耗时"""
    try:
        seconds = int(seconds_str)
        if seconds < 60:
            return f"{seconds}s"
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}min{secs}s" if secs else f"{minutes}min"
    except (ValueError, TypeError):
        return str(seconds_str)


def generate_prompt(results_dir, mapping):
    """生成盲评 prompt"""
    reverse_map = {v: k for k, v in mapping.items()}
    timing = load_timing(results_dir)

    parts = []
    parts.append("# 编程能力盲评\n")
    parts.append(f"你是编程能力评测专家。以下有 {len(mapping)} 个模型的编程任务输出，标识为 {'/'.join(mapping.keys())}。")
    parts.append("你不知道它们对应哪个模型，请客观评分。\n")

    parts.append("## 评分标准\n")
    parts.append(RUBRIC)

    parts.append("## 任务输出\n")

    results_subdir = os.path.join(results_dir, "results")

    for task in TASKS:
        parts.append(f"### {task['id']} {task['name']}\n")

        for label, model in mapping.items():
            # 读取结果文件
            result_file = os.path.join(results_subdir, f"{model}__{task['id']}.txt")
            output = ""
            if os.path.isfile(result_file):
                with open(result_file, "r", encoding="utf-8") as f:
                    output = f.read()
                    if len(output) > 3000:
                        output = output[:3000] + "\n... (truncated)"

            # 读取工作区代码
            code = ""
            if task["code_file"]:
                # 尝试多种工作区命名
                for ws_pattern in [f"ws_{model}_{task['id'][1:]}", f"ws_{model}{task['id'][1:]}"]:
                    code_file = os.path.join(results_dir, ws_pattern, task["code_file"])
                    if os.path.isfile(code_file):
                        with open(code_file, "r", encoding="utf-8") as f:
                            code = f.read()
                            if len(code) > 3000:
                                code = code[:3000] + "\n... (truncated)"
                        break

            # 获取耗时
            timing_key = f"{model}__{task['id']}"
            time_info = timing.get(timing_key, "N/A")

            parts.append(f"#### Model {label}")
            parts.append(f"耗时：{time_info}\n")

            if code:
                parts.append(f"生成的代码（{task['code_file']}）：\n```\n{code}\n```\n")

            if output:
                parts.append(f"输出：\n```\n{output}\n```\n")

            parts.append("")

    # 评分要求
    parts.append("## 评分要求\n")
    parts.append(f"请对每个任务的每个模型按5个维度打分（0-10），输出以下格式：\n")
    parts.append("### T1 代码生成")

    labels = list(mapping.keys())
    header = "| 维度 | " + " | ".join(f"Model {l}" for l in labels) + " |"
    sep = "|------|" + "|".join(["---------|"] * len(labels))
    parts.append(header)
    parts.append(sep)
    for dim in ["正确性(0-15)", "完整性(0-12)", "工具使用(0-10)", "代码质量(0-8)", "效率(0-5)"]:
        parts.append(f"| {dim} | " + " | ".join(["?"] * len(labels)) + " |")
    parts.append("| **总分** | " + " | ".join(["**?**"] * len(labels)) + " |")
    parts.append("")
    parts.append("（每题一段评语，指出各模型的关键优缺点）\n")
    parts.append("### 最终汇总")

    header2 = "| Task | " + " | ".join(f"Model {l}" for l in labels) + " |"
    parts.append(header2)
    parts.append("|------|" + "|".join(["---------|"] * len(labels)))
    for task in TASKS:
        parts.append(f"| {task['id']} | " + " | ".join(["?"] * len(labels)) + " |")
    parts.append("| **总计** | " + " | ".join(["**?**"] * len(labels)) + " |")
    parts.append("")
    parts.append("### 综合排名与评语")

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Generate blind evaluation prompt")
    parser.add_argument("--results-dir", required=True, help="Benchmark results directory")
    parser.add_argument("--output", required=True, help="Output prompt file path")

    args = parser.parse_args()

    mapping = load_mapping(args.results_dir)
    prompt = generate_prompt(args.results_dir, mapping)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"Generated evaluation prompt: {args.output}")
    print(f"Mapping ({len(mapping)} models):")
    for label, model in mapping.items():
        print(f"  {label} = {model}")


if __name__ == "__main__":
    main()
