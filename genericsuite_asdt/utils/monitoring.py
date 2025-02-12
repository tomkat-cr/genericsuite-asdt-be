"""
Monitoring tools
"""
import os
from dotenv import load_dotenv

from genericsuite_asdt.utils.app_logger import log_debug, log_error

DEBUG = True

load_dotenv()


class MonitoringTools:
    """
    Monitoring tools
    """

    def __init__(self):
        """
        Initializes the MonitoringTools object
        """
        self.monitoring_app_name = os.environ.get('MONITORING_APP_NAME')
        self.error_message = None

        self.monitoring_app_enabled = False
        if self.monitoring_app_name:
            self.monitoring_app_enabled = True

    def is_monitoring_app_enabled(self):
        return self.monitoring_app_enabled

    def get_monitoring_app_name(self):
        return self.monitoring_app_name

    def get_error_message(self):
        return self.error_message

    def init_monitoring(self):
        if self.is_monitoring_app_enabled():
            if self.get_monitoring_app_name() == "openlit":
                self.init_openlit()
            elif self.get_monitoring_app_name() == "agentops":
                self.init_agentops()
            else:
                self.error_message = "[DISABLED] Monitoring app " \
                    f"'{self.get_monitoring_app_name()}' " \
                    "could not be initialized because it is not supported"
                _ = DEBUG and log_error(self.error_message)
        else:
            _ = DEBUG and log_debug("[DISABLED] Monitoring app not enabled")

    def init_openlit(self):
        """
        Monitoring with OpenLit

        Requirements:
        pip install openlit

        Documentation:
        https://docs.crewai.com/how-to/openlit-observability
        """
        if not os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT'):
            self.error_message = "[DISABLED] OpenLit could not be " \
                "initialized because OTEL_EXPORTER_OTLP_ENDPOINT is not set"
            _ = DEBUG and log_error(self.error_message)
            return

        _ = DEBUG and log_debug("Initializing OpenLit...")
        try:
            import openlit
        except Exception as e:
            self.error_message = f"OpenLit could not be initialized: {e}"
            _ = DEBUG and log_error(self.error_message)
            return
        openlit.init()
        _ = DEBUG and log_debug("OpenLit initialized")

    def init_agentops(self):
        """
        Monitoring with AgentOps

        Requirements:
        pip install 'crewai[tools,agentops]'

        Documentation:
        https://docs.crewai.com/how-to/agentops-observability
        """
        if not os.environ.get('AGENTOPS_API_KEY'):
            self.error_message = "[DISABLED] AgentOps could not be " \
                "initialized because AGENTOPS_API_KEY is not set"
            _ = DEBUG and log_error(self.error_message)
            return

        _ = DEBUG and log_debug("Initializing AgentOps...")
        try:
            import agentops
        except Exception as e:
            self.error_message = f"AgentOps could not be initialized: {e}"
            _ = DEBUG and log_error(self.error_message)
            return
        agentops.init()
        _ = DEBUG and log_debug("AgentOps initialized")
