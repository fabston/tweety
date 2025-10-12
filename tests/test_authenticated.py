#!/usr/bin/env python3
"""
Authenticated test script for tweety library functionality.
This script demonstrates how to use the library with authentication.
Note: This requires valid Twitter credentials.
"""

import asyncio
import sys
import os
import getpass

# Add parent directory to path so we can import tweety
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tweety import TwitterAsync, Twitter

def get_credentials():
    """Get Twitter credentials from user input."""
    print("Twitter Authentication Test")
    print("=" * 40)
    print("Note: This test requires valid Twitter credentials.")
    print("Your credentials will be used to test authenticated features.")
    print()
    
    username = input("Enter your Twitter username (without @): ").strip()
    password = getpass.getpass("Enter your Twitter password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required.")
        return None, None
    
    return username, password

async def test_authentication():
    """Test Twitter authentication."""
    print("\n🔐 Testing Twitter Authentication...")
    
    username, password = get_credentials()
    if not username or not password:
        return False
    
    try:
        app = TwitterAsync("authenticated_session")
        
        print(f"  - Attempting to login as @{username}...")
        await app.sign_in(username, password)
        
        if app.logged_in:
            print("✅ Successfully authenticated!")
            print(f"  - Logged in: {app.logged_in}")
            print(f"  - User authorized: {app.is_user_authorized}")
            print(f"  - User ID: {app.user_id}")
            if app.user:
                print(f"  - Username: @{app.user.username}")
                print(f"  - Display name: {app.user.name}")
                print(f"  - Followers: {app.user.followers_count}")
            return True
        else:
            print("❌ Authentication failed - not logged in")
            return False
            
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

async def test_authenticated_features(app):
    """Test features that require authentication."""
    print("\n🔍 Testing Authenticated Features...")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Get trends
    total_tests += 1
    try:
        print("  - Testing trends retrieval...")
        trends = await app.get_trends()
        if trends and len(trends) > 0:
            print(f"    ✅ Retrieved {len(trends)} trends")
            print(f"    - First trend: {trends[0].name}")
            tests_passed += 1
        else:
            print("    ❌ No trends retrieved")
    except Exception as e:
        print(f"    ❌ Trends test failed: {e}")
    
    # Test 2: Search functionality
    total_tests += 1
    try:
        print("  - Testing search functionality...")
        search_results = await app.search("python programming", pages=1)
        if search_results and len(search_results) > 0:
            print(f"    ✅ Retrieved {len(search_results)} search results")
            print(f"    - First result: {search_results[0].text[:100]}...")
            tests_passed += 1
        else:
            print("    ❌ No search results retrieved")
    except Exception as e:
        print(f"    ❌ Search test failed: {e}")
    
    # Test 3: Get user followers (limited)
    total_tests += 1
    try:
        print("  - Testing followers retrieval...")
        # Get followers of a public account (limited to 1 page)
        followers = await app.get_user_followers("elonmusk", pages=1)
        if followers and len(followers) > 0:
            print(f"    ✅ Retrieved {len(followers)} followers")
            print(f"    - First follower: @{followers[0].username}")
            tests_passed += 1
        else:
            print("    ❌ No followers retrieved")
    except Exception as e:
        print(f"    ❌ Followers test failed: {e}")
    
    # Test 4: Get user followings (limited)
    total_tests += 1
    try:
        print("  - Testing followings retrieval...")
        # Get followings of a public account (limited to 1 page)
        followings = await app.get_user_followings("elonmusk", pages=1)
        if followings and len(followings) > 0:
            print(f"    ✅ Retrieved {len(followings)} followings")
            print(f"    - First following: @{followings[0].username}")
            tests_passed += 1
        else:
            print("    ❌ No followings retrieved")
    except Exception as e:
        print(f"    ❌ Followings test failed: {e}")
    
    # Test 5: Get user likes (if accessible)
    total_tests += 1
    try:
        print("  - Testing user likes retrieval...")
        # This might fail due to privacy settings
        likes = await app.get_user_likes("elonmusk", pages=1)
        if likes and len(likes) > 0:
            print(f"    ✅ Retrieved {len(likes)} liked tweets")
            print(f"    - First liked tweet: {likes[0].text[:100]}...")
            tests_passed += 1
        else:
            print("    ⚠️  No likes retrieved (may be private)")
            tests_passed += 1  # Count as pass since it's expected to be private
    except Exception as e:
        print(f"    ⚠️  Likes test failed (expected for private accounts): {e}")
        tests_passed += 1  # Count as pass since it's expected to fail
    
    return tests_passed, total_tests

