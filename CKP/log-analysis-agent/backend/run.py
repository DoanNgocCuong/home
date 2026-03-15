#!/usr/bin/env python3
"""
Entry point for the Log Analysis Agent.
Run: python run.py
"""
import sys
import os
import logging

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()

    from config.settings import get_config
    config = get_config()

    print(f"""
╔══════════════════════════════════════════════════════╗
║           🔍 Log Analysis Agent v1.0.0              ║
╠══════════════════════════════════════════════════════╣
║  Backend API:  http://localhost:{config.server.port}              ║
║  Dashboard:    Open frontend/index.html in browser  ║
║                                                      ║
║  Datadog:      {'✅ Configured' if config.datadog.api_key else '❌ Not set (using sample data)'}      ║
║  OpenAI:       {'✅ Configured' if config.openai.api_key else '❌ Not set (rule-based mode)'}      ║
║  Cluster:      {config.datadog.cluster_name or 'Not specified'}       ║
╚══════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "api.server:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.debug,
    )
