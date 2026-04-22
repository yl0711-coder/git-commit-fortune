# Git Commit Fortune

[English](README.md) | 简体中文

读取一个 Git 仓库的提交历史，并生成一份有趣的仓库运势报告。

它不是严肃的 Git 数据分析工具，而是一个本地 CLI 小玩具：把提交记录里的模式变成适合截图分享的终端输出。

## 为什么做

Git 历史里经常藏着一些很有意思的信号：

- 太多深夜提交
- 太多带有 `fix` 的提交
- 太多 `final`、`temporary`、`wip`
- 周末提交看起来过于努力
- commit message 太短，像是在隐藏动机

`git-commit-fortune` 会读取这些信号，然后生成一份仓库运势报告。

## 安装

从源码目录直接运行：

```bash
bin/git-commit-fortune
```

或者本地 editable 安装：

```bash
python3 -m pip install -e .
git-commit-fortune
```

## 使用

分析当前仓库：

```bash
git-commit-fortune
```

分析指定仓库：

```bash
git-commit-fortune /path/to/repo
```

限制读取的 commit 数量：

```bash
git-commit-fortune --limit 30
```

只分析最近一段时间的提交：

```bash
git-commit-fortune --since "2 weeks ago"
git-commit-fortune --since 2026-01-01
```

输出 JSON：

```bash
git-commit-fortune --json
```

输出适合截图的一行结果：

```bash
git-commit-fortune --one-line
```

## 示例输出

```text
Git Commit Fortune

Repository: /path/to/repo

Omen: The Final That Was Not Final
Fortune level: cursed but deployable
Repository mood: functional but emotionally unavailable
Spirit animal: a caffeinated octopus holding a rollback plan

Signs:
- 80 recent commits were consulted
- 2 author(s) left fingerprints in the history
- 26 commit(s) mention fix, bug, or hotfix
- 7 commit(s) happened after 10 PM or before 6 AM
- "final" appeared 2 time(s), which is rarely final

Prediction:
A commit called 'final final' will appear before anyone admits defeat.

Advice:
Before the next fix, ask whether the bug is a symptom or a tradition.

Lucky command:
git log --oneline --grep=final
```

## 一行输出

```bash
git-commit-fortune --one-line
```

```text
Git Commit Fortune: The Calm Before Refactor | mostly harmless | a calm capybara sitting on green CI
```

## JSON 输出

```bash
git-commit-fortune --json
```

JSON 输出包含：

- 仓库路径
- 生成的运势报告
- 生成报告所使用的统计信息
- lucky command 建议

这适合用来做徽章、仪表盘，或者包装成其他工具。

## 检查内容

第一版会读取最近的 commit 历史，并分析：

- 作者数量
- commit 数量
- 可选的 Git 原生 `--since` 时间窗口
- 深夜提交
- 周末提交
- commit subject 平均长度
- `fix`、`bug`、`hotfix`、`wip`、`temporary`、`final`、`hack`、`release` 等关键词

## 非目标

这个项目刻意保持很小。

它不打算成为：

- 严肃的 Git 数据分析平台
- 生产力追踪工具
- 团队绩效衡量工具
- 仪表盘
- 远程服务

它应该保持本地、轻量、有趣。

## 开发

运行测试：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

编译源码：

```bash
python3 -m compileall src tests
```

从源码运行 CLI：

```bash
bin/git-commit-fortune --limit 20
```

## 文档维护

本项目保持英文和中文 README 同步。更新 `README.md` 中的用法、示例、参数或项目定位时，需要在同一次变更里同步更新 `README.zh-CN.md`。

## License

MIT
