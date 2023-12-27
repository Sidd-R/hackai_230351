from uagents import Model
from pydantic import Field
from typing import TextIO



class CentralMessage(Model):
  type: int
  # file: TextIO | None
  titleOption: int | None
  compareOption: int | None
