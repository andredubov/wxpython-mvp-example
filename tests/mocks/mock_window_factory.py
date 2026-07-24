from app.interface import WindowFactoryInterface
from tests.mocks import MockCounterView
from tests.mocks import MockLogView

class MockWindowFactory(WindowFactoryInterface):

    def create_counter_view(self, parent, title):
        return MockCounterView()

    def create_log_view(self, parent, title):
        return MockLogView()