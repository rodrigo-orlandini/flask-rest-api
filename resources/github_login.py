from flask import request, url_for, g
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from oa import github

from models.user import UserModel

class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(url_for("github.authorize", _external=True))

class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()
        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args.get("error"),
                "error_description": request.args.get("error_description")
            }
            return error_response

        g.access_token = resp.get("access_token")
        github_user = github.get("user")
        github_username = github.user.data.get("login")
        
        user = UserModel.find_by_username(github_username)
        if not user:
            user = UserModel(username=github_user, password=None)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200