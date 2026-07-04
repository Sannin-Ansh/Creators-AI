import os
import sys
from dotenv import load_dotenv

# Add directory to sys path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.youtube_search import search_youtube
from tools.reddit_search import search_reddit
from tools.trends_tool import fetch_trending_topics

def test_tools():
    print("Testing Search Tools...")
    query = "python programming"
    
    # 1. Test YouTube
    yt_results = search_youtube(query, limit=2)
    print(f"YouTube results fetched: {len(yt_results)}")
    for i, item in enumerate(yt_results):
        print(f"  [{i+1}] {item['title']} - {item['views']} ({item['channel']})")
        
    # 2. Test Reddit
    reddit_results = search_reddit(query, limit=2)
    print(f"Reddit results fetched: {len(reddit_results)}")
    for i, item in enumerate(reddit_results):
        print(f"  [{i+1}] {item['title']} - {item['upvotes']} upvotes in {item['subreddit']}")
        
    # 3. Test Trends RSS
    trends_results = fetch_trending_topics(query)
    print(f"Trends results fetched: {len(trends_results)}")
    for i, item in enumerate(trends_results):
        print(f"  [{i+1}] {item['title']} ({item['source']})")

if __name__ == "__main__":
    load_dotenv()
    test_tools()
    print("\nSearch Tools tests completed successfully!")
