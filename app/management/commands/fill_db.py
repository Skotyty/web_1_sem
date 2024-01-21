from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User

from app.models import Question, Answer, Profile, Tag, Like
import random

fake = Faker()

class Command(BaseCommand):
    help = "Fills the database with fake data for your models"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']
        questions_amount = num * 10

        self.stdout.write(self.style.SUCCESS('Start parsing...'))

        # Создаём пользователей
        # users = []
        # existing_usernames = set(User.objects.values_list('username', flat=True))
        # for _ in range(num):
        #     while True:
        #         username = fake.user_name()
        #         if username not in existing_usernames:
        #             break
        #     user = User.objects.create_user(username=username, email=fake.email(), password=fake.password())
        #     users.append(user)
        #     existing_usernames.add(username)
        # self.stdout.write(self.style.SUCCESS('Users - DONE'))
        #
        # Создаём профили
        # profiles = [Profile(user=user, avatar=fake.image_url()) for user in users]
        # Profile.objects.bulk_create(profiles)
        # self.stdout.write(self.style.SUCCESS('Profiles - DONE'))


        # Извлекаем существующих пользователей(в первый раз программы создала пользователей, но не отработала с тегами, пришлось прервать)
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No users found in the database. Please create some users first.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(users)} users.'))

        # создаём теги
        existing_tag_names = set(Tag.objects.values_list('name', flat=True))
        tags = []
        for _ in range(num):
            tag_name = f"{fake.word()}_{fake.lexify(text='????', letters='abcdefghijklmnopqrstuvwxyz')}_{fake.random_int(min=0, max=9999)}"
            if tag_name not in existing_tag_names:
                tags.append(Tag(name=tag_name, description=fake.text(), rating=fake.random_int(min=0, max=100)))
                existing_tag_names.add(tag_name)
        Tag.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags.'))

        # вопросы
        questions = [Question(user=random.choice(users), title=fake.sentence(nb_words=6), text=fake.text(), date_of_creation=fake.date_between(start_date='-1y', end_date='today')) for _ in range(questions_amount)]
        Question.objects.bulk_create(questions)
        self.stdout.write(self.style.SUCCESS(f'Created {len(questions)} questions.'))

        # ответы
        answers = []
        for question in questions:
            for _ in range(random.randint(1, 5)):
                answer = Answer(user=random.choice(users), question=question, text=fake.text(), correct=fake.boolean(), date_of_creation=fake.date_between(start_date=question.date_of_creation, end_date='today'))
                answers.append(answer)
        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'Created {len(answers)} answers.'))

        # лайки для вопросов и ответов
        likes = []
        for _ in range(questions_amount * 2):
            user = random.choice(users)
            if random.choice([True, False]):
                question = random.choice(questions)
                likes.append(Like(user=user, question=question, value=fake.random_element(elements=(-1, 1))))
            else:
                answer = random.choice(answers)
                likes.append(Like(user=user, answer=answer, value=fake.random_element(elements=(-1, 1))))

        Like.objects.bulk_create(likes)
        self.stdout.write(self.style.SUCCESS(f'Created {len(likes)} likes.'))

        # добавляем теги к вопросам
        all_tags = list(Tag.objects.all())
        for question in questions:
            question.tags.set(random.sample(all_tags, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS('Tags set to questions - DONE'))

        self.stdout.write(self.style.SUCCESS(f"Successfully populated the database with fake data with ratio = {num}."))
    #     # ///////////////////////////////////////////
        # Следующий код был создан, чтобы увеличить кол-во ответов до нужного
        # def add_arguments(self, parser):
        #     parser.add_argument("num", type=int, help="Number of answers to create")
        #
        # def handle(self, *args, **kwargs):
        #     num_answers_to_create = kwargs['num']
        #
        #     self.stdout.write(self.style.SUCCESS('Start parsing...'))
        #
        #
        #     users = list(User.objects.all())
        #     questions = list(Question.objects.all())
        #     if not users or not questions:
        #         self.stdout.write(self.style.ERROR(
        #             'No users or questions found in the database. Please create some users and questions first.'))
        #         return
        #
        #     self.stdout.write(self.style.SUCCESS(f'Found {len(users)} users and {len(questions)} questions.'))
        #
        #     batch_size = 1000
        #     created_answers = 0
        #
        #     while created_answers < num_answers_to_create:
        #         answers_to_create_now = min(batch_size, num_answers_to_create - created_answers)
        #         answers_batch = [
        #             Answer(
        #                 user=random.choice(users),
        #                 question=random.choice(questions),
        #                 text=fake.text(),
        #                 correct=fake.boolean(),
        #                 date_of_creation=fake.date_between(start_date='-1y', end_date='today')
        #             ) for _ in range(answers_to_create_now)
        #         ]
        #
        #         Answer.objects.bulk_create(answers_batch)
        #         created_answers += answers_to_create_now
        #         self.stdout.write(self.style.SUCCESS(f'Created {created_answers} answers so far.'))
        #
        #     self.stdout.write(self.style.SUCCESS(f"Successfully created {num_answers_to_create} answers."))

        # ////////////////////////////////////////////////////////
        # добавляем нормальные теги

        # help = "Fills the database with fake data for your models"
        #
        # def add_arguments(self, parser):
        #     parser.add_argument("num", type=int)
        #
        # def handle(self, *args, **kwargs):
        #     num = kwargs['num']
        #     questions_amount = num * 10
        #
        #     self.stdout.write(self.style.SUCCESS('Start parsing...'))
        #
        #
        #     users = list(User.objects.all())
        #     if not users:
        #         self.stdout.write(self.style.ERROR('No users found in the database. Please create some users first.'))
        #         return
        #
        #     self.stdout.write(self.style.SUCCESS(f'Found {len(users)} users.'))
        #
        #     existing_tag_names = set(Tag.objects.values_list('name', flat=True))
        #     tags_to_create = []
        #     while len(tags_to_create) < 1000:
        #
        #         tag_name = fake.text(max_nb_chars=10).split(' ')[0]
        #         if tag_name not in existing_tag_names:
        #             tag = Tag(name=tag_name, description=fake.text(), rating=fake.random_int(min=0, max=100))
        #             tags_to_create.append(tag)
        #             existing_tag_names.add(tag_name)
        #
        #             if len(tags_to_create) % 100 == 0:
        #                 self.stdout.write(self.style.SUCCESS(f'Created {len(tags_to_create)} tags so far.'))
        #
        #     Tag.objects.bulk_create(tags_to_create)
        #     self.stdout.write(self.style.SUCCESS(f'Created {len(tags_to_create)} tags.'))
        #
        #     self.stdout.write(
        #         self.style.SUCCESS(f"Successfully populated the database with fake data with ratio = {num}."))


