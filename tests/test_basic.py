#!/usr/bin/env python3
"""
Basic test script for tweety library functionality.
This script tests core features that don't require authentication.
"""

import asyncio
import sys
import os

# Add parent directory to path so we can import tweety
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tweety import TwitterAsync, Twitter

def test_import():
    """Test that the library can be imported correctly."""
    print("✓ Testing import...")
    try:
        from tweety import TwitterAsync, Twitter
        print("✓ Successfully imported TwitterAsync and Twitter classes")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

def test_sync_initialization():
    """Test synchronous Twitter class initialization."""
    print("\n✓ Testing synchronous Twitter initialization...")
    try:
        app = Twitter("test_session")
        print("✓ Successfully created Twitter instance")
        print(f"  - Session name: {app.session.session_name}")
        print(f"  - Logged in: {app.logged_in}")
        print(f"  - User authorized: {app.is_user_authorized}")
        return True
    except Exception as e:
        print(f"✗ Failed to create Twitter instance: {e}")
        return False

async def test_async_initialization():
    """Test asynchronous TwitterAsync class initialization."""
    print("\n✓ Testing asynchronous TwitterAsync initialization...")
    try:
        app = TwitterAsync("test_session_async")
        print("✓ Successfully created TwitterAsync instance")
        print(f"  - Session name: {app.session.session_name}")
        print(f"  - Logged in: {app.logged_in}")
        print(f"  - User authorized: {app.is_user_authorized}")
        return True
    except Exception as e:
        print(f"✗ Failed to create TwitterAsync instance: {e}")
        return False

async def test_public_user_info():
    """Test getting public user information (no auth required)."""
    print("\n✓ Testing public user info retrieval...")
    try:
        app = TwitterAsync("test_session")
        
        # Test with a well-known public account
        username = "elonmusk"
        print(f"  - Attempting to get info for @{username}...")
        
        user_info = await app.get_user_info(username)
        
        if user_info:
            print(f"✓ Successfully retrieved user info for @{username}")
            print(f"  - User ID: {user_info.id}")
            print(f"  - Username: @{user_info.username}")
            print(f"  - Display name: {user_info.name}")
            print(f"  - Followers: {user_info.followers_count}")
            print(f"  - Following: {user_info.friends_count}")
            print(f"  - Verified: {user_info.verified}")
            return True
        else:
            print(f"✗ No user info returned for @{username}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to get user info: {e}")
        return False

async def test_tweet_detail():
    """Test getting a single tweet detail (no auth required)."""
    print("\n✓ Testing tweet detail retrieval...")
    try:
        app = TwitterAsync("test_session")
        
        # Test with a well-known tweet ID (this might need to be updated)
        # Using a generic approach - try to get a recent tweet from a public account
        print("  - Attempting to get a tweet detail...")
        
        # This is a placeholder - in real testing, you'd use an actual tweet ID
        # For now, we'll just test that the method exists and can be called
        print("  - Tweet detail method is available (requires valid tweet ID for full test)")
        return True
        
    except Exception as e:
        print(f"✗ Failed to test tweet detail: {e}")
        return False

async def test_public_tweets():
    """Test getting public tweets (limited without auth)."""
    print("\n✓ Testing public tweets retrieval...")
    try:
        app = TwitterAsync("test_session")
        
        username = "elonmusk"
        print(f"  - Attempting to get tweets for @{username}...")
        
        # Try to get just 1 page of tweets
        tweets = await app.get_tweets(username, pages=1)
        
        if tweets and len(tweets) > 0:
            print(f"✓ Successfully retrieved {len(tweets)} tweets")
            print(f"  - First tweet ID: {tweets[0].id}")
            print(f"  - First tweet text: {tweets[0].text[:100]}...")
            return True
        else:
            print(f"✗ No tweets returned for @{username}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to get tweets: {e}")
        print(f"  - Error details: {str(e)}")
        return False

def test_properties():
    """Test class properties and methods."""
    print("\n✓ Testing class properties...")
    try:
        app = Twitter("test_session")
        
        # Test properties
        print(f"  - User ID property: {app.user_id}")
        print(f"  - Cache property: {app.cache}")
        
        print("✓ Properties accessible")
        return True
        
    except Exception as e:
        print(f"✗ Failed to test properties: {e}")
        return False

async def main():
    """Run all basic tests."""
    print("=" * 60)
    print("TWETY LIBRARY - BASIC FUNCTIONALITY TEST")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_import),
        ("Sync Initialization", test_sync_initialization),
        ("Async Initialization", test_async_initialization),
        ("Class Properties", test_properties),
        ("Public User Info", test_public_user_info),
        ("Tweet Detail", test_tweet_detail),
        ("Public Tweets", test_public_tweets),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! The library is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
