# -*- coding: UTF-8 -*-
from flask import jsonify, request
from sqlalchemy import or_, and_

from . import api_doc_mark_entity as blue_print
from ..models import DocMarkEntity
from .. import db
from .utils import success_res, fail_res
import time

# doc_mark_entity表中删除了entity_type、entity_type_id字段，添加了paragraph_index字段

# 按id查询
@blue_print.route('/get_doc_mark_entity_by_id', methods=['GET'])
def get_doc_mark_entity_by_id():
    try:
        id = request.args.get("id", 0, type=int)
        doc_mark_entity = DocMarkEntity.query.filter_by(id=id, valid=1).first()
        if doc_mark_entity:
            res = success_res({
                "id": doc_mark_entity.id,
                "doc_id": doc_mark_entity.doc_id,
                "word": doc_mark_entity.word,
                "entity_id": doc_mark_entity.entity_id,
                "source": doc_mark_entity.source,
                "create_by": doc_mark_entity.create_by,
                "create_time": doc_mark_entity.create_time.strftime("%Y--%m--%d %H:%M:%S") if doc_mark_entity.create_time else None,
                "update_by": doc_mark_entity.update_by,
                "update_time": doc_mark_entity.update_time.strftime("%Y--%m--%d %H:%M:%S") if doc_mark_entity.update_time else None,
                "paragraph_index": doc_mark_entity.paragraph_index,
                "appear_text": doc_mark_entity.appear_text,
                "appear_index_in_text": doc_mark_entity.appear_index_in_text
            })
        else:
            res = fail_res(msg="实体数据不存在")

    except:
        res = fail_res({
            "id": -1,
            "doc_id": -1,
            "word": "",
            "entity_id": -1,
            "source": -1,
            "create_by": -1,
            "create_time": None,
            "update_by": -1,
            "update_time": None,
            "paragraph_index": -1,
            "appear_text": "",
            "appear_index_in_text": -1
        })

    return jsonify(res)


# 按doc_id查询
@blue_print.route('/get_doc_mark_entity_by_doc_id', methods=['GET'])
def get_doc_mark_entity_by_doc_id():
    try:
        doc_id = request.args.get("doc_id", 0, type=int)
        doc_mark_entity_list = DocMarkEntity.query.filter_by(doc_id=doc_id, valid=1).all()
        if doc_mark_entity_list:
            res = success_res(data=[{
                "id": i.id,
                "doc_id": i.doc_id,
                "word": i.word,
                "entity_id": i.entity_id,
                "source": i.source,
                "create_by": i.create_by,
                "create_time": i.create_time.strftime("%Y--%m--%d %H:%M:%S") if i.create_time else None,
                "update_by": i.create_by,
                "update_time": i.update_time.strftime("%Y--%m--%d %H:%M:%S") if i.update_time else None,
                "paragraph_index": i.paragraph_index,
                "appear_text": i.appear_text,
                "appear_index_in_text": i.appear_index_in_text
            } for i in doc_mark_entity_list])
        else:
            res = fail_res(msg="实体数据不存在")

    except:
        res = fail_res(data=[])

    return jsonify(res)


# add
@blue_print.route('/add_doc_mark_entity', methods=['POST'])
def add_doc_mark_entity():
    try:
        doc_id = request.json.get("doc_id", 0)
        word = request.json.get("word", "")
        entity_id = request.json.get("entity_id", 0)
        source = request.json.get("source", 0)
        create_by = request.json.get("create_by", 0)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        update_by = request.json.get("update_by", 0)
        update_time = request.json.get("update_time", None)
        paragraph_index = request.json.get("paragraph_index", 0)
        appear_text = request.json.get("appear_text", "")
        appear_index_in_text = request.json.get("appear_index_in_text", 0)

        if not (isinstance(doc_id, int) and isinstance(entity_id, int) and isinstance(source, int)
                and isinstance(create_by, int) and isinstance(update_by, int) and isinstance(paragraph_index, int)
                and isinstance(appear_index_in_text, int)):
            res = fail_res(msg="参数 \"doc_id\"、 \"entity_id\"、\"source\"、\"create_by\"、"
                               "\"update_by\"、\"paragraph_index\"和\"appear_index_in_text\"应是整数类型")

        else:
            doc_mark_entity_same = DocMarkEntity.query.filter_by(doc_id=doc_id, word=word,
                                                                 entity_id=entity_id, paragraph_index=paragraph_index,
                                                                 valid=1).first()
            if doc_mark_entity_same:
                res = fail_res(msg="相同标注实体已存在")
            else:
                doc_mark_entity = DocMarkEntity(doc_id=doc_id, word=word, entity_id=entity_id, source=source,
                                                create_by=create_by, create_time=create_time,
                                                update_by=update_by, update_time=update_time,
                                                paragraph_index=paragraph_index, appear_text=appear_text,
                                                appear_index_in_text=appear_index_in_text, valid=1)
                db.session.add(doc_mark_entity)
                db.session.commit()
                res = success_res()

    except:
        res = fail_res()

    return jsonify(res)


