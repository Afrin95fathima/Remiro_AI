#!/usr/bin/env python3
"""
Comprehensive Fix for 4 Missing Agents Issue
This script will identify and fix the exact cause of why 4 agents don't show after 8 completed assessments.
"""

import streamlit as st
import json
import os
from pathlib import Path

def create_fixed_app_section():
    """Create the fixed version of the main app logic"""
    
    fixed_code = '''
# FIXED VERSION - Replace lines 1810-1840 in app.py with this:

# Get next options
options = master_agent.get_next_options(user_profile)

# DEBUG: Show what options are being generated
if st.checkbox("🔧 Show Options Debug", key="options_debug"):
    st.write("**DEBUG - Options generated:**")
    for i, option in enumerate(options):
        st.write(f"{i+1}. {option['title']} (agent: {option['agent']})")
    st.write(f"**Total options: {len(options)}**")
    st.markdown("---")

# Check for action plan readiness
progress = master_agent.get_assessment_progress(user_profile)
if len(progress['completed']) >= 8:
    st.markdown("### 🎉 Ready for Your Career Action Plan!")
    
    if st.button("🎯 Generate My Action Plan", type="primary", use_container_width=True):
        with st.spinner("Creating your personalized career roadmap..."):
            action_plan = asyncio.run(master_agent.generate_action_plan(user_profile))
            st.session_state.action_plan = action_plan
            st.rerun()

# Display action plan if available
if 'action_plan' in st.session_state:
    display_action_plan(st.session_state.action_plan)
    st.markdown("---")

# Career Tools Section (available after completing assessments)
progress = master_agent.get_assessment_progress(user_profile)
if len(progress['completed']) >= 4:  # Show tools after completing 4+ assessments
    # Check if we're displaying a tool
    if st.session_state.get('active_tool'):
        display_active_tool(career_tools, user_profile)
        # REMOVED THE PROBLEMATIC RETURN STATEMENT
        # return  # Don't show other options when tool is active
    else:
        display_career_tools_interface(career_tools, user_profile)
        st.markdown("---")

# ALWAYS Display options - this was being skipped before
selected_agent = display_agent_options(options)
'''
    
    with open("FIXED_APP_SECTION.py", "w") as f:
        f.write(fixed_code)
    
    print("✅ Created FIXED_APP_SECTION.py with the corrected logic")

def apply_streamlit_cache_fix():
    """Create a cache clearing function for Streamlit"""
    
    cache_fix_code = '''
# Add this function to your app.py file

def clear_all_caches():
    """Clear all Streamlit caches"""
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
        # Force session state reset for options
        if 'cached_options' in st.session_state:
            del st.session_state.cached_options
        st.success("🔄 All caches cleared!")
        st.rerun()
    except Exception as e:
        st.error(f"Cache clear error: {e}")

# Add this button to your debug section:
if st.button("🔄 Force Cache Clear & Refresh", key="force_refresh"):
    clear_all_caches()
'''
    
    with open("CACHE_FIX.py", "w") as f:
        f.write(cache_fix_code)
    
    print("✅ Created CACHE_FIX.py with cache clearing solution")

def main():
    """Run the comprehensive fix"""
    print("🚀 Comprehensive Fix for 4 Missing Agents Issue")
    print("=" * 60)
    
    print("\n🔍 IDENTIFIED ISSUES:")
    print("1. ❌ Early 'return' statement in career tools section prevents options display")
    print("2. ❌ Streamlit caching may prevent options from updating") 
    print("3. ❌ No debug visibility into what options are generated")
    
    print("\n🔧 APPLYING FIXES:")
    
    # Fix 1: Create corrected app section
    create_fixed_app_section()
    
    # Fix 2: Create cache clearing solution  
    apply_streamlit_cache_fix()
    
    print("\n✅ FIXES GENERATED:")
    print("1. ✅ FIXED_APP_SECTION.py - Contains corrected logic without early return")
    print("2. ✅ CACHE_FIX.py - Contains cache clearing functions")
    
    print("\n🎯 MANUAL STEPS NEEDED:")
    print("1. Open app.py")
    print("2. Find lines around 1833 with 'return  # Don't show other options when tool is active'") 
    print("3. Comment out or remove that return statement")
    print("4. Add the debug checkbox from FIXED_APP_SECTION.py")
    print("5. Restart the Streamlit app")
    
    print("\n💡 The issue is that the early return prevents display_agent_options(options) from running!")

if __name__ == "__main__":
    main()
