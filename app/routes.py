import flask
import http


main = flask.Blueprint("main", __name__)


@main.route("/")
def index() -> flask.Response:
    return flask.render_template("index.html")


@main.route("/api/tasks", methods=["GET"])
def get_tasks() -> flask.Response:
    """
    Handle GET requests to fetch all tasks.
    """
    response_data = flask.jsonify(flask.current_app.tasks)
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

    for task in flask.current_app.tasks:
        if new_task["id"] == task["id"]:
            response = flask.make_response(
                {"error": "Task already exists. Use PATCH to update."},
                http.HTTPStatus.CONFLICT
            )
            return response

    flask.current_app.tasks.append(new_task)
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
    task_update = flask.request.get_json()
    task_id = task_update.get("id")

    for task in flask.current_app.tasks:
        if task["id"] == task_id:
            task.update(task_update)
            response = flask.make_response(
                {"message": "Task updated successfully."},
                http.HTTPStatus.OK
            )
            return response

    response = flask.make_response(
        {"error": "Task not found."},
        http.HTTPStatus.NOT_FOUND
    )
    return response


@main.route("/api/tasks", methods=["DELETE"])
def delete_task() -> flask.Response:
    """
    Handle DELETE requests to delete a task.
    """
    task_id = flask.request.args.get("id")

    for idx, task in enumerate(flask.current_app.tasks):
        if task["id"] == task_id:
            flask.current_app.tasks.pop(idx)
            response = flask.make_response(
                {"message": "Task deleted successfully."},
                http.HTTPStatus.OK
            )
            return response

    response = flask.make_response(
        {"error": "Task not found."},
        http.HTTPStatus.NOT_FOUND
    )
    return response
