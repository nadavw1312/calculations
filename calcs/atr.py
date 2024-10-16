from typing import Dict, Any
import polars as pl


class Atr:
    symbol: str = "atr"
    func_name: str = "atr"
    name: str = "Average True Range"
    description: str = "The ATR measures market volatility by decomposing the entire range of an asset price for that period."
    simple_example: str = "Use a 14-period ATR to measure volatility and identify potential breakout conditions."
    
    params_fields: Dict[str, Dict[str, Any]] = {
        "window": {
            "type": int,
            "range": (1, 100),
            "title": "Window Size",
            "description": "The number of periods over which to calculate the ATR."
        }
    }

    identifiers: list[str] = ["atr", "high", "low", "close", "window"]

    def __init__(self, df: pl.DataFrame, params: Dict[str, Any]) -> pl.Series:
        """
        Initialize the ATR calculation and automatically execute the logic function.
        """
        self.df = df
        self.params = params
        return self.logic_func(df, params)

    @staticmethod
    def logic_func(df: pl.DataFrame, params: Dict[str, Any]) -> pl.Series:
        """
        Calculate the Average True Range (ATR) using the given DataFrame and parameters.
        """
        try:
            window: int = params["window"]
            # Calculate the True Range (TR)
            tr: pl.Series = pl.max_horizontal(
                df["High"] - df["Low"],
                (df["High"] - df["Close"].shift(1)).abs(),
                (df["Low"] - df["Close"].shift(1)).abs()
            )
            # Calculate the rolling ATR
            atr: pl.Series = tr.rolling_mean(window).alias("atr")
            return atr
        except Exception as e:
            raise ValueError(f"Error in ATR calculation: {e}")

    @staticmethod
    def test_func() -> str:
        """
        Test the ATR calculation using a sample dataset.
        """
        test_df: pl.DataFrame = Atr.create_test_data()
        params: Dict[str, Any] = {"window": 14}
        atr_calc = Atr(test_df, params)  # Automatically calls logic_func
        expected_result = pl.Series("atr", [None, None, None, ...])
        
        # Compare the result to the expected result
        if atr_calc.frame_equal(pl.DataFrame([expected_result])):
            return "Test passed!"
        else:
            raise AssertionError(f"Expected {expected_result} but got {atr_calc}")

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

