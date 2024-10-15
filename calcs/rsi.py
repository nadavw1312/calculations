import polars as pl

class RSI:
    symbol = "rsi"
    func_name = "rsi"
    name = "Relative Strength Index"
    description = "The RSI is a momentum oscillator that measures the speed and change of price movements, typically used to identify overbought or oversold conditions."
    simple_example = "Use a 14-period RSI to detect overbought conditions (RSI > 70) or oversold conditions (RSI < 30)."
    params_fields = {
        "window": {
            "type": int,
            "range": (1, 100),
            "title": "Window Size",
            "description": "The number of periods over which to calculate the RSI."
        }
    }
    identifiers = ["rsi", "close", "window"]

    def __init__(self, df, params):
        self.df = df
        self.params = params
        return self.logic_func(df, params)

    @staticmethod
    def logic_func(df, params):
        try:
            window = params["window"]
            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).fillna(0)
            loss = (-delta.where(delta < 0, 0)).fillna(0)
            avg_gain = gain.rolling_mean(window)
            avg_loss = loss.rolling_mean(window)
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            raise ValueError(f"Error in RSI calculation: {e}")

    @staticmethod
    def test_func():
        test_df = RSI.create_test_data()
        params = {"window": 14}
        rsi_calc = RSI(test_df, params)  # Automatically calls logic_func
        expected_result = pl.Series("rsi", [None, None, None, None, ...])
        assert rsi_calc.result.frame_equal(pl.DataFrame([expected_result])), f"Expected {expected_result} but got {rsi_calc.result}"
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
