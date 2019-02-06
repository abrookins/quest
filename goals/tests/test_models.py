import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from goals.models import Goal, TaskStatus


class TestGoal(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pass')
        self.test_file = SimpleUploadedFile('test.png', b'')

    def test_has_name(self):
        goal = Goal(name="The name")
        expected = "The name"
        assert expected == goal.name

    def test_required_fields(self):
        goal = Goal(name="The name", description="The description",
                    image=self.test_file, slug="the-slug",)
        expected = None
        assert expected == goal.clean_fields()

    def test_has_description(self):
        goal = Goal(description="The description")
        expected = "The description"
        assert expected == goal.description

    def test_has_image(self):
        goal = Goal.objects.create(name="The name", description="The description",
                                   image=self.test_file)
        assert "test" in goal.image.file.name

        # Clean up the copy of the image file
        goal.image.delete()

    def test_has_slug(self):
        goal = Goal(slug="the-slug")
        expected = "the-slug"
        assert expected == goal.slug

    def test_percentage_complete_with_some_items_completed(self):
        goal = Goal.objects.create(name="Django")
        goal.tasks.create(name="Item 1")
        item_two = goal.tasks.create(name="Item 2")
        item_two.complete(self.user)
        assert goal.percentage_complete(self.user) == 50

    def test_percentage_complete_with_zero_items_completed(self):
        goal = Goal.objects.create(name="Django")
        goal.tasks.create(name="Item 1")
        assert goal.percentage_complete(self.user) == 0

    def test_percentage_complete_with_all_items_completed(self):
        goal = Goal.objects.create(name="Django")
        task = goal.tasks.create(name="Item 1")
        task.complete(self.user)
        assert goal.percentage_complete(self.user) == 100
