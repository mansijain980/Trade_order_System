from django.apps import AppConfig
import multiprocessing
import sys
import logging
from trade_matching_service.management.commands.start_tms import start_tms

logger = logging.getLogger(__name__)

class TmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trade_matching_service'

    def ready(self):
        """Start the TMS system when the Django server starts."""
        if 'runserver' in sys.argv:  # Ensure it only runs with the 'runserver' command
            logger.info("Starting TMS system with multiprocessing")
            
            # Start the TMS processes (order receiver, matching, trade sender)
            tms_process = multiprocessing.Process(target=start_tms)
            tms_process.daemon = False  # Ensures the process terminates when the server stops
            tms_process.start()
