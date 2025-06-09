import enum

class TaskTypeEnum(str, enum.Enum):
	HABIT = 'привычка'
	TODO = 'todo'
	
class CharClassEnum(str, enum.Enum):
	WARRIOR = 'воин'
	MAGE = 'маг'

class ExpRewardEnum(int, enum.Enum):
	LOW = 10
	MEDIUM = 15
	HIGH = 20

class GoldRewardEnum(int, enum.Enum):
	LOW = 5
	MEDIUM = 8
	HIGH = 10

class TaskDiffName(str, enum.Enum):
	LOW = 'LOW'
	MEDIUM = 'MEDIUM'
	HIGH = 'HIGH'