from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Board, Column

@receiver(post_save, sender=Project)
def create_board_for_project(sender, instance, created, **kwargs):
    if created:
        # Create a board for the new project
        board = Board.objects.create(project=instance)
        
        # Create default columns
        Column.objects.create(board=board, name="To Do", order=1)
        Column.objects.create(board=board, name="In Progress", order=2)
        Column.objects.create(board=board, name="Done", order=3)
