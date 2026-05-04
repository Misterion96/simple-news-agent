import os
import sys
from loguru import logger
from dotenv import load_dotenv

from rss_engine import RSSCollector
from gemini_service import GeminiService
from prompts import NEWS_SYS_PROMPT

load_dotenv()

def main():
    logger.info("Starting Gemini RSS News Agent")
    
    # Initialize services
    collector = RSSCollector()
    gemini = GeminiService()
    
    print("\n--- News Agent (RSS + Gemini) ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            query = input("Enter news topic to search: ").strip()
            
            if not query:
                continue
            if query.lower() in ['exit', 'quit', 'q']:
                break
                
            # 1. Fetch news from RSS (last 7 days)
            print(f"\nSearching for '{query}' in RSS feeds (last 7 days)...")
            articles = collector.fetch_articles(query, days_limit=7)
            
            if not articles:
                print(f"\nNo articles found for '{query}' in current RSS feeds.\n")
                continue
                
            # 2. Format articles for LLM
            formatted_news = collector.format_for_llm(articles)
            
            # 3. Summarize using Gemini
            print("\nSummarizing with Gemini... Please wait.\n")
            summary = gemini.summarize(formatted_news, system_instruction=NEWS_SYS_PROMPT)
            
            # 4. Display result
            print("="*50)
            print(f"SUMMARY FOR: {query.upper()}")
            print("="*50)
            print(summary)
            print("="*50)
            print("\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
