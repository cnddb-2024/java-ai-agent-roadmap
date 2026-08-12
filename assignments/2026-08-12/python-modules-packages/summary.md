# Python 模块与包管理实战

## 作业信息

- **日期**: 2026-08-12
- **Phase**: Phase 1（第 15/168 天）
- **对应飞书任务**: Python 模块与包管理实战：pip/venv/虚拟环境/标准库速览
- **代码仓库**: [cnddb-2024/python-QuickStart](https://github.com/cnddb-2024/python-QuickStart)
- **提交**: `06987da` - feat: 添加 mypackage 包结构与标准库示例 (#5)

## 作业内容

### 1. 包结构（mypackage）

```
src/mypackage/
├── __init__.py          # 包顶层导出：Processor, process_data, normalize, __version__
├── __main__.py          # python -m mypackage 入口
├── core.py              # 核心逻辑：process_data 过滤 + Processor 类
├── utils.py             # 工具函数：normalize
├── data_demo.py         # 标准库：json/collections/functools
├── path_demo.py         # 标准库：pathlib/shutil/tempfile
├── concurrent_demo.py   # 标准库：subprocess/concurrent.futures
└── subpkg/
    └── helpers.py       # 子包绝对导入示例
```

### 2. 覆盖知识点

| 知识点 | 文件 | 对标 Java |
|--------|------|-----------|
| 包结构 `__init__.py` / `__all__` | `__init__.py` | package-info.java |
| 模块入口 `__main__.py` | `__main__.py` | public static void main |
| 相对导入 vs 绝对导入 | `__init__.py`, `helpers.py` | import 机制差异 |
| `python -m` 运行模块 | `__main__.py` | java -jar |
| 标准库 json/collections/functools | `data_demo.py` | Jackson/Guava |
| pathlib 路径操作 | `path_demo.py` | java.nio.file.Path |
| concurrent.futures 线程池 | `concurrent_demo.py` | ExecutorService |
| unittest 单元测试 | `test_demo.py` | JUnit |

### 3. 验收标准

- [x] 包结构完整：`__init__.py` + 子包 + `__main__.py` 入口
- [x] 标准库实战：json/collections/pathlib/concurrent.futures/subprocess
- [x] 单元测试：unittest 测试 Processor 类
- [x] 绝对导入与相对导入对比

## 面试题关联

- Python 的 import 机制与 Java 的 classloader 有何区别？（第一梯队）
- `python -m package` 与 `python package.py` 的区别？（第二梯队）
