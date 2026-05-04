import feedparser
import time
from typing import List, Dict, Optional
from loguru import logger

# Specialized list of Frontend, UX and Web Development RSS feeds
DEFAULT_FEEDS = [
    "https://www.smashingmagazine.com/feed",
    "https://css-tricks.com/feed/",
    "https://tympanus.net/codrops/feed/",
    "https://blog.logrocket.com/feed/",
    "https://www.joshwcomeau.com/rss.xml",
    "https://ishadeed.com/feed.xml"
]

class RSSCollector:
    def __init__(self, feeds: List[str] = None):
        self.feeds = feeds or DEFAULT_FEEDS

    def fetch_articles(self, query: str, limit_per_feed: int = 5, days_limit: Optional[int] = None) -> List[Dict]:
        """
        Fetches and filters articles from RSS feeds based on the query and optional date limit.
        """
        all_articles = []
        query_lower = query.lower()
        
        min_timestamp = None
        if days_limit:
            min_timestamp = time.time() - (days_limit * 24 * 60 * 60)
            logger.info(f"Filtering articles older than {days_limit} days.")

        logger.info(f"Searching RSS feeds for query: '{query}'")
        
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                if feed.get("bozo"): # Check for malformed feed
                    logger.warning(f"Feed at {feed_url} might be malformed.")
                
                count = 0
                for entry in feed.entries:
                    # Date filtering
                    if min_timestamp:
                        published_parsed = entry.get("published_parsed")
                        if published_parsed:
                            published_ts = time.mktime(published_parsed)
                            if published_ts < min_timestamp:
                                continue

                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    
                    # Search in title or summary
                    if query_lower in title.lower() or query_lower in summary.lower():
                        article = {
                            "title": title,
                            "summary": summary,
                            "link": entry.get("link", ""),
                            "published": entry.get("published", "N/A"),
                            "source": feed.feed.get("title", feed_url) # Use URL if title is missing
                        }
                        all_articles.append(article)
                        count += 1
                        
                    if count >= limit_per_feed:
                        break
                        
            except Exception as e:
                logger.error(f"Failed to parse feed {feed_url}: {e}")
                
        logger.success(f"Found {len(all_articles)} articles across all feeds.")
        return all_articles

    def format_for_llm(self, articles: List[Dict]) -> str:
        """
        Formats a list of articles into a single string for LLM processing.
        """
        if not articles:
            return "No news found for the given query."
            
        formatted = "Frontend & UI/UX News Articles:\n\n"
        for i, art in enumerate(articles, 1):
            formatted += f"Article {i}:\n"
            formatted += f"Title: {art['title']}\n"
            formatted += f"Source: {art['source']} ({art['published']})\n"
            formatted += f"Description: {art['summary']}\n"
            formatted += f"Link: {art['link']}\n"
            formatted += "-" * 20 + "\n\n"
            
        return formatted

if __name__ == "__main__":
    # Quick test
    collector = RSSCollector()
    results = collector.fetch_articles("React")
    print(collector.format_for_llm(results[:3]))
