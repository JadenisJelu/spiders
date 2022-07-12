import config
import logging

log = config.setlogger()

for i in range(10**3):
    log.info(f"data: {i}")