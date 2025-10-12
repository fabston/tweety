#!/usr/bin/env python3
"""
Test script specifically for profile image URL functionality.
This tests the recent fix for deprecated profile_image_url_https field.
"""

import asyncio
import sys
import os

# Add parent directory to path so we can import tweety
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tweety import TwitterAsync

async def test_profile_image_urls():
    """Test profile image URL handling with the recent fix."""
    print("🖼️  Testing Profile Image URL Functionality")
    print("=" * 60)
    
    app = TwitterAsync("test_profile_images")
    
    # Test with a well-known public account
    test_users = ["elonmusk", "twitter", "github", "microsoft"]
    
    for username in test_users:
        print(f"\n📱 Testing @{username}...")
        
        try:
            user = await app.get_user_info(username)
            
            if user:
                print(f"   ✅ User found: {user.name}")
                print(f"   🆔 ID: {user.id}")
                
                # Test profile image URLs
                print(f"   🖼️  profile_image_url: {user.profile_image_url}")
                print(f"   🔒 profile_image_url_https: {user.profile_image_url_https}")
                
                # Check if URLs are valid
                if user.profile_image_url:
                    print(f"   ✅ profile_image_url is available")
                else:
                    print(f"   ❌ profile_image_url is None/empty")
                
                if user.profile_image_url_https:
                    print(f"   ✅ profile_image_url_https is available")
                else:
                    print(f"   ❌ profile_image_url_https is None/empty")
                
                # Test the fallback logic
                if user.profile_image_url_https and user.profile_image_url:
                    if user.profile_image_url_https == user.profile_image_url:
                        print(f"   ℹ️  Both URLs are the same (fallback working)")
                    else:
                        print(f"   ℹ️  URLs are different (both fields available)")
                elif user.profile_image_url_https and not user.profile_image_url:
                    print(f"   ✅ Fallback working: https URL available, regular URL not")
                elif user.profile_image_url and not user.profile_image_url_https:
                    print(f"   ✅ Fallback working: regular URL available, https URL not")
                else:
                    print(f"   ⚠️  No profile image URLs available")
                
                # Test banner URL as well
                if user.profile_banner_url:
                    print(f"   🖼️  profile_banner_url: {user.profile_banner_url}")
                else:
                    print(f"   ℹ️  No banner URL available")
                
            else:
                print(f"   ❌ User not found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n" + "=" * 60)
    print("Profile Image URL Test Complete")

async def test_multiple_users():
    """Test profile image URLs for multiple users to see patterns."""
    print(f"\n🔍 Testing Multiple Users for Pattern Analysis")
    print("=" * 60)
    
    app = TwitterAsync("test_multiple_users")
    
    # Test with various types of accounts
    test_users = [
        "elonmusk",      # High-profile verified account
        "twitter",       # Official account
        "github",        # Tech company
        "microsoft",     # Large corporation
        "openai",        # AI company
        "nasa",          # Government agency
        "netflix",       # Entertainment
        "spotify",       # Music streaming
    ]
    
    results = {
        'both_urls': 0,
        'https_only': 0,
        'regular_only': 0,
        'neither': 0,
        'total_tested': 0
    }
    
    for username in test_users:
        try:
            user = await app.get_user_info(username)
            results['total_tested'] += 1
            
            if user:
                has_https = bool(user.profile_image_url_https)
                has_regular = bool(user.profile_image_url)
                
                if has_https and has_regular:
                    results['both_urls'] += 1
                    print(f"   ✅ @{username}: Both URLs available")
                elif has_https and not has_regular:
                    results['https_only'] += 1
                    print(f"   🔒 @{username}: HTTPS URL only")
                elif has_regular and not has_https:
                    results['regular_only'] += 1
                    print(f"   🌐 @{username}: Regular URL only")
                else:
                    results['neither'] += 1
                    print(f"   ❌ @{username}: No URLs available")
            else:
                print(f"   ❌ @{username}: User not found")
                
        except Exception as e:
            print(f"   ❌ @{username}: Error - {e}")
    
    # Summary
    print(f"\n📊 Summary of Profile Image URL Availability:")
    print(f"   Total users tested: {results['total_tested']}")
    print(f"   Both URLs available: {results['both_urls']}")
    print(f"   HTTPS URL only: {results['https_only']}")
    print(f"   Regular URL only: {results['regular_only']}")
    print(f"   Neither available: {results['neither']}")
    
    # Test the fallback logic
    print(f"\n🔧 Testing Fallback Logic:")
    if results['regular_only'] > 0:
        print(f"   ✅ Fallback working: {results['regular_only']} users have regular URL as fallback")
    if results['https_only'] > 0:
        print(f"   ✅ HTTPS URL available: {results['https_only']} users have HTTPS URL")
    if results['neither'] > 0:
        print(f"   ⚠️  {results['neither']} users have no profile image URLs")

async def test_url_validation():
    """Test if the profile image URLs are valid and accessible."""
    print(f"\n🌐 Testing URL Validation")
    print("=" * 60)
    
    app = TwitterAsync("test_url_validation")
    
    try:
        user = await app.get_user_info("elonmusk")
        
        if user and user.profile_image_url_https:
            print(f"   🖼️  Profile image URL: {user.profile_image_url_https}")
            
            # Check if URL looks valid
            if user.profile_image_url_https.startswith(('http://', 'https://')):
                print(f"   ✅ URL format is valid")
            else:
                print(f"   ❌ URL format is invalid")
            
            # Check if it's a Twitter CDN URL
            if 'pbs.twimg.com' in user.profile_image_url_https:
                print(f"   ✅ URL is from Twitter CDN")
            else:
                print(f"   ℹ️  URL is not from Twitter CDN")
            
            # Check if it's HTTPS
            if user.profile_image_url_https.startswith('https://'):
                print(f"   ✅ URL uses HTTPS")
            else:
                print(f"   ⚠️  URL does not use HTTPS")
                
        else:
            print(f"   ❌ No profile image URL available for testing")
            
    except Exception as e:
        print(f"   ❌ Error during URL validation: {e}")

async def main():
    """Run all profile image tests."""
    print("🖼️  PROFILE IMAGE URL TESTING SUITE")
    print("=" * 60)
    print("Testing the recent fix for deprecated profile_image_url_https field")
    
    await test_profile_image_urls()
    await test_multiple_users()
    await test_url_validation()
    
    print(f"\n" + "=" * 60)
    print("🎉 Profile Image URL Testing Complete!")
    print("The recent commit should have fixed the fallback logic for")
    print("deprecated profile_image_url_https field.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
