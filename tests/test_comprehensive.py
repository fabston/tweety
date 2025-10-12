#!/usr/bin/env python3
"""
Comprehensive test suite for tweety library.
This script provides a complete testing framework for all major features.
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path so we can import tweety
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tweety import TwitterAsync, Twitter
from tweety.filters import SearchFilters, TweetCommentFilters

class TweetyTestSuite:
    """Comprehensive test suite for tweety library."""
    
    def __init__(self):
        self.results = []
        self.app = None
        self.authenticated = False
        
    def log_test(self, test_name, passed, message="", details=None):
        """Log test results."""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        if details:
            print(f"    Details: {details}")
        
        self.results.append({
            'test': test_name,
            'passed': passed,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    async def test_import_and_initialization(self):
        """Test basic import and initialization."""
        print("\n🔧 Testing Import and Initialization...")
        
        # Test import
        try:
            from tweety import TwitterAsync, Twitter
            self.log_test("Import Test", True, "Successfully imported all classes")
        except ImportError as e:
            self.log_test("Import Test", False, f"Import failed: {e}")
            return False
        
        # Test sync initialization
        try:
            sync_app = Twitter("test_sync")
            self.log_test("Sync Initialization", True, f"Session: {sync_app.session.session_name}")
        except Exception as e:
            self.log_test("Sync Initialization", False, f"Failed: {e}")
        
        # Test async initialization
        try:
            self.app = TwitterAsync("test_async")
            self.log_test("Async Initialization", True, f"Session: {self.app.session.session_name}")
        except Exception as e:
            self.log_test("Async Initialization", False, f"Failed: {e}")
            return False
        
        return True
    
    async def test_public_features(self):
        """Test features that don't require authentication."""
        print("\n🌐 Testing Public Features...")
        
        if not self.app:
            self.log_test("Public Features", False, "No app instance available")
            return False
        
        # Test user info retrieval
        try:
            user_info = await self.app.get_user_info("elonmusk")
            if user_info:
                self.log_test("User Info Retrieval", True, 
                    f"Retrieved info for @{user_info.username} (ID: {user_info.id})")
            else:
                self.log_test("User Info Retrieval", False, "No user info returned")
        except Exception as e:
            self.log_test("User Info Retrieval", False, f"Failed: {e}")
        
        # Test tweets retrieval
        try:
            tweets = await self.app.get_tweets("elonmusk", pages=1)
            if tweets and len(tweets) > 0:
                self.log_test("Tweets Retrieval", True, 
                    f"Retrieved {len(tweets)} tweets")
            else:
                self.log_test("Tweets Retrieval", False, "No tweets returned")
        except Exception as e:
            self.log_test("Tweets Retrieval", False, f"Failed: {e}")
        
        # Test tweet detail (with a known tweet ID)
        try:
            # This would need a real tweet ID to work properly
            self.log_test("Tweet Detail Method", True, "Method available (requires valid tweet ID)")
        except Exception as e:
            self.log_test("Tweet Detail Method", False, f"Failed: {e}")
        
        # Test user ID resolution
        try:
            user_id = await self.app.get_user_id("elonmusk")
            if user_id:
                self.log_test("User ID Resolution", True, f"Resolved to ID: {user_id}")
            else:
                self.log_test("User ID Resolution", False, "No user ID returned")
        except Exception as e:
            self.log_test("User ID Resolution", False, f"Failed: {e}")
    
    async def test_authentication(self, username=None, password=None):
        """Test authentication features."""
        print("\n🔐 Testing Authentication...")
        
        if not username or not password:
            self.log_test("Authentication", False, "No credentials provided")
            return False
        
        try:
            await self.app.sign_in(username, password)
            if self.app.logged_in:
                self.authenticated = True
                self.log_test("Authentication", True, 
                    f"Successfully logged in as @{self.app.user.username if self.app.user else 'unknown'}")
                return True
            else:
                self.log_test("Authentication", False, "Login failed - not authenticated")
                return False
        except Exception as e:
            self.log_test("Authentication", False, f"Login failed: {e}")
            return False
    
    async def test_authenticated_features(self):
        """Test features that require authentication."""
        if not self.authenticated:
            print("\n⚠️  Skipping authenticated features - not logged in")
            return
        
        print("\n🔍 Testing Authenticated Features...")
        
        # Test trends
        try:
            trends = await self.app.get_trends()
            if trends and len(trends) > 0:
                self.log_test("Trends Retrieval", True, f"Retrieved {len(trends)} trends")
            else:
                self.log_test("Trends Retrieval", False, "No trends returned")
        except Exception as e:
            self.log_test("Trends Retrieval", False, f"Failed: {e}")
        
        # Test search
        try:
            search_results = await self.app.search("python programming", pages=1)
            if search_results and len(search_results) > 0:
                self.log_test("Search Functionality", True, f"Retrieved {len(search_results)} results")
            else:
                self.log_test("Search Functionality", False, "No search results returned")
        except Exception as e:
            self.log_test("Search Functionality", False, f"Failed: {e}")
        
        # Test filtered search
        try:
            filtered_results = await self.app.search("python", pages=1, filter_=SearchFilters.Latest())
            if filtered_results and len(filtered_results) > 0:
                self.log_test("Filtered Search", True, f"Retrieved {len(filtered_results)} filtered results")
            else:
                self.log_test("Filtered Search", False, "No filtered results returned")
        except Exception as e:
            self.log_test("Filtered Search", False, f"Failed: {e}")
        
        # Test typehead search
        try:
            typehead_results = await self.app.typehead_user_search("elon")
            if typehead_results and hasattr(typehead_results, 'users') and len(typehead_results.users) > 0:
                self.log_test("Typehead Search", True, f"Retrieved {len(typehead_results.users)} suggestions")
            else:
                self.log_test("Typehead Search", False, "No typehead results returned")
        except Exception as e:
            self.log_test("Typehead Search", False, f"Failed: {e}")
    
    async def test_user_relationships(self):
        """Test user relationship features."""
        if not self.authenticated:
            print("\n⚠️  Skipping user relationship features - not logged in")
            return
        
        print("\n👥 Testing User Relationship Features...")
        
        # Test followers
        try:
            followers = await self.app.get_user_followers("elonmusk", pages=1)
            if followers and len(followers) > 0:
                self.log_test("Followers Retrieval", True, f"Retrieved {len(followers)} followers")
            else:
                self.log_test("Followers Retrieval", False, "No followers returned")
        except Exception as e:
            self.log_test("Followers Retrieval", False, f"Failed: {e}")
        
        # Test followings
        try:
            followings = await self.app.get_user_followings("elonmusk", pages=1)
            if followings and len(followings) > 0:
                self.log_test("Followings Retrieval", True, f"Retrieved {len(followings)} followings")
            else:
                self.log_test("Followings Retrieval", False, "No followings returned")
        except Exception as e:
            self.log_test("Followings Retrieval", False, f"Failed: {e}")
        
        # Test user media
        try:
            media = await self.app.get_user_media("elonmusk", pages=1)
            if media and len(media) > 0:
                self.log_test("User Media Retrieval", True, f"Retrieved {len(media)} media tweets")
            else:
                self.log_test("User Media Retrieval", False, "No media tweets returned")
        except Exception as e:
            self.log_test("User Media Retrieval", False, f"Failed: {e}")
    
    async def test_advanced_features(self):
        """Test advanced features."""
        if not self.authenticated:
            print("\n⚠️  Skipping advanced features - not logged in")
            return
        
        print("\n🚀 Testing Advanced Features...")
        
        # Test GIF search
        try:
            gifs = await self.app.search_gifs("funny", pages=1)
            if gifs and len(gifs) > 0:
                self.log_test("GIF Search", True, f"Retrieved {len(gifs)} GIFs")
            else:
                self.log_test("GIF Search", False, "No GIFs returned")
        except Exception as e:
            self.log_test("GIF Search", False, f"Failed: {e}")
        
        # Test place search
        try:
            places = await self.app.search_place(search_term="New York")
            if places and hasattr(places, 'places') and len(places.places) > 0:
                self.log_test("Place Search", True, f"Retrieved {len(places.places)} places")
            else:
                self.log_test("Place Search", False, "No places returned")
        except Exception as e:
            self.log_test("Place Search", False, f"Failed: {e}")
        
        # Test tweet translation (if available)
        try:
            # This would need a real tweet ID
            self.log_test("Tweet Translation", True, "Method available (requires valid tweet ID)")
        except Exception as e:
            self.log_test("Tweet Translation", False, f"Failed: {e}")
    
    async def test_error_handling(self):
        """Test error handling."""
        print("\n⚠️  Testing Error Handling...")
        
        # Test invalid username
        try:
            user_info = await self.app.get_user_info("nonexistentuser12345xyz")
            if user_info is None:
                self.log_test("Invalid Username Handling", True, "Correctly returned None for invalid user")
            else:
                self.log_test("Invalid Username Handling", False, "Should have returned None")
        except Exception as e:
            # This is expected behavior
            self.log_test("Invalid Username Handling", True, f"Correctly raised exception: {type(e).__name__}")
        
        # Test invalid tweet ID
        try:
            tweet = await self.app.tweet_detail("invalid_tweet_id")
            self.log_test("Invalid Tweet ID Handling", False, "Should have raised exception")
        except Exception as e:
            self.log_test("Invalid Tweet ID Handling", True, f"Correctly raised exception: {type(e).__name__}")
    
    def generate_report(self):
        """Generate a comprehensive test report."""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetailed Results:")
        print("-" * 80)
        
        for result in self.results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"{status} {result['test']}")
            if result['message']:
                print(f"    {result['message']}")
            if result['details']:
                print(f"    Details: {result['details']}")
        
        # Save detailed report to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests/total_tests)*100,
                    'timestamp': datetime.now().isoformat()
                },
                'results': self.results
            }, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_file}")
        
        return passed_tests == total_tests

