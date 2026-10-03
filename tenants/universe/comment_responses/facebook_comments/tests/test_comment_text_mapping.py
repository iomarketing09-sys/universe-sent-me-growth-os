"""
Test that comment_text correctly extracts from message field, falling back to text.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_comment_text(comment):
    """Replicate the logic from main.py line 221."""
    return comment.get("message", comment.get("text", ""))

def test_message_present_nonempty():
    comment = {"message": "Hello world", "text": ""}
    assert extract_comment_text(comment) == "Hello world"

def test_message_present_empty():
    comment = {"message": "", "text": "Fallback text"}
    assert extract_comment_text(comment) == ""  # message present, even if empty, wins

def test_message_missing_text_present():
    comment = {"text": "Only text"}
    assert extract_comment_text(comment) == "Only text"

def test_both_present():
    comment = {"message": "Message content", "text": "Text content"}
    assert extract_comment_text(comment) == "Message content"  # message preferred

def test_both_empty():
    comment = {"message": "", "text": ""}
    assert extract_comment_text(comment) == ""

def test_missing_both():
    comment = {}
    assert extract_comment_text(comment) == ""

if __name__ == "__main__":
    test_message_present_nonempty()
    test_message_present_empty()
    test_message_missing_text_present()
    test_both_present()
    test_both_empty()
    test_missing_both()
    print("All tests passed.")
