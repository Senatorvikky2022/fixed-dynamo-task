import json
from pathlib import Path


def test_report_exists():
    """The agent produced a report file."""
    assert Path("/app/report.json").exists(), "no report.json found"


def test_report_nonempty():
    """The report file is not empty."""
    assert Path("/app/report.json").stat().st_size > 0, "report.json is empty"


def test_report_is_valid_json():
    """The report file contains valid JSON."""
    with open("/app/report.json") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "report.json is not valid JSON"


def test_report_has_required_fields():
    """The report contains all required fields."""
    with open("/app/report.json") as f:
        data = json.load(f)
    
    assert "total_requests" in data, "missing total_requests field"
    assert "clients" in data, "missing clients field"
    assert "popular_pages" in data, "missing popular_pages field"


def test_clients_structure():
    """The clients field has the correct structure."""
    with open("/app/report.json") as f:
        data = json.load(f)
    
    clients = data["clients"]
    assert isinstance(clients, list), "clients should be an array"
    
    if len(clients) > 0:
        assert "ip" in clients[0], "client objects should have ip field"
        assert "request_count" in clients[0], "client objects should have request_count field"


def test_popular_pages_structure():
    """The popular_pages field has the correct structure."""
    with open("/app/report.json") as f:
        data = json.load(f)
    
    pages = data["popular_pages"]
    assert isinstance(pages, list), "popular_pages should be an array"
    
    if len(pages) > 0:
        assert "path" in pages[0], "page objects should have path field"
        assert "hit_count" in pages[0], "page objects should have hit_count field"


def test_total_requests_count():
    """The total_requests count is correct."""
    with open("/app/report.json") as f:
        data = json.load(f)
    
    # From the log, there are 6 lines
    assert data["total_requests"] == 6, f"total_requests should be 6, got {data['total_requests']}"


def test_clients_count():
    """The clients array has the correct number of unique IPs."""
    with open("/app/report.json") as f:
        data = json.load(f)
    
    # From the log, there are 3 unique IPs: 192.168.0.1, 192.168.0.2, 10.0.0.5
    assert len(data["clients"]) == 3, f"should have 3 unique clients, got {len(data['clients'])}"


def test_popular_pages_count():
    """The popular_pages array has the correct number of pages."""
    with open("/app/report.json") as f:
        data = json.load(f)
    
    # From the log, there are 3 unique pages: /index.html, /about.html, /api/login
    assert len(data["popular_pages"]) == 3, f"should have 3 unique pages, got {len(data['popular_pages'])}"
