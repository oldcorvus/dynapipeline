"""
   Defines stage class  
"""
import asyncio
from typing import Optional

from pydantic import Field

from dynapipeline.pipelines.component import PipelineComponent


class Stage(PipelineComponent):
    """A pipeline stage that can execute a task with an optional timeout"""

    timeout: Optional[float] = Field(
        default=None, description="Timeout in seconds for the stage execution"
    )

    async def run(self, *args, **kwargs):
        """Execute the stage with an optional timeout"""
        try:
            if self.timeout is not None and self.timeout > 0:
                result = await asyncio.wait_for(
                    super().run(*args, **kwargs), timeout=self.timeout
                )
            else:
                result = await super().run(*args, **kwargs)
            return result
        except Exception:
            raise
