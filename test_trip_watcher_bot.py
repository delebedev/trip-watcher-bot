import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from trip_watcher_bot import match_destination, parse_feed, send_message

class TestTripWatcherBot(unittest.TestCase):
    
    def test_match_destination(self):
        self.assertTrue(match_destination("Cheap flights to Tokyo"))
        self.assertTrue(match_destination("Visit Seoul this summer"))
        self.assertFalse(match_destination("Explore Paris"))
        self.assertFalse(match_destination("London calling"))

    @patch('requests.post')
    def test_send_message(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        send_message("test_channel", "Test message")

        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_message_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad Request"}
        mock_post.return_value = mock_response

        with self.assertLogs(level='ERROR') as cm:
            send_message("test_channel", "Error message")
        self.assertIn("Error sending message", cm.output[0])

    @patch('feedparser.parse')
    @patch('trip_watcher_bot.send_message')
    def test_parse_feed(self, mock_send_message, mock_parse):
        mock_entry = MagicMock()
        mock_entry.title = "Cheap flights to Tokyo"
        mock_entry.published = datetime.now(timezone.utc).isoformat()
        mock_entry.link = "http://example.com"

        mock_feed = MagicMock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed

        parse_feed("http://test-feed.com")
        mock_send_message.assert_called_once()

        # Test with non-matching destination
        mock_entry.title = "Explore Paris"
        parse_feed("http://test-feed.com")
        mock_send_message.assert_called_once()  # Should not be called again

if __name__ == '__main__':
    unittest.main()
