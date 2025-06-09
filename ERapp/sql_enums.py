import enum

class TaskTypeEnum(str, enum.Enum):
	HABIT = 'привычка'
	TODO = 'todo'
	
class CharClassEnum(str, enum.Enum):
	WARRIOR = 'воин'
	MAGE = 'маг'
	