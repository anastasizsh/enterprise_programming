from typing import NewType, Literal

UserId = NewType('UserId', int)
TaskId = NewType('TaskId', int)
ProjectId = NewType('ProjectId', int)

TaskStatus = Literal["new", "in_progress", "done"]