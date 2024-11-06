class ActionsService:
    def get_all_personal_actions(self):
        # Here you could get actions from a database or API,
        # but for now, let's use a list of actions.
        personal_actions = [
            {
                "name": "CADCHF",
                "description": "Canadian Dollar vs Swiss Franc.",
                "sell": 0.62979,
                "buy": 0.6301,
                "change": ((0.6301 - 0.62979) / 0.62979) * 100,
            },
            {
                "name": "CADJPY",
                "description": "Canadian Dollar vs Japanese Yen.",
                "sell": 110.776,
                "buy": 110.806,
                "change": ((110.806 - 110.776) / 110.776) * 100,
            },
            {
                "name": "CHFJPY",
                "description": "Swiss Franc vs Japanese Yen.",
                "sell": 175.861,
                "buy": 175.882,
                "change": ((175.882 - 175.861) / 175.861) * 100,
            },
            {
                "name": "EURUSD",
                "description": "Euro vs US Dollar. A widely traded currency pair.",
                "sell": 1.11234,
                "buy": 1.11256,
                "change": ((1.11256 - 1.11234) / 1.11234) * 100,
            },
            {
                "name": "GBPUSD",
                "description": "British Pound vs US Dollar. A popular pair for traders.",
                "sell": 1.29843,
                "buy": 1.29878,
                "change": ((1.29878 - 1.29843) / 1.29843) * 100,
            },
            {
                "name": "AUDUSD",
                "description": "Australian Dollar vs US Dollar. Known for volatility.",
                "sell": 0.74792,
                "buy": 0.74815,
                "change": ((0.74815 - 0.74792) / 0.74792) * 100,
            },
            {
                "name": "USDJPY",
                "description": "US Dollar vs Japanese Yen. A major pair for trading.",
                "sell": 110.423,
                "buy": 110.456,
                "change": ((110.456 - 110.423) / 110.423) * 100,
            },
            {
                "name": "NZDUSD",
                "description": "New Zealand Dollar vs US Dollar. Often traded for volatility.",
                "sell": 0.66912,
                "buy": 0.66945,
                "change": ((0.66945 - 0.66912) / 0.66912) * 100,
            },
            {
                "name": "EURGBP",
                "description": "Euro vs British Pound. A key pair for European traders.",
                "sell": 0.85642,
                "buy": 0.85660,
                "change": ((0.85660 - 0.85642) / 0.85642) * 100,
            },
            {
                "name": "USDCAD",
                "description": "US Dollar vs Canadian Dollar. A solid pair with strong liquidity.",
                "sell": 1.32744,
                "buy": 1.32768,
                "change": ((1.32768 - 1.32744) / 1.32744) * 100,
            },
        ]

        return personal_actions

    def get_all_available_actions(self):
        # List of actions with only buy price data (sell price is omitted for simplicity)
        all_actions = [
            {
                "name": "CADCHF",
                "description": "Canadian Dollar vs Swiss Franc.",
                "buy": 0.6301,
            },
            {
                "name": "CADJPY",
                "description": "Canadian Dollar vs Japanese Yen.",
                "buy": 110.806,
            },
            {
                "name": "CHFJPY",
                "description": "Swiss Franc vs Japanese Yen.",
                "buy": 175.882,
            },
            {
                "name": "EURUSD",
                "description": "Euro vs US Dollar. A widely traded currency pair.",
                "buy": 1.11256,
            },
            {
                "name": "GBPUSD",
                "description": "British Pound vs US Dollar. A popular pair for traders.",
                "buy": 1.29878,
            },
            # Other actions...
        ]

        return all_actions
