from langsmith import Client
from datetime import datetime
import pytz
from utils.logger import logger

# Initialize Langsmith client
ls_client = Client()


def send_feedback(run_id, score):
    """Send feedback to Langsmith."""
    try:
        tz = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(tz).isoformat()
        ls_client.create_feedback(
            run_id=run_id,
            key="user-score",
            score=score
        )
        logger.info(f"Feedback sent successfully to Langsmith for run_id={
                    run_id} with score={score}. Current time={current_time}")
    except Exception as e:
        logger.error(f"Error sending feedback: {e}")
