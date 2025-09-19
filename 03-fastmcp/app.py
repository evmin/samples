"""FastMCP timezone tool application."""
import json
import sys
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import asyncio

from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Annotated

mcp = FastMCP("Time Operator")

class TimezoneRequest(BaseModel):
    """Pydantic model for timezone request parameters."""
    
    timezone: str = Field(
        description="The name of the timezone for which the time is requested "
                   "in format 'Continent/City'. For example, 'Australia/Sydney'."
    )

@mcp.tool(name="time_for_timezone", description="Get the current time for a specific timezone.")
async def time_for_timezone(timezone: str, ctx: Context) -> str:
    """
    A function that returns the current time for a specific timezone.

    Args:
        timezone: The timezone for which to retrieve the current time.

    Returns:
        str: The current time in the specified timezone.
    """
     # Send logs (visible in capable clients)
    await ctx.info(f"Working on {timezone}")
    sys.stdout.write(f"Request for : {timezone}\n")
    sys.stdout.flush()

    range_count = 100
    
    # Emit periodic progress updates (these go over SSE if the client provided a progressToken)
    for i in range(range_count):
        sys.stdout.write(f"{i}\n")
        sys.stdout.flush()
        await ctx.report_progress(progress=i, total=range_count)  # keeps activity flowing
        await asyncio.sleep(5)

    now = datetime.now(ZoneInfo(timezone))
    await ctx.report_progress(progress=range_count, total=range_count)
    sys.stdout.write(f"Final - {range_count} - responding.\n")
    sys.stdout.flush()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)