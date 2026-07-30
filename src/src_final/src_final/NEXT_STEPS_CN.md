# GoldenAI 下一步

## 1. 替换评分文件

把本文件夹中的 `song_scores.csv` 复制到项目：

```text
AI-GEN-MUSIC-DATA-PROJECT/data/song_scores.csv
```

当前文件有 50 行，但分数为 provisional：
- 使用原 50 首实验中的 High / Mid / Low / Pilot 分组作为市场分代理；
- 使用 Metadata 完整度形成临时综合分；
- 以后 04_prepare_song_scores.py 成功匹配真实市场 CSV 后，应覆盖本文件。

## 2. 放置 Agent 文件

保留你现有的：

```text
src/src_final/agent/tools.py
```

把这些文件复制到同一个 `agent` 文件夹：

```text
agent/__init__.py
agent/prompts.py
agent/music_score_agent.py
```

把 `app.py` 和 `test_agent.py` 放进：

```text
src/src_final/
```

## 3. 不使用损坏的 Conda 环境

在项目根目录执行：

```bash
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements_agent.txt
```

把 `.env.example` 复制为 `.env`，填写 API Key。

## 4. 先测试 tools.py

```bash
python src/src_final/test_agent.py
```

## 5. 测试自然语言 Agent

```bash
python -c "from src.src_final.agent.music_score_agent import ask_music_agent; print(ask_music_agent('帮我看 P01B 的市场评分和综合评分'))"
```

## 6. 打开聊天页面

```bash
streamlit run src/src_final/app.py
```
