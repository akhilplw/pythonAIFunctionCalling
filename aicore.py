from ai_core_sdk.ai_core_v2_client import AICoreV2Client

import os


def create_ai_core_client(credCF):
    os.environ["AICORE_CLIENT_ID"] = credCF["SAP_AI_CORE"]["AICORE_CLIENT_ID"]
    os.environ["AICORE_BASE_URL"] = credCF["SAP_AI_CORE"]["AICORE_BASE_URL"]
    os.environ["AICORE_AUTH_URL"] = credCF["SAP_AI_CORE"]["AICORE_AUTH_URL"]
    os.environ["AICORE_CLIENT_SECRET"] = credCF["SAP_AI_CORE"]["AICORE_CLIENT_SECRET"]
    os.environ["AICORE_RESOURCE_GROUP"] = credCF["SAP_AI_CORE"]["AICORE_RESOURCE_GROUP"]
    return AICoreV2Client(
        base_url=os.environ['AICORE_BASE_URL'],
        auth_url=os.environ['AICORE_AUTH_URL'],
        client_id=os.environ['AICORE_CLIENT_ID'],
        client_secret=os.environ['AICORE_CLIENT_SECRET'],
        resource_group=os.environ['AICORE_RESOURCE_GROUP']
    )


