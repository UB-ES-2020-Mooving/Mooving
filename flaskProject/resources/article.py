from flask_restful import Resource, reqparse
from models.article_model import ArticleModel


class ArticlesList(Resource):
    def get(self):
        #Solo devuelve los articulos visibles
        articles = ArticleModel.query.filter_by().all()
        data={"articles":[]}
        for a in articles:
            if a.visible:
                data["articles"].append(a.json())
        return data, 200