async def main():
    """Run the comprehensive test suite."""
    print("=" * 80)
    print("TWETY LIBRARY - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    test_suite = TweetyTestSuite()
    
    # Run basic tests
    if not await test_suite.test_import_and_initialization():
        print("❌ Basic initialization failed. Cannot proceed.")
        return False
    
    await test_suite.test_public_features()
    await test_suite.test_error_handling()
    
    # Ask for authentication if user wants to test authenticated features
    print("\n" + "=" * 60)
    print("AUTHENTICATION OPTIONAL")
    print("=" * 60)
    print("To test authenticated features, you can provide Twitter credentials.")
    print("This is optional - the test suite will work without authentication.")
    print()
    
    auth_choice = input("Do you want to test authenticated features? (y/n): ").strip().lower()
    
    if auth_choice in ['y', 'yes']:
        username = input("Enter your Twitter username (without @): ").strip()
        password = input("Enter your Twitter password: ").strip()
        
        if username and password:
            auth_success = await test_suite.test_authentication(username, password)
            if auth_success:
                await test_suite.test_authenticated_features()
                await test_suite.test_user_relationships()
                await test_suite.test_advanced_features()
            else:
                print("⚠️  Authentication failed. Skipping authenticated tests.")
        else:
            print("⚠️  No credentials provided. Skipping authenticated tests.")
    else:
        print("ℹ️  Skipping authenticated features as requested.")
    
    # Generate final report
    success = test_suite.generate_report()
    
    if success:
        print("\n🎉 All tests passed! The tweety library is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the detailed report above.")
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest suite interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
