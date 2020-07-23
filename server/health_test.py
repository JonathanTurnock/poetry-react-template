from unittest import TestCase

from server.health import Health, Status


class TestHealth(TestCase):

    def setUp(self) -> None:
        self.health_ok = Health.up()
        self.health_down = Health.down(detail={"error": "EXAMPLE_MSG"})

    def test_up_returns_status_ok(self):
        self.assertEqual(Status.OK, self.health_ok.status)

    def test_up_returns_status_empty_detail(self):
        self.assertEqual({}, self.health_ok.detail)

    def test_down_returns_status_down(self):
        self.assertEqual(Status.DOWN, self.health_down.status)

    def test_down_returns_status_with_detail(self):
        self.assertEqual({"error": "EXAMPLE_MSG"}, self.health_down.detail)
