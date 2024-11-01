from typing import Dict, Any
import polars as pl


class Macd:
    symbol: str = "macd"
    func_name: str = "macd"
    name: str = "Moving Average Convergence Divergence"
    description: str = "MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price."
    simple_example: str = "Use MACD (12, 26, 9) to identify potential buy or sell signals based on the crossover between MACD and its signal line."
    
    params_fields: Dict[str, Dict[str, Any]] = {
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

    identifiers: list[str] = ["macd", "fast_period", "slow_period", "signal_period"]

    def __init__(self, df: pl.DataFrame, params: Dict[str, Any]) -> pl.Series:
        """
        Initialize the MACD calculation and automatically execute the logic function.
        """
        return self.logic_func(df, params)

    @staticmethod
    def logic_func(df: pl.DataFrame, params: Dict[str, Any]) -> pl.Series:
        """
        Calculate the Moving Average Convergence Divergence (MACD) using the given DataFrame and parameters.
        """
        try:
            fast_period: int = params["fast_period"]
            slow_period: int = params["slow_period"]
            signal_period: int = params["signal_period"]
            
            # Calculate fast and slow moving averages
            fast_ma: pl.Series = df["Close"].rolling_mean(fast_period)
            slow_ma: pl.Series = df["Close"].rolling_mean(slow_period)
            
            # Calculate MACD line and signal line
            macd_line: pl.Series = (fast_ma - slow_ma).alias("macd_line")
            signal_line: pl.Series = macd_line.rolling_mean(signal_period).alias("signal_line")
            
            # Calculate MACD histogram
            macd_histogram: pl.Series = (macd_line - signal_line).alias("macd_histogram")
            
            return macd_histogram
        except Exception as e:
            raise ValueError(f"Error in MACD calculation: {e}")

    @staticmethod
    def test_func() -> str:
        """
        Test the MACD calculation using a sample dataset.
        """
        test_df: pl.DataFrame = Macd.create_test_data()
        params: Dict[str, Any] = {"fast_period": 12, "slow_period": 26, "signal_period": 9}
        macd_calc = Macd(test_df, params)  # Automatically calls logic_func
        expected_result = pl.Series("macd_histogram", [None, None, None, ...])
        
        # Compare the result to the expected result
        if macd_calc.frame_equal(pl.DataFrame([expected_result])):
            return "Test passed!"
        else:
            raise AssertionError(f"Expected {expected_result} but got {macd_calc}")

    @staticmethod
    def create_test_data() -> pl.DataFrame:
        """
        Create sample OHLCV data for testing.
        """
        data = {
            "Datetime": ["2024-10-01 09:30:00", "2024-10-01 09:35:00", "2024-10-01 09:40:00", "2024-10-01 09:45:00", "2024-10-01 09:50:00"],
            "Open": [100, 102, 101, 103, 104],
            "High": [102, 103, 102, 105, 106],
            "Low": [99, 101, 100, 102, 103],
            "Close": [101, 102, 101, 104, 105],
            "Volume": [1000, 1500, 1200, 1600, 1700]
        }
        # Create a DataFrame and parse the datetime column
        return pl.DataFrame(data).with_column(pl.col("Datetime").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S"))
