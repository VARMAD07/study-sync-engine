class EventBroker:
    _instance = None

    def __new__(cls):
        """Implementing Singleton Pattern so all modules share the exact same broker instance."""
        if cls._instance is None:
            cls._instance = super(EventBroker, cls).__new__(cls)
            cls._instance.subscribers = {}
        return cls._instance

    def subscribe(self, event_type, callback):
        """Registers a function to listen for a specific system event."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, data):
        """Broadcasts data to all listening components instantly."""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"[BROKER ERROR] Failed to route event: {str(e)}")