# modify
@blue_print.route('/modify_doc_mark_entity', methods=['PUT'])
def modify_doc_mark_entity():
    try:
        id = request.json.get("id", 0)
        doc_id = request.json.get("doc_id", 0)
        word = request.json.get("word", "")
        entity_id = request.json.get("entity_id", 0)
        source = request.json.get("source", 0)
        create_by = request.json.get("create_by", 0)
        create_time = request.json.get("create_time", None)
        update_by = request.json.get("update_by", 0)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        paragraph_index = request.json.get("paragraph_index", 0)
        appear_text = request.json.get("appear_text", "")
        appear_index_in_text = request.json.get("appear_index_in_text", 0)

        if not (isinstance(id, int) and isinstance(doc_id, int) and isinstance(entity_id, int)
                and isinstance(paragraph_index, int) and isinstance(source, int) and isinstance(create_by, int)
                and isinstance(update_by, int) and isinstance(appear_index_in_text, int)):
            res =fail_res(msg="参数 \"id\"、\"doc_id\"、\"entity_id\"、\"paragraph_index\"、"
                              "\"source\"、\"create_by\"、\"update_by\"和\"appear_index_in_text\"应是整数类型")

        else:
            doc_mark_entity_same = DocMarkEntity.query.filter_by(doc_id=doc_id, word=word,
                                                                 entity_id=entity_id, paragraph_index=paragraph_index,
                                                                 valid=1).first()
            if doc_mark_entity_same:
                res = fail_res(msg="相同标注实体已存在")
            else:
                doc_mark_entity = DocMarkEntity.query.filter_by(id=id, valid=1).first()
                if doc_mark_entity:
                    if doc_id:
                        doc_mark_entity.doc_id = doc_id
                    if word:
                        doc_mark_entity.word = word
                    if entity_id:
                        doc_mark_entity.entity_id = entity_id
                    if paragraph_index:
                        doc_mark_entity.entity_type_id = paragraph_index
                    if source:
                        doc_mark_entity.source = source
                    if create_by:
                        doc_mark_entity.creater = create_by
                    if create_time:
                        doc_mark_entity.create_time = create_time
                    if update_by:
                        doc_mark_entity.updater = update_by
                    if update_time:
                        doc_mark_entity.update_time = update_time
                    if paragraph_index:
                        doc_mark_entity.paragraph_index = paragraph_index
                    if appear_text:
                        doc_mark_entity.appear_text = appear_text
                    if appear_index_in_text:
                        doc_mark_entity.appear_index_in_text = appear_index_in_text
                    db.session.commit()
                    res = success_res()
                else:
                    res = fail_res(msg="实体数据不存在")

    except:
        res = fail_res()

    return jsonify(res)


# delete
@blue_print.route('/delete_doc_mark_entity_by_id', methods=['POST'])
def delete_doc_mark_entity_by_id():
    try:
        id = request.json.get("id", 0)
        if isinstance(id, int):
            doc_mark_entity = DocMarkEntity.query.filter_by(id=id, valid=1).first()
            if doc_mark_entity:
                doc_mark_entity.valid = 0
                res = success_res()
            else:
                res = fail_res(msg="实体数据不存在")
        else:
            res = fail_res(msg="参数 \"id\" 应是整数类型")

    except:
        res = fail_res()

    return jsonify(res)
