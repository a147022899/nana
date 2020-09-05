"""
A note taking plugin.

This plugin stores notes separately for every single context,
which means none.helpers.context_id() are used to generate a
global unique id to identify who is one note belonging to.
"""

import asyncio
import re

from nonebot import CommandSession, CommandGroup
from nonebot.command import call_command
from nonebot.helpers import context_id, render_expression as expr

from nana import nlp
from nana.command import allow_cancellation
from nana.db import db
from . import expressions as e
from .models import Note

__plugin_name__ = '笔记本'

note = CommandGroup('note')


async def note_count(ctx_id: str) -> int:
    return await db.select([db.func.count(Note.id)]).where(
        Note.context_id == ctx_id).gino.scalar()


@note.command('add', aliases=('记录', '记笔记', '添加笔记'))
async def note_add(session: CommandSession):
    content = session.get('content', prompt=expr(e.ADD_WHAT_CONTENT))
    new_note = await Note.create(
        content=content, context_id=context_id(session.ctx))
    await session.send(expr(e.ADD_SUCCESS,
                            id=new_note.id, content=new_note.content))


@note.command('list', aliases=('查看记录', '查看笔记', '所有笔记'))
async def _(session: CommandSession):
    count = await note_count(context_id(session.ctx))
    if count == 0:
        await session.send(expr(e.LIST_EMPTY))
        return

    all_notes = await Note.query.where(
        Note.context_id == context_id(session.ctx)).gino.all()
    for n in all_notes:
        await session.send(f'ID：{n.id}\r\n内容：{n.content}')
        await asyncio.sleep(0.8)
    await session.send(expr(e.LIST_COMPLETE, count=count))


@note.command('remove', aliases=('删除记录', '删除笔记'))
async def note_remove(session: CommandSession):
    ctx_id = context_id(session.ctx)
    count = await note_count(ctx_id)
    if count == 0:
        await session.send(expr(e.LIST_EMPTY))
        return

    id_ = session.get('id', prompt=expr(e.DEL_WHICH_ID))
    note_ = await Note.query.where(
        (Note.context_id == ctx_id) & (Note.id == id_)).gino.first()
    if note_ is None:
        await session.send(expr(e.DEL_ID_NOT_EXISTS, id=id_))
    else:
        await note_.delete()
        await session.send(expr(e.DEL_SUCCESS,
                                id=id_, content=note_.content))


@note_add.args_parser
@allow_cancellation
async def _(session: CommandSession):
    if not session.current_key and session.current_arg.strip():
        session.state['content'] = session.current_arg
    else:
        session.state[session.current_key] = session.current_arg


@note_remove.args_parser
@allow_cancellation
async def _(session: CommandSession):
    text = session.current_arg_text.strip()

    if session.is_first_run and text:
        # first run, and there is an argument, we take it as the id
        session.current_key = 'id'

    if session.current_key == 'id':
        id_ = None
        try:
            # try parse the text message as an id
            id_ = int(text)
        except ValueError:
            # it's not directly a number
            if not session.is_first_run:
                # we are in and interactive session, do nlp

                # user may want to ask for all notes, check it
                match_score = await nlp.sentence_similarity(
                    session.current_arg_text.strip(), '现在有哪些呢？')
                if match_score > 0.70:
                    # we think it matches
                    await session.send(expr(e.QUERYING_ALL))
                    # sleep to make conversation natural :)
                    await asyncio.sleep(1)
                    await call_command(
                        session.bot, session.ctx,
                        ('note', 'list'),
                        check_perm=False,
                        disable_interaction=True
                    )

                    # pause the session and wait for further interaction
                    await session.pause()
                    return

                # user may also put the id in a natural sentence, check it
                m = re.search(r'\d+', text)
                if m:
                    possible_id = int(m.group(0))
                    match_score = await nlp.sentence_similarity(
                        session.current_arg_text.strip(),
                        f'删掉笔记{possible_id}')
                    if match_score > 0.70:
                        # we think it matches
                        id_ = possible_id
        if id_ is not None:
            session.state['id'] = id_
        else:
            session.pause(expr(e.DEL_CANNOT_RECOGNIZE_ID))
