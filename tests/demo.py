#!/usr/bin/env python3
"""
Demo script showing how to use the tweety library.
This script demonstrates the most common use cases.
"""

import asyncio
import sys
import os

# Add parent directory to path so we can import tweety
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tweety import TwitterAsync, Twitter

async def demo_public_features():
    """Demonstrate public features that don't require authentication."""
    print("🌐 DEMO: Public Features (No Authentication Required)")
    print("=" * 60)
    
    # Create an instance
    app = TwitterAsync("demo_session")
    
    # Get user information
    print("\n1. Getting user information...")
    try:
        user = await app.get_user_info("elonmusk")
        if user:
            print(f"   ✅ User: @{user.username}")
            print(f"   📝 Name: {user.name}")
            print(f"   🆔 ID: {user.id}")
            print(f"   👥 Followers: {user.followers_count:,}")
            print(f"   📊 Following: {user.friends_count:,}")
            print(f"   ✅ Verified: {user.verified}")
            print(f"   📍 Location: {user.location or 'Not specified'}")
            print(f"   📝 Bio: {user.description or 'No bio'}")
            print(f"   🖼️  Profile Image: {user.profile_image_url_https or 'No image'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get recent tweets
    print("\n2. Getting recent tweets...")
    try:
        tweets = await app.get_tweets("elonmusk", pages=1)
        if tweets and len(tweets) > 0:
            print(f"   ✅ Retrieved {len(tweets)} tweets")
            print("\n   Recent tweets:")
            for i, tweet in enumerate(tweets[:3], 1):  # Show first 3 tweets
                print(f"   {i}. {tweet.text[:100]}{'...' if len(tweet.text) > 100 else ''}")
                print(f"      📅 {tweet.date}")
                print(f"      ❤️  {tweet.likes} likes, 🔄 {tweet.retweet_counts} retweets")
                print()
        else:
            print("   ❌ No tweets found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get user ID
    print("\n3. Getting user ID...")
    try:
        user_id = await app.get_user_id("elonmusk")
        print(f"   ✅ User ID: {user_id}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

async def demo_authenticated_features():
    """Demonstrate authenticated features."""
    print("\n🔐 DEMO: Authenticated Features")
    print("=" * 60)
    print("Note: This requires valid Twitter credentials.")
    
    # Get credentials
    username = input("\nEnter your Twitter username (without @): ").strip()
    if not username:
        print("❌ No username provided. Skipping authenticated demo.")
        return
    
    password = input("Enter your Twitter password: ").strip()
    if not password:
        print("❌ No password provided. Skipping authenticated demo.")
        return
    
    app = TwitterAsync("demo_auth_session")
    
    # Authenticate
    print("\n1. Authenticating...")
    try:
        await app.sign_in(username, password)
        if app.logged_in:
            print(f"   ✅ Successfully logged in as @{app.user.username}")
            print(f"   🆔 User ID: {app.user_id}")
        else:
            print("   ❌ Authentication failed")
            return
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
        return
    
    # Get trends
    print("\n2. Getting trending topics...")
    try:
        trends = await app.get_trends()
        if trends and len(trends) > 0:
            print(f"   ✅ Retrieved {len(trends)} trending topics")
            print("\n   Top trends:")
            for i, trend in enumerate(trends[:5], 1):  # Show top 5
                print(f"   {i}. {trend.name}")
        else:
            print("   ❌ No trends found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Search tweets
    print("\n3. Searching tweets...")
    try:
        search_term = "python programming"
        search_results = await app.search(search_term, pages=1)
        if search_results and len(search_results) > 0:
            print(f"   ✅ Found {len(search_results)} tweets for '{search_term}'")
            print("\n   Sample results:")
            for i, tweet in enumerate(search_results[:3], 1):  # Show first 3
                print(f"   {i}. @{tweet.author.username}: {tweet.text[:80]}{'...' if len(tweet.text) > 80 else ''}")
        else:
            print(f"   ❌ No results found for '{search_term}'")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get followers
    print("\n4. Getting user followers...")
    try:
        followers = await app.get_user_followers("elonmusk", pages=1)
        if followers and len(followers) > 0:
            print(f"   ✅ Retrieved {len(followers)} followers")
            print("\n   Sample followers:")
            for i, follower in enumerate(followers[:3], 1):  # Show first 3
                print(f"   {i}. @{follower.username} - {follower.name}")
        else:
            print("   ❌ No followers found")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def demo_sync_usage():
    """Demonstrate synchronous usage."""
    print("\n🔄 DEMO: Synchronous Usage")
    print("=" * 60)
    
    # Create synchronous instance
    app = Twitter("demo_sync_session")
    
    print("✅ Created synchronous Twitter instance")
    print(f"   Session: {app.session.session_name}")
    print(f"   Logged in: {app.logged_in}")
    
    # Note: In real usage, you would call methods like:
    # user = app.get_user_info("elonmusk")
    # tweets = app.get_tweets("elonmusk", pages=1)
    # The sync wrapper automatically handles async/sync conversion

async def main():
    """Run the demo."""
    print("🐦 TWETY LIBRARY DEMO")
    print("=" * 60)
    print("This demo shows how to use the tweety library for Twitter scraping.")
    
    # Demo public features
    await demo_public_features()
    
    # Demo authenticated features (optional)
    print("\n" + "=" * 60)
    auth_choice = input("Do you want to see authenticated features demo? (y/n): ").strip().lower()
    if auth_choice in ['y', 'yes']:
        await demo_authenticated_features()
    
    # Demo sync usage
    demo_sync_usage()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\nFor more examples, check the test scripts:")
    print("  - test_basic.py: Basic functionality tests")
    print("  - test_authenticated.py: Authenticated features tests")
    print("  - test_comprehensive.py: Complete test suite")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
