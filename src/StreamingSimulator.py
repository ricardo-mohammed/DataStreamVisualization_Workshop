import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from IPython.display import clear_output


class StreamingSimulator:

    def __init__(self, file_path, database_url):
        self.df = pd.read_csv(file_path)
        self.current_index = 0
        self.database_url = database_url

    def nextDataPoint(self):
        if self.current_index >= len(self.df):
            return None

        data_point = self.df.iloc[self.current_index]

        self.current_index += 1

        return data_point

    def saveToDatabase(self, data_point):

        # Open a database connection
        engine = create_engine(self.database_url)

        # Convert Series to Python native dictionary, then to DataFrame
        native_dict = {k: (v.item() if hasattr(v, 'item') else v) for k, v in data_point.to_dict().items()}
        record_df = pd.DataFrame([native_dict])

        # Insert the record into PostgreSQL
        record_df.to_sql(
            "robot_stream",
            engine,
            if_exists="append",
            index=False
        )

        # Close the database connection
        engine.dispose()

        print("Record saved to database.")

    def plotDataPoint(self, data_point):

        # Clear the previous chart
        clear_output(wait=True)

        axes = [
            "Axis #1",
            "Axis #2",
            "Axis #3",
            "Axis #4",
            "Axis #5",
            "Axis #6",
            "Axis #7",
            "Axis #8"
        ]

        values = [float(data_point[axis]) for axis in axes]

        plt.figure(figsize=(10, 5))
        plt.bar(axes, values)

        plt.title(
            f"Robot Current - {data_point['Time']}"
        )
        plt.xlabel("Robot Axis")
        plt.ylabel("Current")

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def startStreaming(self, number_of_records=10):
        import time

        for i in range(number_of_records):

            # Get the next record from the CSV
            data_point = self.nextDataPoint()

            if data_point is None:
                print("End of CSV file.")
                break

            # Save the record to PostgreSQL
            self.saveToDatabase(data_point)

            # Plot the current robot data
            self.plotDataPoint(data_point)

            print(f"Streamed record {i + 1}")
            print(f"Time: {data_point['Time']}")

            # Simulate controller reading every 2 seconds
            time.sleep(2)