import datetime
import time
import pytz


def wait_until_1700():
    # Get the New York time zone
    newyork_tz = pytz.timezone("America/New_York")

    print(
        f"Waiting until 17:00 New York time. Current New York time: {datetime.datetime.now(newyork_tz).strftime('%Y-%m-%d %H:%M:%S')}"
    )

    while True:
        # Get the current time in the New York time zone
        current_time = datetime.datetime.now(newyork_tz).time()

        # Check if it's 17:00:00
        if (
            current_time.hour == 17
            and current_time.minute == 50
            and current_time.second == 0
        ):
            break

        # Sleep for 1 second
        time.sleep(1)

    print("It's 17:00 New York time now!")


# Call the function to wait until 17:00 New York time
wait_until_1700()
