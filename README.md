# A collection of scripts for downloading and analyzing WordPress posts

Based on analytics work, these scripts download posts and metadata via the WordPress API

## Usage

Example usage:

```
python3 post_downloader.py -output download/posts.csv -categories news,announcements -start_year 2024 -start_month 02 -domain example.com
```

### Arguments:

- **-output** - CSV file to output to (e.g., `posts.csv`)
- **-categories** - WordPress category slugs to include (comma-separated list). Must be slugs (as in the category archive URL), not IDs or names
- **-exclude_categories** - WordPress category slugs to EXCLUDE (comma-separated list). Must be slugs (as in the category archive URL), not IDs or names
- **-start_year** - Starting year - get posts beginning with this year, up to the current year
- **-start_month** - Starting month - if start_year is set, get posts after this year and month up to the current year/month
- **-domain** - The domain of the WordPress site. Uses the standard root install path for the API under this domain (`/wp-json/wp/v2/`)