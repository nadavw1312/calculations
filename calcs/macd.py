import polars as pl

class MACD:
    symbol = "macd"
    func_name = "macd"
    name = "Moving Average Convergence Divergence"
    description = "MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price."
    simple_example = "Use MACD (12, 26, 9) to identify potential buy or sell signals based on the crossover between MACD and its signal line."
    params_fields = {
        "fast_period": {
            "type": int,
            "range": (1, 100),
            "title": "Fast Period",
            "description": "The number of periods for the fast moving average."
        },
        "slow_period": {
            "type": int,
            "range": (1, 100),
            "title": "Slow Period",
            "description": "The number of periods for the slow moving average."
        },
        "signal_period": {
            "type": int,
            "range": (1, 100),
            "title": "Signal Period",
            "description": "The number of periods for the signal line."
        }
    }
    identifiers = ["macd", "fast_period", "slow_period", "signal_period"]

    def __init__(self, df, params):
        self.df = df
        self.params = params
        return self.logic_func(df, params)


    @staticmethod
    def logic_func(df, params):
        try:
            fast_period = params["fast_period"]
            slow_period = params["slow_period"]
            signal_period = params["signal_period"]
            fast_ma = df["Close"].rolling_mean(fast_period)
            slow_ma = df["Close"].rolling_mean(slow_period)
            macd_line = fast_ma - slow_ma
            signal_line = macd_line.rolling_mean(signal_period)
            macd_histogram = macd_line - signal_line
            return macd_histogram
        except Exception as e:
            raise ValueError(f"Error in MACD calculation: {e}")

    @staticmethod
    def test_func():
        test_df = MACD.create_test_data()
        params = {"fast_period": 12, "slow_period": 26, "signal_period": 9}
        macd_calc = MACD(test_df, params)  # Automatically calls logic_func
        expected_result = pl.Series("macd_histogram", [None, None, None, ...])
        assert macd_calc.result.frame_equal(pl.DataFrame([expected_result])), f"Expected {expected_result} but got {macd_calc.result}"
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
