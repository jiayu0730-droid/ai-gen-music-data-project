## Music Platform Data Fetching Results

### iTunes Data Fetching

I implemented a Python script to fetch music data from the iTunes Search API. The script successfully collected 250 music records based on several search terms, including AI-generated music, Suno AI music, Taylor Swift, Drake, and The Weeknd.

The collected iTunes dataset includes 250 rows and 10 columns:

* Search term
* Track name
* Artist name
* Album name
* Release date
* Genre
* Track price
* Currency
* Preview URL
* iTunes / Apple Music URL

Based on the collected data, iTunes is useful for music catalog and metadata analysis. For example, the top genres in the dataset were R&B/Soul, Pop, Hip-Hop/Rap, Orchestral, and Country. The average track price was approximately $1.19.

However, iTunes does not provide deeper performance or business metrics such as stream counts, artist followers, popularity scores, revenue, royalties, listener demographics, or user-level listening behavior.

### Spotify Data Fetching

I also implemented a Python script using the Spotify Web API and Spotipy package. The Spotify API connection was successfully established using a developer app, Client ID, Client Secret, and a local `.env` file.

The script successfully searched for artist profiles including Taylor Swift, Drake, The Weeknd, Bad Bunny, and Ariana Grande, and returned basic artist information such as artist name, Spotify artist ID, and Spotify profile URL.

However, in the current fetching result, several expected fields, including followers, popularity score, and genres, were returned as missing values. Therefore, these fields are recorded as unavailable in the current implementation and may require further API troubleshooting or permission review.

### Summary of Available and Unavailable Data

| Data Type                 | iTunes        | Spotify                                |
| ------------------------- | ------------- | -------------------------------------- |
| Track Name                | Available     | Partial                                |
| Artist Name               | Available     | Available                              |
| Album Name                | Available     | Partial                                |
| Genre                     | Available     | Not returned in current Spotify result |
| Release Date              | Available     | Partial                                |
| Track Price               | Available     | Not available                          |
| Preview URL               | Available     | Partial                                |
| Artist ID                 | Not available | Available                              |
| Artist Profile URL        | Available     | Available                              |
| Followers                 | Not available | Not returned in current Spotify result |
| Popularity Score          | Not available | Not returned in current Spotify result |
| Revenue                   | Not available | Not available                          |
| Royalty / Payout Data     | Not available | Not available                          |
| Listener Demographics     | Not available | Not available                          |
| User-level Listening Data | Not available | Not available                          |

### Key Finding

iTunes is more suitable for catalog-level music metadata collection, while Spotify is potentially more useful for artist-level popularity analysis. However, the current Spotify implementation only successfully returned basic artist identity fields and profile URLs. More troubleshooting is needed to access richer artist metrics.
