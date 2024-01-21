from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class ProfileManager(models.Manager):
    def retrieve_profile(self, user_id):
        return self.filter(user_id=user_id).first()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="static/img", null=True, blank=True, default="cat_web.jpg")
    objects = ProfileManager()

    def __str__(self):
        return f"Profile of {self.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    rating = models.IntegerField(null=True, default=0, db_index=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'Tag'

    def __str__(self):
        return f"Tag: {self.name}"


class LikeManager(models.Manager):
    def adjust_vote(self, user, question=None, answer=None, like_value=0):
        like, created = self.get_or_create(
            user=user, question=question, answer=answer,
            defaults={'value': like_value}
        )
        if not created and like.value != like_value:
            like.value = like_value
            like.save()
        return like

    def calculate_score(self, question):
        likes = self.filter(question=question, value=1).count()
        dislikes = self.filter(question=question, value=-1).count()
        return likes - dislikes


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True, blank=True)
    value = models.IntegerField()
    objects = LikeManager()

    def __str__(self):
        target = self.question or self.answer
        return f"{self.user.username}'s vote on {target}"


class QuestionManager(models.Manager):

    def get_by_tags(self, *tags):
        return self.filter(tags__name__in=tags).distinct()

    def recent_questions(self):
        return self.order_by('-date_of_creation')

    def top_rated_questions(self):
        return self.annotate(
            total_votes=Sum('like__value')
        ).filter(
            total_votes__gt=0
        ).order_by('-total_votes')[:20]
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')
    date_of_creation = models.DateField(auto_now_add=True)
    objects = QuestionManager()

    def __str__(self):
        return f"Question: {self.title}"


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    correct = models.BooleanField(default=False)
    date_of_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} to '{self.question.title}'"
