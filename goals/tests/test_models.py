import os
from django.conf import settings
from django.core.files import File
from django.test import TestCase

from goals.models import Goal


class TestGoal(TestCase):

    def setUp(self):
        test_file_path = os.path.join(
            settings.BASE_DIR, "static", "img", "test", "gallery01.jpg")
        self.test_file = File(open(test_file_path, 'rb'))

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
        assert "gallery01" in goal.image.file.name

        # Clean up the copy of the image file
        goal.image.delete()

    def test_has_slug(self):
        goal = Goal(slug="the-slug")
        expected = "the-slug"
        assert expected == goal.slug

    def test_percentage_complete_with_some_items_completed(self):
        goal = Goal.objects.create(name="Django")
        goal.task_set.create(name="Item 1")
        item_two = goal.task_set.create(name="Item 2")
        item_two.complete()
        assert goal.percentage_complete() == 50

    def test_percentage_complete_with_zero_items_completed(self):
        goal = Goal.objects.create(name="Django")
        goal.task_set.create(name="Item 1")
        assert goal.percentage_complete() == 0

    def test_percentage_complete_with_all_items_completed(self):
        goal = Goal.objects.create(name="Django")
        goal.task_set.create(name="Item 1")
        assert goal.percentage_complete() == 100
