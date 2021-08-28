import requests
import pytest


class TestUserAgent:
    user_agent_data = [
    {
        "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "platform": "Mobile",
        "browser": "No",
        "device": "Android"},
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "platform": "Mobile",
        "browser": "Chrome",
        "device": "iOS"},
    {
        "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "platform": "Googlebot",
        "browser": "Unknown",
        "device": "Unknown"},
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "platform": "Web",
        "browser": "Chrome",
        "device": "No"},
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "platform": "Mobile",
        "browser": "No",
        "device": "iPhone"}
    ]
    @pytest.mark.parametrize("user_agent_data", user_agent_data)
    def test_user_agent(self, user_agent_data):
        user_agent = user_agent_data["user_agent"]
        expected_device = user_agent_data["device"]
        expected_browser = user_agent_data["browser"]
        expected_platform = user_agent_data["platform"]
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers={"User-Agent": user_agent})

        device = response.json()["device"]
        browser = response.json()["browser"]
        platform = response.json()["platform"]
        print(device, browser, platform)

        assert expected_device == device, f"Incorrect: Actual device '{device}' instead of expected device '{expected_device}'"
        assert expected_browser == browser, f"Incorrect: Actual browser '{browser}' instead of expected browser '{expected_browser}'"
        assert expected_platform == platform, f"Incorrect: Actual platform '{platform}' instead of expected platform '{expected_platform}'"