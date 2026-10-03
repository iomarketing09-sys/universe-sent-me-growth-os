#!/usr/bin/env python3
"""
Script to fetch real comments from Facebook Graph API for Universe Sent Me page,
process them with UniverseResponder, and output proposed responses for review.
"""
import os
import sys
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from growth.metrics_snapshot import api_get, get_page_token
from growth.meta_publisher import load_integration_env
from tenants.universe.comment_responses.universe_responder import UniverseResponder
from tenants.universe.comment_responses.parse_real_pubs import parse_publication_contexts_real

def load_env():
    """Load integration environment (Meta credentials)."""
    if not load_integration_env():
        print("Warning: Could not load integration environment. Checking for META_ACCESS_TOKEN and PAGE_ID in os.environ.")
    # Ensure we have the necessary variables
    if not os.environ.get("META_ACCESS_TOKEN"):
        print("Error: META_ACCESS_TOKEN environment variable not set.")
        sys.exit(1)
    if not os.environ.get("PAGE_ID"):
        print("Error: PAGE_ID environment variable not set.")
        sys.exit(1)

def get_post_id_from_url(url):
    """Extract post ID from a Facebook post URL."""
    # Example: https://www.facebook.com/photo/?fbid=122160625695072582&set=a.122095282845072582
    match = re.search(r'fbid=(\d+)', url)
    if match:
        return match.group(1)
    # If not found, try to extract from the path
    # Example: https://www.facebook.com/permalink.php?story_fbid=123&id=456
    match = re.search(r'story_fbid=(\d+)', url)
    if match:
        return match.group(1)
    return None

def get_publication_contexts(fixture_path):
    """Parse the fixture file to get publication contexts."""
    try:
        return parse_publication_contexts_real(fixture_path)
    except Exception as e:
        print(f"Warning: Could not parse fixture file: {e}")
        return []

def find_context_by_post_id(contexts, post_id):
    """Find a publication context by post ID."""
    for ctx in contexts:
        post_url = ctx.get("post_url")
        if post_url:
            ctx_post_id = get_post_id_from_url(post_url)
            if ctx_post_id == post_id:
                return ctx
    return None

def main():
    load_env()
    user_token = os.environ["META_ACCESS_TOKEN"]
    page_id = os.environ["PAGE_ID"]
    
    # Get page access token
    page_token = get_page_token(user_token, page_id)
    if not page_token:
        print("Error: Could not obtain page access token.")
        sys.exit(1)
    
    # Initialize responder
    responder = UniverseResponder()
    
    # Load fixture contexts (optional, for context)
    fixture_path = "../tenants/universe/Coment_Responses_Universe/Publication_Contexts_Real_Universe.md"
    contexts = get_publication_contexts(fixture_path)
    
    # We'll get comments from the most recent post of the page.
    # Alternatively, we can specify a post ID via environment or take the first from fixture.
    # Let's try to get the recent posts for the page and take the first one.
    endpoint = f"{page_id}/posts"
    params = {
        "fields": "id,created_time",
        "limit": 1
    }
    try:
        posts_response = api_get(page_token, endpoint, params)
        posts = posts_response.get("data", [])
        if not posts:
            print("Error: No posts found for the page.")
            sys.exit(1)
        post_id = posts[0]["id"]
        print(f"Using most recent post: {post_id}")
    except Exception as e:
        print(f"Error fetching posts: {e}")
        # Fallback: use the first post from the fixture
        if contexts:
            # Try to get post ID from the first context's post_url
            first_ctx = contexts[0]
            post_url = first_ctx.get("post_url")
            if post_url:
                post_id = get_post_id_from_url(post_url)
                if post_id:
                    print(f"Using post ID from fixture: {post_id}")
                else:
                    print("Error: Could not extract post ID from fixture and failed to fetch posts.")
                    sys.exit(1)
            else:
                print("Error: No post URL in fixture and failed to fetch posts.")
                sys.exit(1)
        else:
            print("Error: No contexts in fixture and failed to fetch posts.")
            sys.exit(1)
    
    # Get comments for this post
    endpoint = f"{post_id}/comments"
    params = {
        "fields": "id,from,message,created_time",
        "limit": 50  # Adjust as needed
    }
    try:
        comments_response = api_get(page_token, endpoint, params)
        comments = comments_response.get("data", [])
        print(f"Fetched {len(comments)} comments.")
    except Exception as e:
        print(f"Error fetching comments: {e}")
        sys.exit(1)
    
    # Process each comment
    for comment in comments:
        comment_id = comment.get("id")
        comment_from = comment.get("from", {})
        comment_from_id = comment_from.get("id")
        comment_message = comment.get("message", "")
        comment_created_time = comment.get("created_time")
        
        # Check OWN_PAGE: if comment.from.id == PAGE_ID
        if comment_from_id == page_id:
            print(f"\nComment ID: {comment_id}")
            print(f"Comment: {comment_message}")
            print("-> OWN_PAGE (excluded)")
            continue
        
        # Check NO_TEXT: if message is empty or exactly "(No text)" ignoring spaces
        stripped = comment_message.strip()
        if stripped == "" or stripped.lower() == "(no text)":
            print(f"\nComment ID: {comment_id}")
            print(f"Comment: {comment_message}")
            print("-> NO_TEXT (excluded)")
            continue
        
        # Find publication context for this post (from fixture)
        context = find_context_by_post_id(contexts, post_id)
        if not context:
            # If not found in fixture, use a minimal context (could be empty)
            print(f"\nComment ID: {comment_id}")
            print(f"Comment: {comment_message}")
            print("-> Warning: No publication context found in fixture. Using empty context.")
            context = {
                "publication_id": post_id,
                "published_at": None,
                "asset_ref": None,
                "post_url": f"https://www.facebook.com/{post_id}",
                "character": "",
                "visual_context": "",
                "meme_text": "",
                "caption": ""
            }
        
        # Call the responder
        try:
            result = responder.respond(context, comment_message)
        except Exception as e:
            print(f"\nComment ID: {comment_id}")
            print(f"Comment: {comment_message}")
            print(f"-> Error processing comment: {e}")
            continue
        
        # Output the result
        print("\n" + "="*50)
        print(f"Comment ID: {comment_id}")
        print(f"Comment: {comment_message}")
        print(f"Published at: {comment_created_time}")
        print(f"Publication ID: {result.get('publication_id')}")
        print(f"Comment Type: {result.get('comment_type')}")
        print(f"Relation to Meme: {result.get('relation_to_meme')}")
        print(f"Apparent Intent: {result.get('apparent_intent')}")
        print(f"Decision: {result.get('decision')}")
        print(f"Response: {result.get('response')}")
        print(f"Risk Level: {result.get('risk_level')}")
        if "review_reason" in result:
            print(f"Review Reason: {result.get('review_reason')}")
        print("="*50)
    
    print(f"\nProcessed {len(comments)} comments.")

if __name__ == "__main__":
    main()
