from nonebot import CommandGroup
__table_args__ = {'extend_existing': True}
__plugin_name__ = '签到'

cg = CommandGroup('rpg')

from . import account, signin
from nana import dt
from . import cg
from . import da
from .helpers import inject_account