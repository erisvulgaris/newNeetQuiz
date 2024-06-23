import json
import os
from django.core.management.base import BaseCommand
from quiz.models import Category, Subject, Unit, Chapter, Topic, Question

class Command(BaseCommand):
    help = 'Load questions from JSON files into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file containing questions')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        subject_name = os.path.splitext(os.path.basename(json_file))[0]  # Get subject name from the JSON file name

        with open(json_file, 'r') as file:
            questions = json.load(file)

        for question_data in questions:
            category_name = "Default Category"  # You can change this if you have categories in your JSON
            category, created = Category.objects.get_or_create(name=category_name)

            subject, created = Subject.objects.get_or_create(name=subject_name, category=category)

            parts = question_data['topic_name'].split('>>')
            unit_name = parts[0].strip()
            chapter_name = parts[1].strip() if len(parts) > 1 else ''
            topic_name = parts[2].strip() if len(parts) > 2 else ''

            unit, created = Unit.objects.get_or_create(name=unit_name, subject=subject)
            chapter, created = Chapter.objects.get_or_create(name=chapter_name, unit=unit, subject=subject) if chapter_name else (None, False)
            topic, created = Topic.objects.get_or_create(name=topic_name, unit=unit)  # Updated to use 'unit'

            question, created = Question.objects.update_or_create(
                unique_id=question_data['unique_id'],
                defaults={
                    'text': question_data['question'],
                    'topic': topic,
                    'difficulty': question_data['difficulty_level'],
                    'type': question_data['quiz_type'],
                    'explanation': question_data['explanation'],
                    'option_a': question_data['option_a'],
                    'option_b': question_data['option_b'],
                    'option_c': question_data['option_c'],
                    'option_d': question_data['option_d'],
                    'answer': question_data['answer']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded questions from JSON file'))
