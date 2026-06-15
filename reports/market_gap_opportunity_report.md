# Market Gap Opportunity Report

## Purpose

This report combines YouTube public-demand signals with iTunes catalog-supply signals.

The goal is to identify markets where AI-generated music may have strong demand but relatively lower existing catalog supply.

## Method

- YouTube opportunity score = demand signal
- iTunes catalog count = supply / competition proxy
- Gap score = high demand + low supply
- Final market gap score = demand score + gap score

## Top 10 Market Gap Opportunities

| country_code   | country_name   | genre   | content_type   | lyric_style    | query                   | total_views    |   youtube_opportunity_score |   itunes_catalog_count |   supply_score |   gap_score |   final_market_gap_score |
|:---------------|:---------------|:--------|:---------------|:---------------|:------------------------|:---------------|----------------------------:|-----------------------:|---------------:|------------:|-------------------------:|
| US             | United States  | pop     | lyrical        | english        | English pop song        | 28,436,722,900 |                       0.696 |                     50 |          1     |       0     |                    0.453 |
| ES             | Spain          | pop     | lyrical        | local_language | Spanish pop song Spain  | 31,745,865,978 |                       0.691 |                     50 |          1     |       0     |                    0.449 |
| MX             | Mexico         | pop     | lyrical        | local_language | Mexican pop song        | 19,289,374,269 |                       0.648 |                     50 |          1     |       0     |                    0.421 |
| KR             | South Korea    | pop     | lyrical        | local_language | Korean pop song         | 12,200,630,320 |                       0.646 |                     50 |          1     |       0     |                    0.42  |
| NZ             | New Zealand    | pop     | lyrical        | english        | New Zealand pop song    | 571,494,926    |                       0.404 |                      0 |          0     |       0.404 |                    0.404 |
| FR             | France         | pop     | lyrical        | local_language | French pop song         | 7,542,836,539  |                       0.585 |                     50 |          1     |       0     |                    0.38  |
| MX             | Mexico         | pop     | lyrical        | humorous       | Spanish funny song      | 6,858,342,392  |                       0.579 |                     50 |          1     |       0     |                    0.377 |
| ES             | Spain          | pop     | lyrical        | humorous       | Spanish funny song      | 6,851,765,726  |                       0.577 |                     50 |          1     |       0     |                    0.375 |
| IN             | India          | pop     | lyrical        | local_language | Hindi pop song          | 7,218,745,306  |                       0.57  |                     50 |          1     |       0     |                    0.37  |
| CA             | Canada         | lofi    | instrumental   | no_lyrics      | lofi study music Canada | 93,171,276     |                       0.409 |                      2 |          0.279 |       0.295 |                    0.369 |

## Interpretation

Markets with high YouTube demand and relatively low iTunes catalog supply may be stronger candidates for AI-generated music testing.

This does not prove the market is completely empty. It gives an automated first-pass signal for potential market gaps.

## Next Step

Use the top-ranked markets to design A/B tests across lyrics, language, and genre.