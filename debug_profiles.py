#!/usr/bin/env python3

import json
from pathlib import Path

def check_user_profiles():
    """Check all user profiles to see what assessments are completed"""
    
    users_dir = Path("data/users")
    print("🔍 Checking all user profiles for assessment data...\n")
    
    total_users = 0
    users_with_assessments = 0
    assessment_counts = {}
    
    for user_dir in users_dir.iterdir():
        if user_dir.is_dir():
            total_users += 1
            profile_path = user_dir / "profile.json"
            
            if profile_path.exists():
                try:
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                    
                    user_name = profile.get('name', 'Unknown')
                    assessments = profile.get('assessments', {})
                    
                    if assessments:
                        users_with_assessments += 1
                        completed_assessments = []
                        
                        for assessment_name, assessment_data in assessments.items():
                            if assessment_data.get('completed', False):
                                completed_assessments.append(assessment_name)
                                
                                # Count each assessment type
                                if assessment_name not in assessment_counts:
                                    assessment_counts[assessment_name] = 0
                                assessment_counts[assessment_name] += 1
                        
                        if completed_assessments:
                            print(f"👤 {user_name} (folder: {user_dir.name})")
                            print(f"   ✅ Completed: {len(completed_assessments)} assessments")
                            for assessment in completed_assessments:
                                print(f"      - {assessment.replace('_', ' ').title()}")
                            print()
                    else:
                        print(f"👤 {user_name} (folder: {user_dir.name})")
                        print(f"   ❌ No assessments completed")
                        print()
                        
                except Exception as e:
                    print(f"❌ Error reading {profile_path}: {e}")
    
    print("=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   Total users: {total_users}")
    print(f"   Users with assessments: {users_with_assessments}")
    print(f"   Users with no assessments: {total_users - users_with_assessments}")
    
    if assessment_counts:
        print(f"\n📈 Assessment completion counts:")
        for assessment, count in sorted(assessment_counts.items()):
            print(f"   {assessment.replace('_', ' ').title()}: {count} users")
    else:
        print(f"\n❌ No completed assessments found in any user profile!")
        
    return assessment_counts

if __name__ == "__main__":
    check_user_profiles()
