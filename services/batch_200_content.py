"""
Batch 5 Aggregator - 100 Original Digital SAT Questions
34 Math, 33 Reading, 33 Writing
"""

from typing import Any
from services.batch_200_math import BATCH_5_MATH
from services.batch_200_reading import BATCH_5_READING
from services.batch_200_writing import BATCH_5_WRITING

BATCH_5_ALL_QUESTIONS: list[dict[str, Any]] = BATCH_5_MATH + BATCH_5_READING + BATCH_5_WRITING
