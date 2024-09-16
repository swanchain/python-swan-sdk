class Task:
    def __init__(self):
        self.task_uuid = None
        self.tx_hash = None
        self.instance_type = None
        self.price = None
        self.config_order = None
        self.status = None
        self.created_at = None
        self.start_at = None
        self.end_at = None
        self.job_source_uri = None
        self.wallet_address = None
        self._data = None

    def load_from_data(self, data):
        task_data = data.get('data', {}).get('task', {})
        task_detail = task_data.get('task_detail', {})
        config_order = data.get('config_order', {})

        self.task_uuid = task_data.get('uuid')
        self.tx_hash = data.get('tx_hash')
        self.instance_type = task_detail.get('hardware')
        self.price = task_detail.get('price_per_hour')
        self.config_order = config_order
        self.status = task_data.get('status')
        self.created_at = task_data.get('created_at')
        self.start_at = task_detail.get('start_at')
        self.end_at = task_detail.get('end_at')
        self.job_source_uri = task_detail.get('job_source_uri')
        self.wallet_address = task_data.get('refund_wallet')

        self._data = data

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"Key {key} not found in Task attributes")

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __repr__(self):
        return (f"Task(task_uuid={self.task_uuid}, tx_hash={self.tx_hash}, instance_type={self.instance_type}, "
                f"price={self.price}, config_order={self.config_order}, status={self.status}, "
                f"created_at={self.created_at}, start_at={self.start_at}, end_at={self.end_at}, "
                f"job_source_uri={self.job_source_uri}, wallet_address={self.wallet_address})")