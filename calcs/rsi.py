from typing import Dict, Any
import polars as pl


class Rsi:
    symbol: str = "rsi"
    func_name: str = "rsi"
    name: str = "Relative Strength Index"
    description: str = "The RSI is a momentum oscillator that measures the speed and change of price movements, typically used to identify overbought or oversold conditions."
    simple_example: str = "Use a 14-period RSI to detect overbought conditions (RSI > 70) or oversold conditions (RSI < 30)."

    params_fields: Dict[str, Dict[str, Any]] = {
        "window": {
            "type": int,
            "range": (1, 100),
            "title": "Window Size",
            "description": "The number of periods over which to calculate the RSI."
        }
    }

    identifiers: list[str] = ["rsi", "close", "window"]

    def __init__(self, df: pl.DataFrame, params: Dict[str, Any]) -> pl.Series:
        """
        Initialize the RSI calculation and automatically execute the logic function.
        """
        return self.logic_func(df, params)

    @staticmethod
    def logic_func(df: pl.DataFrame, params: Dict[str, Any]) -> pl.Series:
        """
        Calculate the Relative Strength Index (RSI) using the given DataFrame and parameters.
        """
        try:
            window: int = params["window"]
            delta: pl.Series = df["Close"].diff()
            
            # Calculate gains and losses
            gain: pl.Series = delta.where(delta > 0, 0).fillna(0)
            loss: pl.Series = -delta.where(delta < 0, 0).fillna(0)
            
            # Calculate rolling averages of gains and losses
            avg_gain: pl.Series = gain.rolling_mean(window)
            avg_loss: pl.Series = loss.rolling_mean(window)
            
            # Calculate Relative Strength (RS)
            rs: pl.Series = avg_gain / avg_loss
            
            # Calculate RSI
            rsi: pl.Series = (100 - (100 / (1 + rs))).alias("rsi")
            
            return rsi
        except Exception as e:
            raise ValueError(f"Error in RSI calculation: {e}")

    @staticmethod
    def test_func() -> str:
        """
        Test the RSI calculation using a sample dataset.
        """
        test_df: pl.DataFrame = Rsi.create_test_data()
        params: Dict[str, Any] = {"window": 14}
        rsi_calc = Rsi(test_df, params)  # Automatically calls logic_func
        expected_result = pl.Series("rsi", [None, None, None, None, ...])
        
        # Compare the result to the expected result
        if rsi_calc.frame_equal(pl.DataFrame([expected_result])):
            return "Test passed!"
        else:
            raise AssertionError(f"Expected {expected_result} but got {rsi_calc}")

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

