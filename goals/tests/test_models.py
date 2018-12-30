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
        """A Goal should have a name"""
        goal = Goal(name="The name")
        expected = "The name"
        assert expected == goal.name

    def test_required_fields(self):
        """A Goal's required fields should raise an error if missing"""
        goal = Goal(name="The name", description="The description",
                    image=self.test_file, slug="the-slug",)
        expected = None
        assert expected == goal.clean_fields()

    def test_has_description(self):
        """A Goal should have a description"""
        goal = Goal(description="The description")
        expected = "The description"
        assert expected == goal.description

    def test_has_image(self):
        """A Goal should have an image"""
        goal = Goal.objects.create(name="The name", description="The description",
                                   image=self.test_file)
        assert "gallery01" in goal.image.file.name

        # Clean up the copy of the image file
        goal.image.delete()

    def test_has_slug(self):
        """A Goal should have a slug"""
        goal = Goal(slug="the-slug")
        expected = "the-slug"
        assert expected == goal.slug
