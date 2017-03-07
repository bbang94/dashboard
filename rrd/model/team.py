#-*- coding:utf-8 -*-
import json
from rrd import corelib
from rrd import config
from rrd.model.user import User

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

class Team(object):
    def __init__(self, id, name, resume, creator, users=[]):
        self.id = id
        self.name = name
        self.resume = resume
        self.creator = creator
        self.users = users

    def __repr__(self):
        return "<Team id=%s, name=%s>" % (self.id, self.name)
    __str__ = __repr__

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'resume': self.resume,
            'creator': self.creator,
            "users": self.users,
        }


    @classmethod
    def get_team_users(cls, team_id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", "%s/team/%s" \
                %(config.API_ADDR, team_id), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.json()

    @classmethod
    def get_teams(cls, query_term, limit=20, page=1):
        if not query_term:
            query_term = "."

        d = {
            "q": query_term,
            "limit": limit,
            "page": page,
        }
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("GET", "%s/team" \
                %(config.API_ADDR,), params=d, headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))

        teams = []
        for j in r.json():
            users = [User(x["id"], x["name"], x["cnname"], x["email"], x["phone"], x["im"], x["qq"], x["role"]) for x in j['users']]
            t = Team(j["team"]["id"], j["team"]["name"], j["team"]["resume"], j['creator_name'], users)
            teams.append(t)

        return teams

    @classmethod
    def create_team(cls, name, resume, user_ids=[]):
        h = {"Content-type": "application/json"}
        d = {
            "team_name": name, "resume": resume, "users": user_ids,
        }
        r = corelib.auth_requests("POST", "%s/team" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text

    @classmethod
    def update_team(cls, team_id, resume, user_ids=[]):
        h = {"Content-type": "application/json"}
        d = {
            "team_id": team_id, "resume": resume, "users": user_ids,
        }
        r = corelib.auth_requests("PUT", "%s/team" %(config.API_ADDR,), \
                data=json.dumps(d), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text

    @classmethod
    def delete_team(cls, team_id):
        h = {"Content-type": "application/json"}
        r = corelib.auth_requests("DELETE", "%s/team/%s" \
                %(config.API_ADDR, team_id), headers=h)
        log.debug("%s:%s" %(r.status_code, r.text))

        if r.status_code != 200:
            raise Exception("%s %s" %(r.status_code, r.text))
        return r.text
