import typer
from services.task_service import TaskService
from database.database import SessionLocal
from schemas.task import CreateDto
from uuid import UUID

cli = typer.Typer()


@cli.command()
def create(
        name: str = typer.Option(..., "-name", "-n", "-task-name")
):
    with SessionLocal() as db:
        TaskService(db).create_task(payload=CreateDto(
            name=name
        ))
    typer.echo(f"Была создана задача под названием {name}")


@cli.command()
def get_all():
    with SessionLocal() as db:
        response = TaskService(db).get_all_tasks()
    tasks = response.tasks
    answer = ""
    for task in tasks:
        answer += f"id: {task.id}, name: {task.name}, state: {task.state}\n"
    typer.echo(f"Список задач:\n{answer}")


@cli.command()
def get_by_id(task_id: UUID = typer.Option(..., "-id")):
    with SessionLocal() as db:
        response = TaskService(db).get_task_by_id(task_id)
    task = response.info
    if not task:
        typer.echo("Задача не найдена")
    typer.echo(f"id: {task.id}, name: {task.name}, state: {task.state}")


@cli.command()
def change_state(task_id: UUID = typer.Option(..., "-id")):
    with SessionLocal() as db:
        response = TaskService(db).put_task(task_id)
    task = response.info
    typer.echo(f"Изменения успешно применились.\nid: {task.id}, name: {task.name}, state: {task.state}")


@cli.command()
def delete_task(task_id: UUID = typer.Option(..., "-id")):
    with SessionLocal() as db:
        TaskService(db).delete_task(task_id)
    typer.echo("Задача была успешно удалена")


if __name__ == "__main__":
    cli()
