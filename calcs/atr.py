import polars as pl

class ATR:
    symbol = "atr"
    func_name = "atr"
    name = "Average True Range"
    description = "The ATR measures market volatility by decomposing the entire range of an asset price for that period."
    simple_example = "Use a 14-period ATR to measure volatility and identify potential breakout conditions."
    params_fields = {
        "window": {
            "type": int,
            "range": (1, 100),
            "title": "Window Size",
            "description": "The number of periods over which to calculate the ATR."
        }
    }
    identifiers = ["atr", "high", "low", "close", "window"]

    def __init__(self, df, params):
        self.df = df
        self.params = params
        return self.logic_func(df, params)

    @staticmethod
    def logic_func(df, params):
        try:
            window = params["window"]
            tr = pl.max_horizontal(
                df["High"] - df["Low"],
                (df["High"] - df["Close"].shift(1)).abs(),
                (df["Low"] - df["Close"].shift(1)).abs()
            )
            atr = tr.rolling_mean(window)
            return atr
        except Exception as e:
            raise ValueError(f"Error in ATR calculation: {e}")

    @staticmethod
    def test_func():
        test_df = ATR.create_test_data()
        params = {"window": 14}
        atr_calc = ATR(test_df, params)  # Automatically calls logic_func
        expected_result = pl.Series("atr", [None, None, None, ...])
        assert atr_calc.result.frame_equal(pl.DataFrame([expected_result])), f"Expected {expected_result} but got {atr_calc.result}"
        return "Test passed!"

    @staticmethod
    def create_test_data():
        data = {
            "Datetime": ["2024-10-01 09:30:00", "2024-10-01 09:35:00", "2024-10-01 09:40:00", "2024-10-01 09:45:00", "2024-10-01 09:50:00"],
            "Open": [100, 102, 101, 103, 104],
            "High": [102, 103, 102, 105, 106],
            "Low": [99, 101, 100, 102, 103],
            "Close": [101, 102, 101, 104, 105],
            "Volume": [1000, 1500, 1200, 1600, 1700]
        }
        return pl.DataFrame(data).with_column(pl.col("Datetime").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S"))
