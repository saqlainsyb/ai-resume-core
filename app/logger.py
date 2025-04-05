from loguru import logger
import sys

# Configure Loguru logger
logger.remove()  # remove default handler
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="INFO"
)

logger.add(
    "app/logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)
