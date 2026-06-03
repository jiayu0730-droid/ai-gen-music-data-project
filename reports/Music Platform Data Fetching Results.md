# Platform Analysis: Apple iTunes

## Objective

The objective of this analysis was to evaluate the Apple iTunes Search API as a potential data source for music industry research. Specifically, we investigated what types of music and musician information can be accessed through the public API and assessed its usefulness for future AI-generated music analytics.

---

## Data Collection Method

A Python-based data collection pipeline was developed using the Apple iTunes Search API.

The following search terms were used:

* AI generated music
* Suno AI music
* Taylor Swift
* Drake
* The Weeknd

The script successfully collected and exported 250 music records into a structured CSV dataset.

Output file:

```text
data/itunes_music_data.csv
```

Dataset dimensions:

```text
250 rows × 10 columns
```

---

## Available Data Fields

The iTunes API provides access to music catalog metadata, including:

| Category            | Field                    |
| ------------------- | ------------------------ |
| Song Information    | Track Name               |
| Artist Information  | Artist Name              |
| Album Information   | Album Name               |
| Music Metadata      | Genre                    |
| Music Metadata      | Release Date             |
| Commercial Metadata | Track Price              |
| Commercial Metadata | Currency                 |
| Content Access      | Preview URL              |
| Platform Reference  | iTunes / Apple Music URL |
| Search Context      | Search Keyword           |

---

## Dataset Summary

### Top Genres

Among the 250 collected records, the most common genres were:

| Genre       | Count |
| ----------- | ----- |
| R&B/Soul    | 63    |
| Pop         | 53    |
| Hip-Hop/Rap | 32    |
| Orchestral  | 24    |
| Country     | 19    |
| Rock        | 16    |

Observation:

* Mainstream genres such as Pop, Hip-Hop, and R&B dominate the dataset.
* AI-generated music results frequently appeared in orchestral and cinematic categories.
* Genre metadata is consistently available and can support future genre trend analysis.

---

### Top Artists

The most frequently returned artists were:

| Artist                          | Count |
| ------------------------------- | ----- |
| Taylor Swift                    | 47    |
| The Weeknd                      | 41    |
| Drake                           | 27    |
| M.Ahai                          | 24    |
| Fabian Engelhardt Suno AI Music | 13    |

Observation:

* Major commercial artists dominate the search results.
* Several AI-music-related artists and creators also appeared, including Suno-associated content.
* This suggests that AI-generated music is already being distributed through mainstream music platforms.

---

### Pricing Information

Average track price:

```text
$1.19
```

Observation:

* Pricing metadata is available through the API.
* This allows basic commercial catalog analysis.
* However, pricing does not represent actual revenue or streaming performance.

---

## Data Not Available

Although the API provides rich catalog information, several important analytics fields are not publicly accessible.

### Audience Analytics

Not Available:

* Listener demographics
* Geographic distribution
* User age groups
* User engagement behavior

### Popularity Metrics

Not Available:

* Number of streams
* Monthly listeners
* Track popularity scores
* Playlist placements

### Artist Performance Metrics

Not Available:

* Artist followers
* Fan growth trends
* Engagement statistics

### Revenue Metrics

Not Available:

* Streaming revenue
* Artist earnings
* Royalty payouts
* Platform monetization data

---

## Key Findings

The Apple iTunes API is highly effective for collecting music catalog metadata, including songs, artists, albums, genres, release dates, pricing information, and preview links.

However, the platform provides limited support for music performance analytics. Critical business metrics such as streams, followers, popularity scores, and revenue data are not available through the public API.

As a result:

### Suitable Use Cases

* Music catalog research
* Genre classification
* Release trend analysis
* Artist discovery
* AI-generated music identification

### Not Suitable For

* Popularity analysis
* Revenue analysis
* Audience behavior analysis
* Music marketing performance evaluation

---

## Conclusion

Apple iTunes serves as a strong source of music metadata and catalog information. It is valuable for building music databases and conducting content-level analysis.

However, additional platforms such as Spotify and YouTube Music will be required to obtain artist popularity metrics, audience engagement indicators, and performance-related analytics needed for a comprehensive AI music intelligence platform.
