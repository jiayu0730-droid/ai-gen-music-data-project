# Genre A/B Test: Background Looping vs Active Listening

## 1. Research Question

本次 A/B test 的目标是验证：不同曲风是否呈现不同的收听行为。具体来说，我们想比较背景循环播放型音乐和主动收听型音乐在播放量、点赞率、评论率和综合互动率上的差异。

## 2. A/B Group Design

### Group A: Background / Looping Music

包含曲风：jazz, lofi, bossa nova

这类音乐通常可能用于咖啡厅、餐厅、学习、放松或 playlist 循环播放场景。理论假设是：播放量可能较高，但点赞率和评论率可能相对较低。

### Group B: Active Listening / Entertainment Music

包含曲风：pop, edm, city pop

这类音乐更可能被用户主动点击、收听和互动。理论假设是：播放量不一定最高，但点赞率、评论率或综合互动率可能更高。

## 3. Metrics

- Total Views
- Median Views
- Like Rate = Likes / Views
- Comment Rate = Comments / Views
- Engagement Rate = (Likes + Comments) / Views

## 4. A/B Test Results

| Group | Genres | Total Videos | Total Views | Median Views | Avg Like Rate | Avg Comment Rate | Avg Engagement Rate |
|---|---|---:|---:|---:|---:|---:|---:|
| A_Background_Looping | jazz, lofi, bossa nova | 600 | 2,868,360,980 | 990,044 | 1.90% | 0.11% | 2.01% |
| B_Active_Listening | pop, edm, city pop | 800 | 156,153,431,132 | 4,308,091 | 1.45% | 0.07% | 1.52% |

## 5. Interpretation

Group A 的总播放量为 2,868,360,980，平均互动率为 2.01%。

Group B 的总播放量为 156,153,431,132，平均互动率为 1.52%。

当前结果没有完全支持初始假设，说明还需要扩大样本量、细分曲风和加入更多控制变量。

## 6. Limitations

本次分析是基于公开 YouTube 数据的 observational A/B comparison，并不是严格意义上的真实线上 A/B test。真实 A/B test 需要控制发布时间、封面、标题、推广量、国家市场和歌曲长度等变量。

此外，YouTube public API 当前可以获取 views、likes 和 comments，但不能稳定获取 saves / 收藏量。因此第一版分析使用播放量、点赞率、评论率和综合互动率作为核心指标。

## 7. Next Step: Real A/B Test Design

下一步可以用 Suno 生成多组歌曲，并进行真实 A/B test：

### Test 1: Same Theme, Different Genre

| Version | Theme | Genre |
|---|---|---|
| A | Study / Cafe | Jazz |
| B | Study / Cafe | Lofi |
| C | Study / Cafe | Bossa Nova |

### Test 2: Same Genre, Different Theme

| Version | Genre | Theme |
|---|---|---|
| A | Pop | Romance |
| B | Pop | Hometown |
| C | Pop | Food / Novelty |

真实实验中需要尽量控制：title format、cover style、publish time、song length、language、target country 和 promotion level。
