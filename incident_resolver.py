"""
AIOps Incident Knowledge Base - Auto-Resolution System
Uses Microsoft Fabric preprocessed data + Azure AI Search
"""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json

# ===== CONFIGURATION =====
SEARCH_SERVICE_NAME = "incidenthandling-ai-search"
SEARCH_ADMIN_KEY = "fFC0ONuC0wKym1cwXjBqkaYBn84a0uI0C4u8n4q1UTAzSeBLWdKP"  
INDEX_NAME = "incidents-kb"
SEARCH_ENDPOINT = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"

# ===== INITIALIZE CLIENT =====
credential = AzureKeyCredential(SEARCH_ADMIN_KEY)
search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=credential
)

# ===== CONNECTION TEST =====
def test_connection():
    """Test connection to Azure AI Search"""
    print("\n" + "="*70)
    print("🔍 TESTING CONNECTION TO AZURE AI SEARCH")
    print("="*70)
    
    try:
        # Try a simple search
        results = search_client.search(search_text="test", top=1)
        result_list = list(results)
        
        print(f"✅ Connection successful!")
        print(f"🌐 Endpoint: {SEARCH_ENDPOINT}")
        print(f"📊 Index: {INDEX_NAME}")
        print(f"✓ Search service is responding")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed!")
        print(f"Error: {str(e)}")
        print(f"\n💡 Troubleshooting:")
        print(f"1. Check your SEARCH_ADMIN_KEY is correct")
        print(f"2. Verify index name: {INDEX_NAME}")
        print(f"3. Ensure Azure AI Search service is running")
        return False

# ===== SEARCH FUNCTION =====
def search_incident(user_description, top_results=3):
    """Search for similar incidents based on user description"""
    
    try:
        results = search_client.search(
            search_text=user_description,
            top=top_results,
            select=["ticket_id", "description", "service_category", "root_cause", 
                    "resolution_steps", "resolution_summary", "kb_article_id"]
        )
        
        return list(results)
    
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return []

# ===== DISPLAY RESULTS =====
def display_results(user_input, results):
    """Display search results in a clean format"""
    
    print("\n" + "="*70)
    print("🔍 INCIDENT ANALYSIS")
    print("="*70)
    print(f"\n📝 Your Issue: {user_input}")
    
    if not results:
        print("\n❌ No matching incidents found in knowledge base.")
        return
    
    # Show best match (first result)
    best_match = results[0]
    
    print("\n" + "="*70)
    print("✅ RECOMMENDED SOLUTION (Best Match)")
    print("="*70)
    print(f"\n📋 Ticket Reference: {best_match['ticket_id']}")
    print(f"📂 Service Category: {best_match['service_category']}")
    print(f"🔍 Root Cause: {best_match['root_cause']}")
    print(f"📖 KB Article: {best_match['kb_article_id']}")
    
    print(f"\n💡 Resolution Steps:")
    print(f"   {best_match['resolution_steps']}")
    
    print(f"\n📄 Summary:")
    print(f"   {best_match['resolution_summary']}")
    
    # Show additional similar incidents if any
    if len(results) > 1:
        print("\n" + "="*70)
        print("📚 OTHER SIMILAR INCIDENTS:")
        print("="*70)
        
        for i, result in enumerate(results[1:], 2):
            print(f"\n{i}. {result['ticket_id']}")
            print(f"   Category: {result['service_category']}")
            print(f"   Root Cause: {result['root_cause']}")
            print(f"   KB: {result['kb_article_id']}")

# ===== INTERACTIVE MODE =====
def interactive_mode():
    """Run interactive query mode"""
    
    print("\n" + "="*70)
    print("🤖 AIOps INCIDENT AUTO-RESOLVER - INTERACTIVE MODE")
    print("="*70)
    print("\nType 'quit' or 'exit' to stop\n")
    
    while True:
        user_input = input("🎤 Describe your issue: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thank you for using AIOps Incident Resolver!")
            break
        
        if not user_input:
            print("⚠️ Please enter a description")
            continue
        
        results = search_incident(user_input, top_results=3)
        display_results(user_input, results)
        print("\n" + "-"*70 + "\n")

# ===== BATCH TEST MODE =====
def batch_test_mode(test_cases):
    """Run batch tests with predefined queries"""
    
    print("\n" + "="*70)
    print("🧪 RUNNING BATCH TESTS")
    print("="*70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n{'#'*70}")
        print(f"TEST CASE {i}/{len(test_cases)}")
        print(f"{'#'*70}")
        
        results = search_incident(test_case, top_results=3)
        display_results(test_case, results)
        
        input("\nPress Enter to continue to next test...")

# ===== SAMPLE TEST CASES =====
SAMPLE_TEST_CASES = [
    "VPN keeps asking for password and won't connect",
    "Outlook inbox not loading, application freezing",
    "Getting certificate error when opening internal website",
    "Teams meeting stuck on connecting screen",
    "Cannot access SharePoint files, getting access denied",
    "Printer not working, documents stuck in queue",
    "Application crashes after recent update",
    "Disk space alert, system running out of storage",
    "MFA authentication failing during login",
    "Email bouncing back with delivery errors"
]

# ===== MAIN FUNCTION =====
def main():
    """Main entry point"""
    
    print("\n" + "="*70)
    print("🚀 AIOps INCIDENT AUTO-RESOLVER")
    print("="*70)
    print("\nProject: Knowledge Fabric Setup & Auto-Resolve Incidents")
    print("Technology Stack: Microsoft Fabric + Azure AI Search")
    print("="*70)
    
    # Test connection first
    if not test_connection():
        print("\n❌ Cannot proceed without connection. Please fix the issues above.")
        return
    
    # Show menu
    print("\n" + "="*70)
    print("SELECT MODE:")
    print("="*70)
    print("1. Interactive Mode - Enter your own incident descriptions")
    print("2. Batch Test Mode - Run 10 predefined test cases")
    print("3. Single Query Test")
    print("4. View Sample Test Cases")
    print("5. Exit")
    print("="*70)
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        interactive_mode()
    
    elif choice == "2":
        batch_test_mode(SAMPLE_TEST_CASES)
    
    elif choice == "3":
        test_query = input("\n🎤 Enter incident description: ").strip()
        if test_query:
            results = search_incident(test_query, top_results=3)
            display_results(test_query, results)
    
    elif choice == "4":
        print("\n" + "="*70)
        print("📋 SAMPLE TEST CASES:")
        print("="*70)
        for i, case in enumerate(SAMPLE_TEST_CASES, 1):
            print(f"{i:2d}. {case}")
        print("\nYou can use these in Interactive Mode or run Batch Test Mode!")
    
    elif choice == "5":
        print("\n👋 Goodbye!")
    
    else:
        print("\n⚠️ Invalid choice. Please run the script again.")

# ===== RUN =====
if __name__ == "__main__":
    main()