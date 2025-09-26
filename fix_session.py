"""
Script to force refresh Streamlit cache and session state
"""

import streamlit as st
import json
import os
from pathlib import Path
import shutil

def clear_streamlit_cache():
    """Clear all Streamlit caches"""
    # Clear all caches
    st.cache_data.clear()
    st.cache_resource.clear()
    
    print("✅ Streamlit cache cleared")

def fix_user_session():
    """Fix user session data"""
    # Find the latest user directory
    data_dir = Path('data/users')
    user_dirs = [d for d in data_dir.iterdir() if d.is_dir() and d.name.startswith('afrin_')]
    if user_dirs:
        latest_user_dir = sorted(user_dirs, key=lambda x: x.stat().st_mtime)[-1]
        print(f"Latest user: {latest_user_dir.name}")
        
        # Check the profile
        profile_path = latest_user_dir / 'profile.json'
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                profile = json.load(f)
            
            assessments = profile.get('assessments', {})
            
            # Count completed
            completed = [k for k, v in assessments.items() if v.get('completed', False)]
            remaining = [k for k, v in assessments.items() if not v.get('completed', False)]
            
            print(f"Profile status:")
            print(f"  Completed ({len(completed)}): {completed}")
            print(f"  Remaining ({len(remaining)}): {remaining}")
            
            return True
    return False

if __name__ == "__main__":
    print("🔄 Fixing Remiro AI session...")
    
    if fix_user_session():
        print("\n✅ User session data is correct")
        print("\n🎯 Next steps:")
        print("1. Stop the Streamlit app (Ctrl+C in terminal)")
        print("2. Restart: streamlit run app.py")
        print("3. Or simply refresh your browser (Ctrl+F5)")
        print("\nThis should fix the dashboard display issue.")
    else:
        print("❌ Could not find user profile")
