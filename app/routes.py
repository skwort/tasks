import flask
import http
import sqlalchemy
from .db import Task


main = flask.Blueprint("main", __name__)


def get_tasks_by_category(category: str):
    stmt = sqlalchemy.select(Task)
    stmt = stmt.where(Task.category == category).order_by(Task.category_rank)
    return list(flask.current_app.db_session.scalars(stmt))


def get_task_by_id(id: int):
    stmt = sqlalchemy.select(Task)
    stmt = stmt.where(Task.id == id)
    return flask.current_app.db_session.scalar(stmt)


@main.route("/")
def index() -> flask.Response:

    must_do = get_tasks_by_category("must-do")
    should_do = get_tasks_by_category("should-do")
    will_do = get_tasks_by_category("will-do")
    unsched = get_tasks_by_category("unsched")

    return flask.render_template(
        "index.html",
        must_do=must_do,
        should_do=should_do,
        will_do=will_do,
        unsched=unsched)


@main.route("/api/tasks", methods=["GET"])
def get_tasks() -> flask.Response:
    """
    Handle GET requests to fetch all tasks.
    """
    stmt = sqlalchemy.select(Task)
    tasks = flask.current_app.db_session.scalars(stmt)
    tasks = [t.to_dict() for t in tasks]

    response_data = flask.jsonify(tasks)
    response = flask.make_response(
        response_data,
        http.HTTPStatus.OK
    )
    return response


@main.route("/api/tasks", methods=["POST"])
def create_task() -> flask.Response:
    """
    Handle POST requests to create a new task.
    """
    new_task = flask.request.get_json()

    task = get_task_by_id(int(new_task["id"]))
    if task is not None:
        response = flask.make_response(
            {"error": "Task already exists. Use PATCH to update."},
            http.HTTPStatus.CONFLICT
        )
        return response

    task = Task(
        id=int(new_task["id"]),
        category=new_task["category"],
        category_rank=int(new_task["category_rank"]),
        title=new_task["title"],
        body=new_task["body"]
    )
    flask.current_app.db_session.add(task)
    flask.current_app.db_session.commit()

    response = flask.make_response(
        {"message": "Task created successfully."},
        http.HTTPStatus.CREATED
    )
    return response


@main.route("/api/tasks", methods=["PATCH"])
def update_task() -> flask.Response:
    """
    Handle PATCH requests to update a task.
    """
    new_task = flask.request.get_json()

    print(new_task)

    task = get_task_by_id(int(new_task["id"]))
    if task is None:
        response = flask.make_response(
            {"error": "Task not found."},
            http.HTTPStatus.NOT_FOUND
        )
        return response

    category = new_task.get("category")
    if category is not None:
        task.category = category

    category_rank = new_task.get("category_rank")
    if category_rank is not None:
        print(new_task["id"], category_rank)
        task.category_rank = int(category_rank)

    title = new_task.get("title")
    if title is not None:
        task.title = title

    body = new_task.get("body")
    if body is not None:
        task.body = body

    flask.current_app.db_session.commit()

    response = flask.make_response(
        {"message": "Task updated successfully."},
        http.HTTPStatus.OK
    )
    return response


@main.route("/api/tasks", methods=["DELETE"])
def delete_task() -> flask.Response:
    """
    Handle DELETE requests to delete a task.
    """
    task_id = flask.request.args.get("id")

    task = get_task_by_id(int(task_id))
    if task is None:
        response = flask.make_response(
            {"error": "Task not found."},
            http.HTTPStatus.NOT_FOUND
        )
        return response

    flask.current_app.db_session.delete(task)
    flask.current_app.db_session.commit()
    response = flask.make_response(
        {"message": "Task deleted successfully."},
        http.HTTPStatus.OK
    )
    return response
