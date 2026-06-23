# Genre Engagement Behavior Analysis
## 1. Research Objective
本阶段分析重点是继续围绕曲风（genre）展开，但不再只看不同曲风的发布数量，而是结合播放量、点赞率、评论率和综合互动率，判断不同曲风背后的用户收听行为。
核心研究问题是：
> 不同 AI music genre 是否表现出不同的消费模式？哪些曲风更偏向背景循环播放，哪些曲风更偏向用户主动收听？
## 2. Data Source
本次分析使用 YouTube public video metrics 数据，并基于 genre 维度进行聚合分析。
主要字段包括：
- genre
- video_count
- total_views
- median_views
- total_likes
- total_comments
- avg_like_rate
- avg_comment_rate
- avg_engagement_rate
- listening_behavior

## 3. Key Metrics
本次分析使用以下核心指标：
- Like Rate = Likes / Views
- Comment Rate = Comments / Views
- Engagement Rate = (Likes + Comments) / Views

相比单纯播放量，互动率更能帮助我们判断用户是否真正主动参与。例如，某类音乐播放量很高但点赞率和评论率较低，可能说明它更偏向咖啡厅、餐厅、学习或 playlist 的背景循环播放。而播放量不一定最高但互动率高的曲风，可能更接近用户主动收听和情绪反馈。
## 4. Genre-Level Summary
| Genre | Videos | Total Views | Median Views | Avg Like Rate | Avg Comment Rate | Avg Engagement Rate | Behavior |
|---|---:|---:|---:|---:|---:|---:|---|
| pop | 725 | 153,152,349,675 | 10,241,542 | 0.88% | 0.05% | 0.93% | Background / Looping Consumption |
| edm | 50 | 2,664,221,823 | 4,308,091 | 1.52% | 0.07% | 1.59% | Mixed / Unclear |
| jazz | 275 | 1,701,836,531 | 990,044 | 3.03% | 0.05% | 3.08% | Active Listening / High Engagement |
| devotional | 25 | 1,281,137,821 | 25,030,482 | 0.69% | 0.03% | 0.72% | Background / Looping Consumption |
| lofi | 300 | 1,057,546,649 | 331,835 | 1.62% | 0.26% | 1.88% | Mixed / Unclear |
| city pop | 25 | 336,859,634 | 807,120 | 1.95% | 0.08% | 2.03% | Active Listening / High Engagement |
| bossa nova | 25 | 108,977,800 | 2,499,589 | 1.06% | 0.01% | 1.07% | Mixed / Unclear |

## 5. Findings
### 5.1 Genres with Highest Total Views
- **pop**: total views = 153,152,349,675, median views = 10,241,542, engagement rate = 0.93%
- **edm**: total views = 2,664,221,823, median views = 4,308,091, engagement rate = 1.59%
- **jazz**: total views = 1,701,836,531, median views = 990,044, engagement rate = 3.08%

### 5.2 Genres with Highest Engagement Rate
- **jazz**: engagement rate = 3.08%, like rate = 3.03%, comment rate = 0.05%
- **city pop**: engagement rate = 2.03%, like rate = 1.95%, comment rate = 0.08%
- **lofi**: engagement rate = 1.88%, like rate = 1.62%, comment rate = 0.26%

### 5.3 Background / Looping Consumption Genres
- **pop**: 该曲风在当前数据中表现为高播放量但相对较低互动率，可能更偏向背景播放、playlist 循环或场景型消费。
- **devotional**: 该曲风在当前数据中表现为高播放量但相对较低互动率，可能更偏向背景播放、playlist 循环或场景型消费。

### 5.4 Active Listening / High Engagement Genres
- **jazz**: 该曲风在当前数据中互动率较高，可能更接近用户主动收听、情绪反馈或内容参与。
- **city pop**: 该曲风在当前数据中互动率较高，可能更接近用户主动收听、情绪反馈或内容参与。

## 6. Interpretation
从当前结果来看，播放量最高的曲风不一定拥有最高互动率。这说明播放量和用户喜好不能完全等同。对于 AI music 市场分析来说，播放量可以反映内容曝光和消费规模，但点赞率、评论率和综合互动率更能反映用户主动参与程度。
因此，后续分析不应只判断某个曲风是否发布量高或播放量高，而应结合 engagement metrics 来判断该曲风属于背景场景消费，还是主动用户消费。

## 7. Business Implications
- 高播放量、低互动率的曲风适合用于背景音乐、长时长播放、咖啡厅、学习和 playlist 场景。
- 高互动率曲风更适合做短视频传播、社交媒体测试、用户情绪型内容和主题化营销。
- 如果未来做 A/B test，可以测试同一主题下不同曲风，或同一曲风下不同主题的表现。

## 8. Next Steps
下一步可以继续扩展：
1. 增加更多 genre 和国家市场。
2. 加入 title / description 的 NLP 文本分类。
3. 对比不同国家、语言和主题下的 genre 表现。
4. 设计真实 A/B test，测试不同曲风和主题的市场反馈。
