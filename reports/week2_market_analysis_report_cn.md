# Week 2 中文报告：AI 生成音乐市场机会分析 Workflow 与阶段性结论

## 1. 本周目标

本周的核心目标是把 AI 生成音乐项目从单纯的平台资料整理，推进成一个可以自动化运行的数据分析 workflow。

我们希望回答的问题是：

**AI-generated music 应该优先投放到哪些国家/市场？适合发布什么曲风？有歌词和无歌词哪种更容易起量？哪些市场可能存在供给空白？**

由于目前 AI 生成音乐在早期阶段播放量和互动更重要，收益数据通常需要平台后台或 distributor report 才能完整获得，所以本周主要先围绕两个核心指标展开：

1. **Demand side：市场需求**  
   通过 YouTube 公开视频数据观察播放量、点赞、评论。

2. **Supply side：市场供给 / 竞争强度**  
   通过 iTunes / Apple Music catalog 数据观察不同市场已有曲库数量。

最终目标是建立一个初步判断逻辑：

**高需求 + 低供给 = 潜在市场机会。**

## 2. 本周完成的自动化 Workflow

### Step 1：平台数据可用性整理

首先，我整理了不同音乐和内容平台的数据可获得性，包括 YouTube、Spotify、TikTok、Facebook、Luna、腾讯音乐、网易云音乐和 iTunes / Apple Music。

当前判断是：

- YouTube 可以通过 API 自动获取公开视频的 views、likes、comments。
- iTunes Search API 可以自动获取不同国家和关键词下的 catalog 供给情况。
- Spotify 可以获取 metadata，但真实 streams 和 revenue 需要 Spotify for Artists 或 distributor report。
- TikTok 如果没有 Research API 权限，不适合做全自动抓取，后续可以作为 extension。
- 腾讯、网易、Luna、Facebook 的收益数据需要后台或分销商报表，暂时作为后续 monetization observation。

### Step 2：YouTube 公开数据抓取

第二步，我通过 YouTube Data API 自动抓取不同国家、曲风、语言和歌词风格下的公开视频数据。

抓取指标包括：

- video count
- total views
- median views
- total likes
- total comments
- average like rate
- average comment rate

### Step 3：YouTube 市场机会评分

第三步，我基于 YouTube 数据生成了 YouTube opportunity score，用来衡量不同市场和内容形式的早期需求强度。

这个评分主要结合：

- 总播放量
- 中位数播放量
- 平均点赞率
- 平均评论率

### Step 4：自动生成 YouTube 分析报告

第四步，我写了自动 report generator，把 YouTube 的分析结果整理成 markdown report，包括 top market opportunities、国家分析、曲风分析、有歌词 vs 无歌词分析、limitation 和 next steps。

### Step 5：iTunes / Apple Music catalog supply 抓取

第五步，为了判断哪些市场可能存在“供给空白”，我加入了 iTunes Search API。

YouTube 数据主要说明哪里有需求，但不能说明哪里竞争少。因此，我用 iTunes / Apple Music catalog 数量作为 supply / competition proxy，观察不同国家、曲风和关键词下已有的曲库数量。

### Step 6：合并 YouTube demand 和 iTunes supply，生成 Market Gap Score

最后，我把 YouTube demand score 和 iTunes catalog supply 结合起来，生成了 market gap opportunity score。

逻辑是：

- YouTube opportunity score 高 = 需求强
- iTunes catalog count 高 = 供给多 / 竞争强
- YouTube 需求高 + iTunes 供给低 = 潜在机会市场

## 3. 本周主要发现

### 发现 1：有歌词 Pop 是最强的起量方向

YouTube 数据显示，播放量最高的方向主要集中在 lyrical pop，尤其是 English pop、Spanish pop、Mexican pop、Korean pop、French pop、Hindi pop、Japanese pop、Indonesian pop。

这说明，如果短期目标是先获得播放量和验证市场，**local-language / English lyrical pop 是最适合优先测试的方向。**

### 发现 2：轻音乐 / 无歌词不是最大流量方向，但适合小众差异化

从总播放量来看，instrumental / no lyrics 的表现低于 lyrical pop。

但是 jazz、lofi、study music、café music、relaxing music 等无歌词内容仍然有价值，因为它们适合更垂直的使用场景，例如学习、工作、放松、咖啡厅背景音乐等。

因此目前判断是：

- **有歌词 pop：适合第一阶段起量**
- **instrumental / jazz / lofi：适合小众差异化测试**

### 发现 3：小语种和本地语言市场值得关注

当前 YouTube 数据说明，本地语言内容在多个市场都有明显需求，例如 Spanish、Korean、French、Hindi、Japanese、Indonesian 等市场。

这说明 AI-generated music 不应该只关注英文市场。本地语言内容可能更容易获得文化相关性和用户接受度。

### 发现 4：Pop 是大众流量方向，Jazz / Lofi 是 niche opportunity

从 genre 角度看，pop 是最强的大众流量曲风。