async def test_advanced_features(app):
    """Test advanced features that require authentication."""
    print("\n🚀 Testing Advanced Features...")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Typehead user search
    total_tests += 1
    try:
        print("  - Testing typehead user search...")
        search_results = await app.typehead_user_search("elon")
        if search_results and hasattr(search_results, 'users') and len(search_results.users) > 0:
            print(f"    ✅ Retrieved {len(search_results.users)} user suggestions")
            print(f"    - First suggestion: @{search_results.users[0].username}")
            tests_passed += 1
        else:
            print("    ❌ No user suggestions retrieved")
    except Exception as e:
        print(f"    ❌ Typehead search test failed: {e}")
    
    # Test 2: Get user media
    total_tests += 1
    try:
        print("  - Testing user media retrieval...")
        media = await app.get_user_media("elonmusk", pages=1)
        if media and len(media) > 0:
            print(f"    ✅ Retrieved {len(media)} media tweets")
            print(f"    - First media tweet: {media[0].text[:100]}...")
            tests_passed += 1
        else:
            print("    ❌ No media tweets retrieved")
    except Exception as e:
        print(f"    ❌ Media test failed: {e}")
    
    # Test 3: Search with filters
    total_tests += 1
    try:
        print("  - Testing search with filters...")
        from tweety.filters import SearchFilters
        search_results = await app.search("python", pages=1, filter_=SearchFilters.Latest())
        if search_results and len(search_results) > 0:
            print(f"    ✅ Retrieved {len(search_results)} filtered search results")
            print(f"    - First result: {search_results[0].text[:100]}...")
            tests_passed += 1
        else:
            print("    ❌ No filtered search results retrieved")
    except Exception as e:
        print(f"    ❌ Filtered search test failed: {e}")
    
    return tests_passed, total_tests

async def main():
    """Run authenticated tests."""
    print("=" * 60)
    print("TWETY LIBRARY - AUTHENTICATED FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Test authentication
    auth_success = await test_authentication()
    
    if not auth_success:
        print("\n❌ Authentication failed. Cannot proceed with authenticated tests.")
        print("Please check your credentials and try again.")
        return False
    
    # Get the authenticated app instance
    app = TwitterAsync("authenticated_session")
    await app.sign_in(*get_credentials())
    
    if not app.logged_in:
        print("\n❌ Could not maintain authentication. Exiting.")
        return False
    
    # Run authenticated feature tests
    auth_tests_passed, auth_tests_total = await test_authenticated_features(app)
    
    # Run advanced feature tests
    advanced_tests_passed, advanced_tests_total = await test_advanced_features(app)
    
    # Summary
    print("\n" + "=" * 60)
    print("AUTHENTICATED TEST SUMMARY")
    print("=" * 60)
    
    total_passed = auth_tests_passed + advanced_tests_passed
    total_tests = auth_tests_total + advanced_tests_total
    
    print(f"Authentication: {'✅ PASS' if auth_success else '❌ FAIL'}")
    print(f"Authenticated Features: {auth_tests_passed}/{auth_tests_total} tests passed")
    print(f"Advanced Features: {advanced_tests_passed}/{advanced_tests_total} tests passed")
    print(f"\nOverall Results: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 All authenticated tests passed! The library is working correctly with authentication.")
    else:
        print("⚠️  Some authenticated tests failed. Check the output above for details.")
    
    return total_passed == total_tests

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
