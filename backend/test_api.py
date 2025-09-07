#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Domain Progress Tracker API
"""

import requests
import json

def test_api():
    """Test các API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Domain Progress Tracker API...")
    print("=" * 50)
    
    # Test 1: Get domains
    print("\n1. Testing GET /api/domains")
    try:
        response = requests.get(f"{base_url}/api/domains")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   Found {data['count']} domains")
            
            # Hiển thị chi tiết từng domain
            for domain_name, domain_data in data['domains'].items():
                print(f"   📁 {domain_name}:")
                print(f"      Level: {domain_data['level']}")
                print(f"      XP: {domain_data['xp']}")
                print(f"      Articles: {domain_data['taskCount']}")
                print(f"      Streak: {domain_data['streakDays']} days")
                print(f"      Color: {domain_data['color']}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test 2: Get stats
    print("\n2. Testing GET /api/domains/stats")
    try:
        response = requests.get(f"{base_url}/api/domains/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            stats = data['stats']
            print(f"   Total domains: {stats['total_domains']}")
            print(f"   Total articles: {stats['total_articles']}")
            print(f"   Total XP: {stats['total_xp']}")
            print(f"   Average level: {stats['average_level']:.1f}")
            
            if stats['highest_level_domain']:
                highest = stats['highest_level_domain']
                print(f"   Highest level: {highest[0]} (Level {highest[1]['level']})")
            
            if stats['most_articles_domain']:
                most = stats['most_articles_domain']
                print(f"   Most articles: {most[0]} ({most[1]['taskCount']} articles)")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test 3: Refresh domains
    print("\n3. Testing POST /api/domains/refresh")
    try:
        response = requests.post(f"{base_url}/api/domains/refresh")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   Refreshed {data['count']} domains")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")

if __name__ == "__main__":
    test_api()