但是 jazz、lofi、bossa nova 等类型虽然总播放量不如 pop，但它们更适合作为 niche opportunity，尤其是在 Japanese jazz instrumental、bossa nova instrumental、lofi study music、café / relaxing / work background music 等方向。

### 发现 5：高需求市场不一定是最佳机会，因为竞争也高

合并 iTunes supply 后可以看到，US、Spain、Mexico、Korea、France 等 pop 市场 YouTube demand 很高，但 iTunes catalog count 也很高，说明这些方向竞争非常强。

相反，一些市场虽然 YouTube demand 没有最高，但 iTunes catalog supply 较低，可能更像潜在 market gap，例如 New Zealand pop lyrical、Canada lofi instrumental，以及部分小语种 / 小众 instrumental 方向。

## 4. 当前核心结论

1. **如果目标是先起量，优先测试 local-language / English lyrical pop。**  
   这类内容在 YouTube 上有最强的播放量和市场需求信号。

2. **如果目标是做差异化，可以测试 jazz、lofi、bossa nova、instrumental 等小众场景型内容。**  
   这些方向不一定播放量最高，但更适合长期、垂直、稳定的用户场景。

3. **小语种和本地文化市场值得继续研究。**  
   Spanish、Korean、French、Hindi、Japanese、Indonesian 等市场都显示出一定需求信号。

4. **市场空白不能只看播放量，要结合 supply。**  
   YouTube 代表需求，iTunes catalog 代表供给。高需求但低供给的方向，更可能是 AI-generated music 的机会点。

5. **当前阶段播放量和互动比收益更重要。**  
   收益数据需要 Spotify、YouTube Music、DistroKid、腾讯、网易等后台或分销报表补充，因此目前更适合作为后续验证指标。

## 5. 当前 Limitations

目前分析仍然有几个限制：

1. YouTube public data 不能代表所有音乐平台。
2. YouTube views 不等于 YouTube Music revenue。
3. iTunes catalog count 只是供给/竞争的 proxy，不代表完整市场供给。
4. TikTok 数据目前没有接入 Research API，因此没有全自动 TikTok engagement 数据。
5. 有歌词和无歌词的比较没有完全控制曲风差异，因此不能直接得出因果结论。
6. 收益数据还需要 Spotify、YouTube Music、DistroKid、腾讯、网易等后台或分销报表补充。

## 6. 下一步计划

### 1. 设计 A/B Test

基于当前结果，可以设计以下测试：

- English pop with lyrics vs English pop instrumental
- Spanish funny song vs Spanish emotional pop
- Japanese jazz instrumental vs Japanese jazz vocal
- Hindi pop vs Hindi lofi
- Portuguese pop vs bossa nova instrumental

目标是进一步验证：

- 有歌词是否真的比无歌词更好
- 本地语言是否比英文更适合本地市场
- 幽默歌词是否更适合短视频传播
- jazz / lofi 是否适合小众差异化市场

### 2. 加入更多供给侧数据

后续可以继续扩展 Spotify metadata、iTunes catalog、YouTube search saturation，进一步判断哪些市场供给少。

### 3. 加入收益观察数据

如果后续可以拿到 distributor report，可以加入 Spotify streams / revenue、YouTube Music country-level revenue、Facebook / Instagram revenue、Luna revenue、腾讯 / 网易播放量和收益单价。

## 7. 本周交付物

### Python scripts

- `src/01_build_platform_evidence_table.py`
- `src/02_fetch_youtube_public_metrics.py`
- `src/03_analyze_youtube_market.py`
- `src/04_write_youtube_final_report.py`
- `src/05_fetch_itunes_market_supply.py`
- `src/06_build_market_gap_score.py`

### Data outputs

- `data/youtube_public_video_metrics.csv`
- `data/youtube_market_opportunity_score.csv`
- `data/youtube_country_summary.csv`
- `data/youtube_genre_summary.csv`
- `data/youtube_content_type_summary.csv`
- `data/itunes_market_supply_raw.csv`
- `data/itunes_market_supply_summary.csv`
- `data/market_gap_opportunity_score.csv`

### Reports

- `reports/platform_streaming_evidence_plan.md`
- `reports/youtube_final_market_report.md`
- `reports/market_gap_opportunity_report.md`
- `reports/week2_market_analysis_report_cn.md`

### Figures

- `figures/top_youtube_market_opportunities.png`
- `figures/youtube_views_by_country.png`
- `figures/youtube_views_by_genre.png`
- `figures/youtube_views_by_content_type.png`

## 8. Final Summary

本周完成了 AI-generated music 市场分析的自动化 workflow。当前 pipeline 已经可以自动抓取 YouTube demand 数据和 iTunes supply 数据，并生成 market opportunity / market gap 分析。

目前最重要的结论是：

**local-language / English lyrical pop 是第一阶段最适合起量的方向；jazz、lofi、bossa nova 和 instrumental 更适合作为小众差异化测试方向。后续应基于这些结果设计 A/B test，并逐步加入平台收益数据。**
